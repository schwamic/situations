"use strict";
$(document).ready(function(){
     if ($.cookie('pop') != 'checked') {
      $('#welcomeModal').modal('show');
    }

    $('.modal_btn').click(function(){
        $.cookie('pop', 'checked', { expires: 7 });
    });
});