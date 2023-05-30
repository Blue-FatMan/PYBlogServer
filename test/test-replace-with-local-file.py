#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2023/5/25 15:08
# @Author  : liuqiao
# @Email   : LQ65535@163.com
# @File    : test-replace-with-local-file.py
# @desc    : test-replace-with-local-file
# @Software: PyCharm

import os
import pytest
from utils.replace_with_local_file import replace_with_local_file

TEST_DIR = os.path.dirname(os.path.abspath(__file__))

# 测试数据存放路径
test_data_dir = os.path.join(TEST_DIR, "test-data")
# 下载，输出文件存放路径
output_dir = os.path.join(TEST_DIR, "test-replace-output")
if not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)


def test01():
    replace_with_local_file(local_html=os.path.join(test_data_dir, "test-replace.html"),
                            download_dir=output_dir, output_html_dir=output_dir, test=True)


def test02():
    replace_with_local_file(local_html=os.path.join(test_data_dir, "test-replace-99255253.html"),
                            download_dir=output_dir, output_html_dir=output_dir, test=True)


if __name__ == '__main__':
    pytest.main()
