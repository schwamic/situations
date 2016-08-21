$('.thumbnail').hover(function(){
    $(this).find('.caption').css('opacity','1');
}, function(){
    $(this).find('.caption').css('opacity','0');
});