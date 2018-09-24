#!/usr/bin/python
#  -*- coding: utf-8 -*-

"""This module defines a Cleaner class which will get rid of unwanted characters
in strings.

"""

__author__ = "Simonkey"
__credits__ = ["Simon Q.", "王笑尘"]
__version__ = "1.0.1"
__email__ = "simon.queyrut@ensta-bretagne.org"
__status__ = "Production"

import tools


class Cleaner(object):
    """Cleaner class to create cleaners with certain rules to remove specific
    characters from strings.
    """

    @staticmethod
    def andword_split(string):
        """This rule splits input string in two (and so on) if a character or
        word from file 'and_characters.txt' is in input string. Also removes
        this character.

        """
        w = string
        with open("./kp/and_characters.txt") as and_characters:
            character_list = [lines.strip() for lines in and_characters]
        character_list.sort(key=lambda s: len(s))  # sort by length min -> max
        character_list = character_list[::-1]

        def rec_split(l):
            temp = l
            flag1 = False
            flag2 = False
            for split in l:
                for character in character_list:
                    if character in split:
                        flag1 = True
                        flag2 = True
                        beg = split.index(character)
                        end = beg + len(character)
                        split1 = split[: beg]
                        split2 = split[end:]
                        temp.append(split1)
                        temp.append(split2)
                temp = tools.without_redundant(temp)
                if flag2:
                    temp.remove(split)
                flag2 = False
            final = temp
            if flag1:
                final = rec_split(temp)
            else:
                return final
            return final
        a_split = rec_split([w])
        if len(a_split) == 1:
            a_split = a_split[0]
        return a_split

    @staticmethod
    def outer_spaces(string):
        """Removes outer spaces from input string"""
        w = string
        if w == '' or w == ' ':
            return ''
        try:
            while w[0] == ' ':
                print(w)
                w = w[1:]
            while w[-1] == ' ':
                w = w[: -1]
            return w
        except IndexError as e:
            print(e)
            return w

    @staticmethod
    def special_char(string):
        """This rule removes every occurrence of special characters as listed in
        special_characters.txt from input string.

        """
        with open("./kp/special_characters.txt") as spchar:
            char_list = [lines.strip() for lines in spchar]
        char_list.sort(key=lambda s: len(s))  # sort by length min -> max
        char_list = char_list[::-1]
        for char in char_list:
            if char in string:
                string = string.replace(char, '')
        spchar.close()
        return string

    @staticmethod
    def parenthesis(string):
        """This rule removes every occurrence of parenthesis characters "(" or
        "（" and ")" or "）" as well as every character in between from input
        string.

        """
        for char in string:
            if char == "(":
                print(string)
                print(string.index("("))
                fir = string.index("(")
                sec = string.index(")")
                string = string[:fir] + string[sec + 1:]
            if char == "（":
                fir = string.index("（")
                sec = string.index("）")
                string = string[:fir] + string[sec + 1:]
        return string

    @staticmethod
    def word(string):
        """This rule removes every occurrence of characters listed in .txt file
        from input string.

        """
        w = string
        with open("./kp/stop_words.txt") as stop_words:
            word_list = [lines.strip() for lines in stop_words]
        word_list.sort(key=lambda s: len(s))  # sort by length min -> max
        word_list = word_list[::-1]
        for word in word_list:
            if word in w:
                w = w.replace(word, '')
        stop_words.close()
        return w

    @staticmethod
    def chapter_header(string):
        """This rule removes first occurrence of chinese characters "第" and "章"
        as well as every character in between from input string.

        """
        w = string
        for char in string:
            if char == "第" and tools.find_occurrences(w, "章"):
                fir = w.index(char)
                sec = w.index("章")
                w = w[: fir] + w[sec + 1:]
                w = w.strip()
            elif char == "第" and tools.find_occurrences(w, "周"):
                fir = w.index(char)
                sec = w.index("周")
                w = w[: fir] + w[sec + 1:]
                w = w.strip()
        return w

    @staticmethod
    def numbers(string):
        """This rule removes every digit from input string.

        """
        for char in string:
            if char.isdigit():
                i = string.index(char)
                string = string[:i] + string[i + 1:]
        return string

    def __init__(self, *args):
        """Creates an instance of class Cleaner.

        Args:
            *args:
        """
        self.rules = {i for i in args}
        self.available_rules = {"word": self.word,
                                "chapter_header": self.chapter_header,
                                "numbers": self.numbers,
                                "dots": self.dots,
                                "parenthesis": self.parenthesis,
                                "andword_split": self.andword_split,
                                "special_char": self.special_char,
                                "outer_spaces": self.outer_spaces,
                                }
        self.order = ["parenthesis",
                      "chapter_header",
                      "andword_split",
                      "dots",
                      "numbers",
                      "special_char",
                      "outer_spaces",
                      "word"
                      ]

    def dots(self, string):
        """This rule removes first occurrence of character ":" as well as
        everything that comes before from input string.

        """
        w = string
        result = []
        if type(w) == list:
            for k in w:
                result.append(self.dots(k))
            return result
        else:
            for char in w:
                if char == ":" or char == "：":
                    i = w.index(char)
                    if i == 0:
                        i = w.index("：")
                    # print("i vaut buen sur", i)
                    w = w[i + 1:]
                    w = w.strip()
            return w

    def clean(self, identifier):
        """Applies every initial input cleaning rule to string argument.

        Particular order is observed according to self.order.

        """
        new_id = identifier
        if type(new_id) == list:
            for i in range(len(new_id)):
                for rule in self.order:
                    if rule in self.rules and self.available_rules.get(rule):
                        new_id[i] = self.available_rules[rule](new_id[i])
        else:
            for rule in self.order:
                if rule in self.rules and self.available_rules.get(rule):
                    new_id = self.available_rules[rule](new_id)
        return new_id

# Example:
# --------
#
# my_cleaner = Cleaner("beep", "numbers", "parenthesis","chapter_header",
#                      "char", "dots")
# a = "wo:第五十 九章a(o一me)sdc1threedssn"
# my_cleaner.clean(a)
