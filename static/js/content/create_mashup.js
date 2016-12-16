"use strict";

$('#id_title').prop('classs', 'form-control');
$('#id_title').prop('placeholder', 'Together at Last! <mashup title goes here>');


$('.corpus-card').click(
    function(){
    /* behavior when each corpus is clicked */

        // get the id of the one they clicked
        var $corpus_id = $(this).data('corpus_id');

        // add and remove the active class to highlight this card
        $(this).toggleClass('active');

        // Check and uncheck hidden checkboxes and hide/unhide thumb from preview
        if ($(this).children('input').prop('checked'))
        {
            // it's checked, change to unchecked
            $(this).children('input').prop('checked', false);

            // remove the image from the preview box
            $('span[data-corpus_id="' + $corpus_id + '"]' ).remove();

            // Remove the any plus signs from in front of the thumbnail that is now first

            var $firstspan = $('#corpus_preview').children('span:first');
            // if ($firstspan.length > 0) {
                    // will remove the <i> tag from the first one if there is one
                    $firstspan.children('i:first.fa-plus').remove();
            //        }

        } else {
            // not checked, so check it
            $(this).children('input').prop('checked', true);

            // add this thumb to the preview card
            var $image_url = $(this).data('corpus_image_url');
            var $corpus_id = $(this).data('corpus_id');

            var $elem = $('<span class="preview-thumb-wrapper" data-corpus_id="' + $corpus_id + '">');

            // check if this is the first image added to the div
            if ($('#corpus_preview').find('span[class="preview-thumb-wrapper"]').length > 0){

                // some pics are already there, so drop a plus sign into the span
                $elem.append($('<i class="fa fa-plus" aria-hidden="true"></i>'));

            }

            var thumb_div = '<div style="background-image:url(' + $image_url  + ')" class="corpus-thumb">';

            // append icon and /span tags

            if ($(this).data('corpus_type') === 'TW'){
                thumb_div += ' <i class="fa fa-twitter"></i> '
            }
            else if ($(this).data('corpus_type') === 'EX'){
                thumb_div += ' <i class="fa fa-book"></i> '
            }

            thumb_div += "</span>";

            // OK, thumb div is constructed, now append it
            $elem.append(thumb_div);

            // insert all of these elements into the div
            $('#corpus_preview').append($elem);

            }

    });

/* update the preview card the minute they type something */

$('#id_title').keyup(
    function(){
        // update the preview card
        $('#title_preview').text($('#id_title').val());




});