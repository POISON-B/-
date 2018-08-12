#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-9 下午10:27
# @Author  : Shark
# @File    : uilt.py
# @Software: PyCharm


def is_isbn_or_key(word):
    """
    搜索关键字判断
    :param word:搜索关键字
    :return: isbn 或 书名
    """
    sbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'
        return isbn_or_key

    short_q = word.replace('-', '')
    if '-' in word and len(short_q) == 10 and short_q.isdigit():
        isbn_or_key = 'isbn'

        return isbn_or_key
    return sbn_or_key
