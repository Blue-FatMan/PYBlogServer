#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2023/5/24 17:52
# @Author  : liuqiao
# @Email   : LQ65535@163.com
# @File    : replace_with_local_file.py
# @desc    : 该文件是把下载好的原始html里面的 css, js, img标签里面的src连接下载到本地，然后用本地连接替换掉
# @Software: PyCharm
import copy
import os.path

from bs4 import BeautifulSoup
from utils.downloader import DownloadMedia, DownloadStatic


def replace_with_local_file(local_html, download_dir, output_html_dir, test=False):
    """
    把本地原始html里面的 css, js, img，video等静态文件，媒体文件标签里面的src连接下载到本地，然后用本地连接替换掉
    :param local_html: 本地原始html文件
    :param download_dir: 本地存储的静态文件，媒体文件的文件夹
    :param output_html_dir: 替换本地链接之后的html文件输出文件夹, 该值最好和download_dir保持一致
    :param test: 测试模式，如果是测试模式，则替换本地下载文件使用相对路径替换，如果是非测试模式，则使用匹配django的url开头的模式
    :return: 输出html的路径
    """
    with open(local_html, "r", encoding="utf-8") as fr:
        html = fr.read()

    source_page = BeautifulSoup(html, "lxml")

    link_label_list = source_page.find_all("link")
    link_href_list = [item["href"] for item in link_label_list]

    script_label_list = source_page.find_all("script")
    script_href_list = [item["src"] for item in script_label_list]

    img_label_list = source_page.find_all("img")
    img_href_list = [item["src"] for item in img_label_list]

    video_label_list = source_page.find_all("video")
    video_href_list = [item["src"] for item in video_label_list]

    # 合并静态文件链接
    static_link_list = []
    static_link_list.extend(link_href_list)
    static_link_list.extend(script_href_list)

    # 合并媒体文件链接
    media_link_list = []
    media_link_list.extend(img_href_list)
    media_link_list.extend(video_href_list)
    # print(static_link_list)
    # print(media_link_list)

    # 下载静态文件
    static_link_replace_map = {}
    download_static_dir = f"{download_dir}/static"  # static文件统一存放在static文件夹下
    for link in static_link_list:
        download = DownloadStatic(link)
        output_path = download.start(download_static_dir)
        if output_path:
            if test:
                # 如果是测试模式下，那就默认为html和下载的文件处于同一个路径下
                output_path = f'.{output_path.split(download_dir)[1]}'
            else:
                # 根据django url最终配置，返回对应的值
                output_path = f'/blog/download/static/{output_path.split("download-blog")[1]}'
            static_link_replace_map[link] = f"{output_path}"

    # 下载媒体文件
    media_link_replace_map = {}
    download_media_dir = f"{download_dir}/media"  # media文件统一存放在media文件夹下
    for link in media_link_list:
        download = DownloadMedia(link)
        output_path = download.start(download_media_dir)
        if output_path:
            if test:
                # 如果是测试模式下，那就默认为html和下载的文件处于同一个路径下
                output_path = f'.{output_path.split(download_dir)[1]}'
            else:
                # 根据django url最终配置，返回对应的值
                output_path = f'/blog/download/media/{output_path.split("download-blog")[1]}'
            media_link_replace_map[link] = f"{output_path}"

    # print(static_link_replace_map)
    # print(media_link_replace_map)

    # 替换为新的html字符串
    new_html_str = copy.deepcopy(html)
    for item in static_link_replace_map:
        new_html_str = new_html_str.replace(item, static_link_replace_map[item])
    for item in media_link_replace_map:
        new_html_str = new_html_str.replace(item, media_link_replace_map[item])

    # 生成新的html到本地
    output_html_path = output_html_dir + "/" + os.path.basename(local_html)
    with open(output_html_path, "w+", encoding="utf-8") as fw:
        fw.write(new_html_str)
    print(f"本地文件替换成功,输出html路径: {output_html_path}")
    return output_html_path


if __name__ == '__main__':
    pass
