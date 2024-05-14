# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_LLM
author: 子不语
date: 2024/4/27
contact: 【公众号】思维兵工厂
description: 基于通义万相网页端逆向实现API调用，不过官方仍有每天额度限制。
--------------------------------------------
"""

import json
import time
import logging
from typing import Literal

import requests

from .base import LLMBase
from .errors import RequestsError
from .types import WanXianImage


class WanXiangWeb(LLMBase):
    """
    WanXiangWeb：通义万相web端
    """

    model_name = 'WanXiang'

    api_base: str = "https://wanx.aliyun.com/wanx"

    def __init__(self,
                 cookies_str: str = None,
                 cookies_dict: dict = None,
                 logger_obj: logging.Logger = None,
                 error_dir: str = None):
        """
        QwenWeb初始化
        :param cookies_str: cookies字符串
        :param cookies_dict: cookies字典
        :param logger_obj: 日志记录对象
        :param error_dir: 错误请求记录的保存目录，当出现请求失败时，会将关于该请求的URL、请求参数、响应数据整理成文件，存放于此目录
        """

        # 1. 日志记录对象
        if logger_obj:
            self.logger = logger_obj

        # 2. 错误请求记录的保存目录
        self.error_dir = error_dir

        # 3. 处理cookies
        if cookies_str and cookies_dict:
            self.logger.warning("cookies_str和cookies_dict同时传入；使用cookies_dict，cookies_str将失效")
        self.cookies_str = cookies_str
        self.cookies_dict = cookies_dict

        super().__init__()

        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/json",
            "referer": "https://wanx.aliyun.com/creation",
            "user-agent": self.user_agent,
            "x-xsrf-token": self.cookies_dict['XSRF-TOKEN'],
        }

        self.style_list = {
            "水彩": "<watercolor>",
            "油画": "<oil painting>",
            "中国风": "<chinese painting>",
            "扁平插画": "<flat illustration>",
            "二次元": "<anime>",
            "素描": "<sketch>",
            "3D卡通": "<3d cartoon>",
            "默认": "<auto>",
        }

    def get_style_list(self):
        """
        获取风格列表
        """

        for style in self.style_list.keys():
            print(style)

    def _get_task_id(self, prompt: str,
                     resolution: Literal["1024*1024", "1280*720", "720*1280"] = "1024*1024",
                     style: str = "默认", ):
        """
        提交会话任务，获取任务id
        :param prompt: (str)图片描述
        :param resolution: (str, optional)分辨率. Defaults to "1024*1024", 支持："1280*720", "720*1280"
        :param style: (str)图片风格
        :return: task_id (str)
        """

        if style not in self.style_list.keys():
            raise ValueError(f"【{style}】is not in style list!")

        style_code = self.style_list[style]

        request_data = {
            "taskType": "text_to_image",
            "taskInput": {
                "prompt": prompt,
                "style": style_code,
                "resolution": resolution
            }
        }

        resp = requests.post(
            url=self.api_base + "/imageGen",
            cookies=self.cookies_dict,
            headers=self.headers,
            data=json.dumps(request_data),
            timeout=10
        )

        resp_json = resp.json()

        if 'success' in resp_json and resp_json['success']:
            self.logger.info(f"提交绘图任务成功！")
        else:
            request_url = self.api_base + "/imageGen"
            request_data = json.dumps(request_data)
            request_response = resp.text

            all_data = f"{request_url}\n\n{request_data}\n\n{request_response}"
            file_path = self.save_bad_request_data('提交绘图任务-出现错误', all_data)
            self.logger.error(f"提交绘图任务出现错误，相关数据已写入【{file_path}】")

            raise RequestsError("functon [generate_image] got an unexpected response.")

        task_id = resp_json['data']
        return task_id

    def _get_latest_id(self):
        """
        获取最新任务id
        """

        request_data = {"taskTypes": ["image_variation", "style_transfer", "text_to_image"]}

        resp = requests.post(
            url=self.api_base + "/task/list",
            cookies=self.cookies_dict,
            headers=self.headers,
            data=json.dumps(request_data),
            timeout=10
        )

        if 'success' not in resp.json() or not resp.json()['success']:
            request_url = self.api_base + "/imageGen"
            request_data = json.dumps(request_data)
            request_response = resp.text

            all_data = f"{request_url}\n\n{request_data}\n\n{request_response}"
            file_path = self.save_bad_request_data('获取最新任务id-出现错误', all_data)
            self.logger.error(f"获取最新任务id出现错误，相关数据已写入【{file_path}】")
            raise RequestsError("functon [generate_image] got an unexpected response.")

        latest_id = resp.json()['data'][0]['id']
        return latest_id

    def generate_image(self,
                       prompt: str,
                       resolution: Literal["1024*1024", "1280*720", "720*1280"] = "1024*1024",
                       style: Literal[
                           "水彩", "油画", "中国风", "扁平插画", "二次元", "素描", "3D卡通", "默认"] = "默认",
                       total_timeout=120) -> list[WanXianImage]:
        """
        文生图功能主入口，根据描述词生成图片
        :param prompt: (str)图片描述
        :param resolution: (str, optional)分辨率. Defaults to "1024*1024", 支持："1280*720", "720*1280"
        :param style: (str)图片风格
        :param total_timeout: 最长等待时间
        :return:
        """

        task_id = self._get_task_id(prompt, resolution, style)

        latest_id = self._get_latest_id()

        now = int(time.time())
        # 检查结果
        while True:
            if int(time.time()) - now > total_timeout:
                raise TimeoutError

            resp = requests.post(
                url=self.api_base + "/taskResult",
                cookies=self.cookies_dict,
                headers=self.headers,
                data=json.dumps({
                    "id": latest_id,
                    "taskId": task_id
                }),
                timeout=10
            )

            response_data = resp.json()

            if 'success' in response_data and response_data['success']:

                if response_data['data']['status'] != 2:
                    continue

                image_list = response_data['data']['taskResult']
                images = []
                for image_dict in image_list:
                    image_obj = WanXianImage(
                        resource_id=image_dict.get("resourceId"),
                        oss_path=image_dict.get("ossPath"),
                        url=image_dict.get("url"),
                        resize_url=image_dict.get("resizeUrl"),
                        is_security=image_dict.get("isSecurity"),
                        task_id=image_dict.get("taskId"),
                        vague_url=image_dict.get("vagueUrl"),
                        download_url=image_dict.get("downloadUrl"),
                    )
                    images.append(image_obj)
                return images
