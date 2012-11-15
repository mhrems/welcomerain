// document ready function
$(document).ready(function() {

//----------------------------------- Yepnope condition load  ---------------------------//
yepnope([
	//load all scripts included in every page or depencies
	{
	load: [
        'js/jquery.cookie.js',
        'js/bootstrap/bootstrap.min.js', 
        'js/jquery.mousewheel.js', 
        'plugins/qtip/jquery.qtip.min.js', 
        'plugins/uniform/jquery.uniform.min.js', 
        'plugins/pnotify/jquery.pnotify.min.js', 
        'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.21/jquery-ui.min.js', 
        'plugins/touch-punch/jquery.ui.touch-punch.min.js', 
        'plugins/ios-fix/ios-orientationchange-fix.js',
        'plugins/prettify/prettify.js',
        'plugins/watermark/jquery.watermark.min.js',
        'plugins/lazy-load/jquery.lazyload.min.js',
        'plugins/dualselect/jquery.dualListBox-1.3.min.js',
        'js/app.js',
        'js/main.js'
      ]
	},

	//check charts if have chart on page load the flot
	{
	    test: $(".visitors-chart").length && 
	    	  $(".pieStats").length && 
	    	  $(".simple-chart").length && 
	    	  $(".simple-donut").length &&
	    	  $(".simple-pie").length && 
	    	  $(".order-bars-chart").length &&  
	    	  $(".stacked-bars-chart").length && 
	    	  $(".lines-chart").length && 
	    	  $(".horizontal-bars-chart").length && 
	    	  $(".auto-update-chart").length
	    ,
	    yep: ['plugins/flot/jquery.flot.js',
	    	  'plugins/flot/jquery.flot.grow.js',
	    	  'plugins/flot/jquery.flot.pie.js',
	    	  'plugins/flot/jquery.flot.resize.js',
	    	  'plugins/flot/jquery.flot.tooltip_0.4.4.js',
	    	  'plugins/flot/jquery.flot.orderBars.js'
	    ],
	    callback: function(url, res, key) {
	    	//------------- Visitor chart -------------//
	    	$(function () {
				//some data
				var d1 = [[1, 3+randNum()], [2, 6+randNum()], [3, 9+randNum()], [4, 12+randNum()],[5, 15+randNum()],[6, 18+randNum()],[7, 21+randNum()],[8, 15+randNum()],[9, 18+randNum()],[10, 21+randNum()],[11, 24+randNum()],[12, 27+randNum()],[13, 30+randNum()],[14, 33+randNum()],[15, 24+randNum()],[16, 27+randNum()],[17, 30+randNum()],[18, 33+randNum()],[19, 36+randNum()],[20, 39+randNum()],[21, 42+randNum()],[22, 45+randNum()],[23, 36+randNum()],[24, 39+randNum()],[25, 42+randNum()],[26, 45+randNum()],[27,38+randNum()],[28, 51+randNum()],[29, 55+randNum()], [30, 60+randNum()]];
				var d2 = [[1, randNum()-5], [2, randNum()-4], [3, randNum()-4], [4, randNum()],[5, 4+randNum()],[6, 4+randNum()],[7, 5+randNum()],[8, 5+randNum()],[9, 6+randNum()],[10, 6+randNum()],[11, 6+randNum()],[12, 2+randNum()],[13, 3+randNum()],[14, 4+randNum()],[15, 4+randNum()],[16, 4+randNum()],[17, 5+randNum()],[18, 5+randNum()],[19, 2+randNum()],[20, 2+randNum()],[21, 3+randNum()],[22, 3+randNum()],[23, 3+randNum()],[24, 2+randNum()],[25, 4+randNum()],[26, 4+randNum()],[27,5+randNum()],[28, 2+randNum()],[29, 2+randNum()], [30, 3+randNum()]];
				//define placeholder class
				var placeholder = $(".visitors-chart");
				//graph options
				var options = {
						grid: {
							show: true,
						    aboveData: true,
						    color: "#3f3f3f" ,
						    labelMargin: 5,
						    axisMargin: 0, 
						    borderWidth: 0,
						    borderColor:null,
						    minBorderMargin: 5 ,
						    clickable: true, 
						    hoverable: true,
						    autoHighlight: true,
						    mouseActiveRadius: 20
						},
				        series: {
				        	grow: {
				        		active: true,
				        		stepMode: "linear",
				        		steps: 50,
				        		stepDelay: true
				        	},
				            lines: {
			            		show: true,
			            		fill: true,
			            		lineWidth: 4,
			            		steps: false
				            	},
				            points: {
				            	show:true,
				            	radius: 5,
				            	symbol: "circle",
				            	fill: true,
				            	borderColor: "#fff",
				            }
				        },
				        legend: { 
				        	position: "ne", 
				        	margin: [0,-25], 
				        	noColumns: 0,
				        	labelBoxBorderColor: null,
				        	labelFormatter: function(label, series) {
							    // just add some space to labes
							    return label+'&nbsp;&nbsp;';
							 }
				    	},
				        yaxis: { min: 0 },
				        xaxis: {ticks:11, tickDecimals: 0},
				        colors: chartColours,
				        shadowSize:1,
				        tooltip: true, //activate tooltip
						tooltipOpts: {
							content: "%s : %y.0",
							shifts: {
								x: -30,
								y: -50
							}
						}
				    };   
			
		        	$.plot(placeholder, [ 

		        		{
		        			label: "Visits", 
		        			data: d1,
		        			lines: {fillColor: "#f2f7f9"},
		        			points: {fillColor: "#88bbc8"}
		        		}, 
		        		{	
		        			label: "Unique Visits", 
		        			data: d2,
		        			lines: {fillColor: "#fff8f2"},
		        			points: {fillColor: "#ed7a53"}
		        		} 

		        	], options);
			        
		    });
			
			//Pie visit graph
			$(function () {
			   var data = [
				    { label: "%78.75 New Visitor",  data: 78.75, color: "#88bbc8"},
				    { label: "%21.25 Returning Visitor",  data: 21.25, color: "#ed7a53"}
				];
				
				$.plot($(".pieStats"), data, 
				{
					series: {
						pie: { 
							show: true,
							highlight: {
								opacity: 0.1
							},
							stroke: {
								color: '#fff',
								width: 3
							},
							startAngle: 2,
							label: {
								radius:1
							}
						},
						grow: {	active: false},
					},
					legend: { 
			        	position: "ne", 
			        	labelBoxBorderColor: null
			    	},
					grid: {
			            hoverable: true,
			            clickable: true
			        },
			        tooltip: true, //activate tooltip
					tooltipOpts: {
						content: "%s : %y.1",
						shifts: {
							x: -30,
							y: -50
						}
					}
				});
			});

			//Simple chart 
			$(function () {
				var sin = [], cos = [];
			    for (var i = 0; i < 14; i += 0.5) {
			        sin.push([i, Math.sin(i)]);
			        cos.push([i, Math.cos(i)]);
			    }
			    //graph options
				var options = {
						grid: {
							show: true,
						    aboveData: true,
						    color: "#3f3f3f" ,
						    labelMargin: 5,
						    axisMargin: 0, 
						    borderWidth: 0,
						    borderColor:null,
						    minBorderMargin: 5 ,
						    clickable: true, 
						    hoverable: true,
						    autoHighlight: true,
						    mouseActiveRadius: 20
						},
				        series: {
				        	grow: {active: false},
				            lines: {
			            		show: true,
			            		fill: false,
			            		lineWidth: 4,
			            		steps: false
				            	},
				            points: {
				            	show:true,
				            	radius: 5,
				            	symbol: "circle",
				            	fill: true,
				            	borderColor: "#fff",
				            }
				        },
				        legend: { position: "se" },
				        colors: chartColours,
				        shadowSize:1,
				        tooltip: true, //activate tooltip
						tooltipOpts: {
							content: "%s : %y.3",
							shifts: {
								x: -30,
								y: -50
							}
						}
				};  
				var plot = $.plot($(".simple-chart"),
		           [{
		    			label: "Sin", 
		    			data: sin,
		    			lines: {fillColor: "#f2f7f9"},
		    			points: {fillColor: "#88bbc8"}
		    		}, 
		    		{	
		    			label: "Cos", 
		    			data: cos,
		    			lines: {fillColor: "#fff8f2"},
		    			points: {fillColor: "#ed7a53"}
		    		}], options);
			});

			//Donut simple chart
			$(function () {
				var data = [
				    { label: "USA",  data: 38, color: "#88bbc8"},
				    { label: "Brazil",  data: 23, color: "#ed7a53"},
				    { label: "India",  data: 15, color: "#9FC569"},
				    { label: "Turkey",  data: 9, color: "#bbdce3"},
				    { label: "France",  data: 7, color: "#9a3b1b"},
				    { label: "China",  data: 5, color: "#5a8022"},
				    { label: "Germany",  data: 3, color: "#2c7282"}
				];

			    $.plot($(".simple-donut"), data, 
				{
					series: {
						pie: { 
							show: true,
							innerRadius: 0.4,
							highlight: {
								opacity: 0.1
							},
							radius: 1,
							stroke: {
								color: '#fff',
								width: 8
							},
							startAngle: 2,
						    combine: {
			                    color: '#353535',
			                    threshold: 0.05
			                },
			                label: {
			                    show: true,
			                    radius: 1,
			                    formatter: function(label, series){
			                        return '<div class="pie-chart-label">'+label+'&nbsp;'+Math.round(series.percent)+'%</div>';
			                    }
			                }
						},
						grow: {	active: false}
					},
					legend:{show:false},
					grid: {
			            hoverable: true,
			            clickable: true
			        },
			        tooltip: true, //activate tooltip
					tooltipOpts: {
						content: "%s : %y.1"+"%",
						shifts: {
							x: -30,
							y: -50
						}
					}
				});
			});
			
			//Pie simple chart
			$(function () {
				var data = [
				    { label: "USA",  data: 38, color: "#88bbc8"},
				    { label: "Brazil",  data: 23, color: "#ed7a53"},
				    { label: "India",  data: 15, color: "#9FC569"},
				    { label: "Turkey",  data: 9, color: "#bbdce3"},
				    { label: "France",  data: 7, color: "#9a3b1b"},
				    { label: "China",  data: 5, color: "#5a8022"},
				    { label: "Germany",  data: 3, color: "#2c7282"}
				];

			    $.plot($(".simple-pie"), data, 
				{
					series: {
						pie: { 
							show: true,
							highlight: {
								opacity: 0.1
							},
							radius: 1,
							stroke: {
								color: '#fff',
								width: 2
							},
							startAngle: 2,
						    combine: {
			                    color: '#353535',
			                    threshold: 0.05
			                },
			                label: {
			                    show: true,
			                    radius: 1,
			                    formatter: function(label, series){
			                        return '<div class="pie-chart-label">'+label+'&nbsp;'+Math.round(series.percent)+'%</div>';
			                    }
			                }
						},
						grow: {	active: false}
					},
					legend:{show:false},
					grid: {
			            hoverable: true,
			            clickable: true
			        },
			        tooltip: true, //activate tooltip
					tooltipOpts: {
						content: "%s : %y.1"+"%",
						shifts: {
							x: -30,
							y: -50
						}
					}
				});
			});

			//Ordered bars chart
			$(function () {
				//some data
				var d1 = [];
			    for (var i = 0; i <= 10; i += 1)
			        d1.push([i, parseInt(Math.random() * 30)]);
			 
			    var d2 = [];
			    for (var i = 0; i <= 10; i += 1)
			        d2.push([i, parseInt(Math.random() * 30)]);
			 
			    var d3 = [];
			    for (var i = 0; i <= 10; i += 1)
			        d3.push([i, parseInt(Math.random() * 30)]);
			 
			    var ds = new Array();
			 
			     ds.push({
			     	label: "Data One",
			        data:d1,
			        bars: {order: 1}
			    });
			    ds.push({
			    	label: "Data Two",
			        data:d2,
			        bars: {order: 2}
			    });
			    ds.push({
			    	label: "Data Three",
			        data:d3,
			        bars: {order: 3}
			    });

				var options = {
						bars: {
							show:true,
							barWidth: 0.2,
							fill:1
						},
						grid: {
							show: true,
						    aboveData: false,
						    color: "#3f3f3f" ,
						    labelMargin: 5,
						    axisMargin: 0, 
						    borderWidth: 0,
						    borderColor:null,
						    minBorderMargin: 5 ,
						    clickable: true, 
						    hoverable: true,
						    autoHighlight: false,
						    mouseActiveRadius: 20
						},
				        series: {
				        	grow: {active:false}
				        },
				        legend: { position: "ne" },
				        colors: chartColours,
				        tooltip: true, //activate tooltip
						tooltipOpts: {
							content: "%s : %y.0",
							shifts: {
								x: -30,
								y: -50
							}
						}
				};

				$.plot($(".order-bars-chart"), ds, options);
			});
			
			//Stacked bars chart
			$(function () {
				//some data
				var d1 = [];
			    for (var i = 0; i <= 10; i += 1)
			        d1.push([i, parseInt(Math.random() * 30)]);
			 
			    var d2 = [];
			    for (var i = 0; i <= 10; i += 1)
			        d2.push([i, parseInt(Math.random() * 30)]);
			 
			    var d3 = [];
			    for (var i = 0; i <= 10; i += 1)
			        d3.push([i, parseInt(Math.random() * 30)]);
			 
			    var ds = new Array();
			 
			     ds.push({
			     	label: "Data One",
			        data:d1
			    });
			    ds.push({
			    	label: "Data Two",
			        data:d2
			    });
			    ds.push({
			    	label: "Data Tree",
			        data:d3
			    });

				var stack = 0, bars = true, lines = false, steps = false;

				var options = {
						grid: {
							show: true,
						    aboveData: false,
						    color: "#3f3f3f" ,
						    labelMargin: 5,
						    axisMargin: 0, 
						    borderWidth: 0,
						    borderColor:null,
						    minBorderMargin: 5 ,
						    clickable: true, 
						    hoverable: true,
						    autoHighlight: true,
						    mouseActiveRadius: 20
						},
				        series: {
				        	grow: {active:false},
				        	stack: stack,
			                lines: { show: lines, fill: true, steps: steps },
			                bars: { show: bars, barWidth: 0.5, fill:1}
					    },
				        xaxis: {ticks:11, tickDecimals: 0},
				        legend: { position: "se" },
				        colors: chartColours,
				        shadowSize:1,
				        tooltip: true, //activate tooltip
						tooltipOpts: {
							content: "%s : %y.0",
							shifts: {
								x: -30,
								y: -50
							}
						}
				};

				$.plot($(".stacked-bars-chart"), ds, options);
			});
			
			//Lines chart without points
			$(function () {

				//some data
				var d1 = [[1, 3+randNum()], [2, 6+randNum()], [3, 9+randNum()], [4, 12+randNum()],[5, 15+randNum()],[6, 18+randNum()],[7, 21+randNum()],[8, 15+randNum()],[9, 18+randNum()],[10, 21+randNum()],[11, 24+randNum()],[12, 27+randNum()],[13, 30+randNum()],[14, 33+randNum()],[15, 24+randNum()],[16, 27+randNum()],[17, 30+randNum()],[18, 33+randNum()],[19, 36+randNum()],[20, 39+randNum()],[21, 42+randNum()],[22, 45+randNum()],[23, 36+randNum()],[24, 39+randNum()],[25, 42+randNum()],[26, 45+randNum()],[27,38+randNum()],[28, 51+randNum()],[29, 55+randNum()], [30, 60+randNum()]];
				var d2 = [[1, randNum()-5], [2, randNum()-4], [3, randNum()-4], [4, randNum()],[5, 4+randNum()],[6, 4+randNum()],[7, 5+randNum()],[8, 5+randNum()],[9, 6+randNum()],[10, 6+randNum()],[11, 6+randNum()],[12, 2+randNum()],[13, 3+randNum()],[14, 4+randNum()],[15, 4+randNum()],[16, 4+randNum()],[17, 5+randNum()],[18, 5+randNum()],[19, 2+randNum()],[20, 2+randNum()],[21, 3+randNum()],[22, 3+randNum()],[23, 3+randNum()],[24, 2+randNum()],[25, 4+randNum()],[26, 4+randNum()],[27,5+randNum()],[28, 2+randNum()],[29, 2+randNum()], [30, 3+randNum()]];
				//define placeholder class
				var placeholder = $(".lines-chart");
				//graph options
				var options = {
						grid: {
							show: true,
						    aboveData: true,
						    color: "#3f3f3f" ,
						    labelMargin: 5,
						    axisMargin: 0, 
						    borderWidth: 0,
						    borderColor:null,
						    minBorderMargin: 5 ,
						    clickable: true, 
						    hoverable: true,
						    autoHighlight: true,
						    mouseActiveRadius: 20
						},
				        series: {
				        	grow: {active:false},
				            lines: {
			            		show: true,
			            		fill: true,
			            		lineWidth: 2,
			            		steps: false
				            	},
				            points: {show:false}
				        },
				        legend: { position: "se" },
				        yaxis: { min: 0 },
				        xaxis: {ticks:11, tickDecimals: 0},
				        colors: chartColours,
				        shadowSize:1,
				        tooltip: true, //activate tooltip
						tooltipOpts: {
							content: "%s : %y.0",
							shifts: {
								x: -30,
								y: -50
							}
						}
				    };   
			
		        	$.plot(placeholder, [ 

		        		{
		        			label: "Visits", 
		        			data: d1,
		        			lines: {fillColor: "#f2f7f9"},
		        			points: {fillColor: "#88bbc8"}
		        		}, 
		        		{	
		        			label: "Unique Visits", 
		        			data: d2,
		        			lines: {fillColor: "#fff8f2"},
		        			points: {fillColor: "#ed7a53"}
		        		} 

		        	], options);

			});

			//Horizontal bars chart
			$(function () {
				//some data
				//Display horizontal graph
		    var d1_h = [];
		    for (var i = 0; i <= 5; i += 1)
		        d1_h.push([parseInt(Math.random() * 30),i ]);

		    var d2_h = [];
		    for (var i = 0; i <= 5; i += 1)
		        d2_h.push([parseInt(Math.random() * 30),i ]);

		    var d3_h = [];
		    for (var i = 0; i <= 5; i += 1)
		        d3_h.push([ parseInt(Math.random() * 30),i]);
		                
		    var ds_h = new Array();
		    ds_h.push({
		        data:d1_h,
		        bars: {
		            horizontal:true, 
		            show: true, 
		            barWidth: 0.2, 
		            order: 1,
		        }
		    });
			ds_h.push({
			    data:d2_h,
			    bars: {
			        horizontal:true, 
			        show: true, 
			        barWidth: 0.2, 
			        order: 2
			    }
			});
			ds_h.push({
			    data:d3_h,
			    bars: {
			        horizontal:true, 
			        show: true, 
			        barWidth: 0.2, 
			        order: 3
			    }
			});


				var options = {
						grid: {
							show: true,
						    aboveData: false,
						    color: "#3f3f3f" ,
						    labelMargin: 5,
						    axisMargin: 0, 
						    borderWidth: 0,
						    borderColor:null,
						    minBorderMargin: 5 ,
						    clickable: true, 
						    hoverable: true,
						    autoHighlight: false,
						    mouseActiveRadius: 20
						},
				        series: {
				        	grow: {active:false},
					        bars: {
					        	show:true,
								horizontal: true,
								barWidth:0.2,
								fill:1
							}
				        },
				        legend: { position: "ne" },
				        colors: chartColours,
				        tooltip: true, //activate tooltip
						tooltipOpts: {
							content: "%s : %y.0",
							shifts: {
								x: -30,
								y: -50
							}
						}
				};

				$.plot($(".horizontal-bars-chart"), ds_h, options);
			});
			
			//Auto update chart
			$(function () {
				// we use an inline data source in the example, usually data would
			    // be fetched from a server
			    var data = [], totalPoints = 300;
			    function getRandomData() {
			        if (data.length > 0)
			            data = data.slice(1);

			        // do a random walk
			        while (data.length < totalPoints) {
			            var prev = data.length > 0 ? data[data.length - 1] : 50;
			            var y = prev + Math.random() * 10 - 5;
			            if (y < 0)
			                y = 0;
			            if (y > 100)
			                y = 100;
			            data.push(y);
			        }

			        // zip the generated y values with the x values
			        var res = [];
			        for (var i = 0; i < data.length; ++i)
			            res.push([i, data[i]])
			        return res;
			    }

			    // Update interval
			    var updateInterval = 200;

			    // setup plot
			    var options = {
			        series: { 
			        	grow: {active:false}, //disable auto grow
			        	shadowSize: 0, // drawing is faster without shadows
			        	lines: {
		            		show: true,
		            		fill: true,
		            		lineWidth: 2,
		            		steps: false
			            }
			        },
			        grid: {
						show: true,
					    aboveData: false,
					    color: "#3f3f3f" ,
					    labelMargin: 5,
					    axisMargin: 0, 
					    borderWidth: 0,
					    borderColor:null,
					    minBorderMargin: 5 ,
					    clickable: true, 
					    hoverable: true,
					    autoHighlight: false,
					    mouseActiveRadius: 20
					}, 
					colors: chartColours,
			        tooltip: true, //activate tooltip
					tooltipOpts: {
						content: "Value is : %y.0",
						shifts: {
							x: -30,
							y: -50
						}
					},	
			        yaxis: { min: 0, max: 100 },
			        xaxis: { show: true}
			    };
			    var plot = $.plot($(".auto-update-chart"), [ getRandomData() ], options);

			    function update() {
			        plot.setData([ getRandomData() ]);
			        // since the axes don't change, we don't need to call plot.setupGrid()
			        plot.draw();
			        
			        setTimeout(update, updateInterval);
			    }

			    update();
			});

	    },//end callback function
	    complete: function (url, res, key) {

	    }
	},

	//test for circular stats and circular sliders 
	{
	    test: $(".greenCircle").length && 
	    	  $(".redCircle").length &&
	    	  $(".blueCircle").length &&
	    	  $(".progressBlue").length &&
	    	  $(".progressRed").length &&
	    	  $(".progressGreen").length
	    ,
	    yep: 'plugins/knob/jquery.knob.js',
	    callback: function(url, res, key) {
	      	//circular progrress bar
			$(function () {

				$(".greenCircle").knob({
		            'min':0,
		            'max':100,
		            'readOnly': true,
		            'width': 80,
		            'height': 80,
		            'fgColor': '#9FC569',
		            'dynamicDraw': true,
		            'thickness': 0.2,
		            'tickColorizeValues': true
		        })
		        $(".redCircle").knob({
		            'min':0,
		            'max':100,
		            'readOnly': true,
		            'width': 80,
		            'height': 80,
		            'fgColor': '#ED7A53',
		            'dynamicDraw': true,
		            'thickness': 0.2,
		            'tickColorizeValues': true
		        })
		        $(".blueCircle").knob({
		            'min':0,
		            'max':100,
		            'readOnly': true,
		            'width': 80,
		            'height': 80,
		            'fgColor': '#88BBC8',
		            'dynamicDraw': true,
		            'thickness': 0.2,
		            'tickColorizeValues': true
		        })

		        $(".progressBlue").knob({
			        'min':0,
			        'max':100,
			        'readOnly': false,
			        'width': 80,
			        'height': 80,
			        'fgColor': '#88BBC8',
			        'dynamicDraw': false,
			        'thickness': 0.2,
			        'tickColorizeValues': true,
			        "skin":"tron",
			        "cursor":true
			    })

			    $(".progressRed").knob({
			        'min':0,
			        'max':100,
			        'readOnly': false,
			        'width': 80,
			        'height': 80,
			        'fgColor': '#ED7A53',
			        'dynamicDraw': false,
			        'thickness': 0.2,
			        'tickColorizeValues': true,
			        "skin":"tron",
			        "cursor":true
			    })

			    $(".progressGreen").knob({
			        'min':0,
			        'max':100,
			        'readOnly': false,
			        'width': 80,
			        'height': 80,
			        'fgColor': '#9FC569',
			        'dynamicDraw': false,
			        'thickness': 0.2,
			        'tickColorizeValues': true,
			        "skin":"tron",
			        "cursor":true
			    })
			});

	    }//End callback
	},//End knob check

	//test for sparkstats (no need for DOM ready)
	{
	   		  //from sparkStats widget
	    test: $(".sparkLine1").length && 
	    	  $(".sparkLine2").length &&
	    	  $(".sparkLine3").length &&
	    	  $(".sparkLine4").length &&
	    	  $(".sparkLine5").length &&
	    	  $(".sparkLine6").length &&
	    	  $(".sparkLine7").length &&
	    	  //sparkline in sidebar area
	    	  $("#stat1").length && 
	    	  $("#stat2").length && 
	    	  $("#stat3").length && 
	    	  $("#stat4").length && 
	    	  $("#stat5").length && 
	    	  $("#stat6").length 
	    ,
	    yep: 'plugins/sparkline/jquery.sparkline.js',
	    callback: function(url, res, key) {
	      	//circular progrress bar
			$(function () {
				//sparklines (making loop with random data for all 7 sparkline)
				i=1;
				for (i=1; i<8; i++) {
				 	var data = [[1, 3+randNum()], [2, 5+randNum()], [3, 8+randNum()], [4, 11+randNum()],[5, 14+randNum()],[6, 17+randNum()],[7, 20+randNum()], [8, 15+randNum()], [9, 18+randNum()], [10, 22+randNum()]];
				 	placeholder = '.sparkLine' + i;
					$(placeholder).sparkline(data, { 
						width: 100,//Width of the chart - Defaults to 'auto' - May be any valid css width - 1.5em, 20px, etc (using a number without a unit specifier won't do what you want) - This option does nothing for bar and tristate chars (see barWidth)
						height: 30,//Height of the chart - Defaults to 'auto' (line height of the containing tag)
						lineColor: '#88bbc8',//Used by line and discrete charts to specify the colour of the line drawn as a CSS values string
						fillColor: '#f2f7f9',//Specify the colour used to fill the area under the graph as a CSS value. Set to false to disable fill
						spotColor: '#467e8c',//The CSS colour of the final value marker. Set to false or an empty string to hide it
						maxSpotColor: '#9FC569',//The CSS colour of the marker displayed for the maximum value. Set to false or an empty string to hide it
						minSpotColor: '#ED7A53',//The CSS colour of the marker displayed for the mimum value. Set to false or an empty string to hide it
						spotRadius: 3,//Radius of all spot markers, In pixels (default: 1.5) - Integer
						lineWidth: 2,//In pixels (default: 1) - Integer
					});
				}

				//sidebar area
				var positive = [1,5,3,7,8,6,10];
				var negative = [10,6,8,7,3,5,1]
				var negative1 = [7,6,8,7,6,5,4]

				$('#stat1').sparkline(positive,{
					height:15,
					spotRadius: 0,
					barColor: '#9FC569',
					type: 'bar'
				});
				$('#stat2').sparkline(negative,{
					height:15,
					spotRadius: 0,
					barColor: '#ED7A53',
					type: 'bar'
				});
				$('#stat3').sparkline(negative1,{
					height:15,
					spotRadius: 0,
					barColor: '#ED7A53',
					type: 'bar'
				});
				$('#stat4').sparkline(positive,{
					height:15,
					spotRadius: 0,
					barColor: '#9FC569',
					type: 'bar'
				});
				//sparkline in widget
				$('#stat5').sparkline(positive,{
					height:15,
					spotRadius: 0,
					barColor: '#9FC569',
					type: 'bar'
				});

				$('#stat6').sparkline(positive, { 
					width: 70,//Width of the chart - Defaults to 'auto' - May be any valid css width - 1.5em, 20px, etc (using a number without a unit specifier won't do what you want) - This option does nothing for bar and tristate chars (see barWidth)
					height: 20,//Height of the chart - Defaults to 'auto' (line height of the containing tag)
					lineColor: '#88bbc8',//Used by line and discrete charts to specify the colour of the line drawn as a CSS values string
					fillColor: '#f2f7f9',//Specify the colour used to fill the area under the graph as a CSS value. Set to false to disable fill
					spotColor: '#e72828',//The CSS colour of the final value marker. Set to false or an empty string to hide it
					maxSpotColor: '#005e20',//The CSS colour of the marker displayed for the maximum value. Set to false or an empty string to hide it
					minSpotColor: '#f7941d',//The CSS colour of the marker displayed for the mimum value. Set to false or an empty string to hide it
					spotRadius: 3,//Radius of all spot markers, In pixels (default: 1.5) - Integer
					lineWidth: 2,//In pixels (default: 1) - Integer
				});

			});

	    }//End callback
	},//End sparkline check

	//test for Full calendar
	{
	    test: $("#calendar").length && 
	    	  $("#calendar-events").length
	    ,
	    yep: 'plugins/fullcalendar/fullcalendar.min.js',
	    callback: function(url, res, key) {
			
			//------------- Full calendar  -------------//
			$(function () {
				var date = new Date();
				var d = date.getDate();
				var m = date.getMonth();
				var y = date.getFullYear();
				
				//front page calendar
				$('#calendar').fullCalendar({
					//theme: true,
					header: {
						left: 'title,today',
						center: 'prev,next',
						right: 'month,agendaWeek,agendaDay'
					},
					buttonText: {
			        	prev: '<span class="icon24 icomoon-icon-arrow-left"></span>',
			        	next: '<span class="icon24 icomoon-icon-arrow-right"></span>'
			    	},
					editable: true,
					events: [
						{
							title: 'All Day Event',
							start: new Date(y, m, 1)
						},
						{
							title: 'Long Event',
							start: new Date(y, m, d-5),
							end: new Date(y, m, d-2)
						},
						{
							id: 999,
							title: 'Repeating Event',
							start: new Date(y, m, d-3, 16, 0),
							allDay: false
						},
						{
							id: 999,
							title: 'Repeating Event',
							start: new Date(y, m, d+4, 16, 0),
							allDay: false
						},
						{
							title: 'Meeting',
							start: new Date(y, m, d, 10, 30),
							allDay: false
						},
						{
							title: 'Lunch',
							start: new Date(y, m, d, 12, 0),
							end: new Date(y, m, d, 14, 0),
							allDay: false,
							color: '#9FC569'
						},
						{
							title: 'Birthday Party',
							start: new Date(y, m, d+1, 19, 0),
							end: new Date(y, m, d+1, 22, 30),
							allDay: false,
							color: '#ED7A53'
						},
						{
							title: 'Click for Google',
							start: new Date(y, m, 28),
							end: new Date(y, m, 29),
							url: 'http://google.com/'
						}
					]
				});
			});

			/* initialize the external events
			-----------------------------------------------------------------*/
			
			$('#external-events div.external-event').each(function() {
			
				// create an Event Object (http://arshaw.com/fullcalendar/docs/event_data/Event_Object/)
				// it doesn't need to have a start or end
				var eventObject = {
					title: $.trim($(this).text()) // use the element's text as the event title
				};
				
				// store the Event Object in the DOM element so we can get to it later
				$(this).data('eventObject', eventObject);
				
				// make the event draggable using jQuery UI
				$(this).draggable({
					zIndex: 999,
					revert: true,      // will cause the event to go back to its
					revertDuration: 0  //  original position after the drag
				});
				
			});


			/* initialize the calendar
			-----------------------------------------------------------------*/
			
			$('#calendar-events').fullCalendar({
				header: {
					left: 'title,today',
					center: 'prev,next',
					right: 'month,agendaWeek,agendaDay'
				},
				buttonText: {
		        	prev: '<span class="icon24 icomoon-icon-arrow-left"></span>',
		        	next: '<span class="icon24 icomoon-icon-arrow-right"></span>'
		    	},
				editable: true,
				droppable: true, // this allows things to be dropped onto the calendar !!!
				drop: function(date, allDay) { // this function is called when something is dropped
				
					// retrieve the dropped element's stored Event Object
					var originalEventObject = $(this).data('eventObject');
					
					// we need to copy it, so that multiple events don't have a reference to the same object
					var copiedEventObject = $.extend({}, originalEventObject);
					
					// assign it the date that was reported
					copiedEventObject.start = date;
					copiedEventObject.allDay = allDay;
					
					// render the event on the calendar
					// the last `true` argument determines if the event "sticks" (http://arshaw.com/fullcalendar/docs/event_rendering/renderEvent/)
					$('#calendar-events').fullCalendar('renderEvent', copiedEventObject, true);
					$(this).remove();
					
				}

			});

	    }//End callback
	},//End check

	//test for elastic text areas
	{
	    test: $(".elastic").length
	    ,
	    yep: 'plugins/elastic/jquery.elastic.js',
	    callback: function(url, res, key) {
	      	
			$(function () {
				$('.elastic').elastic();
			});

	    }//End callback
	},//End check

	//test for Input limiter
	{
	    test: $(".limit").length 
	    ,
	    yep: 'plugins/inputlimiter/jquery.inputlimiter.1.3.min.js',
	    callback: function(url, res, key) {

			$(function () {
				$('.limit').inputlimiter({
					limit: 100
				});
			});

	    }//End callback
	},//End check

	//test for Masked input fields
	{
	    test: $(".mask").length
	    ,
	    yep: 'plugins/maskedinput/jquery.maskedinput-1.3.min.js',
	    callback: function(url, res, key) {
	      	
			$(function () {
				$("#mask-phone").mask("(999) 999-9999", {completed:function(){alert("Callback action after complete");}});
				$("#mask-phoneExt").mask("(999) 999-9999? x99999");
				$("#mask-phoneInt").mask("+40 999 999 999");
				$("#mask-date").mask("99/99/9999");
				$("#mask-ssn").mask("999-99-9999");
				$("#mask-productKey").mask("a*-999-a999", { placeholder: "*" });
				$("#mask-eyeScript").mask("~9.99 ~9.99 999");
				$("#mask-percent").mask("99%");
			});

	    }//End callback
	},//End check

	//test for Ibutton
	{
	    test: $(".ibutton").length && 
	    	  $(".ibutton1").length &&
	    	  $(".ibuttonCheck").length
	    ,
	    yep: 'plugins/ibutton/jquery.ibutton.min.js',
	    callback: function(url, res, key) {
	      	
			$(function () {
				//------------- I button  -------------//
				$(".ibutton").iButton({
					 labelOn: "ON",
					 labelOff: "OFF",
					 enableDrag: false
				});
				$(".ibutton1").iButton({
					 labelOn: "ONLINE",
					 labelOff: "OFFLINE",
					 enableDrag: false
				});
				$(".ibuttonCheck").iButton({
					 labelOn: "<span class='icon16 typ-icon-checkmark white'></span>",
					 labelOff: "<span class='icon16 typ-icon-cancel white'></span>",
					 enableDrag: false
				});

			});

	    }//End callback
	},//End check

	//test for Stepper/spinner
	{
	    test: $(".ui-stepper").length
	    ,
	    yep: 'plugins/stepper/ui.stepper.js',
	    callback: function(url, res, key) {
	      	
			$(function () {
				//------------- Spinners with steps  -------------//
				$('#ns_0').stepper();
				$('#ns_1').stepper({
					min:-100, 
					max:100, 
					step:10,
					start:-100
				});
				$('#ns_2').stepper({
					step:0.1, 
					decimals:1
				});
				$('#ns_3').stepper({
					step:0.5, 
					format:'currency'
				});

			});

	    }//End callback
	},//End check

	//test for Color picker
	{
	    test: $(".picker").length 
	    ,
	    yep: 'plugins/color-picker/colorpicker.js',
	    callback: function(url, res, key) {
	      	
			$(function () {
				$('.picker').farbtastic('#color');
			});

	    }//End callback
	},//End check

	//test for Time picker (spinner)
	{
	    test: $("#timepicker").length 
	    ,
	    yep: 'plugins/timeentry/jquery.timeentry.min.js',
	    callback: function(url, res, key) {
	      	
			$(function () {
				//------------- Time entry (picker) -------------//
				$('#timepicker').timeEntry({
					show24Hours: true,
					spinnerImage: ''
				});
				$('#timepicker').timeEntry('setTime', '22:15');
			});

	    }//End callback
	},//End check

	//test for Select plugin 
	{
	    test: $("#tags").length && 
	    	  $("#select1").length &&
	    	  $("#select2").length
	    ,
	    yep: 'plugins/select/select2.min.js',
	    callback: function(url, res, key) {
	      	
			$(function () {
				//------------- Tags plugin  -------------//
				$("#tags").select2({
					tags:["red", "green", "blue", "orange"]
				});

				//------------- Select plugin -------------//
				$("#select1").select2();
				$("#select2").select2();

			});

	    }//End callback
	},//End check

	//test for TinyMce plugin
	{
	    test: $(".tinymce").length
	    ,
	    yep: 'plugins/tiny_mce/jquery.tinymce.js',
	    callback: function(url, res, key) {
	      	
			$(function () {
				//--------------- Tinymce ------------------//
				$('textarea.tinymce').tinymce({
					// Location of TinyMCE script
					script_url : 'plugins/tiny_mce/tiny_mce.js',

					// General options
					theme : "advanced",
					plugins : "autolink,lists,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template,advlist",

					// Theme options
					theme_advanced_buttons1 : "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,styleselect,formatselect,fontselect,fontsizeselect",
					theme_advanced_buttons2 : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code,|,insertdate,inserttime,preview,|,forecolor,backcolor",
					theme_advanced_buttons3 : "tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,media,advhr,|,print,|,ltr,rtl,|,fullscreen",
					theme_advanced_buttons4 : "insertlayer,moveforward,movebackward,absolute,|,styleprops,|,cite,abbr,acronym,del,ins,attribs,|,visualchars,nonbreaking,template,pagebreak",
					theme_advanced_toolbar_location : "top",
					theme_advanced_toolbar_align : "left",
					theme_advanced_statusbar_location : "bottom",
					theme_advanced_resizing : true,

					// Example content CSS (should be your site CSS)
					content_css : "css/main.css",

					// Drop lists for link/image/media/template dialogs
					template_external_list_url : "lists/template_list.js",
					external_link_list_url : "lists/link_list.js",
					external_image_list_url : "lists/image_list.js",
					media_external_list_url : "lists/media_list.js",

					// Replace values for the template plugin
					template_replace_values : {
						username : "SuprUser",
						staffid : "991234"
					}
				});

			});

	    }//End callback
	},//End check

	//test for Validation plugin
	{
	    test: $("#form-validate").length && 
	    	  $("#wizzard-form").length
	    ,
	    yep: 'plugins/validate/jquery.validate.min.js',
	    callback: function(url, res, key) {
	      	
			$(function () {
				//--------------- Form validation ------------------//
			    $("#form-validate").validate({
			    	rules: {
						required: "required",
						required1: {
							required: true,
							minlength: 4
						},
						password: {
							required: true,
							minlength: 5
						},
						confirm_password: {
							required: true,
							minlength: 5,
							equalTo: "#password"
						},
						email: {
							required: true,
							email: true
						},
						maxLenght: {
							required: true,
			      			maxlength: 10
						},
						rangelenght: {
					      required: true,
					      rangelength: [10, 20]
					    },
					    minval: {
					      required: true,
					      min: 13
					    },
					    maxval: {
					      required: true,
					      max: 13
					    },
					    range: {
					      required: true,
					      range: [5, 10]
					    },
					    url: {
					      required: true,
					      url: true
					    },
					    date: {
					      required: true,
					      date: true
					    },
					    number: {
					      required: true,
					      number: true
					    },
					    digits: {
					      required: true,
					      digits: true
					    },
					    ccard: {
					      required: true,
					      creditcard: true
					    },
						agree: "required"
					},
					messages: {
						required: "Please enter a something",
						required1: {
							required: "This field is required",
							minlength: "This field must consist of at least 4 characters"
						},
						password: {
							required: "Please provide a password",
							minlength: "Your password must be at least 5 characters long"
						},
						confirm_password: {
							required: "Please provide a password",
							minlength: "Your password must be at least 5 characters long",
							equalTo: "Please enter the same password as above"
						},
						email: "Please enter a valid email address",
						agree: "Please accept our policy"
					}	
			    });

				$("#wizzard-form").validate({
			    	rules: {
			    		fname: {
							required: true,
							minlength: 4
						},
						lname: {
							required: true,
							minlength: 4,
						},
						gender: {
							required: true,
						},
						username1: {
							required: true,
							minlength: 4
						},
						password1: {
							required: true,
							minlength: 5
						},
						confirm_password1: {
							required: true,
							minlength: 5,
							equalTo: "#password1"
						},
						email1: {
							required: true,
							email: true
						}
					},
					messages: {
						fname: {
							required: "This field is required",
							minlength: "This field must consist of at least 4 characters"
						},
						lname: {
							required: "This field is required",
							minlength: "This field must consist of at least 4 characters"
						},
						password1: {
							required: "Please provide a password",
							minlength: "Your password must be at least 5 characters long"
						},
						confirm_password1: {
							required: "Please provide a password",
							minlength: "Your password must be at least 5 characters long",
							equalTo: "Please enter the same password as above"
						},
						email1: "Please enter a valid email address",
						gender: "Choise a gender"
					}	
			    });

			});

	    }//End callback
	},//End check

	//test for Animated progress bar
	{
	    test: $("#progress1").length &&
	    	  $("#progress2").length && 
	    	  $("#progress3").length  
	    ,
	    yep: 'plugins/animated-progress-bar/jquery.progressbar.js',
	    callback: function(url, res, key) {
	      	
			$(function () {
				//animated progress bar
				$('#progress1').anim_progressbar();

				// from second #5 till 15
			    var iNow = new Date().setTime(new Date().getTime() + 5 * 1000); // now plus 5 secs
			    var iEnd = new Date().setTime(new Date().getTime() + 15 * 1000); // now plus 15 secs
			    $('#progress2').anim_progressbar({start: iNow, finish: iEnd, interval: 100});

			    // we will just set interval of updating to 2 sec
			    $('#progress3').anim_progressbar({interval: 2000});

			});

	    }//End callback
	},//End check

	//test for JPages and Gallery
	{
	    test: $(".holder").length 
	    ,
	    yep: 'plugins/jpages/jPages.min.js',
	    callback: function(url, res, key) {
			
			//--------------- Gallery & lazzy load & jpaginate ------------------//
			$(function() {
				//hide the action buttons
				$('.actionBtn').hide();
				//show action buttons on hover image
				$('.galleryView>li').hover(
					function () {
					   $(this).find('.actionBtn').stop(true, true).show();
					},
					function () {
					    $(this).find('.actionBtn').stop(true, true).hide();
					}
				);
				//remove the gallery item after press delete
				$('.actionBtn>.delete').click(function(){
					$(this).closest('li').remove();
					/* destroy and recreate gallery */
				    $("div.holder").jPages("destroy").jPages({
				        containerID : "itemContainer",
				        animation   : "fadeInUp",
				        perPage		: 16,
				        scrollBrowse   : true, //use scroll to change pages
				        keyBrowse   : true,
				        callback    : function( pages ,items ){
				            /* lazy load current images */
				            items.showing.find("img").trigger("turnPage");
				            /* lazy load next page images */
				            items.oncoming.find("img").trigger("turnPage");
				        }
				    });
				    // add notificaton 
					$.pnotify({
						type: 'success',
					    title: 'Done',
			    		text: 'You just delete this picture.',
					    icon: 'picon icon16 brocco-icon-info white',
					    opacity: 0.95,
					    history: false,
					    sticker: false
					});

				});

			    /* initiate lazyload defining a custom event to trigger image loading  */
			    $("ul#itemContainer li img").lazyload({
			        event : "turnPage",
			        effect : "fadeIn"
			    });
			    /* initiate plugin */
			    $("div.holder").jPages({
			        containerID : "itemContainer",
			        animation   : "fadeInUp",
			        perPage		: 16,
			        scrollBrowse   : true, //use scroll to change pages
			        keyBrowse   : true,
			        callback    : function( pages ,items ){
			            /* lazy load current images */
			            items.showing.find("img").trigger("turnPage");
			            /* lazy load next page images */
			            items.oncoming.find("img").trigger("turnPage");
			        }
			    });
			});

	    }//End callback
	},//End check

	//test for Pretty photo
	{
	    test: $("a[rel^='prettyPhoto'").length 
	    ,
	    yep: 'plugins/pretty-photo/jquery.prettyPhoto.js',
	    callback: function(url, res, key) {
	      	
			$(function () {
				//--------------- Prettyphoto ------------------//
				$("a[rel^='prettyPhoto']").prettyPhoto({
					default_width: 800,
					default_height: 600,
					theme: 'facebook',
					social_tools: false,
					show_title: false,
				});

			});

	    }//End callback
	},//End check

	//test for Smart Wizard
	{
	    test: $("#wizard").length && 
	    	  $("#wizard-validation").length
	    ,
	    yep: 'plugins/smartWizzard/jquery.smartWizard-2.0.min.js',
	    callback: function(url, res, key) {
	      	
			$(function () {
				//------------- Smart Wizzard  -------------//	
			  	$('#wizard').smartWizard({
			  		transitionEffect: 'fade', // Effect on navigation, none/fade/slide/
			  		onLeaveStep:leaveAStepCallback,
			        onFinish:onFinishCallback
			    });

			    function leaveAStepCallback(obj){
			        var step = obj;
			        step.find('.stepNumber').stop(true, true).remove();
			        step.find('.stepDesc').stop(true, true).before('<span class="stepNumber"><span class="icon16 iconic-icon-checkmark"></span></span>');
			        return true;
			    }
			    function onFinishCallback(obj){
			    	var step = obj;
			    	step.find('.stepNumber').stop(true, true).remove();
			        step.find('.stepDesc').stop(true, true).before('<span class="stepNumber"><span class="icon16 iconic-icon-checkmark"></span></span>');
			      	$.pnotify({
						type: 'success',
					    title: 'Done',
			    		text: 'You finish the wizzard',
					    icon: 'picon icon16 iconic-icon-check-alt white',
					    opacity: 0.95,
					    history: false,
					    sticker: false
					});
			    }

			    $('#wizard-validation').smartWizard({
			  		transitionEffect: 'fade', // Effect on navigation, none/fade/slide/
			  		onLeaveStep:leaveAStepCallbackValidation,
			        onFinish:onFinishCallbackValidaton
			    });

			    function leaveAStepCallbackValidation(obj){
			        var step = obj;
			        var stepN = step.attr('rel')
			        
			       /* if(stepN == 1) { return true;}     */  
			        //validate step 1
			        if(stepN == 1) {

			        	if ($("#username1").valid() == true ) {
					        var validate = true;
					    } else {
					    	var validate = false;
					    }
					    if ($("#password1").valid() == true ) {
					        var validate1 = true;
					    } 
					    else {
					    	var validate1 = false;
					    }
					    if ($("#passwordConfirm1").valid() == true ) {
					        var validate2 = true;
					    } 
					    else {
					    	var validate2 = false;
					    }

				        if(validate == true && validate1 == true && validate2 == true) {
				        	step.find('.stepNumber').stop(true, true).remove();
			        		step.find('.stepDesc').stop(true, true).before('<span class="stepNumber"><span class="icon16 iconic-icon-checkmark"></span></span>');
				        	return true;
				        } else {
				        	return false;
				        }
			        }
			        //validate step 2
			        if(stepN == 2) {

			        	if ($("#fname").valid() == true ) {
					        var validate3 = true;
					    } else {
					    	var validate3 = false;
					    }
					    if ($("#lname").valid() == true ) {
					        var validate4 = true;
					    } else {
					    	var validate4 = false;
					    }
					    if ($("#gender").valid() == true ) {
					        var validate5 = true;
					    } 
					    else {
					    	var validate5 = false;
					    }

				        if(validate3 == true && validate4 == true && validate5 == true) {
				        	step.find('.stepNumber').stop(true, true).remove();
			        		step.find('.stepDesc').stop(true, true).before('<span class="stepNumber"><span class="icon16 iconic-icon-checkmark"></span></span>');
				        	return true;
				        } else {
				        	return false;
				        }
			        }

			        //validate step 2
			        if(stepN == 3) {

			        	if ($("#email1").valid() == true ) {
					        var validate6 = true;
					    } else {
					    	var validate6 = false;
					    }
					   
				        if(validate6 == true ) {
				        	step.find('.stepNumber').stop(true, true).remove();
			        		step.find('.stepDesc').stop(true, true).before('<span class="stepNumber"><span class="icon16 iconic-icon-checkmark"></span></span>');
				        	return true;
				        } else {
				        	return false;
				        }
			        }
			       
			    }
			    function onFinishCallbackValidaton(obj){
			    	var step = obj;
			    	step.find('.stepNumber').stop(true, true).remove();
			        step.find('.stepDesc').stop(true, true).before('<span class="stepNumber"><span class="icon16 iconic-icon-checkmark"></span></span>');
			      	$.pnotify({
						type: 'success',
					    title: 'Done',
			    		text: 'You finish the wizzard',
					    icon: 'picon icon16 iconic-icon-check-alt white',
					    opacity: 0.95,
					    history: false,
					    sticker: false
					});
					$('#wizzard-form').submit();
			    }

			});

	    }//End callback
	},//End check

	//test for Data tables plugin
	{
	    test: $(".dynamicTable").length &&
	          $(".contactTable").length
	    ,
	    yep: 'plugins/dataTables/jquery.dataTables.min.js',
	    callback: function(url, res, key) {
	      	
			$(function () {
				//--------------- Data tables ------------------//
			
				$('.dynamicTable').dataTable({
					"sPaginationType": "full_numbers",
					"bJQueryUI": false,
					"bAutoWidth": false,
					"bLengthChange": false
				});
						
				$('.contactTable').dataTable({
					"bJQueryUI": false,
					"bAutoWidth": false,
					"iDisplayLength": 5,
					"bLengthChange": false,
					"aoColumnDefs": [{ 
						"bSortable": false, "aTargets": [ 0, 1, 2, 3 ] 
					}],
				});

			});

	    }//End callback
	},//End check

	//test for Elfinder
	{
	    test: $("#elfinder").length 
	    ,
	    yep: 'plugins/elfinder/elfinder.min.js',
	    callback: function(url, res, key) {
	      	
			$(function () {
				//------------- Elfinder file manager  -------------//
			    var elf = $('#elfinder').elfinder({
					// lang: 'ru',             // language (OPTIONAL)
					url : 'php/connector.php'  // connector URL (REQUIRED)
				}).elfinder('instance');

			});

	    }//End callback
	},//End check

	//test for Elfinder
	{
	    test: $("#html4_uploader").length 
	    ,
	    yep: [
	    	  'plugins/plupload/plupload.js',
	    	  'plugins/plupload/plupload.html4.js', 
	          'plugins/plupload/jquery.plupload.queue/jquery.plupload.queue.js'
	    ],
	    callback: function(url, res, key) {
	      	
			$(function () {
				//------------- Plupload php upload  -------------//
			    // Setup html4 version
				$("#html4_uploader").pluploadQueue({
					// General settings
					runtimes : 'html4', 
					url : 'php/upload.php',
					max_file_size : '10mb',
					max_file_count: 15, // user can add no more then 15 files at a time
					chunk_size : '1mb',
					unique_names : true,
					multiple_queues : true,

					// Resize images on clientside if we can
					resize : {width : 320, height : 240, quality : 80},
					
					// Rename files by clicking on their titles
					rename: true,
					
					// Sort files
					sortable: true,

					// Specify what files to browse for
					filters : [
						{title : "Image files", extensions : "jpg,gif,png"},
						{title : "Zip files", extensions : "zip,avi"}
					]
				});

			});

	    }//End callback
	},//End check

	//test for Responsive tables
	{
	    test: $(".responsive").length 
	    ,
	    yep: 'plugins/responsive-tables/responsive-tables.js',
	    callback: function(url, res, key) {
	      	//Responsive tables is handled automatic
	    }//End callback
	}//End check
]);	

});