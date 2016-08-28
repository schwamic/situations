$(document).ready(function(){

console.log(window.location.href );

/*DETAILVIEW*/
	$('.lightbox_detail').click(function(event){
		$("body").css("overflow", "hidden");
		$(".lightbox_detailview").css("display", "block")
		$('.backdrop_detail, .box_detail').animate({'opacity':'1.00'}, 300, 'linear');
		$('.box_detail').animate({'opacity':'1.00'}, 300, 'linear');
		$('.backdrop_detail, .box_detail').css('display', 'block');
		thumb_id = (""+$(this).attr("id")).split("_")[1];
		url = $("#img"+thumb_id).attr("src")
		$("#lightbox_img_id_detail").attr("src",url);
		$(".btn_publishview").attr("id", "btn_"+thumb_id);
		detail_image(thumb_id);
	});

/*PUBLISHVIEW*/
	$('.btn_publishview').click(function(event){
		$('.backdrop_pubview, .box_pubview').animate({'opacity':'1.00'}, 300, 'linear');
		$('.box_pubview').animate({'opacity':'1.00'}, 300, 'linear');
		$('.backdrop_pubview, .box_pubview').css('display', 'block');
		//close_box();
		thumb_id = (""+$(this).attr("id")).split("_")[1];
		url = $("#img"+thumb_id).attr("src")
		$("#lightbox_img_id_pubview").attr("src",url);
		$("#lightbox_img_id_pubview").attr("value",thumb_id);
		$("#detail_image").attr("value",thumb_id);
		img_width = $('#lightbox_img_id_pubview').width();
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
			$('.backdrop_detail, .box_detail').animate({'opacity':'0'}, 0, 'linear', function(){
				$('.backdrop_detail, .box_detail').css('display', 'none');
				$(".lightbox_detailview").css("display", "none")
			});
			$('.backdrop_pubview, .box_pubview').animate({'opacity':'0'}, 300, 'linear', function(){
				$('.backdrop_pubview, .box_pubview').css('display', 'none');
			});
		}else{
			$('.backdrop_detail, .box_detail').animate({'opacity':'0'}, 300, 'linear', function(){
				$('.backdrop_detail, .box_detail').css('display', 'none');
				$(".lightbox_detailview").css("display", "none")
			});
		}
	}

/*AJAX for posting*/
	function detail_image(thumb_id) {
		$.ajax({
			url : "detail_image/", // the endpoint
			type : "POST", // http method
			data : { image_id : thumb_id }, // data sent with the post request
			// handle a successful response
			success : function(json) {
				$('#detail_image_title').html(""+json.image_title);
				$('#detail_image_author').html(""+json.image_author);
				$('#publish_image_title').html(""+json.image_title);
				$('#publish_image_author').html(""+json.image_author);
			},
			// handle a non-successful response
			error : function(xhr,errmsg,err) {
				console.log(xhr.status + ": " + xhr.responseText);
			}
		});
	};

/*AJAX_Setuo for django csrf*/
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

$(window).resize(function(){
    img_width = $('#lightbox_img_id_pubview').width();
	$('#publish_caption').css('width',img_width);
});