
var TABLE_TYPE = 0;

function Charter() {

	this.createDashboardChart = function() {
		console.log("this.createDashboardChart");
		var CchartBuilder = new ChartDataBuilder();
		CchartBuilder.setBaseInfo(this.createDataCallback,false);
		CchartBuilder.handleShowDashBoard();
	}
	this.createDataCallback = function(chartObject) {
		console.log("this.createDataCallback");
		cCharterWorker = new CharterWorker();
		cCharterWorker.working(chartObject);
	}
	this.createTreeClickChart = function(apiData){
		console.log("this.createTreeClickChart");
		var CchartBuilder = new ChartDataBuilder();
		CchartBuilder.setBaseInfo(this.createDataCallback,false);
		CchartBuilder.handleTreeClick(apiData);
	}
	this.createDetailChart = function(target,start_time,end_titme) {
		console.log("this.createDetailChart");
		var CchartBuilder = new ChartDataBuilder();
		CchartBuilder.setBaseInfo(this.createDetailDataCallback,false);
		CchartBuilder.handleDetailChart(target,start_time,end_titme);
	}
	this.createDetailDataCallback = function(chartObject){
		console.log("this.createDetailDataCallback");
		var CchartBuilder = new ChartDataBuilder();
		chartObject = CchartBuilder.setDetailLayout(chartObject);
		cCharterWorker = new CharterWorker();
		cCharterWorker.working(chartObject);
	}
	this.createUserLayoutChart = function(idPrefix,targets,start_time,end_titme){
		console.log("this.createUserLayoutChart");
		var CchartBuilder = new ChartDataBuilder();
		CchartBuilder.setBaseInfo(this.createUserLayoutCallback,idPrefix);
		CchartBuilder.handleUserChart(targets,start_time,end_titme);
	}
	this.createUserLayoutCallback = function(chartObject){
		console.log("this.createUserLayoutCallback");
		var CchartBuilder = new ChartDataBuilder();
		chartObject = CchartBuilder.setUserLayout(chartObject);
		cCharterWorker = new CharterWorker();
		cCharterWorker.working(chartObject);
	}
	//idPrefix,targets,'/api/getData/',chartConf
	this.createApiChart = function(idPrefix,targets,apiName,chartConf,start_time,end_titme){
		console.log("this.createApiChart");
		
		var CchartBuilder = new ChartDataBuilder();
		CchartBuilder.setBaseInfo(this.createApiChartCallback,idPrefix);
		CchartBuilder.handleApiChart(apiName,targets,chartConf,start_time,end_titme);
	}
	this.createApiChartCallback = function(chartObject,apiData){
		console.log("this.createApiChartCallback");
		var CchartBuilder = new ChartDataBuilder();
		chartObject = CchartBuilder.setUserLayout(chartObject);
		cCharterWorker = new CharterWorker();
		cCharterWorker.apiWorking(chartObject,apiData.chartConf);
		//console.log(apiData);
	}

}


function CharterWorker(){
	this.working = function(chartObject){
		var cLayoutCreate = new LayoutCreate();
		var cChartCreate = new ChartCreate();
		var cChartHtmlCreate = new ChartHtmlCreate();
		cLayoutCreate.create(chartObject);
		cChartCreate.create(chartObject);
		cChartHtmlCreate.create(chartObject);
	}
	this.apiWorking = function(chartObject,chartConf){
		var cChartCreate = new ChartCreate();
		cChartCreate.create(chartObject,chartConf);
	}
}

function ChartDataBuilder() {

	this.type = null;
	this.callback = null;
	this.chartObject = null;
	this.getDataBrack = false;
	this.isHaveElement = false;
	this.base_body = 'bond_body_'
	this.base_titile = 'bond_title_'
	
	this.setBaseInfo = function(callback,isHaveElement) {
		this.callback = callback;
		if(isHaveElement){
			this.isHaveElement = true;
			this.base_body = isHaveElement;
		}
		this.chartObject = new ChartObject();
	}
	this.handleTreeClick = function(apiData){
		var targets = this.getTargetDataFromTree(apiData);
		var arguments = this.getDataArguments(targets);
		this.sendAajx('/api/getData/',arguments, this.getDataCallback);
	}
	this.handleDetailChart = function(target,start_time,end_titme){
		var arguments = this.getDataArguments(target,start_time,end_titme);
		this.sendAajx('/api/getData/',arguments, this.getDataCallback);
	}
	this.handleUserChart = function(targets,start_time,end_titme){
		var arguments = this.getDataArguments(targets,start_time,end_titme);
		this.sendAajx('/api/getData/',arguments, this.getDataCallback);
	}
	this.handleApiChart = function(apiName,targets,chartConf,start_time,end_titme){
		var arguments = this.getDataArguments(targets,start_time,end_titme);
		//arguments = this.addChartConfInArguments(arguments,chartConf)
		arguments.chartConf = chartConf;
		this.sendAajx(apiName,arguments, this.getDataCallback);
	}
	this.getTargetDataFromTree = function(apiData) {
		var dataSeperat = apiData.split(APIDATA_SEPERATOR);
		var targets = '';

		for (var index = 0; index < dataSeperat.length; index++) {
			var dataNameValue = dataSeperat[index].split(APIDATA_EQUAL);
			if (dataNameValue.length < 2)
				continue;
			targets += dataNameValue[1] + ';';
		}
		return targets;
	}
	this.handleShowDashBoard = function(){
		this.sendAajx('/api/getDashboardTargetList/', {}, this.showDashboardCallback);
	}
	this.sendAajx = function(sUrl, oData, callback){
		var chartDataBuilder = this;
		$.ajax({
			url : sUrl,
			type : 'POST',
			dataType : 'json',
			data : oData,
			success : function(data) {
				callback(data, sUrl, oData,chartDataBuilder);
			},
			error : function(jqXHR, textStatus, errorThrown) {
				console.log(jqXHR)
				console.log(textStatus)
				console.log(errorThrown)
				return false;
			}
		});
	}
	this.showDashboardCallback = function(oResponse, apiUrl, apiData,chartDataBuilder) {
		//chartDataBuilder.setLayoutNumber(oResponse.data.dataSource.length);
		//console.log(oResponse)
		var targets = ''
		for (var index = 0; index < oResponse.data.dataSource.length; index++) {
			//console.log(oResponse.data.dataSource[index].name)
			//console.log(oResponse.data.cluster)
			targets += oResponse.data.cluster + '/' + oResponse.data.dataSource[index].name + ';';
			//console.log(targets)
		}
		if (targets == ''){
			chartDataBuilder.callback(chartDataBuilder.chartObject);
		}
		else{
			//console.log(targets)
			var arguments = chartDataBuilder.getDataArguments(targets);
			//console.log(arguments);
			chartDataBuilder.sendAajx('/api/getData/',arguments, chartDataBuilder.getDataCallback);
			//chartDataBuilder.sendAajx('/static/getDataNew.json/',arguments, chartDataBuilder.getDataCallback);
		}
	}
	this.getDataArguments = function(targets,startTime,endTime){
		if (!(startTime && startTime)){
			var endDate = new Date();
			var endTime = endDate.format("yyyy:mm:dd:HH:MM")
			var startDate = endDate.removeHours(1)
			var startTime = startDate.format("yyyy:mm:dd:HH:MM")
		}
		
		
		return {
			'target' : targets,
			'startTime' : startTime,
			'endTime' : endTime,
			'format' : 'json',
		}
	}
	/*this.addChartConfInArguments = function(arguments,chartConf){
		arguments = arguments.chartConf = chartConf;
		return arguments
	}*/
	this.setChartData = function(chartData){
		this.chartObject.data.push(chartData);
	}
	this.getDataCallback = function(oResponse, apiUrl, apiData, chartDataBuilder){
		//console.log(oResponse)
		for (var index_a = 0; index_a < oResponse.data.length; index_a++) {
			var chartData = new ChartData();
			var oData = oResponse.data[index_a];
			var xlsArguments = ''
			
			for (var index_b = 0; index_b < oData.datapoints.length; index_b++) {
				//var xData = oData.datapoints[index_b].x;
				var xData = index_b;
				var yData = (oData.datapoints[index_b].y == 'None') ? 0 : oData.datapoints[index_b].y;
				xlsArguments += oData.datapoints[index_b].x + '=' + yData;
				if (index_b < oData.datapoints.length - 1) xlsArguments += '|'
				chartData.points.push([xData, yData]);
			}
			for (var index_c =0; index_c < oData.events.length; index_c++){
				var xData = oData.events[index_c].x_axis_index;
				var yData = oData.events[index_c].color;
			 	chartData.events.push([xData,yData]);
			}
			chartData.targetDiv = chartDataBuilder.base_body + index_a;
			chartData.titleDiv = chartDataBuilder.base_titile + index_a;
			chartData.targetInfo = oData.target;
			chartData.xlsArguments = xlsArguments; 
			//chartData.target = chartDataBuilder.getAjaxTarget(oData.target);
			chartDataBuilder.setChartData(chartData);
		}
		chartDataBuilder.callback(chartDataBuilder.chartObject,apiData);
	}
	this.getAjaxTarget = function(targetInfo){
		oTarget = targetInfo.split(',')
		//console.log(oTarget)
		var cluster = $.trim(oTarget[0].split('=')[1]);
		var host = $.trim(oTarget[1].split('=')[1]);
		var datasource = $.trim(oTarget[2].split('=')[1]); 
		//console.log(cluster)
		//console.log(host)
		//console.log(datasource)
		//console.log(cluster + '/' +host + '/' + datasource)
		//return 'good'
		return cluster + '/' +host + '/' + datasource;
	}
	this.setDetailLayout = function(chartObject){
		chartObject.layout.isDetail = true;
		return chartObject;
	}
	this.setUserLayout = function(chartObject){
		chartObject.layout.isCreated = false;
		return chartObject;
	}
}

/*
 
 (function basic(container) {

  var
    d1 = [[0, 3], [4, 8], [8, 5], [9, 13]], // First data series
    d2 = [],                                // Second data series
    i, graph;

  // Generate first data set
  for (i = 0; i < 14; i += 0.5) {
    d2.push([i, Math.sin(i)]);
  }

  // Draw Graph
  graph = Flotr.draw(container, [ d1, d2 ], {
    xaxis: {
      minorTickFreq: 4
    }, 
    grid: {
      minorVerticalLines: true
    }
  });
})(document.getElementById("editor-render-0"));
 
 ----------
 
 (function basic_bars(container, horizontal) {

  var
    horizontal = (horizontal ? true : false), // Show horizontal bars
    d1 = [],                                  // First data series
    d2 = [],                                  // Second data series
    point,                                    // Data point variable declaration
    i;

  for (i = 0; i < 4; i++) {

    if (horizontal) { 
      point = [Math.ceil(Math.random()*10), i];
    } else {
      point = [i, Math.ceil(Math.random()*10)];
    }

    d1.push(point);
        
    if (horizontal) { 
      point = [Math.ceil(Math.random()*10), i+0.5];
    } else {
      point = [i+0.5, Math.ceil(Math.random()*10)];
    }

    d2.push(point);
  };
              
  // Draw the graph
  Flotr.draw(
    container,
    [d1, d2],
    {
      bars : {
        show : true,
        horizontal : horizontal,
        shadowSize : 0,
        barWidth : 0.5
      },
      mouse : {
        track : true,
        relative : true
      },
      yaxis : {
        min : 0,
        autoscaleMargin : 1
      }
    }
  );
})(document.getElementById("editor-render-0"));
 
 
 */

function ChartCreate(){
	this.create = function(chartObject,chartConf){
		var chartConf = this.getChartConf(chartConf);
		for (var index=0; index < chartObject.data.length ;index++){
			var chartData = chartObject.data[index].points;
			//var chartTestData = [[0,5],[1,5],[2,8],[3,7],[4,10],[5,6],[6,5],[7,1],[8,5],[9,2]];
			this.draw(chartObject.data[index].targetDiv,[this.getData(chartData,chartConf)],chartObject.data[index].events,this.getOptions(chartConf));
			//this.draw(chartObject.data[index].targetDiv,[chartObject.data[index].points],chartObject.data[index].events);
		}
	}
	this.getChartConf = function(chartConf){
		var chartConf = "";
		if (chartConf) chartConf = chartConf;
		else chartConf = getUserChartConf();
		return chartConf
	}
	this.getData = function(chartData,chartConf){
		//console.log(chartConf.grahp_line_fill)
		//console.log(chartConf.grahp_line_fill)
		//var fillFlug = chartConf.grahp_line_fill ? true: false
		return {
			data:chartData,
			lines:{
				fill:chartConf.grahp_line_fill
			}
		}
	}
	this.getOptions = function(chartConf){
		
		return {
			colors : [chartConf.grahp_line_color],
			shadowSize : 1,
			xaxis : {
				mode : 'time',
				noTicks : 20,
				scaling : 'linear',
				showLabels : true,
				tickFormatter : function(x) {
					if ((x % 40) == 0) return x;
					return "";
				}
			},
			yaxis : {
				autoscale : true,
				autoscaleMargin : 0.5,
				min : 0,
				base : Math.E,
				margin : true,
				scaling : 'linear'
			},
			grid : {
				color : chartConf.grahp_grid_color,
				outlineWidth: chartConf.grahp_grid_outlineWidth * 1,
				events: events,
				/*
				backgroundColor : {
		          colors : [[0,'#fff'], [1,'#ccc']],
		          start : 'top',
		          end : 'bottom'
		        }
		        */
			}

		}
		
	}
	//this.draw('test_div_id',[],[])
	this.draw = function(divId,datas,events,options){
		//console.log(datas)
		//console.log(events)
		graph = Flotr.draw(document.getElementById(divId), datas, options);
	}
}

function LayoutCreate(){
	this.create = function(chartObject){
		console.log(chartObject)
		if (!(chartObject.layout.isCreated)) return true;
		$("#container").mhrGraphTable({
			'graphNumber' : chartObject.data.length,
			'isDetail' : chartObject.layout.isDetail
		});
	}
}

function ChartHtmlCreate(){
	this.create = function(chartObject){
		if (chartObject.layout.isDetail || (!(chartObject.layout.isCreated))) return true;
		for (var index=0; index < chartObject.data.length ;index++){
			var oData = chartObject.data[index]
			var html = this.createTitleHtml(oData)
			this.renderToTitle(oData,html);
			this.addEvent(oData);
		}
	}
	this.createTitleHtml = function(oData) {
		var titleHtml = '';
		titleHtml += '<div class="in_chart_title">';
		titleHtml += '<span title="' + this.getFullTitle(oData) + '" class="left">' + this.getTitle(oData) + '</span>';
		titleHtml += '<button class="btn-link right detail_btn" id="detail_' + oData.titleDiv + '" href="#"><span class="icomoon-icon-zoom-in"></span></button>';
		titleHtml += '<button class="btn-link right xml_btn" id="xml_' + oData.titleDiv + '" href="#"><a href="/api/downloadxls/?data=' + oData.xlsArguments + '&title=' + this.getTitle(oData) + '"><span class="icomoon-icon-zoom-in"></span></a></button>';
		titleHtml += '<button style="display:none" class="btn-link right favor_btn" id="favor_' + oData.titleDiv + '" href="#"><span class="minia-icon-star-2"></span></button>';
		titleHtml += '</div>';
		return titleHtml;
	}

	this.getFullTitle = function(oData) {
		var oTargetInfo = oData.targetInfo.split('=');
		return oTargetInfo[3];
	}

	this.getTitle = function(oData) {
		var MAX_LEN = 10
		var title = this.getFullTitle(oData);
		if (title.length > MAX_LEN) {
			title = title.substring(0, MAX_LEN) + '...'
		}
		return title;
	}
	
	this.renderToTitle = function(oData,html) {
		$("#" + oData.titleDiv).append(html)
	}

	this.addEvent = function(oData){
		$('#detail_' + oData.titleDiv).click(function() {
			NewWindow('/grahpDetail?target=' + oData.target, 'welcome', '600', '650', 'no');
		})
	}
	this.setTitleFlag = function() {
		
		//myOptions.createTitleFlag = true;
	}
}




function ChartObject() {
	this.data = new Array();
	this.layout = new Layout();
}

function Layout() {
	this.isCreated = true;
	this.type = TABLE_TYPE;
	this.isDetail = false;
}

function ChartData(){
	this.targetDiv = null;
	this.titleDiv = null;
	this.xlsArguments = null;
	this.targetInfo = null;
	this.target = null;
	this.points = new Array();
	this.events = new Array();
}





function ChartDataHandler() {

	this.target = null;
	this.startTime = null;
	this.endTime = null;
	this.grahpDataHour = 1;

	this.setBaseData = function(target) {
		this.target = target;
	}

	this.getAjaxArguments = function() {

		if (!(this.startTime && this.endTime)) {
			var endDate = new Date();
			this.endTime = endDate.format("yyyy:mm:dd:HH:MM")
			var startDate = endDate.removeHours(this.grahpDataHour)
			this.startTime = startDate.format("yyyy:mm:dd:HH:MM")
		}

		var oArgTarget = this.target.split(',');
		oArgTarget.reverse()
		var clusterIndex = $.inArray('Cluster', oArgTarget)
		/*
		 var target = null

		 if(clusterIndex>1){
		 var cluster = oArgTarget[clusterIndex+1];
		 var host = oArgTarget[clusterIndex+2];
		 var dataSource = oArgTarget[clusterIndex+3].slice(1,oArgTarget[clusterIndex+3].length);
		 target = cluster+'/'+host+'/'+dataSource;
		 }
		 //console.log(myOptions);
		 */
		return arguments = {
			'target' : this.target,
			'startTime' : this.startTime,
			'endTime' : this.endTime,
			'format' : 'json'
		}
	}

	this.createChartDataForChart = function() {
		//console.log(this.target);
		oArguments = this.getAjaxArguments()
		//console.log(oArguments)
		this.getAjaxData(oArguments, this.createChartDataForChartCallback)
	}
	this.getAjaxData = function(oData, callBack) {
		$.ajax({
			url : '/api/getData/',
			type : 'POST',
			dataType : 'json',
			data : oData,
			success : function(data) {
				callBack(data);
			},
			error : function(jqXHR, textStatus, errorThrown) {
				console.log(jqXHR)
				console.log(textStatus)
				console.log(errorThrown)
				return false;
			}
		});
	}
	this.createChartDataForChartCallback = function(oResponse) {
		//console.log(oResponse);

		var graphData = new Array();
		for (var index_a = 0; index_a < oResponse.data.length; index_a++) {

			var oData = oResponse.data[index_a];

			var graphDataPoints = new Array();
			for (var index_b = 0; index_b < oData.datapoints.length; index_b++) {
				var xData = oData.datapoints[index_b].x;
				var yData = (oData.datapoints[index_b].y == 'None') ? 0 : oData.datapoints[index_b].y;
				graphDataPoints.push([xData, yData]);
			}
			graphData.push(graphDataPoints)
			/*
			 var graphDataEvent = new Array();
			 for (var index_c =0; index_c < oData.event.length; index_c++){
			 var xData = oData.datapoints[index_c].x;
			 var yData = (oData.datapoints[index_c].y=='None') ? 0 : oData.datapoints[index_c].y;
			 //console.log(xData)
			 //console.log(yData)
			 //var xData = index;
			 graphDataEvent.push([xData,yData]);
			 }
			 */
		}
		//console.log(graphData)

	}
}






/*
 * target Element
 * oGraphData
 * chartOption
 */

function drowChart(targetElement, graphData, chartOptions) {
	graph = Flotr.draw(targetElement, [graphData], chartOptions);
	/*
	 graph = Flotr.draw(targetObject[0], [ oGraphData ], {
	 colors : ['#ed7a53'],
	 shadowSize:1,
	 xaxis : {
	 mode : 'time',
	 //labelsAngle : 45,
	 noTicks:20,
	 scaling:'linear',
	 showLabels : true,
	 //showMinorLabels: false,
	 //tickDecimals:20,
	 //autoscale:true,
	 tickFormatter: function(x) {
	 if ((x % 40)==0) return x;
	 return "";
	 }
	 },
	 yaxis : {
	 autoscale : true,
	 autoscaleMargin:0.5,
	 min:0,
	 base:Math.E,
	 margin:true,
	 scaling: 'linear'
	 },
	 grid : {
	 color : '#d5d5d5'
	 }
	 });
	 */
}

(function($) {

	$.fn.mhrGraphChart = function(passedOptions) {

		var options = {
			debug : false,
			//getDataAjaxUrl : './getData.json',
			//getDataAjaxUrl : '/static/getData.json',
			getDataAjaxUrl : '/api/getData/',
			addFavorAjaxUrl : '/api/registerUserFavoriteChart/',
			target : '1',
			realTimeActive : true,
			realTimeInterval : 10000,
			grahpDataHour : 1,
			titleId : null,
			startTime : null,
			endTime : null,
			createTitleFlag : false,
			isDetail : false,
			data : null,
		};

		var myOptions = jQuery.extend(options, passedOptions);

		return this.each(function() {

			var targetObject = $(this)

			function log(sMessage) {
				if (myOptions.debug)
					console.log(sMessage);
			}

			function init() {
				log("mhrGraphChart init");
				drowChartProcess();
				if (myOptions.realTimeActive) {
					setTimeout(function() {
						refresh();
					}, myOptions.realTimeInterval);
				}
			}

			function refresh() {
				log("mhrGraphChart refresh");
				targetObject.mhrGraphChart(myOptions);
			}

			function drowChartProcess() {
				log("mhrGraphChart drowChartProcess");
				getDataFromServer();
			}

			function getDataFromServer() {
				log("mhrGraphChart getDataFromServer");
				oArguments = getDataArguments()
				//console.log(oArguments)
				ajax(oArguments, myOptions.getDataAjaxUrl, drowChartProcessCallback);
			}

			function getDataArguments() {
				log("mhrGraphChart getDataArguments");

				if (!(myOptions.startTime && myOptions.endTime)) {
					var endDate = new Date();
					myOptions.endTime = endDate.format("yyyy:mm:dd:HH:MM")
					var startDate = endDate.removeHours(myOptions.grahpDataHour)
					myOptions.startTime = startDate.format("yyyy:mm:dd:HH:MM")
				}

				var oArgTarget = myOptions.target.split(',');
				oArgTarget.reverse()
				var clusterIndex = $.inArray('Cluster', oArgTarget)

				var target = null

				if (clusterIndex > 1) {
					var cluster = oArgTarget[clusterIndex + 1];
					var host = oArgTarget[clusterIndex + 2];
					var dataSource = oArgTarget[clusterIndex + 3].slice(1, oArgTarget[clusterIndex + 3].length);
					target = cluster + '/' + host + '/' + dataSource;
				}
				//console.log(myOptions);
				return arguments = {
					'target' : myOptions.target,
					'startTime' : myOptions.startTime,
					'endTime' : myOptions.endTime,
					'format' : 'json'
				}
			}

			function ajax(oArguments, url, callback) {
				log("mhrGraphChart ajax");
				$.ajax({
					url : url,
					type : 'POST',
					dataType : 'json',
					data : oArguments,
					success : function(data) {
						callback(data);
					},
					error : function(jqXHR, textStatus, errorThrown) {
						console.log(jqXHR)
						console.log(textStatus)
						console.log(errorThrown)
						return false;
					}
				});
			}

			function drowChartProcessCallback(oResponse) {
				log("mhrGraphChart drowChartProcessCallback");
				oGraphData = createGraphData(oResponse);
				//myOptions.data = oGraphData
				drowGraph(oGraphData);
				createTitle();
			}

			function createGraphData(oResponse) {
				log("mhrGraphChart createGraphData");
				var graphData = new Array();

				var argumentsData = ''
				for (var index = 0; index < oResponse.data[0].datapoints.length; index++) {
					//var xData = oResponse.data[0].datapoints[index].x;
					var xData = index;
					var yData = (oResponse.data[0].datapoints[index].y == 'None') ? 0 : oResponse.data[0].datapoints[index].y;
					argumentsData += oResponse.data[0].datapoints[index].x + '=' + yData;
					if (index < oResponse.data[0].datapoints.length - 1)
						argumentsData += '|'
					graphData.push([xData, yData]);
				}
				myOptions.data = argumentsData;
				return graphData
			}

			function drowGraph(oGraphData) {
				log("mhrGraphChart drowGraph");
				graph = Flotr.draw(targetObject[0], [oGraphData], {
					colors : ['#ed7a53'],
					shadowSize : 1,
					xaxis : {
						mode : 'time',
						//labelsAngle : 45,
						noTicks : 20,
						scaling : 'linear',
						showLabels : true,
						//showMinorLabels: false,
						//tickDecimals:20,
						//autoscale:true,
						tickFormatter : function(x) {
							if ((x % 40) == 0)
								return x;
							return "";
						}
					},
					yaxis : {
						autoscale : true,
						autoscaleMargin : 0.5,
						min : 0,
						base : Math.E,
						margin : true,
						scaling : 'linear'
					},
					grid : {
						color : '#d5d5d5'
					}

				});
			}

			function createTitle() {
				log("mhrGraphChart createTitle");
				if (!myOptions.createTitleFlag) {
					html = createTitleHtml();
					renderToTitle(html);
					addEvent();
					setTitleFlag();
				}
			}

			function createTitleHtml() {
				log("mhrGraphChart createTitleHtml");
				var titleHtml = '';
				titleHtml += '<div class="in_chart_title">';
				if (myOptions.isDetail) {
					//titleHtml += '<span>'+getFullTitle()+'</span>';
				} else {
					//titleHtml += '<h4 class="clearfix">';
					titleHtml += '<span title="' + getFullTitle() + '" class="left">' + getTitle() + '</span>';
					titleHtml += '<button class="btn-link right detail_btn" id="detail_' + myOptions.titleId + '" href="#"><span class="icomoon-icon-zoom-in"></span></button>';
					titleHtml += '<button class="btn-link right xml_btn" id="xml_' + myOptions.titleId + '" href="#"><a href="/api/downloadxls/?data=' + myOptions.data + '&title=' + getTitle() + '"><span class="icomoon-icon-zoom-in"></span></a></button>';
					titleHtml += '<button style="display:none" class="btn-link right favor_btn" id="favor_' + myOptions.titleId + '" href="#"><span class="minia-icon-star-2"></span></button>';
					//titleHtml += '<a href="#" class="btn btn-mini detail_btn right" id="detail_'+myOptions.titleId+'">D</a>';
					//titleHtml += '<a href="#" class="btn btn-mini favor_btn right" id="favor_'+myOptions.titleId+'">F</a>';
					//titleHtml += '</h4>';
				}
				titleHtml += '</div>';
				return titleHtml
			}

			function getFullTitle() {
				var oTarget = myOptions.target.split('/');
				var title = oTarget[oTarget.length-1].split('.')[0];
				return title
			}

			function getTitle() {
				var MAX_LEN = 10
				var oTarget = myOptions.target.split('/');
				var title = oTarget[oTarget.length-1].split('.')[0];
				if (title.length > MAX_LEN) {
					title = title.substring(0, MAX_LEN) + '...'
				}
				return title
			}

			/*
			 function createTitleHtml(){
			 log("mhrGraphChart createTitleHtml");
			 var titleHtml = '';
			 if(myOptions.isDetail){
			 titleHtml += '<p>| title |</p>';
			 }
			 else{

			 //titleHtml += '<p><a href="/grahp/detail/?target='+myOptions.target+'" target="_blank">D</a> |';
			 titleHtml += '<p><a href="#" class="detail_btn" id="detail_'+myOptions.titleId+'">D</a>';
			 titleHtml += ' | title | ';
			 titleHtml += '<a href="#" class="favor_btn" id="favor_'+myOptions.titleId+'">F</a>';
			 //titleHtml += '<a href="#" class="refresh_btn">R<a></p>';
			 }

			 //titleHtml += '<p>'+myOptions.target+'</p>';
			 return titleHtml
			 }
			 */
			function renderToTitle(html) {
				log("mhrGraphChart renderToTitle");
				$("#" + myOptions.titleId).append(html)
			}

			function addEvent() {
				log("mhrGraphChart renderToTitle");
				$('.refresh_btn').click(function() {
					myOptions.realTimeActive = false;
					refresh();
				})
				$('#detail_' + myOptions.titleId).click(function() {
					//window.open('/grahp/detail/?target='+myOptions.target,'welcome','width=500,height=500');

					NewWindow('/grahpDetail?target=' + myOptions.target, 'welcome', '600', '650', 'no')
					//window.open('/grahp/detail/?target='+myOptions.target+'"','welcome','width=1500,height=1500')
				})
				/*$('#xml_'+myOptions.titleId).click(function(){
				 console.log(myOptions.data);
				 //ajax({},'/api/downloadxls/',function(){console.log(1)});
				 $.ajax({
				 url: '/api/downloadxls/',
				 type : 'POST',
				 //dataType: 'json',
				 data : {},

				 });
				 });*/
				/*$('#favor_'+myOptions.titleId).click(function(){
				 var oArgTarget = myOptions.target.split(',');
				 oArgTarget.reverse();
				 var clusterIndex = $.inArray('Cluster', oArgTarget);

				 var target = null;

				 if(clusterIndex>1){
				 var cluster = oArgTarget[clusterIndex+1];
				 var host = oArgTarget[clusterIndex+2];
				 var dataSource = oArgTarget[clusterIndex+3].slice(1,oArgTarget[clusterIndex+3].length);
				 }

				 var arg = {
				 userid : 1,
				 grid : '',
				 cluster : cluster,
				 host: host,
				 datasource : dataSource
				 };
				 ajax(arg,myOptions.addFavorAjaxUrl,addFavorCallback);
				 })*/
			}

			function addFavorCallback(oResponse) {
				log("mhrGraphChart addFavorCallback");
				//console.log(oResponse);
			}

			function setTitleFlag() {
				log("mhrGraphChart setTitleFlag");
				myOptions.createTitleFlag = true;
			}

			init();
		});
	};
})(jQuery); 