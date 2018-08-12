#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-11 下午3:24
# @Author  : Shark
# @File    : book.py
# @Software: PyCharm
import json


class BookViewModel(object):
    def __init__(self, book):
        book = json.loads(book)
        self.title = book['title']
        self.publisher = book['publisher']
        self.author = book['author']
        self.image = book['image']
        self.price = book['price']
        self.summary = book['summary']
        self.pages = book['pages']
        self.isbn = book['isbn']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False, [self.author, self.publisher, self.price])

        return ' / '.join(intros.__dict__)


class BookCollection(object):
    """
    书籍信息处理
    """
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]

    @classmethod
    def __cut_book_data(cls, data):
        """
        处理书籍信息
        :param data:api获得的原始书籍信息
        :return: 字典类型的想要的书籍信息
        """
        data = json.loads(data)
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'pages': data['pages'] or '',
            'author': data['author'],
            'price': data['price'],
            'summary': data['summary'] or '',
            'image': data['image']

        }

        return book


class _BookViewModel(object):
    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }

        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]

        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }

        if data:
            returned['total'] = data['total']
            returned['books'] = [cls.__cut_book_data(book) for book in data['books']]

        return returned

    @classmethod
    def __cut_book_data(cls, data):
        data = json.loads(data)
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'pages': data['pages'] or '',
            'author': data['author'],
            'price': data['price'],
            'summary': data['summary'] or '',
            'image': data['image']

        }

        return book
