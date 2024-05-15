# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_LLM
author: 子不语
date: 2024/4/26
contact: 【公众号】思维兵工厂
description:
--------------------------------------------
"""


class InvalidFileError(Exception):
    message = "不支持的文件格式"


class RequestsError(Exception):
    message = "请求失败"


class NeedLoginError(Exception):
    message = "cookies过期，需要重新登录"


class LoginFailError(Exception):
    message = "登录失败"


class APIConnectionError(Exception):
    message = "网络连接错误"


class SpiderHasToChangeError(Exception):
    message = "网页出现新逻辑，爬虫需要更换"


class UnexpectResponseError(Exception):
    message = "响应异常"
