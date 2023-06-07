import json
import os

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.utils.safestring import mark_safe
from rest_framework.views import APIView
from rest_framework.response import Response
from collections import OrderedDict
from django.conf import settings
from blog.models import Blog, BlogContent
import traceback


# Create your views here.
def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as fr:
        data = json.load(fr)
    return data


# 主页模块
class Index(View):
    def get(self, request):
        return render(request, "index.html", {})
        # # 判断是否已经登录
        # if request.user.is_authenticated:
        #     user = LocalUser.objects.get(username=request.user.username)
        #     # 选择一些基本信息放到session里面
        #     request.session["user_id"] = user.user_id
        #     request.session["real_name"] = user.real_name
        #
        #     return render(request, "web/index.html", {})
        # else:
        #     return render(request, "web/page/auth/login-3.html", {})


# 返回各静态页面
class PageView(View):
    def get(self, request, page_name):
        request_params = request.GET
        if str(page_name).split("?")[0].endswith('.html'):
            if request_params:
                request_type = request_params.get("type")
                res = self.process_request_type(request, request_type, request_params)
                return render(request, "page/" + page_name, res)
            else:
                return render(request, "page/" + page_name)

    def process_request_type(self, request, request_type, request_params):
        # 首页
        if request_type == "welcome":
            blog = Blog.objects.all()
            result = dict()
            for item in blog:
                if item.categories not in result:
                    result[item.categories] = []

                result[item.categories].append(item)

            return {"blog_dict": result}
        # 编辑博客
        if request_type == "edit-blog":
            blog = Blog.objects.get(pk=request_params["id"])

            # 当前仅支持本地编写的博客，下载的博客不支持修改
            if blog.blog_from != "local":
                raise RuntimeError("only support local write blog, not support download from internet...")
            blog.content = mark_safe(BlogContent.objects.get(pk=blog.content_id).content)
            return {"blog": blog}

        else:
            res = request_params.dict()
        return res


class Login(APIView):
    """登录"""

    def post(self, request):
        # 登录处理
        username = request.data.get("username")
        password = request.data.get("password")
        captcha = request.data.get("captcha")
        # 从session获取的
        server_code = request.session.get("captcha")
        code = "500"
        login_tip = ""
        # 做判断比较
        if server_code.lower() == captcha.lower():
            captcha_status = 0  # 验证码验证成功
        else:
            captcha_status = -1  # 输入验证码错误

        user_obj = auth.authenticate(username=username, password=password)
        if user_obj is not None and user_obj.is_active:
            login_status = 0
        else:
            login_status = -1
        if all((login_status == 0, captcha_status == 0)):
            auth.login(request, user_obj)
            code = "200"
        else:
            login_tip = "账号错误或者验证码错误"

        login_result = {'login_status': login_status,
                        "captcha_status": captcha_status,
                        "login_tip": login_tip,
                        "code": code}
        login_result = OrderedDict(login_result)
        return Response(login_result)


# 退出登录
class LogOut(APIView):

    def get(self, request):
        # 判断是否已经登录
        if request.user.is_authenticated:
            auth.logout(request)
        return HttpResponse(JsonResponse({"code": "200"}), content_type='application/json')


# 主页初始化数据
class WebInit(View):

    def get(self, request):
        """主页初始化 json
        :param request:
        :return:
        """
        json_path = os.path.join(settings.STATIC_ROOT, 'layuimini-v2.0.6.1-iframe', 'api', "init.json")
        init_data = read_json(json_path)
        return JsonResponse(init_data, json_dumps_params={"ensure_ascii": False})
