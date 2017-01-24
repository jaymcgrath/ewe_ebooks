// popover for mashup preview thumbs
$(function () {
  $('[data-toggle="popover"]').popover(
      {
          'trigger':'hover',
          'template':'<div class="popover" role="tooltip"><div class="popover-arrow"></div>' +
          '<h3 class="popover-title"></h3><div class="popover-content thumb-wrapper"></div></div>',
          'html':true
      })
})


/* behavior when each mashup is clicked */
$('.mashup-card').click(
    function() {

        // add and remove the active class to highlight this card
        $(this).toggleClass('active');

        if ($(this).children('input').prop('checked')){
             // it's checked, change to unchecked
            $(this).children('input').prop('checked', false);
        }
        else{
            $(this).children('input').prop('checked', true);
        }

        });