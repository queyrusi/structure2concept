#!/usr/bin/python
#  -*- coding: utf-8 -*-

"""influencer.py

"""

import json
# import tools.datamuse_seek as muse
import tools.main_processing_tools as mpt


# config (slight change to be made again with .txt)
# ++++++++++++++++++++++++++++++
# jieba.load_userdict(file_name)
# ++++++++++++++++++++++++++++++
structure_path = "./Pool_BSC/course30240184course_structure.txt"  # /!/
blocks_path = "./Pool_BSC/course-v1%3ATsinghuaX+30240184+sp_blocks"
one_vid_id = "7a4844aed3c9490f8b4e9974137dc186"


def load_structure(path=structure_path):
    """

    Args:
        path:

    Returns:

    """
    with open(path) as course_structure:
        global structure
        structure = json.load(course_structure)
    return


def get_id_map():
    """

    Args:

    Returns:
        id_map (dict):

    Examples:
        >>>get_id_map()
        >>>id_map
        {'c1': (0, None, None), 'c10': (9, None, None), 'c2': (1, None, None)
         ... }

    """
    global id_map
    id_map = dict()
    i_seq_num = 0
    i_vert_num = 0
    chap_num = 0
    for chapter in structure["chapters"]:
        seq_num = 0
        id_map["c" + str(chap_num)] = (chap_num, None, None)
        for sequential in chapter["sequentials"]:
            vert_num = 0
            id_map["s" + str(i_seq_num)] = (chap_num, seq_num, None)
            for vertical in sequential["verticals"]:
                if vertical:
                    id_map["v" + str(i_vert_num)] = (chap_num,
                                                     seq_num,
                                                     vert_num
                                                     )
                vert_num += 1
                i_vert_num += 1
            seq_num += 1
            i_seq_num += 1
        chap_num += 1
    return


def get_string_map():
    """

    Args:

    Returns:
        string_map (dict):

    Examples:
        >>>get_string_map()
        >>>string_map
        {'c0': '第零章', 's0': '选课之前', 'v0': '写在选课之前', 'v1': '宣传片',
        's1': '考核方式', 'v2': '考核方式', 's2': 'OJ系统说明' ... }

    """
    global string_map
    string_map = dict()
    print(string_map)
    i_seq_num = 0
    i_vert_num = 0
    chap_num = 0
    for chapter in structure["chapters"]:
        seq_num = 0
        string_map["c" + str(chap_num)] = structure["chapters"][chap_num][
            "display_name"]
        for sequential in chapter["sequentials"]:
            vert_num = 0
            string_map["s" + str(i_seq_num)] = \
                structure["chapters"][chap_num][
                "sequentials"][seq_num]["display_name"]
            for vertical in sequential["verticals"]:
                if vertical:
                    string_map["v" + str(i_vert_num)] = structure["chapters"][
                        chap_num]["sequentials"][seq_num]["verticals"][
                        vert_num][
                        "display_name"]
                vert_num += 1
                i_vert_num += 1
            seq_num += 1
            i_seq_num += 1
        chap_num += 1
    return


class OverwriteError(Exception):
    pass


class Influencer(object):
    """

    """
    influencers_strings = set()
    influencers = dict()

    @staticmethod
    def get_instances():
        return Influencer.influencers

    def __init__(self, string, iid, left_brother, right_brother, father,
                 children, influence):
        """

        Args:
            string: name of influencer

        """
        try:
            if string in Influencer.influencers_strings:
                raise OverwriteError("existing influencer was overtwritten")
        except OverwriteError:
            print(string)
        Influencer.influencers_strings.add(string)
        self.str = string
        self.left_brother = left_brother
        self.right_brother = right_brother
        self.father = father
        if children is None:
            self.children = []  # list for ordering
        else:
            self.children = children
        # self.dendrite = muse.get_semantics(string)
        self.id = iid
        self.influence = influence
        self.influencers[self.id] = self

    def __str__(self) -> str:
        return self.str

    def __repr__(self) -> str:
        return self.str

    # def is_worthy(self, concept, minim=0.2):
    #     """
    #
    #     Args:
    #         concept (str): concept under scrutiny.
    #         minim (float): between 0 and 1. Depicts minimum resemblance
    #               between
    #             influencer and concept under scrutiny to assert worthiness.
    #
    #     Returns:
    #         is_worthy (bool): asserts if influencer will participate in
    #           scoring
    #              concept under scrutiny
    #
    #     """
    #     is_worthy = True
    #     concept_sem = muse.get_semantics(concept)
    #     n = len([gram for gram in self.dendrite if gram in concept_sem])
    #     if n / len(self.dendrite) < minim:
    #         return not is_worthy
    #     else:
    #         return is_worthy

# ++++++++++++++++++++++++++++++++++++++++++++
# parameters to be entered by user through GUI
# ++++++++++++++++++++++++++++++++++++++++++++


def get_all_videos():
    """

    Args:

    Returns:

    Examples:
        >>>get_all_videos()
        >>>videos_list
        [{'display_name': 'Video', 'id': '4f184a3de72d418caccbd3fa8624d5b6',
         'chap_num': 0, 'seq_num': 0, 'vert_num': 1},
         {'display_name': '1-注册与登录',
         'id': '8f8dfcd0911949c8aeb12f205e515d73', 'chap_num': 0, 'seq_num': 2,
         'vert_num': 1},
         ... ]

    """
    global videos_list
    videos_list = []
    chap_num = 0
    for chapter in structure["chapters"]:
        seq_num = 0
        for sequential in chapter["sequentials"]:
            vert_num = 0
            for vertical in sequential["verticals"]:
                if vertical["blocks"] and \
                   vertical["blocks"][0]["category"] == "video":
                    videos_list.append({"display_name": vertical["blocks"][0][
                        "display_name"],
                                     'id': vertical["blocks"][0]["id"],
                                     "chap_num": chap_num,
                                     "seq_num": seq_num,
                                     "vert_num": vert_num
                                     }
                                    )
                vert_num += 1
            seq_num += 1
        chap_num += 1


def get_concepts(vid_id="7a4844aed3c9490f8b4e9974137dc186", path=blocks_path):
    """

    Args:
        vid_id:
        path (str):

    Returns:

    """
    global concepts
    blocks = mpt.load_blocks(path)
    video_ids = mpt.get_associated_ids(blocks, vid_id)
    mpt.add_concepts(video_ids)
    del video_ids['subs']
    mpt.concepts_in_list(video_ids)
    mpt.remove_stopwords(video_ids)
    concepts = video_ids["concepts"]
    return


# --------------------------------------------------------------------------
# Note to self: gonna need dendrites that will only be provided by Datamuse,
# as far as I know, so keep in mind translation is inevitable.
# --------------------------------------------------------------------------

tree_set_up_param = {"course": 0.2, "father": 0.2, "left_brother": 0.1,
                     "right_brother": 0.1}

paramt = {"hello"}


def set_up_influencers(selected_vid_id, video_list, param=paramt):
    """

    Args:
        selected_vid_id:
        video_list:
        param:

    Returns:
        None

    Examples:
        >>>set_up_influencers(one_vid_id, videos_list)

    """
    for vid_id in video_list:  # finding corresponding video structure data
        if vid_id["id"] == selected_vid_id:
            name = vid_id["display_name"]
            # -------------
            # Left brother:
            # -------------
            if vid_id["vert_num"] > 0:  # video has left brother
                left_brother_id = [key for key, value in id_map.items()
                                   if value == (vid_id["chap_num"],
                                                vid_id["seq_num"],
                                                vid_id["vert_num"] - 1)][0]
                print(left_brother_id)
                left_string = string_map[left_brother_id]
                left_brother = Influencer(left_string, left_brother_id, None,
                                          None, None, None, [])
            else:
                left_brother = None
            print("entre")
            # --------------
            # Right brother:
            # --------------
            try:
                right_brother_id = [key for key, value in id_map.items()
                                    if value == (vid_id["chap_num"],
                                                 vid_id["seq_num"],
                                                 vid_id["vert_num"] + 1)][0]
                right_string = string_map[right_brother_id]
                right_brother = Influencer(right_string, right_brother_id, None,
                                           None, None, None, [])
            except IndexError:
                right_brother = None
            # -------
            # Father:
            # -------
            father_id = [key for key, value in id_map.items()
                         if value == (vid_id["chap_num"], vid_id["seq_num"],
                                      0)][0]
            father_string = string_map[father_id]
            father = Influencer(father_string, father_id, None, None, None,
                                None, [])
            # -------------------------------------------------------
            video_id = [key for key, value in id_map.items()
                        if value == (vid_id["chap_num"],
                                     vid_id["seq_num"],
                                     vid_id["vert_num"]
                                     )
                        ][0]
            print("video_id", video_id)
            # Siblings will have their relations updated:
            Influencer(name, video_id, left_brother, right_brother, father,
                       None, param)
            print('ok')
            if left_brother:
                print(type([Influencer.get_instances()[left_brother.id]][0]))
                Influencer.get_instances()[left_brother.id].right_brother = \
                    Influencer.get_instances()[video_id]
                print("HOLAQUETAL")
                # children list of father is updated (adding left brother)
                if type(Influencer.get_instances()[father.id].children) == list:
                    print("Influencer children is of type list")
                    Influencer.get_instances()[father.id].children += \
                        [Influencer.get_instances()[left_brother.id]]
                else:
                    print("actually no")
                    Influencer.get_instances()[father.id].children += \
                        [Influencer.get_instances()[left_brother.id]]
                print("HOLAQchicosL")
            print('pok')
            if right_brother:
                Influencer.get_instances()[right_brother.id].left_brother = \
                    Influencer.get_instances()[video_id]
                Influencer.get_instances()[father.id].children += \
                    [Influencer.get_instances()[right_brother.id]]
                # children list of father is updated (adding right brother)
                if type(Influencer.get_instances()[father.id].children) == list:
                    Influencer.get_instances()[father.id].children += \
                        [Influencer.get_instances()[right_brother.id]]
                else:
                    Influencer.get_instances()[father.id].children += \
                        [Influencer.get_instances()[right_brother.id]]
            # children list of father is updated (adding video influencer)
            if type(Influencer.get_instances()[father.id].children) == list:
                Influencer.get_instances()[father.id].children += \
                    [Influencer.get_instances()[video_id]]
            else:
                Influencer.get_instances()[father.id].children += \
                    [Influencer.get_instances()[video_id]]
    return


set_up_influencers(one_vid_id, videos_list)


user_parameters = {"video_id": "123123",
              "recursion_depth": 3,
              "left_uncles": {"how_many": 2, "influence": 0.2},
              "left_brothers": {"how_many": 2, "influence": 0.2},
              "children": 1,
              "course": "beep bap borp",
              "father": True
              }


def check_influencer_exists(relative, position, reach=0):
    """

    Args:
        relative (str):
        position (tuple):
        reach (int):

    Returns:
        exists (bool):

    Examples:
        >>>check_influencer_exists("left_brother", (1, 3, 2))
        False

    """
    exists = False
    # ---------------------
    # Get level of current:
    # ---------------------
    level = "vertical"
    if position[1] is None:
        level = "chapter"
    elif position[2] is None:
        level = "sequential"
    # -----------------------------------------------
    # Check if relative influencer of current exists:
    # -----------------------------------------------
    if relative == "left_brother":
        if level == "chapter" and \
             [key for key, value in id_map.items()
              if value == (position[0] - 1, None, None)][0] \
             in Influencer.get_instances().keys():
            exists = True
        elif level == "sequential" and \
            [key for key, value in id_map.items()
             if value == (position[0], position[1] - 1, None)][0] \
                in Influencer.get_instances().keys():
            exists = True
        elif level == "vertical" and \
            [key for key, value in id_map.items()
             if value == (position[0], position[1], position[2] - 1)][0] \
                in Influencer.get_instances().keys():
            exists = True
    if relative == "right_brother":
        if level == "chapter" and \
            [key for key, value in id_map.items()
             if value == (position[0] + 1, None, None)][0] \
                in Influencer.get_instances().keys():
            exists = True
        elif level == "sequential" and \
            [key for key, value in id_map.items()
             if value == (position[0], position[1] + 1, None)][0] \
                in Influencer.get_instances().keys():
            exists = True
        elif level == "vertical" and \
            [key for key, value in id_map.items()
             if value == (position[0], position[1], position[2] + 1)][0] \
                in Influencer.get_instances().keys():
            exists = True
    if relative == "father":
        if level == "chapter":
            pass
        else:
            exists = True
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if relative == "children":
        if level == "vertical":
            pass
        elif level == "chapter" and \
            [key for key, value in id_map.items()
             if value == (position[0], 0, None)][0] \
                in Influencer.get_instances().keys():
            exists = True
        elif level == "sequential" and \
            [key for key, value in id_map.items()
             if value == (position[0], position[1], 0)][0] \
                in Influencer.get_instances().keys():
            exists = True
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    elif relative == "left uncle":
        if level == "chapter":
            pass
        elif level == "sequential" and \
            [key for key, value in id_map.items()
             if value == (position[0] - reach, None, None)][0] \
                in Influencer.get_instances().keys():
            exists = True
        elif level == "vertical" and \
            [key for key, value in id_map.items()
             if value == (position[0], position[1] - reach, None)][0] \
                in Influencer.get_instances().keys():
            exists = True
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    elif relative == "right uncle":
        if level == "chapter":
            pass
        elif level == "sequential" and \
            [key for key, value in id_map.items()
             if value == (position[0] + reach, None, None)][0] \
                in Influencer.get_instances().keys():
            exists = True
        elif level == "vertical" and \
            [key for key, value in id_map.items()
             if value == (position[0], position[1] + reach, None)][0] \
                in Influencer.get_instances().keys():
            exists = True
    return exists


def check_id_exists(relative, position, reach=0):
    """

    Args:
        relative (str):
        position (tuple):
        reach (int):

    Returns:
        exists (bool):

    Examples:
        >>>check_id_exists("left_brother", (1, 3, 2))
        False

    """
    exists = False
    # ---------------------
    # Get level of current:
    # ---------------------
    level = "vertical"
    if position[1] is None:
        level = "chapter"
    elif position[2] is None:
        level = "sequential"
    # -----------------------------------------------
    # Check if relative influencer of current exists:
    # -----------------------------------------------
    if relative == "left_brother":
        if level == "chapter" and \
             [key for key, value in id_map.items()
              if value == (position[0] - 1, None, None)]:
            exists = True
        elif level == "sequential" and \
            [key for key, value in id_map.items()
             if value == (position[0], position[1] - 1, None)]:
            exists = True
        elif level == "vertical" and \
            [key for key, value in id_map.items()
             if value == (position[0], position[1], position[2] - 1)]:
            exists = True
    elif relative == "right_brother":
        if level == "chapter" and \
            [key for key, value in id_map.items()
             if value == (position[0] + 1, None, None)]:
            exists = True
        elif level == "sequential" and \
            [key for key, value in id_map.items()
             if value == (position[0], position[1] + 1, None)]:
            exists = True
        elif level == "vertical" and \
            [key for key, value in id_map.items()
             if value == (position[0], position[1], position[2] + 1)]:
            exists = True
    elif relative == "father":
        if level == "chapter":
            pass
        else:
            exists = True
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    elif relative == "children":
        if level == "vertical":
            pass
        elif level == "chapter" and \
            [key for key, value in id_map.items()
             if value == (position[0], 0, None)]:
            exists = True
        elif level == "sequential" and \
            [key for key, value in id_map.items()
             if value == (position[0], position[1], 0)]:
            exists = True
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    elif relative == "left uncle":
        if level == "chapter":
            pass
        elif level == "sequential" and \
            [key for key, value in id_map.items()
             if value == (position[0] - reach, None, None)]:
            exists = True
        elif level == "vertical" and \
            [key for key, value in id_map.items()
             if value == (position[0], position[1] - reach, None)]:
            exists = True
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    elif relative == "right uncle":
        if level == "chapter":
            pass
        elif level == "sequential" and \
            [key for key, value in id_map.items()
             if value == (position[0] + reach, None, None)]:
            exists = True
        elif level == "vertical" and \
            [key for key, value in id_map.items()
             if value == (position[0], position[1] + reach, None)]:
            exists = True
    return exists


def get_relative_influencer(relative, position):
    """

    Args:
        relative:
        position (tuple):
            position of current video

    Returns:
        influencer_relative (influencer):

    Examples:
        >>>get_relative_influencer("left_brother", (8, 2, 8))

    """
    influencer_relative = None
    level = "vertical"
    if position[1] is None:
        level = "chapter"
    elif position[2] is None:
        level = "sequential"
    # -----------------------
    if check_influencer_exists(relative, position):
        if relative == "left_brother":
            if level == "chapter":
                influencer_relative = \
                    Influencer.get_instances()[[key for key, value in
                                                id_map.items()
                                                if value == (position[0] - 1,
                                                             None,
                                                             None
                                                             )
                                                ][0]]
            elif level == "sequential":
                influencer_relative = \
                    Influencer.get_instances()[[key for key, value in
                                                id_map.items() if
                                                value == (position[0],
                                                          position[1] - 1,
                                                          None
                                                          )
                                                ][0]]
            elif level == "vertical":
                influencer_relative = \
                    Influencer.get_instances()[[key for key, value in
                                                id_map.items() if
                                                value == (position[0],
                                                          position[1],
                                                          position[2] - 1
                                                          )
                                                ][0]]
        elif relative == "right_brother":
            if level == "chapter":
                    influencer_relative = \
                        Influencer.get_instances()[[key for key, value in
                                                    id_map.items() if
                                                    value == (position[0] + 1,
                                                              None,
                                                              None
                                                              )
                                                    ][0]]
            elif level == "sequential":
                influencer_relative = \
                    Influencer.get_instances()[[key for key, value in
                                                id_map.items() if
                                                value == (position[0],
                                                          position[1] + 1,
                                                          None
                                                          )
                                                ][0]]
            elif level == "vertical":
                influencer_relative = \
                    Influencer.get_instances()[[key for key, value in
                                                id_map.items() if
                                                value == (position[0],
                                                          position[1],
                                                          position[2] + 1
                                                          )
                                                ][0]]
        elif relative == "father":
            if level == "sequential":
                influencer_relative = \
                    Influencer.get_instances()[[key for key, value in
                                                id_map.items() if
                                                value == (position[0],
                                                          position[1] + 1,
                                                          None
                                                          )
                                                ][0]]
            elif level == "vertical":
                influencer_relative = \
                    Influencer.get_instances()[[key for key, value in
                                                id_map.items() if
                                                value == (position[0],
                                                          position[1],
                                                          position[2] + 1
                                                          )
                                                ][0]]
        elif relative == "children":
            print('enter lol ')
            if level == "sequential":
                children = [candidate_child_pos for candidate_child_pos
                            in id_map.values()
                            if candidate_child_pos[0] == position[0]
                            and candidate_child_pos[1] == position[1]
                            and candidate_child_pos[2] is not None
                            ]
                if children:
                    influencer_relative = children
            if level == "chapter":
                children = [candidate_child_pos for candidate_child_pos
                            in id_map.values()
                            if candidate_child_pos[0] == position[0]
                            and candidate_child_pos[1] is not None]
                print('enter')
                if children:
                    influencer_relative = children
                    print('ok')
    return influencer_relative


def left_slider(position, k):
    """slider returns position (id tuple) of hypothetic brother of current.

    Args:
        position:
        k:

    Returns:

    """
    slided_position = tuple()
    level = "vertical"
    if position[1] is None:
        level = "chapter"
    elif position[2] is None:
        level = "sequential"
    # -----------------------
    if level == "vertical":
        slided_position = (position[0], position[1], position[2] - k)
    elif level == "sequential":
        slided_position = (position[0], position[1] - k, None)
    elif level == "chapter":
        slided_position = (position[0] - k, None, None)
    return slided_position


def right_slider(position, k):
    """slider returns position (id tuple) of hypothetic brother of current.

    Args:
        position:
        k:

    Returns:

    """

    slided_position = tuple()
    level = "vertical"
    if position[1] is None:
        level = "chapter"
    elif position[2] is None:
        level = "sequential"
    # -----------------------
    if level == "vertical":
        slided_position = (position[0], position[1], position[2] + k)
    elif level == "sequential":
        slided_position = (position[0], position[1] + k, None)
    elif level == "chapter":
        slided_position = (position[0] + k, None, None)
    return slided_position


def up_slider(position, k):  # k max is 2, min is 1
    """positions (id tuple) of hypothetic father of current.

    Args:
        position:
        k:

    Returns:

    """
    try:
        if k > 2:
            raise ValueError("k can't be more than 2 because verticals have "
                             "father"
                             "and grandfather at most")
    except ValueError:
        pass
    slided_position = position
    level = "vertical"
    if position[1] is None:
        level = "chapter"
    elif position[2] is None:
        level = "sequential"
    # -----------------------
    if k == 1:
        try:
            if level == "chapter":
                raise ValueError("chapter can't have father.")
        except ValueError:
            pass
        if level == "vertical":
            slided_position = (position[0], position[1], None)
        elif level == "sequential":
            slided_position = (position[0], None, None)
    if k == 2:
        try:
            if level == "chapter":
                raise ValueError("chapter can't have grandfather.")
            elif level == "sequential":
                raise ValueError("sequential can't have grandfather.")
        except ValueError:
            pass
        if level == "vertical":
            slided_position = (position[0], None, None)
    return slided_position


def down_slider(position, k):
    """

    Args:
        position:
        k:

    Returns:

    """
    pass


def RBI(n, parameters, video_id=one_vid_id):
    """

    Args:
        n:
        parameters:
        video_id:
    Returns:

    """
    current = []
    vid_id = ""
    for influencer in Influencer.get_instances():
        # -----------------
        # Get id of video :
        # -----------------
        if influencer.right_brother and influencer.left_brother:
            vid_id = influencer.id
            # --------------------------------------------------------
            # from these influencers the recursive ones will be built:
            # --------------------------------------------------------
            current.append(Influencer.get_instances()[vid_id].left_brother)
            current.append(Influencer.get_instances()[vid_id].right_brother)
            current.append(Influencer.get_instances()[vid_id].father)
    while n:
        for current_influencer in current:
            cur_inflncr_pos = id_map[vid_id]
            # -------------
            # Left brother:
            # -------------
            right_brother = current_influencer
            for k in range(parameters["left_brothers"]["how_many"]):  # "all" will be translated to a number in paramaters
                if check_id_exists("left_brother",  # it's check id exist here
                                   left_slider(cur_inflncr_pos, k)
                                   ) \
                    and not check_influencer_exists("left_brother",
                                                    left_slider(cur_inflncr_pos,
                                                                k)
                                                    ):
                    # there is a vacant brother in id_map, we can create an
                    # influencer
                    left_brother_id = [key for key, value in id_map.items()
                                       if value == left_slider(cur_inflncr_pos,
                                                               k)
                                       ][0]
                    left_brother_string = string_map[left_brother_id]
                    left_brother = Influencer(left_brother_string,
                                              left_brother_id,
                                              None,
                                              right_brother,
                                              None,
                                              None,
                                              parameters["left_brothers"][
                                                  "influence"]
                                              )
                    # ----------------
                    # Relatives update:
                    # ----------------
                    # check if newly created influencer has left brother:
                    if check_influencer_exists("left_brother",
                                               left_slider(cur_inflncr_pos,
                                                           k)
                                               ):
                        # if so, relative update:
                        Influencer.get_instances()[left_brother_id
                                                   ].left_brother = \
                            get_relative_influencer("left_brother",
                                                    # is the left brother of
                                                    # left brother ...
                                                    left_brother_id  # is
                                                    # current left brother
                                                    )
                    # also check if newly created influencer has children:
                    left_brother.children += \
                        get_relative_influencer("children", left_brother_id)
                    right_brother = left_brother
            # --------------
            # Right brother:
            # --------------
            left_brother = current_influencer
            for k in range(parameters["right_brothers"]["how_many"]):
                if check_id_exists("right_brother",  # it's check id exist here
                                   right_slider(cur_inflncr_pos, k)
                                   ) \
                    and not check_influencer_exists("right_brother",
                                                    right_slider(
                                                        cur_inflncr_pos, k)
                                                    ):
                    # there is a brother in id_map, we can create an influencer
                    right_brother_id = [key for key, value in id_map.items()
                                        if value == right_slider(
                            cur_inflncr_pos, k)][0]
                    right_brother_string = string_map[right_brother_id]
                    right_brother = Influencer(right_brother_string,
                                               right_brother_id,
                                               left_brother,
                                               None,
                                               None,
                                               None,
                                               parameters["right_brothers"][
                                                   "influence"]
                                               )
                    # -----------------
                    # Relatives update:
                    # -----------------
                    # check if newly created influencer has right brother:
                    if check_influencer_exists("right_brother",
                                               right_brother_id
                                               ):
                        # if so, create corresponding influencer
                        Influencer.get_instances()[right_brother_id
                                                   ].right_brother = \
                            right_brother = \
                            get_relative_influencer("right_brother",
                                                    right_brother_id
                                                    )
                    # also check if newly created influencer has children:
                    right_brother.children += get_relative_influencer(
                        "children", right_brother_id)
                    left_brother = right_brother
            # -------
            # Father:
            # -------
            child = current_influencer
            for k in range(parameters["fathers"]["how_many"]):  # "all" will be translated to a number in paramaters
                if check_id_exists("father",  # it's check id exist here
                                   up_slider(cur_inflncr_pos, k)
                                   ) \
                    and not check_influencer_exists("father",
                                                    up_slider(cur_inflncr_pos,
                                                              k)
                                                    ):
                    # there is a vacant father in id_map, we can create an
                    # influencer
                    father_id = [key for key, value in id_map.items()
                                 if value == up_slider(cur_inflncr_pos,
                                                       k)
                                 ][0]
                    father_string = string_map[father_id]
                    # creation of new influencer:
                    father = Influencer(father_string,
                                        father_id,
                                        None,
                                        None,
                                        None,
                                        [child],
                                        parameters["father"][
                                            "influence"]
                                        )
                    # ----------------
                    # Relatives update:
                    # ----------------
                    # check if newly created influencer has left brother:
                    if check_influencer_exists("left_brother", father_id):
                        # if so, relative update:
                        Influencer.get_instances()[father_id].left_brother = \
                            get_relative_influencer("left_brother", father_id)
                    # check if newly created influencer has right brother:
                    if check_influencer_exists("right_brother", father_id):
                        # if so, relative update:
                        Influencer.get_instances()[father_id].right_brother = \
                            get_relative_influencer("right_brother", father_id)
                    # also check if newly created influencer has children:
                    if check_influencer_exists("children", father_id):
                        father.children += get_relative_influencer("children",
                                                                   father_id)
                    # also check if newly created influencer has father:
                    if check_influencer_exists("father", father_id):
                        father.father = get_relative_influencer("father",
                                                                father_id)
                    child = father
            # -----------
            # Left uncle:
            # -----------
            for k in range(parameters["left uncles"]["how_many"]):
                if check_id_exists("left uncle",  # it's check id exist here
                                   up_slider(cur_inflncr_pos, k)
                                   ) \
                    and not check_influencer_exists("father",
                                                    up_slider(cur_inflncr_pos,
                                                              k)
                                                    ):
                    pass
                

    n -= 1

# ******************************************************************************
# NEED FOR GOOD COMPARISON ALGORITHM.
# ASSOCIATE ALL FUNCTIONS TO GUI. FIRST, THE TREE. THEN, COMMIT OF BLOCK
# SELECTION. THEN, COMMIT OF VIDEO UNDER SCRUTINY AND GET OF CONCEPTS.
# THEN, PARAMETERS FOR RBI. THEN, SPECIFIC INFLUENCERS.
# ******************************************************************************
