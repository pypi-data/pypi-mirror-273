# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_LLM
author: 子不语
date: 2024/4/27
contact: 【公众号】思维兵工厂
description: web逆向-最高级父类

各类AI平台的逆向，均需继承LLMBase类：
    - 定义类变量 model_name ；用于存放错误信息时，区分不同平台
    - 定义 ask 方法；该实现AI文本交互，如果cookie过期，需抛出NeedLoginError错误；
    - 流式输出时，最后需返回结束符号 END_SIGNAL；
    - 在子类的初始化方法中，调用super().__init__()之前，必须先传入自己的logger，否则将新建logger；
--------------------------------------------
"""

import os
import urllib3
import logging
import datetime

import requests
from fake_useragent import UserAgent

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

END_SIGNAL = '<<<end>>>'


class LLMBase(object):
    """
    基础类：提供以下功能：
        1. cookie初始化：从字符串解析为字典；从字典合成为字符串；
        2. 保存错误请求记录；
        3. 日志记录对象初始化（如果子类未定义的话）
    """

    model_name = 'LLMBase'  # 模型名称，用于存放记录时区分不同平台

    error_dir: str = ''  # 错误信息记录存放路径
    cookies_str: str = ''  # cookie字符串
    cookies_dict: dict = {}  # cookie字典
    logger = None
    user_agent = UserAgent().chrome  # 随机生成一个chrome的user-agent
    end_signal: str = END_SIGNAL  # AI流式输出时，最后一帧标识结束的符号

    def __init__(self):
        """
        初始化日志对象与错误记录存放路径
        """

        # 1. 获取项目根目录
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.__log_dir_path: str = ''  # 日志存放目录
        self.__resource_path: str = ''  # 资源存放目录

        # 2. 如果子类没有传入日志记录对象，则新建
        if not self.logger:
            self.logger = self.get_logger()

        if self.error_dir:
            self.logger.info(f"Error request record directory：【{self.error_dir}】")

            if not os.path.isdir(self.error_dir):
                self.logger.error(f"【{self.error_dir}】is not a directory!")
                raise ValueError(f"【{self.error_dir}】is not a directory!")

            if not os.path.exists(self.error_dir):
                os.makedirs(self.error_dir)
                self.logger.info(f"【{self.error_dir}】 does not exist!")
                self.logger.info(f"Create error request record directory：【{self.error_dir}】")

        # 3. cookies和cookies_dict同时传入，使用cookies_str
        if self.cookies_str and self.cookies_dict:
            self.logger.warning("cookies_str and cookies_dict are both set! Using cookies_str!")

        if self.cookies_str and not self.cookies_dict:
            self.cookie_dict_initialize()

        if self.cookies_dict and not self.cookies_str:
            self.cookies_str_initialize()

        self.request_session = requests.Session()

    def cookie_dict_initialize(self):
        """
        初始化cookie：将cookie字符串转化为cookie字典。
        :return:
        """

        cookie_list = self.cookies_str.split(";")
        self.cookies_dict = {}

        for it in cookie_list:
            it = it.strip()
            if it:
                equ_loc = it.find("=")
                key = it[:equ_loc]
                value = it[equ_loc + 1:]
                self.cookies_dict[key] = value

        self.logger.info(f"Complete cookie initialization! ")

    def cookies_str_initialize(self):
        """
        初始化cookie：将cookie字典转换为cookie字符串。
        :return:
        """

        # 使用列表推导式构造cookie字符串的各个部分，然后用join方法组合起来
        cookie_parts = [f"{key}={value}" for key, value in self.cookies_dict.items()]

        # 最后用分号和空格连接所有部分
        self.cookies_str = "; ".join(cookie_parts)

    def save_bad_request_data(self, file_name: str, data: str) -> str:
        """
        保存错误请求记录
        :param file_name: 文件名
        :param data: 错误请求记录数据
        :return: 返回错误记录文件的路径
        """

        if not self.error_dir:
            return ''

        now = datetime.datetime.now()
        format_str = "%Y%m%d_%H-%M-%S"
        file_name = f"{self.model_name}_{now.strftime(format_str)}_{file_name}"

        if not file_name.endswith('.txt'):
            file_name = f"{file_name}.txt"

        file_name = os.path.join(self.error_dir, file_name)

        # 记录文件如果存在，则追加内容
        if os.path.exists(file_name):
            with open(file_name, 'a', encoding='utf-8') as f:
                split_char = '=' * 100
                f.write(f"\n\n{split_char}\n\n{data}\n\n{split_char}\n\n")
            return file_name

        # 记录文件不存在，新建文件
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(f"{data}\n\n")

        return file_name

    @property
    def resource_path(self) -> str:
        """
        资源存放目录：存放程序运行过程中产生的记录文件
        :return:
        """

        if self.__resource_path:
            return self.__resource_path

        self.__resource_path = os.path.join(self.base_path, '.resources')
        if not os.path.exists(self.resource_path):
            os.makedirs(self.resource_path)
            self.logger.info(f"Create resource directory：【{self.resource_path}】")

        return self.__resource_path

    def get_logger(self) -> logging.Logger:
        """
        创建日志记录对象：默认在项目的根目录下创建log文件夹
        :return:
        """

        fmt = f'%(asctime)s.%(msecs)04d | %(levelname)8s | %(message)s'

        # 创建一个Logger，名称是app_log
        logger = logging.getLogger('LLMBase')

        # 设置为日志输出级别
        logger.setLevel(logging.DEBUG)

        # 创建formatter，并设置formatter的格式
        formatter = logging.Formatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S", )

        # 日志存放目录
        self.__log_dir_path = os.path.join(self.base_path, '.logs')
        if not os.path.exists(self.__log_dir_path):
            os.makedirs(self.__log_dir_path)

        file_path = os.path.join(self.__log_dir_path, f"{self.model_name}.log")

        file_handler = logging.FileHandler(
            filename=file_path,
            mode='w',
            encoding='utf8',
            delay=False
        )

        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger
