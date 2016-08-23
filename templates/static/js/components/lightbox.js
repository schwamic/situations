$(document).ready(function(){

	$('.lightbox').click(function(event){
		$('.backdrop, .box').animate({'opacity':'1.00'}, 300, 'linear');
		$('.box').animate({'opacity':'1.00'}, 300, 'linear');
		$('.backdrop, .box').css('display', 'block');
		thumb_id = (""+$(this).attr("id")).split("_")[1];
		url = $("#img"+thumb_id).attr("src")
		$("#lightbox_img_id").attr("src",url);

		/*LOG*/
		console.log("id: "+thumb_id);
		console.log("url: "+url);
		console.log($("#lightbox_img_id").attr("src"));
	});

	$('.close').click(function(){
		close_box();
	});
});

function close_box()
{
	$('.backdrop, .box').animate({'opacity':'0'}, 300, 'linear', function(){
		$('.backdrop, .box').css('display', 'none');
	});
}
