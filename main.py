#!/usr/bin/env python
# coding: utf-8

"""
Author: Sunil Kunnakkat
Year: 2020

Inspired by:
- Concept: https://towardsdatascience.com/simulating-text-with-markov-chains-in-python-1a27e6d13fc6
- Element count functions: https://www.tutorialspoint.com/count-frequencies-of-all-elements-in-array-in-python

This code takes a text file containing any large string, and generates
four-element-wide markov-chain variations based on the corpus. These structures
are then chosen at random to generate new sentences, closely mimicing the styles of
the original text. Sometimes, it's actually an interesting read.

"""

import numpy as np
import random
import re

# The element fucntions search for a "word" in a the corresponding
# corpus, and finds all corresponding n-word pairs based on the size
# of the word.


def word_element(word, word_corpus):
    key = {}
    count = 0
    word_indices = [i for i in range(
        len(word_corpus)) if word_corpus[i] == word]
    elements_count = {}
    word_list = [word_corpus[i+1]
                 for i in word_indices if i+1 < (len(word_corpus)-1)]
    for element in word_list:
        if element in elements_count:
            elements_count[element] += 1
        else:
            elements_count[element] = 1
    return elements_count


def two_word_element(word, corpus_list):
    word_indices = [i for i in range(
        len(corpus_list[0])) if corpus_list[0][i] == word]
    elements_count = {}
    word_list = [corpus_list[0][i+1]
                 for i in word_indices if i+1 < (len(corpus_list[0])-1)]
    for element in word_list:
        if element in elements_count:
            elements_count[element] += 1
        else:
            elements_count[element] = 1

    return elements_count


def three_word_element(word, corpus_list):
    word_indices = [i for i in range(
        len(corpus_list[0])) if corpus_list[0][i] == word]
    elements_count = {}
    word_list = [corpus_list[0][i+1]
                 for i in word_indices if i+1 < (len(corpus_list[0])-1)]
    for element in word_list:
        if element in elements_count:
            elements_count[element] += 1
        else:
            elements_count[element] = 1

    return elements_count


def four_word_element(word, corpus_list):
    word_indices = [i for i in range(
        len(corpus_list[0])) if corpus_list[0][i] == word]
    elements_count = {}
    word_list = [corpus_list[0][i+1]
                 for i in word_indices if i+1 < (len(corpus_list[0])-1)]
    for element in word_list:
        if element in elements_count:
            elements_count[element] += 1
        else:
            elements_count[element] = 1

    return elements_count

# The next two functions simply return key and values for the given element
# dictionary.


def get_keys(element):
    return [key for key in element]


def get_vals(element, key_list):
    return [element[key] for key in key_list]

# All word dictionaries determine the word to be returned based on the
# keys and values from the corresponding element dictionary. The weights
# represent the count of the key word in the corpus.


def one_word(current_word, word_corpus):
    e = word_element(current_word, word_corpus)
    k = get_keys(e)
    v = get_vals(e, k)
    next_word = random.choices(k, weights=v, k=1)[0]
    return next_word


def two_words(current_word_new, current_word, corpus_list):
    e2 = two_word_element(current_word_new, corpus_list[0])
    k2 = [key for key in e2]
    if k2:
        v2 = get_vals(e2, k2)
        next_word = random.choices(k2, weights=v2, k=1)[0]
        return next_word
    else:
        return one_word(current_word, corpus_list[-1])


def three_words(current_word_new, current_word, corpus_list):
    e3 = three_word_element(current_word_new, corpus_list[0])
    k3 = get_keys(e3)
    if k3:
        v3 = get_vals(e3, k3)
        next_word = random.choices(k3, weights=v3, k=1)[0]
        return next_word
    else:
        return two_words(" ".join(current_word_new[-2:]),
                         current_word, corpus_list[1:])


def four_words(current_word_new, current_word, corpus_list):
    e4 = four_word_element(current_word_new, corpus_list[1])
    k4 = get_keys(e4)
    if k4:
        v4 = get_vals(e4, k4)
        next_word = random.choices(k4, weights=v4, k=1)[0]
        return next_word
    else:
        return three_words(" ".join(current_word_new[-3:]),
                           current_word, corpus_list[1:])

# These three functions allow us to generate the necessary corpus lists
# based on on the size of the word count. The original text is split and
# then regrouped every n words.


def two_way_split(string):
    words = string.split()
    return [' '.join(words[i: i + 2]) for i in range(0, len(words), 2)]


def three_way_split(string):
    words = string.split()
    return [' '.join(words[i: i + 3]) for i in range(0, len(words), 3)]


def four_way_split(string):
    words = string.split()
    return [' '.join(words[i: i + 4]) for i in range(0, len(words), 4)]


def size_handler(size, sentence, current_word, corpus_list):
    
    if size > 1 and len(sentence) >= size:
        current_words = sentence[-size:]
        current_word_new = " ".join(current_words)
        if size == 4:
            next_word = four_words(current_word_new,
                                   current_word,
                                   corpus_list)
            sentence.extend(next_word.split())
            current_word = next_word.split()[-1]
            return sentence, current_word
        elif size == 3:
            next_word = three_words(current_word_new,
                                    current_word,
                                    corpus_list[1:])
            sentence.extend(next_word.split())
            current_word = next_word.split()[-1]
            return sentence, current_word
        elif size == 2:
            next_word = two_words(current_word_new,
                                  current_word,
                                  corpus_list[2:])
            sentence.extend(next_word.split())
            current_word = next_word.split()[-1]
            return sentence, current_word
    else:
        next_word = one_word(current_word, corpus_list[3])
        sentence.append(next_word)
        current_word = next_word
        return sentence, current_word


def main():

    # Open the text file to be analyzed.
    with open('text_to_analyze.txt', 'r') as file:
        text = file.read()

    # Create the different corpus variations, up to four-word keys.
    corpus = text.split()
    corpus2 = two_way_split(text)
    corpus3 = three_way_split(text)
    corpus4 = four_way_split(text)

    corpus_list = [corpus4, corpus3, corpus2, corpus]

    # Also start with a random first word based on the one-word corpus.
    first_word = np.random.choice(corpus)

    current_word = first_word
    final = ""

    # We're going to write a random amount of sentences.
    for o in range(0, np.random.choice(range(10, 13))):

        sentence = []

        # Each sentence will be of a random length between 11 and 13 words.
        for i in range(0, np.random.choice(range(10, 13))):

            # Pick a random size to determine corpus to use.
            size = random.choices([1, 2, 3, 4], weights=[1, 4, 2, 16], k=1)[0]

            # Run everything through the size handler, generate a new sentence
            # and current word to replace the old one.
            sentence, current_word = size_handler(size,
                                                  sentence,
                                                  current_word,
                                                  corpus_list)
        length = -i
        sentence = sentence[length:]
        current_word = sentence[-1]
        final = final + " ".join(sentence)
        final = final + "\n"

    print(final)


if __name__ == "__main__":
    main()
