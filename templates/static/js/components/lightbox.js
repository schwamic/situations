$(document).ready(function(){
/*DETAILVIEW*/

	$('.lightbox_detail').click(function(event){
		$('.backdrop_detail, .box_detail').animate({'opacity':'1.00'}, 300, 'linear');
		$('.box_detail').animate({'opacity':'1.00'}, 300, 'linear');
		$('.backdrop_detail, .box_detail').css('display', 'block');
		thumb_id = (""+$(this).attr("id")).split("_")[1];
		url = $("#img"+thumb_id).attr("src")
		$("#lightbox_img_id_detail").attr("src",url);
		$(".btn_publishview").attr("id", "btn_"+thumb_id);
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
	});

/*CLOSE*/
	$('.close_all').click(function(){
		close_box(true);
	});

	$('.close_detail').click(function(){
		close_box();
	});

});

/*FUNCTIONS*/
function close_box(state)
{
	if(state){
		$('.backdrop_detail, .box_detail').animate({'opacity':'0'}, 0, 'linear', function(){
			$('.backdrop_detail, .box_detail').css('display', 'none');
		});
		$('.backdrop_pubview, .box_pubview').animate({'opacity':'0'}, 300, 'linear', function(){
			$('.backdrop_pubview, .box_pubview').css('display', 'none');
		});
	}else{
		$('.backdrop_detail, .box_detail').animate({'opacity':'0'}, 300, 'linear', function(){
			$('.backdrop_detail, .box_detail').css('display', 'none');
		});
	}
}