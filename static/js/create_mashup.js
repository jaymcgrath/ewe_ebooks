$('.corpus-card').bind('click',
                function(){
                    $(this).toggleClass('active');
                    // Assign this.checkbox to a var
                    if ($(this).children('input').prop('checked'))
                    {
                        $(this).children('input').prop('checked', false);
                    } else {
                        $(this).children('input').prop('checked', true);
                    }
                });