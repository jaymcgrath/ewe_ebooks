"""
External tools for parsing bodies of text
"""

from nltk import ngrams, word_tokenize, sent_tokenize


class Excerpt:
    """
    Class for parsing big chunks of text and saving as Corpus objects
    """

    def __init__(self, body, author='Anonymous'):

        # accumulators
        hashtags = []

        # Now process cleaned up text with NLTK
        words = []
        bigrams = []
        trigrams = []
        quadgrams = []
        sentences = []


        words = word_tokenize(body)

        sentences.extend(sent_tokenize(body))

        # Strip whitespace from each sentence
        sentences = [sentence.strip() for sentence in sentences]

        bigrams = ngrams(body, 2)
        trigrams = ngrams(body, 3)
        quadgrams = ngrams(body, 4)

        self.body = body
        self.words = words
        self.bigrams = bigrams
        self.trigrams = trigrams
        self.quadgrams = quadgrams
        self.sentences = sentences
        self.hashtags = hashtags
        self.author = author

        #TODO: Create "hashtags" from arbitrary number of rarest words

    def __str__(self):
        return self.author

    def __repr__(self):
        repr_str = "{} Excerpt object, {} words, {} sentences"
        return repr_str.format(self.author, len(self.words), len(self.sentences))

    def __len__(self):
        return len(self.words)