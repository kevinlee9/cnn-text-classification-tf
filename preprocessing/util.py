# -*- coding: utf-8 -*-

import os
import preprocess


def text2tokens(content):
    return preprocess.splitWords(content)


def process_tfile(file_name):
    with open(file_name) as f:
        i = 0
        empty_num = 0
        for line in f:
            i += 1
            line = line.decode("utf-8")
            items = line.strip().split(u"|")

            # for case which contains "|" in content
            tokens = text2tokens(u"|".join(items[:-1]))
            if len(tokens) == 0:
                print "line {} has 0 valid tokens, content is {}".format(str(i), line.encode("utf-8"))
                empty_num += 1
            yield tokens
        print empty_num


# scrawled weibo file
def process_cfile(file_name):
    with open(file_name) as f:
        i = 0
        empty_num = 0
        for line in f:
            i += 1
            line = line.decode("utf-8")
            items = line.strip().split(u",")
            tokens = text2tokens(u','.join(items[1:]))
            if len(tokens) == 0:
                print "line {} has 0 valid tokens, content is {}".format(str(i), line.encode("utf-8"))
                empty_num += 1
            yield tokens
        print empty_num


def process_label(file_name):
    with open(file_name) as f:
        for line in f:
            line = line.decode("utf-8")
            items = line.strip().split(u"|")
            yield items[-1]


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

if __name__ == "__main__":
    pass

