"use strict";

// Wait until page has loaded
$(document).ready(function() {
  Amplitude.init({
    "songs": [
        {
            "name": "Planet Money",
            "artist": "planet_money_659",
            "url": "https://s3-us-west-2.amazonaws.com/hbpodcastproject/planet_money_659/659.mp3",
            "live": false,
            "cover_art_url": "https://s3-us-west-2.amazonaws.com/hbpodcastproject/planet_money_659/planet_money_659.jpg"
        }
    ],
    "default_album_art": "images/no-cover.png"
});

    /*
      jQuery Visual Helpers
    */
    $('#small-player').hover(function(){
      $('#small-player-middle-controls').show();
      $('#small-player-middle-meta').hide();
    }, function(){
      $('#small-player-middle-controls').hide();
      $('#small-player-middle-meta').show();

    });


    var carousel_images = ['https://s3-us-west-2.amazonaws.com/hbpodcastproject/planet_money_659/planet_money_659.jpg', 'https://s3-us-west-2.amazonaws.com/hbpodcastproject/planet_money_659/MessyAdvancedHoneybadger.gif', 'https://s3-us-west-2.amazonaws.com/hbpodcastproject/planet_money_659/money-printing-press.jpg', 'https://s3-us-west-2.amazonaws.com/hbpodcastproject/planet_money_659/money_shredder.jpg'];
 
      for(var i=0 ; i< carousel_images.length ; i++) {
        $('<div class="item"><img src="'+carousel_images[i]+'" class="img-responsive center-block"><div class="carousel-caption"></div></div>').appendTo('.carousel-inner');
        
        $('<li data-target="#carousel-image" data-slide-to="'+i+'"></li>').appendTo('.carousel-indicators')

      }
      $('.item').first().addClass('active');
      $('.carousel-indicators > li').first().addClass('active');
      $('#carousel-image').carousel();


});
