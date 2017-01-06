"""
Support module for ewe_ebooks containing the various business algorithms for combining texts/tweets

"""

import random
from nltk import pos_tag, word_tokenize
import re
from .corpus_utils import rem_contractions


def mouse_join(corpora, smashtag=False):
    """
    Takes list of sources.Corpus objects. Selects two at random, then extracts random sentences from each,
    tags them using nltk.pos_tag and then then chains them together, alternating on each successive verb.

    Props to @tripofmice for this methodology in her @brandnewfacts bot.

    :param corpora: list of ewe_ebooks.sources.Corpus objects
    :param smashtag: Boolean flag, include a hashtag taken from combining two random hashtags
    :return: Tuple containing new sentence with optional hashtag and the two parent sentence objects
    """

    def tag_sentence(sentence):
        """
        helper function for tagging sentences. tosses sentences without verbs
        """

        def post_proc(toks):
            """
            helper func for conjoining contractions
            :param toks:
            :return:
            """
            toks_out = []
            while len(toks) > 1:
                bigram = toks[:2]
                if bigram[1][0] == "'":
                    toks_out.append("".join(bigram))
                    toks = toks[2:]
                else:
                    toks_out.append(bigram[0])
                    toks = toks[1:]

            toks_out.extend(toks)

            return toks_out

        tagged = []
        tokens = post_proc(word_tokenize(sentence))
        tags = pos_tag(tokens)
        if len([word for word in tags if word[1].startswith('VB')]):
            return tags
        else:
            return False

    def gen_smashtag(corpus1, corpus2):
        """
        tries to create a "smashtag," a hashtag composed of two randomly selected ones smashed together
        :param corpus1:
        :param corpus2:
        :return:
        """
        try:
            first_hashtags = [hashtag.hashtag for hashtag in corpus1.hashtags.all()]
            second_hashtags = [hashtag.hashtag for hashtag in corpus2.hashtags.all()]
            return ' #{}{}'.format(random.choice(first_hashtags), random.choice(second_hashtags))
        except IndexError:
            # One of these didn't have any hashtags..
            return ''

    # Get two corpora from the list
    first_corpus, second_corpus = corpora[:2]

    # Get random sentences from our two sources (corpora)
    # Try to find sentences with verbs.. to avoid an infinite loop, just try ten times

    sentence1 = first_corpus.sentences.random()
    num_tries = 0
    while (len([word for word in pos_tag(word_tokenize(sentence1.sentence)) if word[1].startswith('VB')]) < 1) and num_tries < 10:
        sentence1 = first_corpus.sentences.random()
        num_tries += 1

    sentence2 = second_corpus.sentences.random()
    num_tries = 0
    while (len([word for word in pos_tag(word_tokenize(sentence2.sentence)) if word[1].startswith('VB')]) < 1) and num_tries < 10:
        sentence2 = second_corpus.sentences.random()
        num_tries += 1


    # OK, hopefully got some valid sentences. it's #GoTime

    # TODO: do some error handling here

    # Initialize accumulator variable, will be a words that we'll join to produce the polished output
    output = []


# TODO: implement lookahead and pivot once we reach a non-verb

    try:
        found_verb = False

        for word, tag in tag_sentence(rem_contractions(sentence1.sentence)):
            output.append(word)

            if tag.startswith('VB'):
                # At the first verb. We want all verbs after this, then pivot at the first non-verb
                found_verb = True
                continue


            if not tag.startswith('VB') and found_verb is True:
                # Ok, got all the verbs that appear in a row, break
                break

        # Flag to discard the first half of the sentence til we hit a verb
        second_half = False

        first_verb = True

        for word, tag in tag_sentence(rem_contractions(sentence2.sentence)):
            if tag.startswith('VB'):
                second_half = True
                if first_verb:
                    first_verb = False
                    continue  # Don't add this verb, but add the rest
            # OK, now start adding words after this verb

            if second_half:
                output.append(word)
    except:
        raise ValueError('Invalid source material, mashup failed. Please try a different source')

    # Join the output into a sentence
    output = " ".join(output)

    # Tack a hashtag onto this puppy if they want it

    if smashtag is True:
        output += gen_smashtag(first_corpus, second_corpus)


    # Returns (string, Sentence object, Sentence object)
    return (output, sentence1, sentence2)

