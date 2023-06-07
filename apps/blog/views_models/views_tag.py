#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2023/6/1 10:37
# @Author  : liuqiao
# @Email   : LQ65535@163.com
# @File    : views_tag.py
# @desc    : views_tag
# @Software: PyCharm

import traceback

from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import os
import datetime

from blog.operate_res_code import OperateResCode
from blog.models import Tag


# Create your views here.


class TagsApi(APIView):
    """
    method: get: 返回标签json数据
    """

    def get(self, request):
        res = OperateResCode()

        try:
            objects = Tag.objects.all().order_by('-id')
            result = [{"name": __.name, "value": __.pk} for __ in objects]
            res.success["data"] = result
            res.success["count"] = len(result)
            return Response(res.success)
        except:
            print(traceback.format_exc())
            return Response(res.unknown_error, status=res.unknown_error["code"])
