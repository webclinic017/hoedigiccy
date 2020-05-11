# -*- coding:utf-8 -*-

"""
Error Message.

Aioquant Study from HuangTao
Author: Redhoe
Date:   2020/05/11
Email:  lamusxiao@qq.com
"""


class Error:

    def __init__(self, msg):
        self._msg = msg

    @property
    def msg(self):
        return self._msg

    def __str__(self):
        return str(self._msg)

    def __repr__(self):
        return str(self)
