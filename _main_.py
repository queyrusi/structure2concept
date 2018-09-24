#!/usr/bin/python
#  -*- coding: utf-8 -*-

"""__main__.py

This module tests the definition and running of functions to collect useful
concepts from a json block provided by xuetangX videos, through data from
course structure (mainly chapter title, sequential title and vertical title).


     1/ build index (server)

   / 2/ load blocks
  |  3/ clean ids
  |  4/ translate ids
   ` 5/ subtitles + concept processing

     6/ get_n_depths (server)

     7/ build semantics
     8/ all_scores
"""

__author__ = "Simonkey"
__credits__ = ["Simon Q.", "王笑尘"]
__version__ = "1.0.1"
__email__ = "simon.queyrut@ensta-bretagne.org"
__status__ = "Production"

import logging
from tools.main_processing_tools import *

from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
xiaomu = client.xiaomu

# logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] \
                            %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./logs/kp.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


# 0 -- SETTING UP
# ================
with open(relations_path) as dump:
    relations = [lines for lines in dump]
    relations = relations[1:]
blocks = load_blocks()
video_dict = get_associated_ids(blocks, "f4d2dfd663054221933e7c849a215a59")
print("\n ORIGINAL DICT \n", video_dict)
clean_ids(video_dict)
print("\n CLEANED DICT \n", video_dict)
translate_ids(video_dict)
print("\n TRANSLATED DICT \n", video_dict)
add_concepts(video_dict)
del video_dict['subs']  # careful: mutates the dict
print("video dict purgé \n \n \n \n", video_dict)
concepts_in_list(video_dict)
remove_stopwords(video_dict)
print("\n \n \nSTOP WORDS REMOVED DICT", video_dict)
translate_concepts(video_dict)
print("\n \n \nTRANSLATED CONCEPTS", video_dict)
add_underscores(video_dict)
# ================================
#  2 -- SUB-CATEGORIES EXTRACTION
# ================================
n_depths_subcats = []
sc = get_n_depths(get_seed(video_dict)[0], 20)
# ====================================
#  3 -- CONCEPT-SEED MATCHING/SCORING
# ====================================
semantics_sc = build_semantics(sc)
all_scores(video_dict)
video_dict["concepts"] = all_scores(video_dict)
