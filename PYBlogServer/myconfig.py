#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2023/5/18 17:12
# @Author  : liuqiao
# @Email   : LQ65535@163.com
# @File    : myconfig.py
# @desc    : myconfig
# @Software: PyCharm

import pymysql
pymysql.install_as_MySQLdb()

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': 'db.sqlite3'
    # }

    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "pyblogserver",
        'USER': 'root',
        'PASSWORD': 'rootpasswd',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},  # 支持emoji
    },
}


# session 配置
# 参考 https://www.cnblogs.com/sly27/p/12361941.html
# 登录失效时间设置为 1 周
SESSION_COOKIE_AGE = 604800  # Session的cookie失效日期（数字为秒数）（默认1周）
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # 是否关闭浏览器使得Session过期（默认 false）
SESSION_SAVE_EVERY_REQUEST = True  # 是否每次请求都保存Session，默认修改之后才保存（默认 false）

# 邮箱配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.163.com"  # 163邮箱主机
EMAIL_PORT = 25
EMAIL_HOST_USER = "LQ65535@163.com"  # 发送邮箱
EMAIL_HOST_PASSWORD = "*******"  # 发件邮箱授权码
EMAIL_USE_TLS = False  # 与SMTP服务器通信时,是否启用安全模式
DEFAULT_FROM_EMAIL = "博客管理平台<LQ65535@163.com>"  # 收件人看到的发件人
# 管理员站点，一般为发送人的邮箱
SERVER_EMAIL = '博客管理平台<LQ65535@163.com>'  # 服务报错的时候，admin管理员看到的发件人显示
EMAIL_SUBJECT_PREFIX = '[博客管理平台]'  # 服务报错的时候，admin管理员邮箱里面的看到的邮箱标题

# https://docs.djangoproject.com/en/1.8/ref/settings/#admins
# 当DEBUG为False而views发生异常的时候发email通知这些开发人员
ADMINS = (('liuqiao', 'LQ65535@163.com'), )

# https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-MANAGERS
# 和ADMINS类似,并且结构一样,当出现'broken link'的时候给manager发邮件.
MANAGERS = ('LQ65535@163.com', )


X_FRAME_OPTIONS = 'SAMEORIGIN'
# # DENY ：表示该页面不允许在 frame 中展示，即便是在相同域名的页面中嵌套也不允许
# # SAMEORIGIN ：表示该页面可以在相同域名页面的 frame 中展示
# # ALLOW-FROM uri ：表示该页面可以在指定来源的 frame 中展示
#
# SECURE_CONTENT_TYPE_NOSNIFF = False
#
# import mimetypes
# mimetypes.add_type('text/css', '.css')
# mimetypes.add_type('application/javascript', '.js')
