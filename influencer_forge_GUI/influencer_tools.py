#!/usr/bin/python
#  -*- coding: utf-8 -*-

"""influencer_tools.py

Setting up influencer model based on structure data.

"""

# config
blocks_path = "./un_Pool_BSC/all_vids_idfgvsds.txt"  # /!\ ACHTUNG path

def tree_set_up():
    """

    Returns:

    """
    with open(blocks_path) as structure:
        course_structure = json.load(structure)
    tree = dict()
