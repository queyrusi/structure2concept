#!/usr/bin/python
#  -*- coding: utf-8 -*-

"""Translation module"""

import httplib2
import hashlib
import urllib.parse
import random
import json
import tools as tl

appid = '20180720000187326'
secretKey = 'OSKCkOaJ42PGRSKQNAyr'

final = ''
flag_first_half = False
flag_second_half = False
flag_end = False


def big_zh2lang(q, lang='en'):
    """Translates given chinese word/sentence to input language.

    API: Baidu fanyi

    :param q: (str) chinese word to be translated
    :param lang: (str) language for the word to be translated into
    :return: (str) translated word

    """
    global final
    global flag_first_half
    global flag_second_half
    global flag_end
    # --------------------------------------------------------------------------
    # Could use translation database prior to API
    #
    # try:
    #     if xiaomu is not None and lang == 'en':
    #         answer_dict = xiaomu.translation.find_one({"zh": q})
    #         return answer_dict["en"]
    # except ValueError as e:
    #     pass
    # --------------------------------------------------------------------------
    print("THE QUERIE IS", q)
    myurl = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    from_lang = 'zh'
    to_lang = lang
    if type(q) == list and not flag_first_half:
        print("ON A UNE LISTE")
        stringed_list = str(q)
        stringed_list = stringed_list[1: -1]
        occ = tl.various.find_occurrences(stringed_list, " ")
        print(occ)
        print(int(len(occ) / 2 + 1))
        i = occ[int(len(occ) / 2 + 1)]
        global first_half
        first_half = stringed_list[: i]
        global second_half
        second_half = stringed_list[i:]
        flag_first_half = True
        final = big_zh2lang(first_half)
    else:
        print("ON A Un STRING", q)
        salt = random.randint(32768, 65536)
        print("q est de type", type(q))
        sign = appid + q + str(salt) + secretKey
        sign = sign.encode("utf-8")
        m1 = hashlib.md5()
        m1.update(sign)
        sign = m1.hexdigest()
        print("Q VAUT", q)
        myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
            q) + '&from=' + from_lang + '&to=' + to_lang + '&salt=' + str(
            salt) + '&sign=' + sign
        try:
            h = httplib2.Http('.cache')
            httplib2.debuglevel = 0
            response, content = h.request(myurl)
            js = json.loads(content)
            result = js['trans_result'][0]['dst']
            if flag_first_half and not flag_second_half:
                print("1", flag_first_half, flag_second_half)
                print("SECOND HALF", second_half)
                final += result
            if not flag_second_half and (second_half is not None):
                print("2", flag_first_half, flag_second_half)
                flag_second_half = True
                big_zh2lang(second_half)
            if flag_second_half and not flag_end:
                print("3", flag_first_half, flag_second_half)
                final += result
                flag_end = True
            return final
        except ValueError:
            pass
    return final
