#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2023/6/1 11:35
# @Author  : liuqiao
# @Email   : LQ65535@163.com
# @File    : views_blog.py
# @desc    : views_blog
# @Software: PyCharm
import os.path
import time
import traceback

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.safestring import mark_safe
from django.conf import settings


from blog.operate_res_code import OperateResCode
from blog.tools.common import get_current_time
from blog.models import Blog
from blog.models import BlogDownloadContent
from downloaders.downloader_csdn import CsdnEngine
from utils.replace_with_local_file import replace_with_local_file


class BlogApi(APIView):
    """
    method: post: 新建下载的博客
    method: put: 修改下载的博文内容
    """

    def post(self, request):
        res = OperateResCode()

        try:
            if not request.user.is_authenticated:
                raise RuntimeError("user not login, request fail !!!")

            data = request.data
            title = data.get("title", None)
            description = data.get("description", None)
            categories = data.get("categories", None)
            tags = data.get("tags", None)
            source_site = data.get("source_site", None)
            source_url = data.get("source_url", None)

            if source_site.lower() == "csdn":
                download_engine = CsdnEngine(url=source_url)
            else:
                raise RuntimeError("error download engine")

            current_date = time.strftime("%Y%m", time.localtime())  # 年份+月份
            time_stamp = int(time.time())  # 时间戳
            output_dir = f"{settings.DOWNLOAD_BLOG_DIR}/{current_date}/{source_site.lower()}/{time_stamp}" # 202306/csdn/时间戳/download.html
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            download_path = download_engine.download_html(output_dir=output_dir)
            replace_download_path = replace_with_local_file(local_html=download_path, download_dir=output_dir, output_html_dir=output_dir, test=False)

            relative_path = replace_download_path.split(settings.DOWNLOAD_BLOG_FOLDER_NAME)[1][1:]  # 抽取出来相对路径，以便给django的template dir文件夹自动寻找
            # print(replace_download_path)
            # print(relative_path)
            current_time = get_current_time()
            new_blog_download_content_data = {
                "source_site": source_site,
                "source_url": source_url,
                "local_path": relative_path,
                "create_time": current_time,
                "update_time": current_time,
            }
            content_obj = BlogDownloadContent.objects.create(**new_blog_download_content_data)

            new_blog_data = {
                "title": title,
                "description": description,
                "blog_from": "internet",
                "categories": categories,
                "tags": tags,
                "content_id": content_obj.pk,
                "create_time": current_time,
                "update_time": current_time,
            }
            Blog.objects.create(**new_blog_data)

            return Response(res.success)

        except:
            print(traceback.format_exc())
            return Response(res.unknown_error, status=res.unknown_error["code"])

    def put(self, request, blog_pk):
        res = OperateResCode()

        try:
            if not request.user.is_authenticated:
                raise RuntimeError("user not login, request fail !!!")

            data = request.data
            pass
            return Response(res.success)

        except:
            print(traceback.format_exc())
            return Response(res.unknown_error, status=res.unknown_error["code"])
