#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2023/6/1 11:27
# @Author  : liuqiao
# @Email   : LQ65535@163.com
# @File    : common.py
# @desc    : common
# @Software: PyCharm

import time
import copy


def get_current_time():
    """
    获取当前时间 "%Y%m%d%H%M%S"
    :return:
    """
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return current_time


def process_search_params(data):
    """
    处理搜素参数，把没有给值的搜索字段全都去除
    :param data:
    :return: 返回去除空搜索键之后的搜索字典
    """
    result = copy.deepcopy(data)
    for _ in data:
        if not data[_]:
            result.pop(_)
        else:
            # 把bool参数做个转换
            if _ in ["is_active"]:
                result[_] = eval(data[_])

    return result
