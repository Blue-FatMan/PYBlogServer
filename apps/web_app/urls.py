"""CmTestManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from .views import Index, PageView, Login, LogOut
from .get_veriy_img import get_verify_img

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),  # 首页

    # [登录-退出]
    url(r'^get_verify_img/', get_verify_img, name='verify_img'),  # 登录验证码
    url(r'^api/v1/user/login/$', Login.as_view(), name='login'),  # 登录
    url(r'^api/v1/user/logout/$', LogOut.as_view(), name='logout'),  # 退出登录

    url(r'^page/(.+)', PageView.as_view(), name='web_page_view'),  # 返回web/page下面的各静态页面
]
