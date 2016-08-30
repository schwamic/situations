"use strict";
$(document).ready(function(){
	var COUNT_OF_ALL_IMAGES = -1;
	var IMAGE_ID = -1;
	var img_width;

	/*DETAILVIEW*/
	$('.lightbox_detail').click(function(event){
		$("body").css("overflow", "hidden");
		$(".lightbox_detailview").fadeIn(300);
		$('.backdrop_detail').fadeIn(300);
		$('.box_detail').fadeIn(300);
		IMAGE_ID = (""+$(this).attr("id")).split("_")[1];
		$("#detail_image").attr("value",IMAGE_ID);
		get_image_info(IMAGE_ID);
	});

	/*SLIDER*/
	$('#show_next').click(function(event){
		if(IMAGE_ID > 0){
			IMAGE_ID = parseInt(IMAGE_ID)+1;
				if(IMAGE_ID > COUNT_OF_ALL_IMAGES){
					IMAGE_ID = 1;
			}
			$("#detail_image").attr("value",IMAGE_ID);
			get_image_info(IMAGE_ID, function(){
				//fade_img_detail();
			});
		}
	});

		$('#show_pref').click(function(event){
		if(IMAGE_ID > 0){
			IMAGE_ID = parseInt(IMAGE_ID)-1;
			if(IMAGE_ID <= 0){
				IMAGE_ID = COUNT_OF_ALL_IMAGES;
			}
			$("#detail_image").attr("value",IMAGE_ID);
			get_image_info(IMAGE_ID, function(){
				fade_img_detail();
			});

		}
	});

	/*PUBLISHVIEW*/
	$('.btn_publishview').click(function(event){
		$('.backdrop_pubview, .box_pubview').fadeIn(300);
		img_width = $('#lightbox_img_pubview').width();
		$('#publish_caption').css('width',img_width);
	});

	/*CLOSE*/
	$('.close_all').click(function(){
		close_box(true);
	});

	$('.close_detail').click(function(){
		close_box();
	});

	/*FUNCTIONS*/
	function close_box(state)
	{
		$("body").css("overflow", "");
		if(state){
				$('.backdrop_detail').fadeOut(300);
				$('.box_detail').fadeOut(300);
				$(".lightbox_detailview").fadeOut(300);
				$('.backdrop_pubview').fadeOut(300);
				$('.box_pubview').fadeOut(300);
		}else{
				$('.backdrop_detail').fadeOut(300);
				$('.box_detail').fadeOut(300);
				$(".lightbox_detailview").fadeOut(300);
		}
	}

	function fade_img_detail(){
	    $('.box_detail').imagesLoaded( function() {
    	$('img').fadeIn(1000);
    	});
	}

	/*AJAX for detail*/
	function get_image_info(my_id) {
		if(my_id > 0){
			$.ajax({
				url : "detail_image/", // the endpoint
				type : "POST", // http method
				data : { image_id : my_id }, // data sent with the post request
				// handle a successful response
				success : function(json) {
					$('#detail_image_title').html(""+json.image_title);
					$('#detail_image_author').html(""+json.image_author);
					$('#lightbox_img_detail').attr('src',""+json.image_filename);
					$('#publish_image_title').html(""+json.image_title);
					$('#publish_image_author').html(""+json.image_author);
					$('#lightbox_img_pubview').attr('src',""+json.image_filename);
					COUNT_OF_ALL_IMAGES = json.image_count;
				},
				// handle a non-successful response
				error : function(xhr,errmsg,err) {
					console.log(xhr.status + ": " + xhr.responseText);
				}
			});
		}
	};

	/*AJAX_Setup for django csrf*/
		function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});
});

/*RESIZE*/
$(window).resize(function(){
	var img_width;
    img_width = $('#lightbox_img_pubview').width();
	$('#publish_caption').css('width',img_width);

	//col_height = $('.box_detail').height();
	//$('.col_wrap').css('height', col_height);
});