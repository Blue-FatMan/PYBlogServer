#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@time: 2022/5/23 17:01
@author: LQ
@email: LQ65535@163.com
@File: pagination.py
@Software: PyCharm
"""
from rest_framework.pagination import PageNumberPagination


class CustomNumberPagination(PageNumberPagination):
    """自定义分页器?page=xx&size=??"""
    page_size = 20  # 默认每页显示的多少条记录
    page_query_param = 'page'  # 默认查询参数名为 page
    page_size_query_param = 'size'  # 默认查询参数名为 size
    max_page_size = 100  # 后台控制显示的最大记录条数，防止用户输入的查询条数过大


if __name__ == '__main__':
    pass
    # demo如下
    # class ArticleList0(APIView):
    #     """
    #     List all articles, or create a new article.
    #     """
    #
    #     def get(self, request, format=None):
    #         articles = Article.objects.all()
    #
    #         page = CustomNumberPagination()  # 产生一个分页器对象
    #         ret = page.paginate_queryset(articles, request)
    #         serializer = ArticleSerializer(ret, many=True)
    #
    #         return Response(serializer.data)
