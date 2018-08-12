#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-12 上午10:37
# @Author  : Shark
# @File    : user.py
# @Software: PyCharm
from sqlalchemy import Column, String, Boolean, Float, Integer
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import login_manager
from app.libs.book_info import YuShuBook
from app.libs.uilt import is_isbn_or_key
from app.models.base import Base


class User(UserMixin, Base):
    __tablename__ = 'user'
    # __bind_key__ = 'fisher'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column('password', String(128))
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    gifts = relationship('Gift')

    @property
    def password(self):
        '''
        获取类属性
        :return:
        '''
        return self._password

    @password.setter
    def password(self, raw):
        """
        设置类属性
        :param raw: 需加密密码
        :return:
        """
        self._password = generate_password_hash(raw)  # 加密密码

    def check_password(self, raw):
        """
        用户登录时密码比对
        :param raw: 明文密码
        :return: True or False
        """
        return check_password_hash(self._password, raw)  # 密码比对

    def can_save_to_list(self, isbn):
        """
        判断上传是否能上传
        :param isbn: 书籍编码
        :return:
        """
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False


    # def get_id(self):
    #     """
    #     固定写法，能让login_user获得用户id身份, 继承UserMixin默认使用id其他字段需重写
    #     :return:
    #     """
    #     return self.id


@login_manager.user_loader
def get_user(uid):
    """
    权限控制函数
    :param uid: 用户id
    :return: 用户模型
    """
    return User.query.get(int(uid))
