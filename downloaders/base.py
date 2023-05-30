#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2023/5/24 15:58
# @Author  : liuqiao
# @Email   : LQ65535@163.com
# @File    : base.py
# @desc    : base
# @Software: PyCharm

from abc import ABC, abstractmethod


class ABCDownloader(ABC):

    @abstractmethod
    def download_html(self, output_dir, output_name):
        pass
