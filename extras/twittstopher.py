"""
Twitter backend functions for retrieving tweets and seeding a corpus

"""
import re
import tweepy
from nltk import ngrams, word_tokenize, sent_tokenize
from secrets.secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


class Timeline:
    """
    User timeline class for retrieving  and parsing tweets via Tweepy wrapper and NLTK

    properties:
    tweets - list of strings, tweet bodies from this timeline
    hashtags - list of strings, all hashtags from this timeline

    Tweepy Status Object dir (excludes dunders):
    'author',
    'contributors',
    'coordinates',
    'created_at',
    'destroy',
    'entities',
    'extended_entities',
    'favorite',
    'favorite_count',
    'favorited',
    'geo',
    'id',
    'id_str',
    'in_reply_to_screen_name',
    'in_reply_to_status_id',
    'in_reply_to_status_id_str',
    'in_reply_to_user_id',
    'in_reply_to_user_id_str',
    'is_quote_status',
    'lang',
    'parse',
    'parse_list',
    'place',
    'possibly_sensitive',
    'retweet',
    'retweet_count',
    'retweeted',
    'retweeted_status',
    'retweets',
    'source',
    'source_url',
    'text',
    'truncated',
    'user']

    """
    # TODO: write a real docstring

    def __init__(self, username, count=100, last_tweet_id=1):
        # TODO: Login to twitter for corpus generation using end user's credentials
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        # Connect to Twitter - raise
        try:
            api = tweepy.API(auth)
        except tweepy.TweepError:
            # TODO: make sure this error bubbles up and gets handled gracefully
            raise PermissionError("Twitter Auth failed")

        # Gets a list of status objects (tweets) for this user
        timeline = api.user_timeline(username, count=count, since_id=last_tweet_id)

        """
        some setup for tweet parsing
        """

        # accumulators
        tweets = []
        hashtags = []

        # TODO: test and tweak url and hashtag regular expressions
        # url and hashtag regexes - quick n dirty - just matches start and non-whitespace

        url_regex = re.compile(r'(https?|ftp)://[^\s]+')
        """
        The problem: want to remove tweet addressees but retain inline mentions as they are semantically
         relevant. This regex will strip all @'s at the beginning of a tweet while retaining ones appearing later
        """
        at_regex = re.compile(r'(^@.*? )([^@]|$)')


        # Extract the tweet body out of each Status object

        for tweet in timeline:
            # retweeted_status only exists in retweets
            if 'retweeted_status' not in tweet._json:
                tweet_body = tweet.text
                # Filter out most URLs
                tweet_body = url_regex.sub('', tweet_body)
                # Filter out addressees at beginning of tweet
                tweet_body = at_regex.sub(r'\2', tweet_body)

                if tweet_body:
                    # Add it to the list if we have anything left
                    tweets.append(tweet_body)

                for hash_obj in tweet.entities['hashtags']:
                        hashtags.append(hash_obj['text'])

        # Get the ID of the last tweet fetched, for freshening purposes
        try:
            last_tweet_id = timeline.ids()[0]
        except:
            raise tweepy.TweepError("Nothing fetched!")


        # Now process cleaned up tweets with NLTK
        words = []
        bigrams = []
        trigrams = []
        quadgrams = []
        sentences = []

        for tweet in tweets:
            these_words = word_tokenize(tweet)
            sentences.extend(sent_tokenize(tweet))
            words.extend(these_words)
            bigrams.extend(ngrams(these_words, 2))
            trigrams.extend(ngrams(these_words, 3))
            quadgrams.extend(ngrams(these_words, 4))

        self.words = words
        self.bigrams = bigrams
        self.trigrams = trigrams
        self.quadgrams = quadgrams
        self.sentences = sentences
        self.tweets = tweets
        self.hashtags = hashtags
        # TODO: Remove this api property after testing finished.
        self.api = api
        self.timeline = timeline
        self.author = username
        self.last_tweet_id = last_tweet_id

    def __str__(self):
        return self.author

    def __repr__(self):
        repr_str = "{} Timeline object, {} tweets, {} hashtags"
        return repr_str.format(self.author, len(self.tweets), len(self.hashtags))


class Tweet:
    """
    Individual instance of a tweet object. Used for posting tweets from various bots
    """
    # TODO: flesh out Tweet object - Tweet.post(), Tweet.retweets() methods
    pass


class User:
    """
    Twitter user class.
    Primary use: fetching profile picture and details/statistics when initializing as a source
    """

    def __init__(self, twitter_username):
        # TODO: Login to twitter for corpus generation using end user's credentials
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        # Connect to Twitter - raise TweepError if we brick out on this
        try:
            api = tweepy.API(auth)
        except tweepy.TweepError:
            # TODO: make sure this error bubbles up and gets handled gracefully
            raise PermissionError("Twitter Auth failed")

        usr = api.get_user(twitter_username)
        self.username = twitter_username
        self.image = usr.profile_image_url
        self.api = usr
        self.description = usr.description
        self.screen_name = usr.screen_name

    def __repr__(self):
        return self.username + "(Tweepy User object)"

    def __str__(self):
        return self.username + "(Tweepy User object)"
