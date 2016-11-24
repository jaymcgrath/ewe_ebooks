"""
Twitter backend functions for retrieving tweets and seeding corpora

"""
import re
import tweepy
from secrets.secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


class Timeline:
    """
    User timeline class for retrieving tweets via Tweepy wrapper

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
    # TODO: add some methods

    def __init__(self, username, count=100):
        # TODO: Login to twitter for corpus generation using end user's credentials
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        # Connect to Twitter - raise
        try:
            api = tweepy.API(auth)
        except tweepy.TweepError:
            # TODO: fix error raised by failed twitter login
            raise PermissionError("Twitter Auth failed")

        # Gets a list of status objects (tweets) for this user
        timeline = api.user_timeline(username, count=count)

        """
        some setup for tweet parsing
        """

        # accumulators
        tweets = []
        hashtags = []

        # TODO: test and tweak url and hashtag regular expressions
        # url and hashtag regexes - quick n dirty - just matches start and non-whitespace

        url_regex = re.compile(r'(https?|ftp)://[^\s]+')
        hashtag_regex = re.compile(r'\#[^\s]+')

        # Extract the tweet body out of each Status object
        # TODO: filter out retweets, prepended by 'RT'
        for tweet in timeline:
            tweet_body = tweet.text
            #TODO: make this less ugly

            these_tags = hashtag_regex.findall(tweet.text)
            hashtags.extend(these_tags) if these_tags else None
            # ht = [t for t in hashtags if t is not None]
            tweet_body = url_regex.sub('', tweet_body)
            tweets.append(tweet_body)

        self.tweets = tweets
        self.hashtags = hashtags

    def __str__(self):
        #TODO: fill out __str__ method
        pass

    def __repr__(self):
        #TODO: fill out __repr__ method
        pass


class Tweet:
    """
    Individual instance of a tweet object. Used for posting tweets from various bots
    """
    # TODO: flesh out Tweet object - Tweet.post(), Tweet.retweets() methods
    pass






