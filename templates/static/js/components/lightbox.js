"use strict";
$(document).ready(function(){
	var COUNT_OF_ALL_IMAGES = -1;
	var COUNT_OF_ALL_POSTS = -1;
	var IMAGE_ID = -1;
	var POST_ID = -1;
	var img_width;

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
		$("body").css("overflow", "hidden");
		IMAGE_ID = (""+$(this).attr("id")).split("_")[1];
		$("#detail_image").attr("value",IMAGE_ID);
		$('#lightbox_img_detail').fadeOut(0,function(){
			$(".lightbox_detailview").hide(0).fadeIn(300);
			get_image_info(IMAGE_ID);
		});

	});

	/*Posts*/
	$('.lightbox_post').click(function(event){
		$("body").css("overflow", "hidden");
		POST_ID = (""+$(this).attr("id")).split("_")[1];
		$('#lightbox_img_pubview').fadeOut(0, function(){
			$(".lightbox_detailview").hide(0).fadeIn(300);
			get_post_info(POST_ID);
		});
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
			$('#lightbox_img_detail').fadeOut(0,function(){
				get_image_info(IMAGE_ID);
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
			$('#lightbox_img_detail').fadeOut(0,function(){
				get_image_info(IMAGE_ID);
		});
		}
	});
	/*Posts*/
	$('#post_show_next').click(function(event){
		if(POST_ID > 0){
			POST_ID = parseInt(POST_ID)+1;
				if(POST_ID > COUNT_OF_ALL_POSTS){
					POST_ID = 1;
			}
			$('#lightbox_img_pubview').fadeOut(0,function(){
				get_post_info(POST_ID);
			});
		}
	});

	$('#post_show_pref').click(function(event){
		if(POST_ID > 0){
			POST_ID = parseInt(POST_ID)-1;
			if(POST_ID <= 0){
				POST_ID = COUNT_OF_ALL_POSTS;
			}
			$('#lightbox_img_pubview').fadeOut(0,function(){
				get_post_info(POST_ID);
			});
		}
	});



	/*PUBLISHVIEW*/
	$('.btn_publishview').click(function(event){
		getLocation();
		//$('.lightbox_publishview').fadeIn(300);
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
		$("body").css("overflow", "");
		if(state){
				$(".lightbox_detailview").fadeOut(0);
				$('.backdrop_pubview').fadeOut(400);
		}else{
				$(".lightbox_detailview").fadeOut(400);
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
					$('#lightbox_img_detail').fadeOut(0, function(){
						$('#lightbox_img_detail').attr('src',""+json.image_filename);
					}).fadeIn(400);
					$('#lightbox_img_pubview').fadeOut(0, function(){
						$('#lightbox_img_pubview').attr('src',""+json.image_filename);
					}).fadeIn(400);
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
		console.log('get_post_info called');
		if(my_id > 0){
			console.log(my_id);
			$.ajax({
				url : "detail_post/", // the endpoint
				type : "POST", // http method
				data : { post_id : my_id }, // data sent with the post request
				// handle a successful response
				success : function(json) {
					console.log(json);
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
					$('#lightbox_img_pubview').fadeOut(0, function(){
						$('#lightbox_img_pubview').attr('src',""+json.image_filename);
					}).fadeIn(400);
					COUNT_OF_ALL_POSTS = json.post_count;
				},
				// handle a non-successful response
				error : function(xhr,errmsg,err) {
					console.log(xhr.status + ": " + xhr.responseText);
				}
			});
		}
	}

	if (initial_lightbox_post != -1) {
		console.log('initial lighbox called');
		$('#lightbox_img_pubview').fadeOut(0, function () {
			$(".lightbox_detailview").hide(0).fadeIn(300);
			POST_ID = initial_lightbox_post;
			get_post_info(POST_ID);
		});
	}
});