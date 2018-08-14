#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-9 下午11:59
# @Author  : Shark
# @File    : book.py
# @Software: PyCharm
import json

from flask import jsonify, request, render_template, flash

from app.view_models.book import BookViewModel, BookCollection
from . import web
from app.libs.book_info import YuShuBook
from app.libs.uilt import is_isbn_or_key
from app.forms.search_book import SearchForm


@web.route('/book/search')
def search():
    """
    书籍搜索
    :param q:普通关键字 isbn 13个0到9数字组成， 可能含有一些空格
    :param page:
    :return:
    """

    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)

        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
        # return json.dumps(books, default=lambda o: o.__dict__)
        # return jsonify(books.__dict__)

    else:

        flash('搜索的关键字不符合要求，请重新输入关键字')

        # return jsonify(form.errors)
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    return render_template('book_detail.html', book=book, wishes=[], gifts=[])
