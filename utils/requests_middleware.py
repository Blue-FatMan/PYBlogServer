# -*- coding: utf-8 -*-
# @Time    : 2021/12/27 17:40
# @Author  : liuqiao
# @Email   : LQ65535@163.com
# @File    : requests_middleware.py
# @Software: PyCharm

# 该文件是请求requests部分，专门负责发送请求，并且返回结果的模块
import traceback
import json
import requests
import logging


# 获取一个代理
def get_proxy():
    proxy_ip = {'http': '125.108.68.188888:9000'}
    return proxy_ip


# 进行http请求
def requests_main(request_type, url, need_proxy=False, *args, **kwargs):
    '''
    :param request_type: str类型，请求类型，可选输入：``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
    :param url: str类型，请求的网页URL
    :param need_proxy: bool类型，是否需代理，默认不需要
    :param args:
    :param kwargs:
    :return: 返会requests请求结果，或者报错
    '''
    request_type = request_type.lower()
    try:
        custom_header = kwargs.get("headers")
        if custom_header:
            kwargs["headers"] = custom_header
        else:
            pass

        logging.debug("请求方式：{}, 请求url: {}".format(request_type, url))
        if need_proxy:
            proxy_ip = get_proxy()
            response = getattr(requests, request_type)(url, proxies=proxy_ip, **kwargs)
        else:
            response = getattr(requests, request_type)(url, **kwargs)

        logging.debug("响应状态码：{}".format(response.status_code))
        return response

    except:
        logging.error('request failed, fail info is: \n' + traceback.format_exc())
        raise


if __name__ == '__main__':
    # proxy_ip = {'http': '125.108.68.188888:9000'}  # 想验证的代理IP,HTTP要和代理IP网站一致大写
    url = "https://www.baidu.com/"
    res = requests_main("get", url, timeout=15)
    print(res.text)
