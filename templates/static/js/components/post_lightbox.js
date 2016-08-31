"use strict";
$(document).ready(function(){
	/*AJAX for POSTVIEW*/
	function get_post_info(my_id) {
		if(my_id > 0){
			$.ajax({
				url : "detail_post/", // the endpoint
				type : "POST", // http method
				data : { image_id : my_id }, // data sent with the post request
				// handle a successful response
				success : function(json) {
					$('#detail_image_title').html(""+json.image_title);
					$('#detail_image_author').html(""+json.image_author);
					$('#lightbox_img_detail').fadeOut(0, function(){
						$('#lightbox_img_detail').attr('src',""+json.image_filename);
					}).fadeIn(300);
					$('#lightbox_img_postview').fadeOut(0, function(){
						$('#lightbox_img_postview').attr('src',""+json.image_filename);
					}).fadeIn(300);
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