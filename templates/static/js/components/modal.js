"use strict";
$(document).ready(function(){
     console.log('cookie: '+$.cookie('pop'));
     if ($.cookie('pop') != 'checked') {
      $('#welcomeModal').modal('show');
      $.cookie('pop', 'checked', { expires: 7 });
    }
});