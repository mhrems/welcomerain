function getFormElement(label, value) {
	//console.log("asdfasfsadfsafasdfasdfsa");
	var html = '<div class="form-row row-fluid">';
	html = html + '<div class="span12">';
	html = html + '   <div class="row-fluid">';
	html = html + '      <label class="form-label span4" for="normal">' + label + '</label>';
	html = html + '      <input class="span8 text" id="normalInput" readonly="readonly" type="text" value="' + value + '">';
	html = html + '   </div>';
	html = html + '</div>';
	html = html + '</div>';
	return html;
}

function getFormBoxTitle(title) {
	var html = '<div class="title">';
	html += '<h3 class="borderBottom">';
	html += '   <span>' + title + '</span>';
	html += '</h3>';
	html += '</div>';
	return html;
}

function getNoDataBox(caption) {
	
	var html='<div class="box gradient">';
	html += '<div class="title">';
	html += '<h3 class="borderBottom"><span class="icon16 icomoon-icon-power"></span><span>Notice</span></h3>';
	html += '</div>';
	html += '<div class="content">';
	html += '<ul class="activity">';
	html += '<li>';
	html += '	<div class="noData">';
	html += '		<h3 class="centered">';						
	html += caption;							
	html += '		</h3>';								
	html += '	</div>';
	html += '</li>';						
	html += '</ul>';					
	html += '	</div>';
	html += '	</div>';
	
	return html;
}
