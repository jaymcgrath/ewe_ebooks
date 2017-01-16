"""
Utilities for posting bots' content to twitter
""""""


# Snippet for saving an output
this_output = Output()

        # select a random mashup to use to generate output
        try:
            this_output.mashup = bot.mashup.random()
        except:
            # create a sensible error message
            num_mashups = len(bot.mashup.all())
            error_msg = 'Unable to select a random mashup. There are {n} mashups configured'.format(num_mashups)
            ValueError(error_msg)

