"""
Support module for ewe_ebooks containing the various business algorithms for combining texts/tweets

"""

import random
from nltk import pos_tag, word_tokenize

def mouse_join(first_source, second_source):
    """
    Takes two lists of words. Jumps to a random starting place in one,
    then chains them together, alternating on each successive verb.
    Props to @tripofmice for this methodology in her @brandnewfacts bot.

    :param first_source: list of sentences from first source (usually from Timeline.sentences)
    :param second_source: list of sentences from first source (usually from Timeline.sentences)
    :return: Novel sentence
    """
    # Randomly select starting text
    if random.choice([True, False]):
        second_source, first_source = first_source, second_source

    # Generate tags for each set of sentences

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

    first_tags = tag_sentences(first_source)
    second_tags = tag_sentences(second_source)

    output = []

    for word, tag in random.choice(first_tags):
        output.append(word)

        if tag.startswith('VB'):
            break

    # Haven't hit second half of sentence yet
    second_half = False
    first_verb = True
    for word, tag in random.choice(second_tags):
        if tag.startswith('VB'):
            second_half = True
            if first_verb:
                first_verb = False
                continue # Don't add this verb, but add the rest
            # OK, now start adding words after this verb

        if second_half:
            output.append(word)

    return output