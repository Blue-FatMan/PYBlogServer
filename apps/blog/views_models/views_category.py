#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2023/6/1 10:38
# @Author  : liuqiao
# @Email   : LQ65535@163.com
# @File    : views_category.py
# @desc    : views_category
# @Software: PyCharm

import traceback

from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import os
import datetime

from blog.operate_res_code import OperateResCode
from blog.models import Category


# Create your views here.


class CategoriesApi(APIView):
    """
    method: get: 返回分类json数据
    """

    def get(self, request):
        res = OperateResCode()

        try:
            objects = Category.objects.all().order_by('-id')
            result = [{"name": __.name, "value": __.pk} for __ in objects]
            res.success["data"] = result
            res.success["count"] = len(result)
            return Response(res.success)
        except:
            print(traceback.format_exc())
            return Response(res.unknown_error, status=res.unknown_error["code"])

