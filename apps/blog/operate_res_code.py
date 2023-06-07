#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@time: 2022/5/24 16:48
@author: LQ
@email: LQ65535@163.com
@File: operate_res_code.py
@Software: PyCharm
"""
from collections import OrderedDict

__all__ = ["OperateResCode"]


class OperateResCode(object):
    """操作响应状态码"""
    def __init__(self):
        self.success_res = OrderedDict({"code": "200", "message": "成功", "data": "成功"})
        self.unknown_error_res = OrderedDict({"code": "500", "message": "未知错误", "data": "未知错误"})
        self.delete_error_res = OrderedDict({"code": "501", "message": "删除失败,对象可能不存在", "data": "删除失败,对象可能不存在"})
        self.permission_denied_res = OrderedDict({"code": "404", "message": "权限不足", "data": "权限不足"})
        self.timeout_res = OrderedDict({"code": "504", "message": "操作超时！！！(如果是搜索操作，可以尝试减少搜索关键词)", "data": []})

    @property
    def success(self):
        return self.success_res

    @property
    def unknown_error(self):
        return self.unknown_error_res

    @property
    def delete_error(self):
        return self.delete_error_res

    @property
    def permission_denied(self):
        return self.permission_denied_res

    @property
    def timeout(self):
        return self.timeout_res


if __name__ == '__main__':
    print(OperateResCode.permission_denied)
