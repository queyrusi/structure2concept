import translate as tr
import translate.big_translate as btr
import tools as tl
import tools.datamuse_seek as muse
import jieba
import copy
import codecs
import json


# config
vids_ids_path = "./un_Pool_BSC/all_vids_ids.txt"
cat_profile_path = "./kp/cat_profile/"
stop_categories_path = "./kp/stop_categories.csv"
relations_path = "./kp/article_categories_en.txt"
blocks_path = "./un_Pool_BSC/course-v1%3ATsinghuaX+40250074X+sp_blocks"


# 0 -- SETTING UP
# ================

# with open(relations_path) as dump:  # ACHTUNG /!\
#     relations = [lines for lines in dump]
#     relations = relations[1:]

# index = tl.build_index()    # ----> to be run on server
index = {'a': 0,
         'b': 4628,
         'c': 2790,
         'd': 471,
         'e': 607,
         'f': 543,
         'g': 1981,
         'h': 1799,
         'i': 15,
         'j': 22761,
         'k': 4442,
         'l': 24,
         'm': 1032,
         'n': 2023,
         'o': 8255,
         'p': 765,
         'q': 38796,
         'r': 2056,
         's': 4004,
         't': 766,
         'u': 5494,
         'v': 10443,
         'w': 14657,
         'y': 21497,
         'z': 16645}


def load_blocks(filename=blocks_path):
    """Loads the blocks from which subtitles will be drawn, and from which we
     find associated chapter, sequential & vertical names.

    Args:
        filename (str): json blocks of required format (blocks can be found at

    Returns:
        (list) list of every block in a chapter

    """
    with codecs.open(filename, 'r', 'utf8') as file:
        return json.loads(file.read())


# blocks = load_blocks()


def get_associated_ids(all_blocks, video_id=""):
    """Returns dict associated to video_id with video subtitles, name and ID +
    all associated names and IDs.

    Args:
        video_id (str): id of video under scrutiny
        all_blocks: list of every block associated to a chapter containing video
            under scrutiny

    Returns:
        video_ids (dict): every id associated to video under scrutiny

    """
    i = 0
    while not all_blocks[i].get("block_id") == video_id:
        i += 1
    block = all_blocks[i]
    video_ids = {"video_name": block["video_name"],
                 "video_id": block["video_id"],
                 "chapter_name": block["chapter_name"],
                 "chapter_id": block["chapter_id"],
                 "sequential_name": block["sequential_name"],
                 "sequential_id": block["sequential_id"],
                 "vertical_name": block["vertical_name"],
                 "vertical_id": block["vertical_id"],
                 "subs": block["text"]
                 }
    return video_ids


# 1 -- PROCESSING
# ================


def clean_ids(ids):
    """ Cleans chapter, sequential and vertical names of dict argument according
    to my_cleaner object's input cleaning rules.

    Args:
        ids (dict): should be given in following format :

                        {"video_name": block["video_name"],
                         "video_id": block["video_id"],
                         "chapter_name": block["chapter_name"],
                         ...
                         "vertical_name": block["vertical_name"],
                         "vertical_id": block["vertical_id"],
                         "subs": block["text"]
                         }

    Returns:
        None
    """
    my_cleaner = tl.Cleaner("word", "parenthesis", "chapter_header",
                            "dots", "andword_split")
    ids["video_name"] = my_cleaner.clean(ids["video_name"])
    ids["chapter_name"] = my_cleaner.clean(ids["chapter_name"])
    ids["sequential_name"] = my_cleaner.clean(ids["sequential_name"])
    ids["vertical_name"] = my_cleaner.clean(ids["vertical_name"])
    return


# video_dict = get_associated_ids("f4d2dfd663054221933e7c849a215a59")
# print("\n ORIGINAL DICT \n", video_dict)
# clean_ids(video_dict)
# print("\n CLEANED DICT \n", video_dict)


def translate_ids(ids, lang='en'):
    """Translates chinese names of video dictionary to input language.

    Args:
        ids (dict):
        lang (str): language for the names to be translated into

    Returns:
        None

    """
    ids["video_name"] = tr.zh2lang(ids["video_name"], lang)
    ids["chapter_name"] = tr.zh2lang(ids["chapter_name"], lang)
    ids["sequential_name"] = tr.zh2lang(ids["sequential_name"], lang)
    ids["vertical_name"] = tr.zh2lang(ids["vertical_name"], lang)
    return



# translate_ids()
# print("\n TRANSLATED DICT \n", video_dict)


def add_concepts(ids):
    """Extracts grams from subs of input dict and adds them to the dict with
    key name 'concepts'.

    Package used: Jieba

    Args:
        ids (dict):

    Returns:
        None

    """
    ids['concepts'] = ["/".join(jieba.cut(sentence, cut_all=False))
                       for sentence in ids['subs']]
    return


# add_concepts()
# del video_dict['subs']  # careful: mutates the dict
# print("video dict purgé \n \n \n \n", video_dict)


def gram_b2w_slashes(line, ids):
    """Quick generator to yield grams between slashes.

    Args:
        line:
        ids (dict):

    Yields:

    """
    occ = tl.find_occurrences(ids['concepts'][line], '/')
    if not occ:
        yield ''
    else:
        yield ids['concepts'][line][: occ[0]]
        for i in range(0, len(occ) - 1):
            yield ids['concepts'][line][occ[i] + 1: occ[i + 1]]
        yield ids['concepts'][line][occ[-1] + 1:]
    return


def concepts_in_list(ids):
    """Puts all concepts into one list, deletes redundant words.

    Args:
        ids (dict):

    Returns:
        None
    """
    gram_list = []
    for line in range(len(ids['concepts'])):
        for gram in gram_b2w_slashes(line, ids):
            if not gram == '' and not gram == ' ':
                gram_list.append(gram)
    gram_list = tl.without_redundant(gram_list)
    ids.update({'concepts': gram_list})
    return


# concepts_in_list()

# -----------------------
# processing of concepts:
# -----------------------

def remove_stopwords(ids):
    """Removes stopwords from extracted concepts. Removes blanks ' /' and digits
    as well. Removes special characters

    Args:
        ids:

    Returns:
        ids:
    """
    with open("./kp/stop_words.txt", 'r') as wordfile:
        swords = wordfile.read()
    with open("./kp/special_characters.txt", 'r') as charfile:
        spchar = charfile.read()
    concepts = []
    for gram in ids['concepts']:
        if gram not in swords and gram not in spchar and not gram.isdigit():
            concepts.append(gram)
    ids.update({'concepts': concepts})
    return


# remove_stopwords(video_dict)
# print("\n \n \nSTOP WORDS REMOVED DICT", video_dict)


def translate_concepts(ids):
    """Translates every concept (list value of key "concepts") in input
    video_dict.

    Instead of summoning API for each word, we gather the words in one list so
    the API translates it in one shot.

    Note:
        The list containing all words is usually too long (API error)
        so tr.zh2lang() systematically splits the list in half before sending
        request.

    Args:
        ids:

    Returns:
        ids:

    """
    global translated_concepts
    translated_concepts = btr.big_zh2lang(ids["concepts"])
    print("TRANSLATED CONCEPTS PLEASE", translated_concepts)
    global L
    L = []

    def translated_concepts_process(tc=translated_concepts):
        global L
        print("\n \n \nLISTE VIDE \n \n \n", L)
        print("\n la liste l vaut \n:", tc)
        cleaner = tl.Cleaner("special_char", "outer_spaces")
        try:
            comma_index = tc.index(",")
            concept = tc[:comma_index]
            tc = tc[comma_index + 1:]
            while tc[0] == ' ':
                tc = tc[1:]
            concept = cleaner.clean(concept)
            print("\n \n \n ON APPEND LE CNCEPT\n ", concept)
            L.append(concept)
            L = tl.various.remove_parasites(L)  # in case concept is ''
            translated_concepts_process(tc)
        except ValueError:
            L.append(cleaner.clean(tc[0]))  # last element of the list
            L = tl.various.remove_parasites(L)  # in case last element is ''
            return tl.without_redundant(L)  # in case last element is redundant
        return tl.without_redundant(L)

    translated_concepts = translated_concepts_process()
    ids.update({'concepts': translated_concepts})
    return


# translate_concepts(video_dict)
# print("\n \n \nTRANSLATED CONCEPTS", video_dict)

# -----------------------------
# final processing of concepts:
# -----------------------------

def add_underscores(ids):
    """Adds underscores in spaces of elements within ids["concepts"] and titles
    as well so they can be parsed in dbpedia.

    Args:
        ids:

    Returns:
        None
    """
    ids["chapter_name"] = ids["chapter_name"].replace(' ', '_')
    ids["sequential_name"] = ids["sequential_name"].replace(' ', '_')
    ids["vertical_name"] = ids["vertical_name"].replace(' ', '_')
    ids["concepts"] = [concept.replace(' ', '_') for concept in ids["concepts"]]
    return


# add_underscores()

# ------------------------------------------------------------------------------
# We now have desired format for video_dict to start comparison. Let's proceed
# to extracting sub-cats.
# ------------------------------------------------------------------------------


# 2 -- SUB-CATEGORIES EXTRACTION
# ===============================


# --------------------------------------------------------
# first step is getting adequate seed by using LCS method:
# --------------------------------------------------------

def lcs(s, t):
    """Returns longest common substring of s and t.

    Slightly adapted from bogotobogo.com (K. Hong).

    Args:
        s:
        t:

    Returns:
        (list): all lcs

    Example:
        >>>lcs("Python","marathon")
        ['thon']

    """
    m = len(s)
    n = len(t)
    counter = [[0] * (n + 1)] * (m + 1)
    longest = 0
    lcs_set = set()
    for i in range(m):
        for j in range(n):
            if s[i] == t[j]:
                c = counter[i][j] + 1
                counter[i + 1][j + 1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(s[i - c + 1: i + 1])
                elif c == longest:
                    lcs_set.add(s[i - c + 1: i + 1])
    return list(lcs_set)


def get_seed(ids):
    """Returns seed based on chapter_name and available article title in dump.

    Seed comes in tuple (size 2) with line number in dump from which parsing
    should begin. This considerably increases speed of algorithm.

    Args:
        ids (dict):

    Returns:
        tple (tuple): (seed, line in dump)

    """
    line_n = 0
    r_words = []
    chapter_name = ids["chapter_name"].lower()
    for line in relations:
        if ids["chapter_name"].lower() in line[29: line.index('>')].lower() or \
               line[29: line.index('>')].lower() in ids["chapter_name"].lower():
            r_words.append((line[29: line.index('>')].lower(), line_n))
        line_n += 1
    # print("RWORD VAUT", r_words)
    list_lcs = {}
    for tple in r_words:
        if tple[0] == chapter_name:
            return tple
        candidate = tple[0].lower()
        lcstr = lcs(candidate, chapter_name.lower())[0]
        list_lcs[lcstr] = tple[0]
    # print("LISTE LCS", list_lcs)
    list_lcs = list(list_lcs)
    list_lcs.sort(key=lambda s: len(s))
    best_candidate = list_lcs[-1]
    # print("BEST CANDIDATE", best_candidate)
    for tple in r_words:
        if tple[0] == best_candidate:
            return tple


def get_subcats(video_ids_seed):
    """Gathers depth-1 sub-cats from seed.

    Args:
        video_ids_seed (tuple):

    Returns:
        subcat_list (list):

    Examples:

    """
    print("LA VIDEO_IDS_SEED VAUT", video_ids_seed)
    subcat_list = []
    cut_relations = relations[video_ids_seed[1]:]
    print(cut_relations[0])
    target_lines = [lines for lines in cut_relations
                    if lines[29: lines.index('>')].lower() ==
                    video_ids_seed[0].lower()]
    print("TARGET LINES", target_lines)
    for lines in target_lines:
        beg = lines.index("<http://dbpedia.org/resource/Category:") + 38
        # third occurrence of '>' sets border on the right side
        end = tl.find_occurrences(lines, '>')[2]
        subcat_list.append(lines[beg: end])
    return subcat_list


def get_n_depths(catlist, n):
    """Gets n-depths sub-cats list.

    Args:
        catlist (list):             [seed_1, seed_2, ...]
        n (int): depth

    Returns:
        n_depths_subcats (list):

                        SC = [[t_11, t_12, ...],  # depth-1 sub-cats
                              [t_111, t_112, ..., t_121, t_122, ..., ],
                               ... ]

    """
    global n_depths_subcats
    if type(catlist) == str:
        catlist = [catlist]
    if n == 0:
        return catlist
    nth_list = []
    if type(catlist[-1]) == str:
        target_list = copy.deepcopy(catlist)
    else:
        target_list = copy.deepcopy(catlist[-1])
    for cat in target_list:
        print("CAT VAUT", cat)
        subcats = get_subcats((cat, index[cat[0].lower()]))
        print("ON ARRIVE LA")
        for subcat in subcats:
            if len(n_depths_subcats) == 0:
                nth_list += [subcat]
            else:
                if not any(subcat in L_subc for L_subc in n_depths_subcats):
                    # print("on ajoute le subcat", subcat,
                    #       "car il n'est pas dans", n_depths_subcats)
                    nth_list += [subcat]
        nth_list = tl.without_redundant(nth_list)
    n_depths_subcats.append(nth_list)
    get_n_depths(n_depths_subcats, n - 1)
    # important step for removing empty generations:
    while [] in n_depths_subcats:
        n_depths_subcats.remove([])
    return n_depths_subcats

# ** **** **** **** **** **** **** **** **** **** **** **** **** ****
# ** **** **** **** **** **** **** **** **** **** **** **** **** ****
# ** **** **** **** **** **** **** **** **** **** **** **** **** ****


# video_dict = {}
# n_depths_subcats = []
# sc = get_n_depths(get_seed(video_dict)[0], 20)  # needless to put 30...


# 3 -- CONCEPT-SEED MATCHING/SCORING
# ===================================
# Should be interesting to consider ascendants

def build_semantics(catlist):
    """

    Args:
        catlist:

    Returns:
        (list): semantics

                [
                 [{cat1: {semantics set}}, {cat2: {semantics set}}] , #depth1
                 [ ... ], # depth 2
                 ... ]

    Examples:
        >>>build_semantics([['Greek_loanwords', 'Cybernetics'],['Evolution']])
        [[{'Greek_loanwords': set()},
          {'Cybernetics': {'advancement',
                           'animal',
                             ... }],
         [{'Evolution': {'behavior',
                         'biological',
                            ...}]]

    """
    semantics = []
    for generation in catlist:
        list_w_semantics = []
        for cat in generation:
            catw_semantics = {cat: muse.get_semantics(cat)}
            list_w_semantics.append(catw_semantics)
        semantics.append(list_w_semantics)
        print(list_w_semantics)
    return semantics


# semantics_sc = build_semantics()


def get_concept_depths(concept, n_depth_sc):
    """Gets depth in semantic sets generations of input concept drawn from
    video_dict's concepts.

    Args:
        concept (str):
        n_depth_sc (list):

    Returns:
        all_depths (list): [0, '*', 1, 0, 1, ...]

    Examples:
        >>>get_concept_depths("engineering")
        [0, 0, '*', 1, 1, 0]

    """
    all_depths = []
    for depth in range(len(n_depth_sc)):
        for generation in n_depth_sc:
            for subcat in generation:
                if any(cat_name == concept.lower()
                       for cat_name in generation[0].keys()):
                            # reward star if concept  Wiki sub-cat
                            all_depths.append('*')
                elif any(concept.lower() in s_set for s_set in subcat.values()):
                    all_depths.append(1)
                else:
                    all_depths.append(0)
    return all_depths


def g(all_depths):
    """Rating depth of a concept.

    The younger the generation of sub-cats of which semantic set the concept
    belongs to, the higher the score.

    Args:
        all_depths:

    Returns:
        score:

    Examples:
        >>>g([0, 0, '*', 1, 1, 0])
        117.5

    """
    score = 0
    print("all depths", all_depths)
    for n in range(len(all_depths)):
        if all_depths[n] == 1:
            score += 30 / (n ** 2)
        if all_depths[n] == '*':
            score += 200 / n
    return score


def all_scores(ids):
    """Provides all concept/score pairs.

    Args:
        ids (dict):

    Returns:
        scores (dict):

    """
    scores = {}
    for concept in ids["concepts"]:
        scores[concept] = g(get_concept_depths(concept, sc))
    return scores


def ressemblance():
    pass