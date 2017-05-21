# -*- coding: utf-8 -*-
import sys
import os
import codecs
import traceback
from xml.sax.saxutils import unescape

import untangle

from util import *


def extractXmlFile(filename):
    # with codecs.open(filename, "r", encoding="utf-16-be") as f:
    #     content = f.read()
    # obj = untangle.parse(content)

    obj = untangle.parse(filename)
    weibo_list = obj.Result.weibo
    comment_list = []
    sentiment_list = []
    for weibo in weibo_list:
        for sentence in weibo.sentence:
            cdata = unescape(sentence.cdata, {"&apos;": "'", "&quot;": '"'})
            # token_list = text2token(cdata.encode('UTF-8'))
            #
            # if len(token_list) == 0:
            #     print "Current weibo doesn't have valid tokens, content is {}".format(cdata.encode('UTF-8'))

            comment_list.append(cdata)
            if sentence["opinionated"] != "Y":
                # drop sentences which opinion are N
                sentiment_list.append(3)
            else:
                if sentence["polarity"] == "POS":
                    sentiment_list.append(1)
                elif sentence["polarity"] == "NEG":
                    sentiment_list.append(0)
                else:
                    # OTHER
                    sentiment_list.append(2)

    return comment_list, sentiment_list


if __name__ == '__main__':
    fileNames = getFiles("../dataset/test")
    # fileNames = ["dataset/raw/jiu_lin_hou_dang_jiao_shou.xml"]
    comment_list = []
    sentiment_list = []
    for fileName in fileNames:
        (comment, sentiment) = extractXmlFile(fileName)
        comment_list += comment
        sentiment_list += sentiment
    print len(comment_list)

    with open("12_result.txt", "wb") as f:
        for i in range(len(comment_list)):
            content = comment_list[i]
            f.write("{}|{}\n".format(content.encode('utf-8'), sentiment_list[i]))

    print 'hello'

