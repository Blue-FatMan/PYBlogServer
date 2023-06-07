import traceback

from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import os
import datetime

from blog.operate_res_code import OperateResCode
from blog.tools.common import get_current_time

# Create your views here.


class UploadMedia(APIView):
    """
    method: post: 上传媒体文件
    """

    def post(self, request):
        res = OperateResCode()

        try:
            if not request.user.is_authenticated:
                raise RuntimeError("user not login, request fail !!!")

            if 'HTTP_X_FORWARDED_FOR' in request.META.keys():
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            ip = ip.replace(".", "-")
            username = request.user.username
            upload_file = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
            current_time = get_current_time().replace("-", "").replace(" ", "").replace(":", "")  # 获取当前时间
            relative_path = os.path.join("blog", "upload", f"{current_time}-{username}-{ip}-{upload_file.name}")  # 生成相对路径
            save_path = os.path.join(settings.MEDIA_ROOT, relative_path)  # 生成最终的绝对路径

            # 检查media路径是否存在，不存在则创建
            if not os.path.exists(os.path.dirname(save_path)):
                os.makedirs(os.path.dirname(save_path))

            if not upload_file or not upload_file.name.endswith(".png"):
                res.unknown_error["data"] = "请确认上传文件格式是否是.xlsx格式"
                res.unknown_error["message"] = "请确认上传文件格式是否是.xlsx格式"
                return Response(res.unknown_error, status=res.unknown_error["code"])
            with open(save_path, 'wb+') as fw:  # 打开特定的文件进行二进制的写操作
                for chunk in upload_file.chunks():  # 分块写入文件
                    fw.write(chunk)
            # print(save_path)
            res.success["location"] = os.path.join(settings.MEDIA_URL, relative_path)
            return Response(res.success)
        except:
            print(traceback.format_exc())
            return Response(res.unknown_error, status=res.unknown_error["code"])
