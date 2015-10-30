"use strict";

// Wait until page has loaded
$(document).ready(function() {

    // Initialize a variable for time
    var t;

    // Initialize a variable for the start of the carousel
    var start = $('#podcast-carousel').find('.active').attr('data-interval');

    // Settimeout on carousel
    t = setTimeout("$('#podcast-carousel').carousel({interval:1000});", start-1000);

    $('#podcast-carousel').on('slid.bs.carousel', function () {   
         clearTimeout(t);  

         var duration = $(this).find('.active').attr('data-interval');

         $('#podcast-carousel').carousel('pause');

         t = setTimeout("$('#podcast-carousel').carousel();", duration-1000);
    })

    $('.carousel-control.right').on('click', function(){
        clearTimeout(t);   
    });

    $('.carousel-control.left').on('click', function(){
        clearTimeout(t);   
    });

});
