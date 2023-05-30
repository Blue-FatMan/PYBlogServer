#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2023/5/24 19:22
# @Author  : liuqiao
# @Email   : LQ65535@163.com
# @File    : test-downloader.py
# @desc    : test-downloader
# @Software: PyCharm

import os
import pytest
from utils.downloader import DownloadMedia, DownloadStatic

TEST_DIR = os.path.dirname(os.path.abspath(__file__))

output_dir = os.path.join(TEST_DIR, "test-download-media-static")
if not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)


def test_download_png():
    url = "https://img-blog.csdnimg.cn/img_convert/2e83b44314336d01219853f785bc763f.png"
    download = DownloadMedia(url, thread_num=5, limit_time=10000)
    out_path = download.start(output_dir)
    assert out_path is not None


def test_download_gif():
    url = "https://img-blog.csdnimg.cn/63f5c8ac23fa4553a2ffc9a2e05db27c.gif#pic_center"
    download = DownloadMedia(url, thread_num=5, limit_time=10000)
    out_path = download.start(output_dir)
    assert out_path is not None


def test_download_js():
    url = "https://g.csdnimg.cn/user-accusation/1.0.5/user-accusation.js"
    download = DownloadStatic(url)
    out_path = download.start(output_dir)
    assert out_path is not None


def test_download_css():
    url = "https://csdnimg.cn/release/blogv2/dist/mdeditor/css/editerView/ck_htmledit_views-25cebea3f9.css"

    download = DownloadStatic(url)
    out_path = download.start(output_dir)
    assert out_path is not None


if __name__ == '__main__':
    pytest.main()
