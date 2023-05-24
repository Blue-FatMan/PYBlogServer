import json
import os

from django.shortcuts import render
from django.views.generic.base import View
from django.conf import settings
from django.http import JsonResponse


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
        #     user = CmLocalUser.objects.get(username=request.user.username)
        #     # 选择一些基本信息放到session里面
        #     request.session["user_id"] = user.user_id
        #     request.session["real_name"] = user.real_name
        #
        #     return render(request, "web/index.html", {})
        # else:
        #     return render(request, "web/page/auth/login-3.html", {})

    def post(self, request):
        pass


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
        # 用例步骤详情
        res = request_params.dict()
        return res


class WebInit(View):

    def get(self, request):
        """主页初始化 json
        :param request:
        :return:
        """
        json_path = os.path.join(settings.STATIC_ROOT, 'layuimini-v2.0.6.1-iframe', 'api', "init.json")
        init_data = read_json(json_path)
        return JsonResponse(init_data, json_dumps_params={"ensure_ascii": False})
