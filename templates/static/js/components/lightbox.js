"use strict";
$(document).ready(function(){
	var COUNT_OF_ALL_IMAGES = -1;
	var COUNT_OF_ALL_POSTS = -1;
	var IMAGE_ID = -1;
	var POST_ID = -1;
	var img_width;
	var csrftoken = $.cookie('csrftoken');
	var initial_lightbox_post;

	/*
	console.log('cookie: '+$.cookie('c'));
	console.log(csrftoken);
	*/

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

	/*DETAILVIEW*/
	/*Images*/
	$('.lightbox_detail').click(function(event){
		IMAGE_ID = (""+$(this).attr("id")).split("_")[1];
		$("#detail_image").attr("value",IMAGE_ID);
		$("#lightbox_img_detail").css("opacity", "0");
		$(".lightbox_detailview").hide(0).fadeIn(300,function(){
			$("body").css({'overflow':'hidden'});
		});
		get_image_info(IMAGE_ID);

	});

	/*Posts*/
	$('.lightbox_post').click(function(event){
		POST_ID = (""+$(this).attr("id")).split("_")[1];
		$('#lightbox_img_pubview').css("opacity", "0");
		$(".lightbox_detailview").hide(0).fadeIn(300,function(){
			$("body").css({'overflow':'hidden'});
		});
		get_post_info(POST_ID);
	});

	/*SLIDER*/
	/*Images*/
	$('#show_next').click(function(event){
		if(IMAGE_ID > 0){
			IMAGE_ID = parseInt(IMAGE_ID)+1;
				if(IMAGE_ID > COUNT_OF_ALL_IMAGES){
					IMAGE_ID = 1;
			}
			$("#detail_image").attr("value",IMAGE_ID);
			$("#lightbox_img_detail").css("opacity", "0");
			get_image_info(IMAGE_ID);
		}
	});

	$('#show_pref').click(function(event){
		if(IMAGE_ID > 0){
			IMAGE_ID = parseInt(IMAGE_ID)-1;
			if(IMAGE_ID <= 0){
				IMAGE_ID = COUNT_OF_ALL_IMAGES;
			}
			$("#detail_image").attr("value",IMAGE_ID);
			$("#lightbox_img_detail").css("opacity", "0");
			get_image_info(IMAGE_ID);
		}
	});
	/*Posts*/
	$('#post_show_next').click(function(event){
		if(POST_ID > 0){
			POST_ID = parseInt(POST_ID)+1;
				if(POST_ID > COUNT_OF_ALL_POSTS){
					POST_ID = 1;
			}
			$('#lightbox_img_pubview').css("opacity", "0");
			get_post_info(POST_ID);
		}
	});

	$('#post_show_pref').click(function(event){
		if(POST_ID > 0){
			POST_ID = parseInt(POST_ID)-1;
			if(POST_ID <= 0){
				POST_ID = COUNT_OF_ALL_POSTS;
			}
			$('#lightbox_img_pubview').css("opacity", "0");
			get_post_info(POST_ID);
		}
	});



	/*PUBLISHVIEW*/
	$('.btn_publishview').click(function(event){
		getLocation();
		$('#lightbox_img_pubview').css("opacity", "1");
		$('.backdrop_pubview').fadeIn(300);
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
		$("body").css({'overflow': ""});
		if(state){
				$(".lightbox_detailview").fadeOut(0,function(){
					$("#lightbox_img_detail").css("opacity", "0");
					$('#lightbox_img_pubview').css("opacity", "0");
				});
				$('.backdrop_pubview').fadeOut(400);
		}else{
				$(".lightbox_detailview").fadeOut(400, function(){
					$("#lightbox_img_detail").css("opacity", "0");
					$('#lightbox_img_pubview').css("opacity", "0");
				});
		}
	}

	/*AJAX for DETAILVIEW*/
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
					$("#lightbox_img_detail").css("display", "none").attr("src", ""+json.image_filename).one("load",function(){
					//fires (only once) when loaded
							$(this).css("opacity", "1");
							$(this).fadeIn("slow");
						 }).each(function(){
							if(this.complete) //trigger load if cached in certain browsers
							  $(this).trigger("load");
						 });
					$('#lightbox_img_pubview').attr('src',""+json.image_filename);
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
	}

	/*AJAX for POSTVIEW*/
	function get_post_info(my_id) {
		if(my_id > 0){
			$.ajax({
				url : "detail_post/", // the endpoint
				type : "POST", // http method
				data : { post_id : my_id }, // data sent with the post request
				// handle a successful response
				success : function(json) {
					$('.list_id').html(""+json.publisher_id);
					$('.list_date').html(""+json.post_publishing_date);
					$('.list_gender').html(""+json.publisher_gender);
					$('.list_occupation').html(""+json.publisher_occupation);
					$('.list_age').html(""+json.publisher_age);
					$('.list_location').html(""+json.publisher_location);
					$('.list_activity').html(""+json.publisher_active_time);
					$('.list_description').html(""+json.post_description);
					$('.list_reason').html(""+json.post_reason);

					$('#publish_image_title').html(""+json.image_title);
					$('#publish_image_author').html(""+json.image_author);
					$("#lightbox_img_pubview").css("display", "none").attr("src", ""+json.image_filename).one("load",function(){
					//fires (only once) when loaded
							$(this).css({"opacity": "1"})
							$(this).fadeIn("slow");
						 }).each(function(){
							if(this.complete) //trigger load if cached in certain browsers
							  $(this).trigger("load");
						 });
					COUNT_OF_ALL_POSTS = json.post_count;
				},
				// handle a non-successful response
				error : function(xhr,errmsg,err) {
					console.log(xhr.status + ": " + xhr.responseText);
				}
			});
		}
	}

	// wo findet die uebergabe statt
	if($('#social_id').attr('value') != ""){
		initial_lightbox_post = $('#social_id').attr('value');
		if (initial_lightbox_post != -1 && initial_lightbox_post > -1) {
			POST_ID = initial_lightbox_post;
			$(".lightbox_detailview").hide(0).fadeIn(0,function(){
				$("body").css({'overflow':'hidden'});
			});
			get_post_info(POST_ID);
		}
	}
});