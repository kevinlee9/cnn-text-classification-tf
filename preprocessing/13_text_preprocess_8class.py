# -*- coding: utf-8 -*-
import sys
import os
import codecs
import traceback
from xml.sax.saxutils import unescape

import untangle


def getFiles(directoryName):
    fileNames = []
    getFilesIter(directoryName, fileNames)
    return fileNames


# return file names
def getFilesIter(directoryName, item_list):
    if not os.path.isdir(directoryName):
        raise Exception("directory is not found")
    for item in list_dir(directoryName):
        item = os.path.join(directoryName, item)
        if os.path.isdir(item):
            getFilesIter(item, item_list)
        else:
            item_list.append(item)


def list_dir(directoryName):
    raw_list = os.listdir(directoryName)
    try:
        out_list = sorted(raw_list, key=int)
    except Exception as e:
        out_list = raw_list
    return out_list


class EmotionCheck:
    emotion_dict = {
        u'愤怒': 0,
        u'厌恶': 1,
        u'恐惧': 2,
        u'悲伤': 3,
        u'高兴': 4,
        u'喜好': 5,
        u'惊讶': 6,
        u'': 7
    }

    def __init__(self):
        pass

    @staticmethod
    def get_emotion_type(emotion):
        if isinstance(emotion, unicode):
            if emotion in EmotionCheck.emotion_dict:
                emotion_type = EmotionCheck.emotion_dict[emotion]
            else:
                raise Exception("input {} is not a valid emotion type".format(emotion.encode('utf-8')))
            return emotion_type
            if emotion_type == 7:
                return 2
            if emotion_type > 3:
                return 1
            else:
                return 0

        else:
            raise Exception("input {} is not unicode".format(emotion))


def extractXmlFile(filename):
    # with codecs.open(filename, "r", encoding="utf-16-be") as f:
    #     content = f.read()
    # obj = untangle.parse(content)

    obj = untangle.parse(filename)
    weibo_list = obj.TestingData.weibo
    comment_list = []
    sentiment_list = []
    for weibo in weibo_list:
        weibo_id = int(weibo['id'])
        for sentence in weibo.sentence:
            sentence_id = int(sentence['id'])
            cdata = unescape(sentence.cdata, {"&apos;": "'", "&quot;": '"'})

            comment_list.append(cdata)
            if sentence["opinionated"] != "Y":
                # drop sentences which opinion are N
                sentiment_list.append(8)
            else:
                emotion = sentence["emotion-1-type"]
                try:
                    sentiment = EmotionCheck.get_emotion_type(emotion)
                except Exception as e:
                    print "weibo {} sentence {} error: {}".format(weibo_id, sentence_id, str(e))
                sentiment_list.append(sentiment)

    return comment_list, sentiment_list


if __name__ == '__main__':
    # reload(sys)
    # sys.setdefaultencoding('utf-8')

    fileNames = getFiles("../dataset/13")
    # fileNames = ["dataset/raw/jiu_lin_hou_dang_jiao_shou.xml"]
    comment_list = []
    sentiment_list = []
    for fileName in fileNames:
        (comment, sentiment) = extractXmlFile(fileName)
        comment_list += comment
        sentiment_list += sentiment
    print len(comment_list)

    with open("13.8class.txt", "wb") as f:
        for i in range(len(comment_list)):
            content = comment_list[i]
            f.write("{}|{}\n".format(content.encode('utf-8'), sentiment_list[i]))

    print 'hello'

