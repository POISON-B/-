#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-9 下午11:04
# @Author  : Shark
# @File    : book_info.py
# @Software: PyCharm
import json

from app.libs.httper import Http
from flask import current_app


class YuShuBook(object):
    """
    根据参数到api查询书籍信息
    """
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{0}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={0}&start={1}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        """
        isbn搜索
        :param isbn:书籍isbn参数
        :return: 书籍信息对象
        """
        url = self.isbn_url.format(isbn)
        result = Http.get(url)
        # print(result)
        self.__fill_single(result)

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        data = json.loads(data)
        self.total = data['total']
        self.books = data['books']

    def search_by_keyword(self, keyword, page=1):
        url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'], self.calculate_start(page))
        result = Http.get(url)
        # print(result)
        self.__fill_collection(result)

    @classmethod
    def calculate_start(cls, page):
        return (page - 1) * current_app.config['PER_PAGE']

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None
