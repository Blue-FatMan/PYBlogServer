#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2023/5/24 15:37
# @Author  : liuqiao
# @Email   : LQ65535@163.com
# @File    : test-csdn.py
# @desc    : test-csdn
# @Software: PyCharm

import os
import pytest
from downloaders.downloader_csdn import CsdnEngine
from test.config import csdn_cookie


TEST_DIR = os.path.dirname(os.path.abspath(__file__))

output_dir = os.path.join(TEST_DIR, "test-download-html")
if not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)

cookie = csdn_cookie

#
# def test_csdn01():
#     url = "https://blog.csdn.net/YZL40514131/article/details/120690565"  # 普通文章
#
#     obj = CsdnEngine(url=url, cookie=cookie)
#     output_path = obj.download_html(output_dir=output_dir)
#     print(output_path)
#
#
# def test_csdn02():
#     url = "https://blog.csdn.net/rhn_111/article/details/129125277"  # 普通文章
#
#     obj = CsdnEngine(url=url, cookie=cookie)
#     output_path = obj.download_html(output_dir=output_dir)
#     print(output_path)
#
#
# def test_csdn03():
#     url = "https://blog.csdn.net/sogouauto/article/details/44568893?spm=1001.2014.3001.5501"  # 带有markdown编辑器的文章
#
#     obj = CsdnEngine(url=url, cookie=cookie)
#     output_path = obj.download_html(output_dir=output_dir)
#     print(output_path)
#
#
# def test_csdn04():
#     url = "https://blog.csdn.net/I_r_o_n_M_a_n/article/details/123190510"  # 关注博主即可阅读全文
#
#     obj = CsdnEngine(url=url, cookie=cookie)
#     output_path = obj.download_html(output_dir=output_dir)
#     print(output_path)


def test_csdn05():
    url = "https://blog.csdn.net/weixin_30859423/article/details/99255253"  # 开通VIP 解锁文章

    obj = CsdnEngine(url=url, cookie=cookie)
    output_path = obj.download_html(output_dir=output_dir)
    print(output_path)


if __name__ == '__main__':
    pytest.main()
