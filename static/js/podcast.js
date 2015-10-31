"use strict";

// Wait until page has loaded
$(document).ready(function() {
    var carousel_images = ['https://s3-us-west-2.amazonaws.com/hbpodcastproject/planet_money_659/planet_money_659.jpg', 'https://s3-us-west-2.amazonaws.com/hbpodcastproject/planet_money_659/MessyAdvancedHoneybadger.gif', 'https://s3-us-west-2.amazonaws.com/hbpodcastproject/planet_money_659/money-printing-press.jpg', 'https://s3-us-west-2.amazonaws.com/hbpodcastproject/planet_money_659/money_shredder.jpg'];
 
      for(var i=0 ; i< carousel_images.length ; i++) {
        $('<div class="item"><img src="'+carousel_images[i]+'"><div class="carousel-caption"></div></div>').appendTo('.carousel-inner');
        
        $('<li data-target="#carousel-example-generic" data-slide-to="'+i+'"></li>').appendTo('.carousel-indicators')

      }
      $('.item').first().addClass('active');
      $('.carousel-indicators > li').first().addClass('active');
      $('#carousel-example-generic').carousel();


});
