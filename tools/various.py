#!/usr/bin/python
#  -*- coding: utf-8 -*-

"""various.py

Various tools for releasing some burden on main
"""


def find_occurrences(s, ch):
    """Returns a list of positions of each occurrence of ch in s.

    Args:
        s:
        ch:

    Returns:

    """
    return [i for i, letter in enumerate(s) if letter == ch]


def without_redundant(l):
    """Deletes redundant element in input list.

    Args:
        l:

    Returns:

    """
    return list(set(l))


def remove_parasites(l):
    """Removes every occurrence of '' from input list.

    Args:
        l:

    Returns:

    """
    temp = []
    for i in range(len(l)):
        if not l[i] == '':
            temp.append(l[i])
    return temp
