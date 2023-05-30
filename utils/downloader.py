#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import os
import traceback
from time import time
import threadpool
import threading
import requests
import urllib.parse


__all__ = ["DownloadMedia", "DownloadStatic"]


def translate_decode_adapter(words):
    """
    编码转换适配器，尝试使用不同的编码类型转换结果
    :param words: 需要转换的编码
    :return:
    """

    error_msg = ""
    decode_list = ["gb2312", "gb18030", "utf-8-sig", "gbk", "utf-8"]
    while decode_list:
        decode_type = decode_list.pop()
        try:
            result = words.encode(decode_type, "ignore").decode(decode_type, "ignore")  # https://blog.csdn.net/whatday/article/details/122807958
            return result
        except:
            error_msg = error_msg + traceback.format_exc()
    raise RuntimeError(error_msg)


def make_dir(out_put_dir) -> None:
    """
    创建缓存和保存目录
    """
    if not os.path.exists(out_put_dir):
        os.makedirs(out_put_dir, exist_ok=True)


# https://blog.csdn.net/wsfsp_4/article/details/127019804
class DownloadMedia(object):
    """ 多线程分块下载媒体文件"""

    def __init__(self, url: str, file_name: str = None, per_part_size: int = 1024 * 1024 * 10, thread_num: int = 5,
                 limit_time=3000) -> None:
        """
        初始化
        @url：文件链接
        @file_name：文件名(默认从链接中获取)
        @per_part_size：单线程下载大小(默认10MB)
        @thread_num：线程数(默认5)
        @limit_time：单线程1%进度限制时间,超时重新执行该线程(ms)
        """
        self.url = url
        self.per_part_size = per_part_size
        self.thread_num = thread_num
        self.limit_time = limit_time
        if not file_name:
            self.file_name = self.get_file_name()
        else:
            self.file_name = file_name

        self.out_put_dir = None
        self.output_path = None

    def get_file_name(self) -> str:
        """
        从链接中获取文件名
        """
        url = urllib.parse.unquote(self.url)
        return url.split("?")[0].split("/")[-1].split("#")[0]  # 切割路径获取文件名，考虑异常处理，例如 /test.png#pic_center

    def get_total_size(self) -> int:
        """
        获取文件总大小
        """
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
        res = requests.head(url=self.url, headers=headers)
        if res.status_code == 200:
            if "Content-Length" in res.headers:
                return int(res.headers['Content-Length'])
            else:
                return False
        else:
            return False

    def pre_download(self, index: int, totalSize: int) -> int:
        """
        检查分块下载进度 返回剩余大小
        """
        file_name = self.out_put_dir + f"/temp/{self.file_name}_{index}"
        if os.path.isfile(file_name):
            stat = os.stat(file_name)
            return totalSize - stat.st_size  # 剩余大小
        else:
            return totalSize

    def download(self, index: int, start: int, end: int) -> None:
        """
        下载分块
        """
        indexTip = f"{index}/{self.part_num - 1}"  # 分块位置提示
        totalSize = end - start + 1  # 分块总大小
        needDownSize = self.pre_download(index, totalSize)  # 分块剩余大小

        if needDownSize == 0:  # 分块已下载
            print(f"[{indexTip}][{start}-{end}]下载完成")
            return

        make_dir(self.out_put_dir+"/temp")
        if totalSize != needDownSize:  # 分块已存在,追加模式
            file = open(self.out_put_dir + f"/temp/{self.file_name}_{index}", mode="ba")
        else:  # 分块未存在，新建模式
            file = open(self.out_put_dir + f"/temp/{self.file_name}_{index}", mode="bw")

        currentSize = 0  # 已经下载大小
        progress = 0  # 下载进度

        headers = {
            "Range": f"bytes={end - needDownSize + 1}-{end}"  # 设置下载范围
        }
        req = requests.get(url=self.url, stream=True, headers=headers)  # 流式下载

        startTime = int(time() * 1000)  # 下载开始时间
        reDownload = False  # 重新下载标志
        for content in req.iter_content(chunk_size=2048):  # 读取并保存下载数据
            if content:
                file.write(content)
                currentSize += 2048  # 更新已下载大小
                if currentSize < needDownSize:  # 未完成下载
                    newProgress = int(currentSize * 100 / needDownSize)  # 下载进度
                    if progress != newProgress:
                        progress = newProgress
                        divTime = int(time() * 1000) - startTime  # 1%进度花费时间
                        if divTime > self.limit_time:  # 超时,重新下载
                            reDownload = True
                            print(
                                f"[{divTime}ms][{indexTip}][{progress}%]超时，重新下载")
                            file.close()
                            break
                        else:
                            startTime = int(time() * 1000)
                            print(
                                f"[{divTime}ms][{indexTip}][{progress}%]下载中")
        if reDownload:
            self.download(index, start, end)
        else:
            print(f"[{indexTip}][{start}-{end}]下载完成")

    def check_parts(self, partList: list) -> bool:
        """
        检查全部分块是否已下载
        """
        for part in partList:
            if self.pre_download(part['index'], part['totalSize']):
                return False
        return True

    def check_task(self) -> bool:
        """
        检查目标文件是否已下载
        """
        file_name = self.out_put_dir + "/" + self.file_name
        return os.path.isfile(file_name)

    def merge_parts(self, out_put_dir):
        """
        合并分块
        :param out_put_dir: 输出目录
        """
        self.output_path = out_put_dir + "/" + self.file_name
        targetFile = open(self.output_path, mode="bw")
        for index in range(self.part_num):
            partFile = self.out_put_dir + f"/temp/{self.file_name}_{index}"
            file = open(partFile, mode="br")
            targetFile.write(file.read())
            file.close()
            print(f"合并[{partFile}]成功")
        targetFile.close()

    def delete_parts(self):
        """
        删除缓存分块
        """
        for index in range(self.part_num):
            partName = self.out_put_dir + f"/temp/{self.file_name}_{index}"
            if os.path.isfile(partName):
                os.remove(partName)
                print(f"删除[{partName}]成功")

    def start(self, out_put_dir):
        """
        启动下载
        :param out_put_dir: 输出目录
        :return: 返回下载好的文件路径，如果返回None，代表下载失败
        """
        self.out_put_dir = out_put_dir
        make_dir(out_put_dir)

        totalSize = self.get_total_size()  # 文件总大小
        if not totalSize:
            print("文件不支持流式下载，程序退出")
            return self.output_path

        self.part_num = math.ceil((totalSize / self.per_part_size))  # 计算分块数量

        # *****  注释掉断点继续下载功能，使其每次都重新下载 *****
        # if self.check_task():
        #     self.delete_parts()
        #     print("文件已下载，任务退出")
        #     return
        # ***********************************************

        pool = threadpool.ThreadPool(self.thread_num)  # 创建线程池
        partList = []  # 分块列表(包含序号和大小)
        argsList = []  # 任务参数列表

        for i in range(self.part_num):  # 构建参数
            if i+1 == self.part_num:
                args = ([i, i * self.per_part_size, totalSize - 1], None)
            else:
                args = ([i, i * self.per_part_size, (i + 1) * self.per_part_size - 1], None)
            argsList.append(args)
            partList.append({"index": i, "totalSize": args[0][2] - args[0][1] + 1})

        reqs = threadpool.makeRequests(self.download, argsList)  # 构建任务队列
        for req in reqs:  # 提交任务
            pool.putRequest(req)
        pool.wait()  # 等待线程结束

        if self.check_parts(partList):  # 检查分块状态
            self.merge_parts(out_put_dir)
            self.delete_parts()
            return self.output_path
        else:
            print("分块未完全下载，请重新执行程序")
            return self.output_path


class DownloadStatic(object):
    """ 异步单线程下载静态文件"""

    def __init__(self, url: str, file_name: str = None) -> None:
        """
        初始化
        @url：文件链接
        @file_name：文件名(默认从链接中获取)
        """
        self.url = url
        if not file_name:
            self.file_name = self.get_file_name()
        else:
            self.file_name = file_name

        self.output_path = None

    def get_file_name(self) -> str:
        """
        从链接中获取文件名
        """
        url = urllib.parse.unquote(self.url)
        return url.split("?")[0].split("/")[-1].split("#")[0]  # 切割路径获取文件名，考虑异常处理，例如 /test.gif#pic_center

    def download(self, out_put_dir) -> None:
        """
        下载文件
        :param out_put_dir: 输出目录
        :return:
        """
        make_dir(out_put_dir)

        self.output_path = out_put_dir + "/" + self.file_name
        file = open(self.output_path, mode="w+", encoding="utf-8")
        try:
            headers = {
                "accept-language": "zh-CN,zh;q=0.9",
                "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
            response = requests.get(url=self.url, headers=headers, verify=False, allow_redirects=True)
            response_text = translate_decode_adapter(response.text)
            file.write(response_text)
        except:
            self.output_path = None
            print(f"下载失败：{self.url}")
            raise
        finally:
            file.close()
        print(f"下载完成")

    def start(self, out_put_dir):
        """
        启动下载
        :param out_put_dir: 输出目录
        :return: 返回下载好的文件路径，如果返回None，代表下载失败
        """
        job = threading.Thread(target=self.download, args=(out_put_dir, ))
        job.start()
        job.join()  # 等待线程结束
        return self.output_path


if __name__ == '__main__':
    pass
