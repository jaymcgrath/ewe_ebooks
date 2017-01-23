$(document).ready(function(){
    $('.radio-label').click(function() {
        if ( $(this).children("input").val() === 'TW')
        {
            $("#twitter_items").show();
            $("#excerpt_items").hide();
            $("#hashtag_items").hide();
        }
        else  if ( $(this).children("input").val() === 'EX')
        {
            $("#excerpt_items").show();
            $("#twitter_items").hide();
            $("#hashtag_items").hide();
        }
        else  if ( $(this).children("input").val() === 'HS')
        {
            $("#hashtag_items").show();
            $("#excerpt_items").hide();
            $("#twitter_items").hide();

        }
    });
});