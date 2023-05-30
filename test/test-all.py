#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2023/5/25 15:28
# @Author  : liuqiao
# @Email   : LQ65535@163.com
# @File    : test-all.py
# @desc    : test-all
# @Software: PyCharm

import os
import sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(PROJECT_DIR)
sys.path.insert(0, PROJECT_DIR)

if __name__ == '__main__':
    test_py_list = os.listdir(".")
    test_py_list = [_ for _ in test_py_list if _.startswith("test") and _.endswith(".py") and _ != "test-all.py"]

    for test_py in test_py_list:
        os.system(f"pytest {test_py}")
