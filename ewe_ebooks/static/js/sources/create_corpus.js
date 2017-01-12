$(document).ready(function(){
    $('#variety').on('change', function() {
      if ( this.value === 'TW')
      {
        $("#twitter_items").show();
        $("#excerpt_items").hide();
      }
      else
      {
        $("#excerpt_items").show();
        $("#twitter_items").hide();
      }
    });
});