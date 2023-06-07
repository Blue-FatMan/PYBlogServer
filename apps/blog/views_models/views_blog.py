#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2023/6/6 10:59
# @Author  : liuqiao
# @Email   : LQ65535@163.com
# @File    : views_blog.py
# @desc    : views_blog
# @Software: PyCharm

import json
import traceback
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.safestring import mark_safe
from django.db.models import Q

from blog.operate_res_code import OperateResCode
from blog.models import Blog, BlogContent, BlogDownloadContent
from blog.serializers.serializers_blog import BlogSerializer
from blog.tools.pagination import CustomNumberPagination
import blog.tools.common as common_tools


class BlogListApi(APIView):
    """
    method: get: 返回博文列表
    """

    def get(self, request):
        res = OperateResCode()

        try:
            search_params = request.GET.get("searchParams", None)
            if search_params:
                search_params = json.loads(search_params)
                search_params = common_tools.process_search_params(search_params)
                search_params_conditions = Q()
                if "categories" in search_params:
                    search_params_conditions.add(Q(categories__in=search_params["categories"].split(",")), Q.OR)
                if "tags" in search_params:
                    search_params_conditions.add(Q(tags__in=search_params["tags"].split(",")), Q.OR)
                if "title_or_content" in search_params:
                    title_or_content = search_params["title_or_content"].strip()
                    search_params_conditions.add(Q(title__icontains=title_or_content), Q.OR)
                    local_content = BlogContent.objects.filter(content__icontains=title_or_content)  # 暂时只能从本地编写的内容中搜索，因为下载的博文数据库只存储本地路径，无法搜索
                    search_params_conditions.add(Q(content_id__in=[item.pk for item in local_content]), Q.OR)

                if search_params_conditions:
                    blog_obj_list = Blog.objects.filter(search_params_conditions).order_by("-id")
                else:
                    blog_obj_list = Blog.objects.filter().order_by("-id")

            else:
                blog_obj_list = Blog.objects.filter().order_by("-id")
            res.success["count"] = len(blog_obj_list)
            page = CustomNumberPagination()
            ret = page.paginate_queryset(blog_obj_list, request)
            serializer = BlogSerializer(ret, many=True)
            res.success["data"] = serializer.data
            return Response(res.success)
        except:
            print(traceback.format_exc())
            return Response(res.unknown_error, status=res.unknown_error["code"])


class BlogDetailApi(APIView):
    """
    method: get: 返回博文详情
    """

    def get(self, request, blog_pk):
        blog = Blog.objects.get(pk=blog_pk)
        if blog.blog_from == "local":
            blog.content = mark_safe(BlogContent.objects.get(pk=blog.content_id).content)
            return render(request, "page/blog/detail.html", {"blog": blog})
        elif blog.blog_from == "internet":
            local_path = BlogDownloadContent.objects.get(pk=blog.content_id).local_path
            return render(request, local_path)  # 从 settings.DOWNLOAD_BLOG_FOLDER_NAME 下面查找


class BlogDeleteApi(APIView):
    """
    method: delete: 删除博文
    """

    def delete(self, request):
        res = OperateResCode()

        try:
            if not request.user.is_authenticated:
                raise RuntimeError("user not login, request fail !!!")

            data = request.data
            blog_id_list = data.get("data")
            blog_obj = Blog.objects.filter(pk__in=blog_id_list)

            content_local_id_list = [__.content_id for __ in blog_obj if __.blog_from == "local"]
            content_local_obj = BlogContent.objects.filter(pk__in=content_local_id_list)

            content_download_id_list = [__.content_id for __ in blog_obj if __.blog_from == "internet"]
            content_download_obj = BlogDownloadContent.objects.filter(pk__in=content_download_id_list)

            blog_obj.delete()
            content_local_obj.delete()
            content_download_obj.delete()
            # 暂时不删除富文本上传的媒体文件
            return Response(res.success)

        except:
            print(traceback.format_exc())
            return Response(res.unknown_error, status=res.unknown_error["code"])
