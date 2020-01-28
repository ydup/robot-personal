# -*- coding: utf-8 -*-

"""
Created by Wang Han on 2020/1/28 17:10.
E-mail address is hanwang.0501@gmail.com.
Copyright © 2018 Wang Han. SCU. All Rights Reserved.
"""
import os

import pytesseract
from PIL import Image
from snownlp import SnowNLP


class Image2Title:
    def __init__(self, topK=5):
        self.topK = topK

    def __preprocessing(self, text):
        # 去除空格
        text = text.replace(" ", "")
        # 去除换行符
        text = text.replace("\n", "")
        # 去除引号
        text = text.replace("\"", "").replace("\'", "").replace("“", "").replace("”", "")
        return text

    def __call__(self, image_path):
        assert not os.path.exists(image_path), "The image does not exist!"

        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='chi_sim')
        text = self.__preprocessing(text)
        s = SnowNLP(text)
        topK_titles = s.summary(self.topK)

        return topK_titles


if "__main__" == '__main__':
    from urllib.request import quote
    import requests
    from src.util.parse_jsonp import loads_jsonp

    ocr = Image2Title()
    topK_titles = ocr("/Users/wanghan/Desktop/test2.jpeg")
    for idx, title in enumerate(topK_titles):
        print("title No.{}: {}".format(idx, title))
        url = "https://vp.fact.qq.com/searchresult?title={}&num=0&_=1580200136791&callback=jsonp1".format(quote(title))
        response = requests.get(url)
        res = loads_jsonp(response.text)
        print(res)
        print("*" * 10)
