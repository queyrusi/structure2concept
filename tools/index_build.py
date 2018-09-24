#!/usr/bin/python
#  -*- coding: utf-8 -*-

"""index_build.py

Building index for faster parsing of DBpedia dump.
"""


def build_index(relations_path):
    """Index for fast parsing dump based on first letter of seed.

    First line of dump is removed (no interesting information).

    relations_path (str):

    Returns:
        index (dict):
                          {'A': line number in dump,
                           'B': line number in dump,
                           'C': line number in dump,
                           ... }
    """
    with open(relations_path) as db_dump:
        global relations
        relations = [lines for lines in db_dump]
        relations = relations[1:]
    char_index = {}
    for chr_num in range(65, 91):
        l_num = 0
        for line in relations:
            try:
                a = line.index("<http://dbpedia.org/resource/" + chr(chr_num))
                if not a:
                    char_index[chr(chr_num).lower()] = l_num
                    break
            except ValueError:
                pass
            l_num += 1
    return char_index
