"""
Support module for ewe_ebooks containing the various business algorithms for combining texts/tweets

"""

import random
from nltk import pos_tag

def mouse_join(first_source, second_source):
    """
    Takes two lists of words. Jumps to a random starting place in one,
    then chains them together, alternating on each successive verb.
    Props to @mousereeve for this methodology in her @brandnewfacts bot.

    :param first_source: list of sentences from first source (usually from Timeline.sentences)
    :param second_source: list of sentences from first source (usually from Timeline.sentences)
    :return: Novel sentence
    """
    # Randomly select starting text
    if random.choice([True, False]):
        second_source, first_source = first_source, second_source



    first_tags = pos_tag(first_source)
    second_tags = pos_tag(second_source)



    if random.choice([True, False]):
        pass
    else:
        pass









def (first_source, second_source):
    """
    given a text, creates a random sentence based on collapsing chained
    trigrams, chaining word 3 with the most common trigram starting with word 3
    avoids linking with stopwords to prevent looping phrases like "as well as"
    :param body_text - text on which to base the sentence:
    :return prints new sentence:
    """


    tg_counts = dict()

    # Collect trigram counts in the dictionary
    for trigram in trigrams:
        tg_counts[trigram] = tg_counts.get(trigram, 0)+1

    # Get a set of unique trigrams for organizational purposes
    unique_trigrams = set(tg_counts.keys())

    # Create data structure for first word meta dictionary
    trigrams_by_first_word = dict()

    # We only need the first word.. add an entry and empty list to the dictionary for each word
    for first_word, second_word, third_word in unique_trigrams:
        #  Some suboptimal overlapping here
        trigrams_by_first_word[first_word] = []

    # Push the trigram counts into meta dictionary , structure word: (count,(trigram))
    for trigram, count in sorted(tg_counts.items()):
        w1, w2, w3 = trigram
        trigrams_by_first_word[w1].append((count, trigram))

    # Choose a random starting point
    startword = random.choice(tokenized_text)


    # Generate a random sentence length of trigrams
    sentence_length = random.choice(range(3,15))
    print("SENTENCE LENGTH:", sentence_length)
    tg_count, current_trigram = max(trigrams_by_first_word[startword])
    print(current_trigram)
    word1, word2, word3 = current_trigram
    #Capitalize first word
    word1 = word1.title()
    sentence = [word1, word2]
    nextword = word3

    for _ in range(sentence_length):
        tg_count, current_trigram = (max(trigrams_by_first_word[nextword]))
        print(current_trigram)
        word1, word2, word3 = current_trigram

        sentence.extend([word1, word2])
        nextword = word3
        while nextword in stopwords.words('english'):
            nextword = random.choice(tokenized_text)


    output  = " ".join(sentence) + "."
    print(output)