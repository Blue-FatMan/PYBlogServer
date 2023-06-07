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
from django.views import static
from django.conf import settings

from .views_models.views_upload import UploadMedia
from .views_models.views_tag import TagsApi
from .views_models.views_category import CategoriesApi
from .views_models.views_blog_local import BlogApi as LocalBlogApi
from .views_models.views_blog_download import BlogApi as DownloadBlogApi
from .views_models.views_blog import BlogListApi, BlogDetailApi, BlogDeleteApi


urlpatterns = [
    url(r'^api/v1/upload/media/$', UploadMedia.as_view(), name='upload-media'),  # 上传媒体文件

    # [标签接口]
    url(r'^api/v1/tags/all/$', TagsApi.as_view(), name='tags-all'),  # 返回全部标签信息接口

    # [分类接口]
    url(r'^api/v1/category/all/$', CategoriesApi.as_view(), name='categories-all'),  # 返回全部分类信息接口

    # [博客接口]
    url(r'^article/(?P<blog_pk>\w+)/detail/$', BlogDetailApi.as_view(), name='article-detail'),  # 查看博文详情
    url(r'^api/v1/article/local/all/$', BlogListApi.as_view(), name='article-list'),  # 查看博文列表

    url(r'^api/v1/article/create/$', LocalBlogApi.as_view(), name='article-create'),  # 博文新建接口
    url(r'^api/v1/article/download/$', DownloadBlogApi.as_view(), name='article-download'),  # 博文下载接口
    url(r'^api/v1/article/delete/$', BlogDeleteApi.as_view(), name='article-delete'),  # 博文删除接口
    url(r'^api/v1/article/(?P<blog_pk>\w+)/update/$', LocalBlogApi.as_view(), name='article-update'),  # 博文更新接口

    url(r'^download/static/(?P<path>.*)$', static.serve, {'document_root': settings.DOWNLOAD_BLOG_DIR}, name='download-static'),
    url(r'^download/media/(?P<path>.*)$', static.serve, {'document_root': settings.DOWNLOAD_BLOG_DIR}, name='download-media'),
]
