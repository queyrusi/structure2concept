#!/usr/bin/python
#  -*- coding: utf-8 -*-

"""datamuse_seek.py

Module to get adequate semantics for scoring English concepts relatively to
video subtitles"""

__author__ = "Simonkey"
__credits__ = ["Simon Q.", "datamuse.com"]
__version__ = "1.0.1"
__email__ = "simon.queyrut@ensta-bretagne.org"
__status__ = "Production"

import requests


def get_semantics(subcat):
    """Get semantics from a gram.

    API: datamuse.com

    Args:
        subcat (str): Wiki sub-cat from which semantics are grown to compare
                      concepts given by subtitles and give them a score

    Returns:
        L (set)
    """
    # words that are triggered by (strongly associated with) the sub-cat
    q1 = requests.get("https://api.datamuse.com/words?rel_trg=" + subcat)
    dict1 = q1.json()
    list1 = [dic['word'].replace(' ', '_') for dic in dict1]
    print(list1)
    # suggestions for the user if they have typed in subcat so far ****
    q2 = requests.get("https://api.datamuse.com/sug?s=" + subcat)
    dict2 = q2.json()
    list2 = [dic['word'].replace(' ', '_') for dic in dict2]
    # adjectives that are often used to describe subcat **
    q3 = requests.get("https://api.datamuse.com/words?rel_jjb=" + subcat)
    dict3 = q3.json()
    list3 = [dic['word'].replace(' ', '_') for dic in dict3]
    # words with a meaning similar to subcat **
    q4 = requests.get("https://api.datamuse.com/words?ml=" + subcat)
    dict4 = q4.json()
    list4 = [dic['word'].replace(' ', '_') for dic in dict4]
    # words related to subcat by topic *
    q5 = requests.get("https://api.datamuse.com/words?topics=" + subcat)
    dict5 = q5.json()
    list5 = [dic['word'].replace(' ', '_') for dic in dict5]
    #
    # rel_[code] with [code] = ...
    # -----------------------------
    # syn	 Synonyms (words contained within the same WordNet synset) ****
    q6 = requests.get("https://api.datamuse.com/words?rel_syn=" + subcat)
    dict6 = q6.json()
    list6 = [dic['word'].replace(' ', '_') for dic in dict6]
    # spc   "Kind of" (direct hypernyms, per WordNet)	gondola → boat ***
    q7 = requests.get("https://api.datamuse.com/words?rel_spc=" + subcat)
    dict7 = q7.json()
    list7 = [dic['word'].replace(' ', '_') for dic in dict7]
    # par	"Part of" (direct meronyms, per WordNet)	trunk → tree
    q8 = requests.get("https://api.datamuse.com/words?rel_par=" + subcat)
    dict8 = q8.json()
    list8 = [dic['word'].replace(' ', '_') for dic in dict8]
    # com	"Comprises" (direct holonyms, per WordNet)	car → accelerator
    q9 = requests.get("https://api.datamuse.com/words?rel_com=" + subcat)
    dict9 = q9.json()
    list9 = [dic['word'].replace(' ', '_') for dic in dict9]
    word_set = set(list1 + list2 + list3 + list4 + list5 + list6 + list7 + list8
                   + list9)
    return word_set
