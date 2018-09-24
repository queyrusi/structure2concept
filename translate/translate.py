#!/usr/bin/python
#  -*- coding: utf-8 -*-

"""Translation module"""

import httplib2
import hashlib
import urllib.parse
import random
import json

appid = '20180720000187326'
secretKey = 'OSKCkOaJ42PGRSKQNAyr'


def zh2lang(q, lang='en'):
    """Translates given chinese word/sentence to input language.

    API: Baidu fanyi

    Args:
        q (str): chinese word to be translated
        lang (str): language for the word to be translated into

    Returns:
        result (str): translated word

    """
    # Could use translation database prior to API

    # try:
    #     if xiaomu is not None and lang == 'en':
    #         answer_dict = xiaomu.translation.find_one({"zh": q})
    #         print("passe par xiaomu")
    #         return answer_dict["en"]
    # except ValueError as e:
    #     pass

    print("THE QUERIE IS", q)
    myurl = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    from_lang = 'zh'
    to_lang = lang
    if type(q) == list:
        print("ON A UNE LISTE")
        stringed_list = str(q)
        stringed_list = stringed_list[1: -1]
        result = zh2lang(stringed_list)
    else:
        print("ON A Un STRING")
        salt = random.randint(32768, 65536)
        sign = appid + q + str(salt) + secretKey
        sign = sign.encode("utf-8")
        m1 = hashlib.md5()
        m1.update(sign)
        sign = m1.hexdigest()
        myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
            q) + '&from=' + from_lang + '&to=' + to_lang + '&salt=' + str(
            salt) + '&sign=' + sign
        h = httplib2.Http('.cache')
        httplib2.debuglevel = 0
        response, content = h.request(myurl)
        js = json.loads(content)
        result = js['trans_result'][0]['dst']
    return result
