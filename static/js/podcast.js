"use strict";

// Wait until page has loaded
$(document).ready(function() {

    /*
      jQuery Visual Helpers for Audio Player
    */
    $('#small-player').hover(function(){
      $('#small-player-middle-controls').show();
      // $('#small-player-middle-meta').hide();
    }, function(){
      $('#small-player-middle-controls').hide();
      // $('#small-player-middle-meta').show();

    });

});
