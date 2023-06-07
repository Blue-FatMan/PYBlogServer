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
from .views_models.views_upload import UploadMedia
from .views_models.views_tag import TagsApi
from .views_models.views_category import CategoriesApi
from .views_models.views_blog_local import BlogApi as LocalBlogApi
from .views_models.views_blog import BlogListApi, BlogDetailApi


urlpatterns = [
    url(r'^api/v1/upload/media/$', UploadMedia.as_view(), name='upload-media'),  # �ϴ�ý���ļ�

    # [��ǩ�ӿ�]
    url(r'^api/v1/tags/all/$', TagsApi.as_view(), name='tags-all'),  # ����ȫ����ǩ��Ϣ�ӿ�

    # [����ӿ�]
    url(r'^api/v1/category/all/$', CategoriesApi.as_view(), name='categories-all'),  # ����ȫ��������Ϣ�ӿ�

    # [���ͽӿ�]
    url(r'^article/(?P<blog_pk>\w+)/detail/$', BlogDetailApi.as_view(), name='article-detail'),  # �鿴��������
    url(r'^api/v1/article/local/all/$', BlogListApi.as_view(), name='article-list'),  # �鿴�����б�

    url(r'^api/v1/article/create/$', LocalBlogApi.as_view(), name='article-all'),  # �����½��ӿ�
    url(r'^api/v1/article/delete/$', LocalBlogApi.as_view(), name='article-delete'),  # ����ɾ���ӿ�
    url(r'^api/v1/article/(?P<blog_pk>\w+)/update/$', LocalBlogApi.as_view(), name='article-update'),  # ���ĸ��½ӿ�
]
