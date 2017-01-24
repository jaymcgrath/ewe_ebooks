/**
 * Extra javascript for popovers
 *
 **/

// called on hover for mashup popovers
$(function () {
  $('[data-toggle="popover"]').popover(
      {
          'trigger':'hover',
          'template':'<div class="popover" role="tooltip"><div class="popover-arrow"></div>' +
          '<h3 class="popover-title"></h3><div class="popover-content thumb-wrapper"></div></div>',
          'html':true


      })
})

