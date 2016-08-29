"use strict";
$(document).ready(function() {
    $('#content').imagesLoaded( function() {
    console.log('#container background image loaded');
    $('img').fadeIn(1000);
    });

    $('.thumbnail').hover(function(){
        $(this).find('.caption').css('opacity','1');
        }, function(){
            $(this).find('.caption').css('opacity','0');
    });
});

