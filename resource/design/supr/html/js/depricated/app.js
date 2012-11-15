$(document).ready(function() {	
	//prevent font flickering in some browsers 
	(function(){
	  // if firefox 3.5+, hide content till load (or 3 seconds) to prevent FOUT
	  var d = document, e = d.documentElement, s = d.createElement('style');
	  if (e.style.MozTransform === ''){ // gecko 1.9.1 inference
	    s.textContent = 'body{visibility:hidden}';
	    e.firstChild.appendChild(s);
	    function f(){ s.parentNode && s.parentNode.removeChild(s); }
	    addEventListener('load',f,false);
	    setTimeout(f,3000); 
	  }
	})();

	//loading animation disable if not want it.
	//loadingAnimation();
	
  	// Disable certain links
    $('a[href^=#]').click(function (e) {
      e.preventDefault()
    })

    $('.search-btn').addClass('nostyle');//tell uniform to not style this element


	//------------- Navigation -------------//

	mainNav = $('.mainnav>ul>li');
	mainNav.find('ul').siblings().addClass('hasUl').append('<span class="hasDrop icon16 icomoon-icon-arrow-down"></span>');
	mainNavLink = mainNav.find('a').not('.sub a');
	mainNavLinkAll = mainNav.find('a');
	mainNavSubLink = mainNav.find('.sub a').not('.sub li .sub a');
	mainNavCurrent = mainNav.find('a.current');

	//remove current class if have
	mainNavCurrent.removeClass('current');
	//set the seleceted menu element
	if ($.cookie("newCurrentMenu")) {
		mainNavLinkAll.each(function(index) {
			if($(this).attr('href') == $.cookie("newCurrentMenu")) {
				//set new current class
				$(this).addClass('current');

				ulElem = $(this).closest('ul');
				if(ulElem.hasClass('sub')) {
					//its a part of sub menu need to expand this menu
					aElem = ulElem.prev('a.hasUl').addClass('drop');
					ulElem.addClass('expand');
				} 
				//destroy cookie	
				$.cookie("newCurrentMenu",null);
			}
		});
	}	
	
	//hover magic add blue color to icons when hover - remove or change the class if not you like.
	mainNavLinkAll.hover(
	  function () {
	    $(this).find('span.icon16').addClass('blue');
	  }, 
	  function () {
	    $(this).find('span.icon16').removeClass('blue');
	  }
	);

	//click magic
	mainNavLink.click(function(event) {
		$this = $(this);
		
		if($this.hasClass('hasUl')) {
			event.preventDefault();
			if($this.hasClass('drop')) {
				$(this).siblings('ul.sub').slideUp(500, 'jswing').siblings().removeClass('drop');
			} else {
				$(this).siblings('ul.sub').slideDown(500, 'jswing').siblings().addClass('drop');
			}			
		} else {
			//has no ul so store a cookie for change class.
			$.cookie("newCurrentMenu",$this.attr('href') ,{expires: 1});
		}
	});
	mainNavSubLink.click(function(event) {
		$this = $(this);
		
		if($this.hasClass('hasUl')) {
			event.preventDefault();
			if($this.hasClass('drop')) {
				$(this).siblings('ul.sub').slideUp(500).siblings().removeClass('drop');
			} else {
				$(this).siblings('ul.sub').slideDown(250).siblings().addClass('drop');
			}			
		} else {
			//has no ul so store a cookie for change class.
			$.cookie("newCurrentMenu",$this.attr('href') ,{expires: 1});
		}
	});

	//responsive buttons
	$('.resBtn>a').click(function(event) {
		$this = $(this);
		if($this.hasClass('drop')) {
			$('#sidebar>.shortcuts').slideUp(500);
			$('#sidebar>.sidenav').slideUp(500);
			$this.removeClass('drop');
		} else {
			$('#sidebar>.shortcuts').slideDown(250);
			$('#sidebar>.sidenav').slideDown(250);
			$this.addClass('drop');
		}
	});
	$('.resBtnSearch>a').click(function(event) {
		$this = $(this);
		if($this.hasClass('drop')) {
			$('.search').slideUp(500);
			$this.removeClass('drop');
		} else {
			$('.search').slideDown(250);
			$this.addClass('drop');
		}
	});

	//Hide and show sidebar btn
	$( '.collapseBtn' ).bind( 'click', function(){
		$this = $(this);
		//check if sidebar is show
		if($(this).hasClass('hide')) {
			console.log('Sidebar is hided');
			$('#sidebarbg').show();
			$('#content').css('margin-left', '213'+'px');
			$('#sidebar').css('left', '0').show();
			$this.removeClass('hide');
			$('.collapseBtn').css('top', '118'+'px').css('left', '170'+'px').removeClass('shadow');
			$this.children('a').attr('title','Hide Sidebar')

		} else {
			console.log('Sidebar is show');
			//hide sidbar
			$('#sidebarbg').hide();
			$('#sidebar').hide();
		    $('.collapseBtn').animate({ //use .hide() if you experience heavy animation :)
			    left: '200',
			    top: '20'
			  }, 500, 'easeInExpo', function() {
			    // Animation complete.
			  
			}).addClass('shadow');
			//expand content
			$this.addClass('hide');
			$this.children('a').attr('title','Show Sidebar')
			$('#content').css('margin-left', '0');
			
		}
	});


	//------------- widget box magic -------------//

	var widget = $('div.box');
	var widgetOpen = $('div.box').not('div.box.closed');
	var widgetClose = $('div.box.closed');
	//close all widgets with class "closed"
	widgetClose.find('div.content').hide();
	widgetClose.find('.title>.minimize').removeClass('minimize').addClass('maximize');

	widget.find('.title>a').click(function (event) {
		event.preventDefault();
		var $this = $(this);
		if($this .hasClass('minimize')) {
			//minimize content
			$this.removeClass('minimize').addClass('maximize');
			$this.parent('div').addClass('min');
			cont = $this.parent('div').next('div.content')
			cont.slideUp(500, 'easeOutExpo'); //change effect if you want :)
			
		} else  
		if($this .hasClass('maximize')) {
			//minimize content
			$this.removeClass('maximize').addClass('minimize');
			$this.parent('div').removeClass('min');
			cont = $this.parent('div').next('div.content');
			cont.slideDown(500, 'easeInExpo'); //change effect if you want :)
		} 
		
	})

	//show minimize and maximize icons
	widget.hover(function() {
		    $(this).find('.title>a').show(50);	
		}
		, function(){
			$(this).find('.title>a').hide();	
	});

	//add shadow if hover box
	widget.hover(function() {
		    $(this).addClass('hover');	
		}
		, function(){
			$(this).removeClass('hover');	
	});

	//generate random number for charts
	randNum = function(){
		//return Math.floor(Math.random()*101);
		return (Math.floor( Math.random()* (1+40-20) ) ) + 20;
	}

	var chartColours = ['#88bbc8', '#ed7a53', '#9FC569', '#bbdce3', '#9a3b1b', '#5a8022', '#2c7282'];

	//------------- Prettify code  -------------//
	prettyPrint();

	//------------- placeholder fallback  -------------//
	/*$('input[placeholder], textarea[placeholder]').watermark();*/
	$('input[placeholder], textarea[placeholder]').placeholder();

	//------------- Check all checkboxes  -------------//
	
	$("#masterCh").click(function() {
		var checkedStatus = $(this).find('span').hasClass('checked');
		$("#checkAll tr .chChildren input:checkbox").each(function() {
			this.checked = checkedStatus;
				if (checkedStatus == this.checked) {
					$(this).closest('.checker > span').removeClass('checked');
				}
				if (this.checked) {
					$(this).closest('.checker > span').addClass('checked');
				}
		});
	});

	//------------- Datepicker -------------//
	$("#datepicker").datepicker({
		showOtherMonths:true
	});

	$('#datepicker-inline').datepicker({
	    inline: true,
		showOtherMonths:true
	});

	//------------- Tooltips -------------//

	//top tooltip
	$('.tip').qtip({
		content: false,
		position: {
			my: 'bottom center',
			at: 'top center',
			viewport: $(window)
		},
		style: {
			classes: 'ui-tooltip-tipsy'
		}
	});

	//tooltip in right
	$('.tipR').qtip({
		content: false,
		position: {
			my: 'left center',
			at: 'right center',
			viewport: $(window)
		},
		style: {
			classes: 'ui-tooltip-tipsy'
		}
	});

	//tooltip in bottom
	$('.tipB').qtip({
		content: false,
		position: {
			my: 'top center',
			at: 'bottom center',
			viewport: $(window)
		},
		style: {
			classes: 'ui-tooltip-tipsy'
		}
	});

	//tooltip in left
	$('.tipL').qtip({
		content: false,
		position: {
			my: 'right center',
			at: 'left center',
			viewport: $(window)
		},
		style: {
			classes: 'ui-tooltip-tipsy'
		}
	});

	//--------------- Dual multi select ------------------//
	$.configureBoxes();

	//--------------- button state demo ------------------//
    $('#fat-btn').click(function () {
        var btn = $(this)
        btn.button('loading')
        setTimeout(function () {
          btn.button('reset')
        }, 3000);
     })

    //--------------- Tabs ------------------//
    $('#myTab a').click(function (e) {
	  	e.preventDefault();
	  	$(this).tab('show');
	})

    //make 2 tab active ( remove if not want )
	$('.tabs-right li:eq(1) a').tab('show'); // Select third tab (0-indexed)
	$('.tabs-left li:eq(1) a').tab('show'); // Select third tab (0-indexed)

	$('#loadersTab a').click(function (e) {
	  e.preventDefault();
	  $(this).tab('show');
	})

	//--------------- Accordion ------------------//
    var acc = $('.accordion'); //get all accordions
    var accHeading = acc.find('.accordion-heading');
	var accBody = acc.find('.accordion-body');

	//function to put icons
	accPutIcon = function () {
		acc.each(function(index) {
		   accExp = $(this).find('.accordion-body.in');
		   accExp.prev().find('a.accordion-toggle').append($('<span class="icon12 entypo-icon-minus-2 gray"></span>'));

		   accNor = $(this).find('.accordion-body').not('.accordion-body.in');
		   accNor.prev().find('a.accordion-toggle').append($('<span class="icon12 entypo-icon-plus-2 gray"></span>'));


		});
	}

	//function to update icons
	accUpdIcon = function() {
		acc.each(function(index) {
		   accExp = $(this).find('.accordion-body.in');
		   accExp.prev().find('span').remove();
		   accExp.prev().find('a.accordion-toggle').append($('<span class="icon12 entypo-icon-minus-2 gray"></span>'));

		   accNor = $(this).find('.accordion-body').not('.accordion-body.in');
		   accNor.prev().find('span').remove();
		   accNor.prev().find('a.accordion-toggle').append($('<span class="icon12 entypo-icon-plus-2 gray"></span>'));


		});
	}

	accPutIcon();

	$('.accordion').on('shown', function () {
		accUpdIcon();
	}).on('hidden', function () {
		accUpdIcon();
	})


	//--------------- Sliders ------------------//
	//simple slider
	$( "#slider" ).slider(); 
	//with 50 range
	$( "#slider1" ).slider({
		range: "min",
		value:100,
		min: 1,
		max: 500,
		step: 50,
		slide: function( event, ui ) {
			$( "#amount" ).val( "$" + ui.value );
		}
	});
	$( "#amount" ).val( "$" + $( "#slider" ).slider( "value" ) );
	//range slider
	$( "#slider-range" ).slider({
		range: true,
		min: 0,
		max: 500,
		values: [ 75, 300 ],
		slide: function( event, ui ) {
			$( "#amount1" ).val( "Price range: $" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
		}
	});
	$( "#amount1" ).val( "Price range: $" + $( "#slider-range" ).slider( "values", 0 ) +
		" - $" + $( "#slider-range" ).slider( "values", 1 ) );

	//with minimum
	$( "#slider-range-min" ).slider({
		range: "min",
		value: 37,
		min: 1,
		max: 700,
		slide: function( event, ui ) {
			$( "#amount2" ).val( "Maximum price: $" + ui.value );
		}
	});
	$( "#amount2" ).val( "Maximum price: $" + $( "#slider-range-min" ).slider( "value" ) );
	//with maximum
	$( "#slider-range-max" ).slider({
		range: "max",
		min: 1,
		max: 10,
		value: 2,
		slide: function( event, ui ) {
			$( "#amount3" ).val("Minimum number of bedrooms:" + ui.value );
		}
	});
	$( "#amount3" ).val( "Minimum number of bedrooms:" + $( "#slider-range-max" ).slider( "value" ) );

	//vertical sliders
	$( "#eq > span" ).each(function() {
		// read initial values from markup and remove that
		var value = parseInt( $( this ).text(), 10 );
		$( this ).empty().slider({
			value: value,
			range: "min",
			animate: true,
			orientation: "vertical"
		});
	});

	//--------------- Progress bars ------------------//
	$( "#progressbar" ).progressbar({
		value: 37
	});

	//--------------- Dialogs ------------------//
	$('#openDialog').click(function(){
		$('#dialog').dialog('open');
		return false;
	});

	$('#openModalDialog').click(function(){
		$('#modal').dialog('open');
		return false;
	});

	// JQuery Dialog			
	$('#dialog').dialog({
		autoOpen: false,
		dialogClass: 'dialog',
		buttons: {
			"Close": function() { 
				$(this).dialog("close"); 
			}
		}
	});

	// JQuery UI Modal Dialog			
	$('#modal').dialog({
		autoOpen: false,
		modal: true,
		dialogClass: 'dialog',
		buttons: {
			"Close": function() { 
				$(this).dialog("close"); 
			}
		}
	});

	$("div.dialog button").addClass("btn");

	//Boostrap modal
	$('#myModal').modal({ show: false});
	//add event to modal after closed
	$('#myModal').on('hidden', function () {
	  	$.pnotify({
		    title: 'Modal',
		    text: 'Modal window is closed',
		    icon: 'picon icon16 entypo-icon-warning white',
		    opacity: 0.95,
		    sticker: false,
		    history: false
		});
	})

	//--------------- Popovers ------------------//
	$("a[rel=popover]")
      .popover()
      .click(function(e) {
        e.preventDefault()
     })

    //--------------- Typeahead ------------------//
	$('.typeahead').typeahead({
		source: ['jonh','carlos','arcos','stoner']
	})

	$('.findUser').typeahead({
		source: ['Sammy','Jonny','Sugge Elson','Elenna','Rayan','Dimitrios','Sidarh','Jana','Daniel','Morerira','Stoichkov']
	})

	//--------------- carousel ------------------//
	$('.carousel').carousel({
	  interval: 5000
	})

	//--------------- Pines notify  ------------------//

    //regular notice
    $('#noticeR').click(function(){
		$.pnotify({
		    title: 'Regular Notice',
		    text: 'Check me out! I\'m a notice.',
		    icon: 'picon icon16 entypo-icon-warning white',
		    opacity: 0.95,
		    sticker: false,
		    history: false
		});
	});

	//Sticky notice
    $('#noticeS').click(function(){
		$.pnotify({
		    title: 'Sticky Notice',
		    text: 'Check me out! I\'m a sticky notice. You\'ll have to close me yourself.',
		    hide: false,
		    icon: 'picon icon16 entypo-icon-warning white',
		    opacity: 0.95,
		    history: false,
		    sticker: false
		});
	});

	//Regular info
    $('#infoR').click(function(){
		$.pnotify({
			type: 'info',
		    title: 'New Thing',
    		text: 'Just to let you know, something happened.',
		    icon: 'picon icon16 brocco-icon-info white',
		    opacity: 0.95,
		    history: false,
		    sticker: false
		});
	});

	//Sticky info
    $('#infoS').click(function(){
		$.pnotify({
			type: 'info',
		    title: 'Sticky Info',
   			text: 'Sticky info, you know, like a newspaper covered in honey.',
		    icon: 'picon icon16 brocco-icon-info white',
		    hide: false,
		    opacity: 0.95,
		    history: false,
		    sticker: false
		});
	});

	//Regular success
    $('#successR').click(function(){
		$.pnotify({
			type: 'success',
		    title: 'Regular Success',
    		text: 'That thing that you were trying to do worked!',
		    icon: 'picon icon16 iconic-icon-check-alt white',
		    opacity: 0.95,
		    history: false,
		    sticker: false
		});
	});

	//Sticky success
    $('#successS').click(function(){
		$.pnotify({
			type: 'success',
		    title: 'Sticky Success',
    		text: 'Sticky success... I\'m not even gonna make a joke.',
		    icon: 'picon icon16 iconic-icon-check-alt white',
		    opacity: 0.95,
		    hide:false,
		    history: false,
		    sticker: false
		});
	});

	//Regular success
    $('#errorR').click(function(){
		$.pnotify({
			type: 'error',
		    title: 'Oh No!',
    		text: 'Something terrible happened.',
		    icon: 'picon icon24 typ-icon-cancel white',
		    opacity: 0.95,
		    history: false,
		    sticker: false
		});
	});

	//Sticky success
    $('#errorS').click(function(){
		$.pnotify({
			type: 'error',
		    title: 'Oh No!',
    		text: 'Something terrible happened.',
		    icon: 'picon icon24 typ-icon-cancel white',
		    opacity: 0.95,
		    hide:false,
		    history: false,
		    sticker: false
		});
	});


	//------------- Uniform  -------------//
	//add class .nostyle if not want uniform to style field
	$("input, textarea, select").not('.nostyle').uniform();

	//remove loadstate class from body and show the page
	setTimeout('$("html").removeClass("loadstate")',500);

});