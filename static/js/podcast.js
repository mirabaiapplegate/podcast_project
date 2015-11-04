"use strict";

// Wait until page has loaded
$(document).ready(function() {

  // Initialize Amplitude Audio Player
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
      jQuery Visual Helpers for Audio Player
    */
    $('#small-player').hover(function(){
      $('#small-player-middle-controls').show();
      $('#small-player-middle-meta').hide();
    }, function(){
      $('#small-player-middle-controls').hide();
      $('#small-player-middle-meta').show();

    });

});
