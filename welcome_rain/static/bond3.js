(function($){
	$.fn.mhrChart = function(passedOptions){
		var options = {
			ajaxUrl : '/static/getData.json',
			ajaxArgumentTarget : 'grid|cluster|host|datasource',
			grahpTotalHours : 2,
			realTime : true,
			realTimeInterval : 1000,
			targetHeight : 250,
			targetWidth : 250
			
		};
		
	    var myOptions = jQuery.extend(options, passedOptions);
		
	   	
		return this.each(function(){
			
			var targetObject = $(this)
			
			//console.log(targetObject.width())
			//console.log(targetObject.height())
			
			if(targetObject.width()==0 || targetObject.height() ==0){
				$(this).css('width',myOptions.targetWidth);
				$(this).css('height',myOptions.targetHeight);
			}
			
			
			
			
			//var targetObject = $(this)[0];
			//$(this).css('width',myOptions.targetWidth)
			//$(this).css('height',myOptions.targetHeight)
			//console.log(targetObject)
			//getDataFromServer();
			//console.log($(this))
			//var obj = $(this)
			
			function init() {         
		      	console.log('mhrChart init');       
		      	//console.log(this)
		      	//($.fn.mhrChart.func())
		      	getDataFromServer();
		      	// problem -->http://www.codingforums.com/showthread.php?t=174099
		      	if(myOptions.realTime){
		      		setTimeout(function () {
		      			targetObject.mhrChart(myOptions);
					    //console.log(1)
						//init();
					}, 1000);
		      		//setTimeout('drowChart();', myOptions.realTimeInterval);
		      	}
		      	//setTimeout('drowChart();', myOptions.realTimeInterval);
		      	/*
		      	setTimeout(function () {
				    console.log(1)
					init();
				}, 1000);*/
		      	
		    }
		    
		    function getDataFromServer(){
		    	console.log('getDataFromServer');     
		    	var oArguments = getArguments()
		    	console.log(oArguments)
		    	ajax(oArguments,getDataFromServerCallback);
		    	//console.log(myOptions.ajaxUrl) 
		    }
		    function getDataFromServerCallback(oResponse){
		    	console.log('getDataFromServerCallback');     
		    	console.log(oResponse)
		    	var graphData = getGraphData(oResponse);
		    	drowGraph(graphData);	
		    }
		    function drowGraph(graphData){
		    	graph = Flotr.draw(targetObject[0], [ graphData ], {
			        	
			    });
		    }
		    function getGraphData(oResponse){
		    	var graphData = new Array();
	  			
	  			for (var index=0; index<oResponse.data.length; index++){
	  				graphData.push([oResponse.data[index].x,oResponse.data[index].y])
	  			}
	  			return graphData
		    }
		    function getArguments(){
		    	console.log('getArguments');     
		    	var endDate = new Date();
		    	var endTime = endDate.format("yyyy:mm:dd:hh:MM")
				var startDate = endDate.removeHours(myOptions.grahpTotalHours)
				var startTime = startDate.format("yyyy:mm:dd:hh:MM")
		    	return getArguments = {
		    		'target' : myOptions.ajaxArgumentTarget,
		    		'startTime' : startTime,
	  				'endTime' : endTime
		    	}
		    }
		    function ajax(oArguments,callback){
				$.ajax({
  					url: myOptions.ajaxUrl,
  					dataType: 'json',
  					data : oArguments,
  					success: function(data){
  						callback(data)
  					},
  					error: function (jqXHR, textStatus, errorThrown) {
      				console.log(jqXHR)
      				console.log(textStatus)
      				console.log(errorThrown)
						return false;
      			}
				});
			}
			
			
			init();
		});
	};
})(jQuery);
