"""
Support module for ewe_ebooks containing the various business algorithms for combining texts/tweets

"""

import random
from nltk import pos_tag, word_tokenize


def mouse_join(corpora, smashtag=False):
    """
    Takes list of sources.Corpus objects. Selects two at random, then extracts random sentences from each,
    tags them using nltk.pos_tag and then then chains them together, alternating on each successive verb.

    Props to @tripofmice for this methodology in her @brandnewfacts bot.

    :param corpora: list of ewe_ebooks.sources.Corpus objects
    :param smashtag: Boolean flag, include a hashtag taken from combining two random hashtags
    :return: New sentence with optional hashtag
    """

    def tag_sentences(sentences):
        """
        helper function for tagging sentences. tosses sentences without verbs
        """

        tagged = []
        for sentence in sentences:
            tags = pos_tag(word_tokenize(sentence))
            if len([word for word in tags if word[1].startswith('VB')]):
                tagged.append(tags)

        return tagged

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

    # Get two of them from the list
    first_corpus, second_corpus = corpora[:2]

    # import ipdb; ipdb.set_trace()

    # Get some random sentences from our two sources (corpora)

    # Shuffle up the sentences, then grab up to 25 of them
    first_sents = [sentence.sentence for sentence in first_corpus.sentences.all()]
    second_sents = [sentence.sentence for sentence in second_corpus.sentences.all()]

    random.shuffle(first_sents)
    random.shuffle(second_sents)

    first_sents = first_sents[:25]
    second_sents = second_sents[:25]

    # These will contain tuples in the format (word, tag)
    first_tags = tag_sentences(first_sents)
    second_tags = tag_sentences(second_sents)

    # OK, hopefully got some valid sentences. it's #GoTime
    # TODO: do some error handling here

    # Initialize accumulator variable, will be a words that we'll join to produce the polished output
    output = []


# TODO: implement lookahead and pivot once we reach a non-verb

    try:
        found_verb = False
        for word, tag in random.choice(first_tags):
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
        for word, tag in random.choice(second_tags):
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

    return output

