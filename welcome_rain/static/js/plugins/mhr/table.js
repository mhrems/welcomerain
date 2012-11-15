(function($) {
	$.fn.mhrGraphTable = function(options) {
		var defaults = {
			graphNumber : 1,
			graphDivPrefix : 'bond',
			debug : false,
			isDetail : false
		};
		var myOptions = $.extend(defaults, options);

		this.each(function() {
			var targetObject = $(this);

			var tableOption = {
				row : 1,
				column : 1,
				border : false,
				divMargin : 10,
				divPadding : 20,
				divWidth : 500,
				titleDivHeight : 20,
				bodyDivHeight : 400
			}

			function log(sMessage) {
				if (myOptions.debug)
					console.log(sMessage);
			}

			function init() {
				log("mhrGraphTable init");
				clearDom(targetObject);
				html = createTalbeHtml();
				renderToDom(targetObject, html);
			}

			function clearDom(object) {
				log("mhrGraphTable clearDom");
				object.empty();
			}

			function createTalbeHtml() {
				log("mhrGraphTable createTalbeHtml");
				setBaseTableConfig();
				var html = getTableHtml();
				return html;
			}

			function setBaseTableConfig() {
				log("mhrGraphTable setBaseTableConfig");
				setTableMetrix();
				setTableSize();

			}

			function setTableMetrix() {
				log("mhrGraphTable setTableMetrix");

				var sizeOneMetrix = {
					maxNum : 1,
					row : 1,
					column : 1
				}
				var sizeTwoMetrix = {
					maxNum : 12,
					row : 4,
					column : 3
				}
				var sizeThreeMetrix = {
					maxNum : 30,
					row : 8,
					column : 4
				}
				var sizeFourMetrix = {
					maxNum : 50,
					row : 13,
					column : 4
				}
				var sizeMaxMetrix = {
					row : 20,
					column : 4
				}

				if (myOptions.graphNumber == sizeOneMetrix.maxNum) {
					tableOption.row = sizeOneMetrix.row;
					tableOption.column = sizeOneMetrix.column;
				} else if (myOptions.graphNumber <= sizeTwoMetrix.maxNum) {
					tableOption.row = sizeTwoMetrix.row;
					tableOption.column = sizeTwoMetrix.column;
				} else if (myOptions.graphNumber <= sizeThreeMetrix.maxNum) {
					tableOption.row = sizeThreeMetrix.row;
					tableOption.column = sizeThreeMetrix.column;
				} else if (myOptions.graphNumber <= sizeFourMetrix.maxNum) {
					tableOption.row = sizeFourMetrix.row;
					tableOption.column = sizeFourMetrix.column;
				} else {
					tableOption.row = sizeMaxMetrix.row;
					tableOption.column = sizeMaxMetrix.column;
				}
			}

			function setTableSize() {
				log("mhrGraphTable setTableSize");
				var targetWidth = targetObject.width();
				//tableOption.divWidth = (targetWidth - (targetWidth)/30) / tableOption.column;
				//console.log(targetWidth);

				//tableOption.divWidth = Math.floor((targetWidth / tableOption.column) - (tableOption.divMargin * tableOption.column));
				tableOption.divWidth = Math.floor((targetWidth / tableOption.column) - (tableOption.divMargin * 2) - (tableOption.divPadding *2));
				
				//tableOption.divWidth = Math.floor((targetWidth / tableOption.column) - (tableOption.divMargin * 2));
				//tableOption.divWidth = Math.floor((targetWidth / tableOption.column));
				//console.log((targetWidth / tableOption.column))
				//console.log((tableOption.divMargin * tableOption.column));
				//console.log(tableOption.divWidth);

				//tableOption.bodyDivHeight = tableOption.divWidth;
				if(myOptions.isDetail) tableOption.bodyDivHeight = 300;
				else tableOption.bodyDivHeight = tableOption.divWidth;
				//console.log(tableOption.divWidth);
			}

			function getTableHtml() {
				log("mhrGraphTable getTableHtml");

				var idNum = 0;
				var tableHtml = '';
				if (tableOption.border)
					tableHtml += '<table class="graphTable" border=1>';
				else
					tableHtml += '<table class="graphTable">';
				for (var row = 0; row < tableOption.row; row++) {
					tableHtml += '<tr>';
					for (var column = 0; column < tableOption.column; column++) {
						tableHtml += '<td>';
						//tableHtml += '<div class="chart_box" style="margin:' + tableOption.divMargin + 'px;padding:' + tableOption.divPadding + 'px;">';
						tableHtml += '<div class="chart_box" style="margin:' + tableOption.divMargin + 'px;">';
						//tableHtml += '<div>';
						
						if(myOptions.isDetail){
							tableHtml += '<div class="chart_title" id="' + myOptions.graphDivPrefix + '_title_' + idNum + '" style="width:' + tableOption.divWidth + 'px;height:0px;padding:0px; "></div>';
						}
						
						else{
							tableHtml += '<div class="chart_title" id="' + myOptions.graphDivPrefix + '_title_' + idNum + '" style="width:' + tableOption.divWidth + 'px;height:' + tableOption.titleDivHeight + 'px;padding:'+tableOption.divPadding+'px; "></div>';
						}
						
						tableHtml += '<div style="padding:'+tableOption.divPadding+'px; ">'
						tableHtml += '<div class="chart_content" id="' + myOptions.graphDivPrefix + '_body_' + idNum + '" style="width:' + tableOption.divWidth + 'px;height:' + tableOption.bodyDivHeight + 'px"></div>';
						tableHtml += '</div>';
						tableHtml += '</div>';
						tableHtml += '</td>';
						idNum++;
					}
					tableHtml += '</tr>';
				}
				tableHtml += '</table>';
				return tableHtml;
			}

			function renderToDom(object, html) {
				log("mhrGraphTable renderToDom");
				object.append(html)
			}

			init();
		});
	};
})(jQuery); 