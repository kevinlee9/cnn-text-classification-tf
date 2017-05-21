# -*- coding: utf-8 -*-

import os
import re
import jieba
import jieba.posseg as posseg
import inspect
import logging

logger = logging.getLogger(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))
# fn = "stopwords.txt"
fn = "punctuation.txt"

stopwords = set()
with open(os.path.join(dir_path,fn), 'r') as f:
    for line in f.xreadlines():
        word = line.strip().decode('utf8','ignore')
        if word == '':
            continue
        stopwords.add(word)

# todo: train a new model to cut sentence
def cut_sentence(para):
    #words = (words).decode('utf8') 如果是从编码为 utf8 的 txt 文本中直接输入的话，需要先把文本解码成 unicode 来处理
    start = 0
    i = 0  #记录每个字符的位置
    sents = []
    # punt_list = ',.!?:;~，。！？：；～'.decode('utf8')  #string 必须要解码为 unicode 才能进行匹配
    punt_list = '.!?;~。！？；～'.decode('utf8')  #string 必须要解码为 unicode 才能进行匹配
    for word in para:
        if word in punt_list:
            sents.append(para[start:i+1])
            start = i + 1  #start标记到下一句的开头
            i += 1
        else:
            i += 1  #若不是标点符号，则字符位置继续前移
    if start < len(para):
        sents.append(para[start:])  #这是为了处理文本末尾没有标点符号的情况
    return sents


# not use
#先过滤掉文本中的数字,同时保留词间的空格和换行符
def is_ustr(in_str):
    out_str=''
    for i in range(len(in_str)):
        if is_uchar(in_str[i]):
            out_str=out_str+in_str[i]
        # else:
        #     out_str=out_str+' '
    return out_str

# not use
def is_uchar(uchar):

    #判断一个unicode是否是汉字
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            return True
    #判断一个unicode是否是数字,是数字则过滤掉
    if uchar >= u'\u0030' and uchar<=u'\u0039':
            return False
    #判断一个unicode如果是英文字母，则过滤掉
    if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
            return False
    if uchar in ('\n', ' '):
            return True
    return False


# not use
def remove_nonchn(content):
    return is_ustr(content)


# def remove_stopwords(content):
#     sent = re.sub("[（\(\[].*?[）\)\]]".decode('utf8'), "".decode('utf-8'), content) # remove brackets
#     words = [word for word in jieba.cut(sent) if word not in stopwords and word != ' ']
#     return words


def splitWords(sent):
    # stopwords = readStopwords('stopwords.txt')
    # todo: pattern prob
    # sent = re.sub("[（\(\[].*?[）\)\]]".decode('utf8'), "".decode('utf-8'), sent) # remove brackets
    words = [word for word in jieba.cut(sent) if word not in stopwords and word != ' ']
    return words


# todo: do precisely removing. This pattern remove to much
def remove_punctuation(content):
    return re.sub("[+\.\!\/_,$%‰^*()+\"\'\-\]\[\{\}]+|[+——！，。？?、~@#￥%……&*:;：；·”“`【】‘’《》<>（〔1234567890〕）*^@!|=]+".decode('utf-8'),
                           "".decode('utf-8'), content)


# todo: add parse for xml, thinking about interface
def ext_content_from_line(line):
    items = line.split(u'\t')
    if len(items) != 3:
        raise Exception("the processing line doesn't has three items")
    return items[2]


# no tested
def strQ2B(ustring):
    """把字符串全角转半角"""
    ustring = ustring.decode('utf-8')
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            inside_code = 0x0020
        else:
            inside_code -= 0xfee0
        if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符则返回原来的字符
            rstring += uchar.encode('utf-8')
        else:
            rstring += (unichr(inside_code)).encode('utf-8')
    return rstring


def check_empty_token(token, pos):
    if token == " ".decode("utf-8"):
        return True
    else:
        return False


def check_puncutation_token(token, pos):
    if remove_punctuation(token) == "".decode("utf-8"):
        return True
    else:
        return False


def check_valid_pos(token, pos):
    logger.debug((u"{}:{}".format(token, pos)).encode('utf-8'))
    # if pos[0] in [u'a', u'd', u'v', u'o', u'z', u'l', u'i']:
    if pos[0] in [u'a', u'd', u'v', u'o', u'z', u'l', u'i', u'n']:
        return False
    else:
        return True


filter_funcs_default = [check_empty_token, check_puncutation_token]


# input type: unicode, utf-8
# output type: unicode
def text2tokens(sentence, plain=True, filter_funcs=None):
    tokens = posseg.cut(sentence)
    tokened_sentence = []

    if filter_funcs:
        filter_funcs = filter_funcs_default + filter_funcs
    else:
        filter_funcs = filter_funcs_default

    # remove punctuation, stop words, invalid words
    for token, pos in tokens:
        for filter_func in filter_funcs:
            # argspec = inspect.getargspec(filter_func)
            # if len(argspec.args) != 2:
            #     raise Exception("invalid filter function")

            if filter_func(token, pos):
                break

        else:
            # keeped items
            if plain:
                tokened_sentence.append(token)
            else:
                tokened_sentence.append(Token(token, pos))

    return tokened_sentence


class Token:
    def __init__(self, content, pos):
        self.content = content
        self.pos = pos

    def __str__(self):
        return (u"{}:{}".format(self.content, self.pos)).encode('utf-8')

if __name__ == '__main__':
    pass
