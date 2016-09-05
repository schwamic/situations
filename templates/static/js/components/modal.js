"use strict";
$(document).ready(function(){

     console.log('cookie: '+$.cookie('pop'));
     if ($.cookie('pop') != 'checked') {
      $('#welcomeModal').modal('show');
    }

    $('.modal_btn').click(function(){
        $.cookie('pop', 'checked', { expires: 7 });
    });
});