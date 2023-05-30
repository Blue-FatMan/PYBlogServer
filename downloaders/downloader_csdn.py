#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2023/5/24 11:17
# @Author  : liuqiao
# @Email   : LQ65535@163.com
# @File    : downloader.py
# @desc    : downloader
# @Software: PyCharm


import os
from bs4 import BeautifulSoup

from utils.requests_middleware import requests_main
from .base import ABCDownloader

# csdn博文公共模板
common_template = '''
<!-- csdn共用css -->
<link rel="stylesheet" href="https://csdnimg.cn/release/blog_editor_html/release1.6.12/ckeditor/plugins/codesnippet/lib/highlight/styles/atom-one-light.css">
<link href="https://csdnimg.cn/release/blogv2/dist/mdeditor/css/editerView/markdown_views-98b95bb57c.css" rel="stylesheet">
<link href="https://csdnimg.cn/release/blogv2/dist/mdeditor/css/style-c216769e99.css" rel="stylesheet">

<!-- jquery -->
<script src="https://csdnimg.cn/public/common/libs/jquery/jquery-1.9.1.min.js" type="text/javascript"></script>

<!-- 富文本柱状图  -->
<link rel="stylesheet" href="https://csdnimg.cn/release/blog_editor_html/release1.6.12/ckeditor/plugins/chart/chart.css" />
<script type="text/javascript" src="https://csdnimg.cn/release/blog_editor_html/release1.6.12/ckeditor/plugins/chart/lib/chart.min.js"></script>
<script type="text/javascript" src="https://csdnimg.cn/release/blog_editor_html/release1.6.12/ckeditor/plugins/chart/widget2chart.js"></script>
<script src="https://csdnimg.cn/release/blogv2/dist/components/js/axios-83fa28cedf.min.js" type="text/javascript"></script>
<script src="https://csdnimg.cn/release/blogv2/dist/components/js/pc_wap_highlight-8defd55d6e.min.js" type="text/javascript"></script>
<script src="https://csdnimg.cn/release/blogv2/dist/components/js/pc_wap_common-be82269d23.min.js" type="text/javascript"></script>
<script src="https://csdnimg.cn/release/blogv2/dist/components/js/edit_copy_code-2d3931414f.min.js" type="text/javascript"></script>
<link rel="stylesheet" href="https://csdnimg.cn/release/blog_editor_html/release1.6.12/ckeditor/plugins/codesnippet/lib/highlight/styles/atom-one-light.css">
<script src="https://g.csdnimg.cn/user-accusation/1.0.5/user-accusation.js" type="text/javascript"></script>
'''


class CsdnEngine(ABCDownloader):
    def __init__(self, url, cookie=None):
        self.url = url
        self.cookie = cookie

        # init headers
        self.__init_headers()

    def __init_headers(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        }
        if self.cookie:
            headers["cookie"] = self.cookie.encode("utf-8").decode("latin1")  # cookie如果不经过编码转换，requests请求的时候，会有编码报错问题
        else:
            pass
        self.headers = headers

    def download_html(self, output_dir, output_name=None):
        """
        下载html文件到本地
        :param output_dir: 本地输出目录
        :param output_name: 输出文件名称
        :return: 返回下载到本地的html的路径
        """
        response = requests_main("GET", url=self.url, headers=self.headers, verify=False, allow_redirects=True)
        response_code = response.status_code
        if response_code != 200:
            raise RuntimeError("csdn http response status code is not 200 !!!")

        response_text = response.text
        # response_content = content.content
        """
        查找CSDN存放博文标题的容器
        <h1 class="title-article" id="articleContentId">  --2023.05.24
        
        查找CSDN存放博文内容的容器
        <div class="article_content clearfix" id="article_content">  --2023.05.24
        """
        source_page = BeautifulSoup(response_text, "lxml")

        article_title_label = source_page.find_all(id="articleContentId")  # 标题标签
        article_label = source_page.find_all("div", id="article_content")  # 文章内容标签
        vip_mask_label = source_page.find_all("div", attrs={"class": "vip-mask"})  # 开通VIP 解锁文章

        article_title = ""
        if article_title_label:
            article_title = article_title_label[0]
        article_content = ""
        if article_label:
            article_content = article_label[0]
        vip_mask_content = ""
        if vip_mask_label:
            vip_mask_content = vip_mask_label[0]

        source_link = f'<a href="{self.url}" title="点击跳转到原始链接" target="_blank">点击跳转到原始链接 {self.url}</a>'
        artitle = f"{source_link}  \n<br/>\n " \
                  f"{article_title} \n<br/>\n " \
                  f"{article_content} \n<br/>\n" \
                  f"{vip_mask_content} \n<br/>\n" \
                  f"{common_template}"

        if not output_name:
            output_name = self.url.split("/")[-1].split("?")[0] + ".html"

        output_path = os.path.join(output_dir, output_name)
        with open(output_path, "w+", encoding="utf-8") as fw:
            fw.write(artitle)
        return output_path
