$('.corpus-card').bind('click',
                function(){

                    // get the id of the one they clicked

                    var $corpus_id = $(this).data('corpus');
                    // add and remove the active class to highlight this card
                    $(this).toggleClass('active');

                    // Check and uncheck hidden checkboxes and hide/unhide thumb from preview
                    if ($(this).children('input').prop('checked'))
                    {
                        // it's checked, change to unchecked
                        $(this).children('input').prop('checked', false);

                        // remove the image from the preview box
                        $('span[data-corpus="' + $corpus_id + '"]' ).remove();

                        // Remove the any plus signs from in front of the thumbnail that is now first

                        var $firstspan = $('#corpus-preview').children('span:first');
                        // if ($firstspan.length > 0) {
                                // will remove the <i> tag from the first one if there is one
                                $firstspan.children('i:first').remove();
                        //        }

                    } else {
                        // not checked, so check it
                        $(this).children('input').prop('checked', true);

                        // add this thumb to the preview card
                        var $image_url = $(this).find('img').prop('src')
                        var $elem = $('<span data-corpus="' + $corpus_id + '">');

                        if ($('#corpus-preview').find('img').length > 0){
                            // some pics are already there, so drop a plus sign into the span
                            $elem.append($(' <i class="fa fa-plus" aria-hidden="true"></i> '));
                            }

                        // append img and /span tags
                        $elem.append($('<img class="thumbnail" id="preview_img' + $corpus_id + '" src="' + $image_url + '" />'));
                        $elem.append($('</span>'));

                        // insert all of these elements into the div
                        $('#corpus-preview').append($elem);

                        }


                });
