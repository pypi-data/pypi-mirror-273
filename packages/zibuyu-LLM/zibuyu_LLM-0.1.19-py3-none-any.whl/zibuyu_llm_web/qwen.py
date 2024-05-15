# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_LLM
author: 子不语
date: 2024/4/26
contact: 【公众号】思维兵工厂
description: 基于通义千问网页端逆向实现API调用，包括AI文档、文生图、文档问答
--------------------------------------------
"""

import os
import re
import traceback
import imghdr
import uuid
import json
import logging
import hashlib
from typing import Optional, Literal

import filetype
import requests

from .base import LLMBase
from .errors import RequestsError, InvalidFileError, NeedLoginError
from .types import QwenWebResponse, QwenChatContent, QwenPluginWebSearchResult, ReferenceLink, \
    QwenChatHistory, QwenSession, AiAnswer


class QwenWeb(LLMBase):
    """
    QwenWeb：通义千问web端
    """

    file_size_limit: int = 150 * 1024 * 1024  # 上传文档时，对单个文档的大小限制
    file_count_limit: int = 100  # 上传文档时，对文档数量的限制

    model_name = 'Qwen'

    api_base: str = "https://qianwen.biz.aliyun.com/dialog"

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

        if not cookies_str and not cookies_dict:
            raise ValueError("cookies_str和cookies_dict不能同时为空")

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

        # 4. 公用请求头
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Content-Type": "application/json",
            "Origin": "https://tongyi.aliyun.com",
            "Referer": "https://tongyi.aliyun.com/",
            "User-Agent": self.user_agent,
            "X-Platform": "pc_tongyi",
            "X-Xsrf-Token": self.cookies_dict['XSRF-TOKEN'],
        }

        self.parent_id: str = ''
        self.session_id: str = ''
        self.timeout: int = 60

        self.single_answer: str = ''  # 单次（最新）AI交互的回答
        self.single_answer_obj: Optional[QwenWebResponse] = None  # 单次（最新）AI交互的结果对象(QwenWebResponse)
        self.single_padding: str = ''  # 流式输出时，每次接收到的回答中的增量部分

    @property
    def random_str(self) -> str:
        """生成随机字符串，用作requestId"""

        request_id = uuid.uuid4().hex  # uuid无分隔符
        return request_id

    def check_file_list(self, file_path_list: list[str]):
        for file_path in file_path_list:

            self.logger.info(f"checking file: 【{file_path}】")

            # 检查文件是否存在
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"【{file_path}】 does not exist")

            # 检查文件大小是否超过限制
            if os.path.getsize(file_path) > self.file_size_limit:
                raise InvalidFileError(
                    f"【{file_path}】 size exceeds the limit of 【{self.file_size_limit / 1024 / 1024}】MB")

            self.logger.info(f"checking done: 【{file_path}】 ")

    def ask(
            self,
            question: str,
            callback_func=None,
            parent_id: str = '',
            session_id: str = '',
            image_path: str = None,
            image_url: str = None,
            file_path_list: list[str] = None,
            timeout: int = 60,
    ) -> AiAnswer:

        """
        获取AI回复
        :param question: 向AI发送的文本
        :param callback_func: 回调函数，处理流式输出中的增量文本
        :param parent_id: 上一次消息的id，与session_id一起保证对话的记忆
        :param session_id: 会话id，与parent_id一起保证对话的记忆
        :param image_path: 图片路径，需要是绝对路径
        :param image_url: 图片网络路径
        :param file_path_list: 文档路径列表，即可以上传多个文档。（需要是绝对路径）
        :param timeout: 请求超时时间
        :return:
        """

        # 文档问答和图片问答不能同时进行
        if (file_path_list and image_path) or (file_path_list and image_url):
            raise InvalidFileError("image and file cannot be set at the same time")

        # 本地图片和网络图片不能同时进行
        if image_path and image_url:
            raise InvalidFileError("image_path and image_url cannot be set at the same time")

        if not (parent_id is None) == (session_id is None):
            self.logger.error("parent_id and session_id have to be set at the same time", exc_info=True)
            raise InvalidFileError("parent_id and session_id have to be set at the same time")

        if session_id and parent_id:
            self.logger.info(f"parent_id：【{parent_id}】")
            self.logger.info(f"session_id：【{session_id}】")
        else:
            self.logger.info("parent_id and session_id are not set, using default values")

        self.parent_id = parent_id
        self.session_id = session_id

        self.timeout = timeout

        # 获取请求体数据
        data = self._get_request_data(
            question=question,
            image_path=image_path,
            image_url=image_url,
            file_path_list=file_path_list
        )

        # 获取请求头数据
        headers = self.headers.copy()
        headers['Accept'] = 'text/event-stream'

        resp = requests.post(
            url=self.api_base + "/conversation",
            cookies=self.cookies_dict,
            headers=headers,
            data=json.dumps(data),
            timeout=timeout,
            stream=True,
            verify=False,
        )

        index = 0
        pending = ""

        for chunk in resp.iter_lines(decode_unicode=True):

            if not chunk:
                continue

            index += 1
            chunk = str(chunk).strip()
            pending += chunk

            # Incomplete chunk
            if not chunk.endswith("}"):
                self.logger.debug("The chunk is incomplete.")
                continue

            self.logger.debug(f"The chunk is complete.")

            # Complete chunk
            try:
                pending = pending.split("\n")[-1]
                pending = pending[6:]

                resp_json = json.loads(pending)

                error_msg = resp_json.get("errorMsg")
                if not error_msg:
                    pass
                elif error_msg == 'NOT_LOGIN':
                    raise NeedLoginError("通义千问cookies过期，需要重新登录")
                else:
                    raise RequestsError("There is an error msg in received content.")

                pending = ""

                self.parent_id = resp_json["msgId"]
                self.session_id = resp_json.get("sessionId")

                content_list = resp_json.get("contents")

                if not content_list:
                    self.logger.info("This content_list is empty.")
                    continue

                msg_status = resp_json["msgStatus"]

                # 处理最后一帧：包含完整回复文本
                if msg_status == 'finished':

                    session_warn_new = resp_json.get("sessionWarnNew")
                    if session_warn_new:
                        self.logger.warning("sessionWarnNew为True。可能需要重置【parent_id】和【session_id】")
                        self.logger.info(f"收到的响应内容是：【{resp_json}】")

                    can_regenerate = resp_json["canRegenerate"]
                    if not can_regenerate:
                        self.logger.warning("canRegenerate为False。可能需要重置【parent_id】和【session_id】")
                        self.logger.info(f"收到的响应内容是：【{resp_json}】")

                    self.single_answer_obj = QwenWebResponse(
                        msg_status=msg_status,
                        web_search_list=[],
                        content_list=[],
                        reference_link_list=[],
                        image_url_list=[],
                        can_regenerate=can_regenerate,
                        session_warn_new=session_warn_new,

                        msg_id=resp_json.get("msgId"),
                        parent_msg_id=resp_json.get("parentMsgId"),
                        session_id=resp_json.get("sessionId"),
                        params=resp_json.get("params"),
                        stop_reason=resp_json.get("stopReason"),
                        trace_id=resp_json.get("traceId"),
                        content_type=resp_json.get("contentType"),
                        content_from=resp_json.get("contentFrom"),
                        ai_disclaimer=resp_json.get("aiDisclaimer"),
                        can_share=resp_json.get("canShare"),
                        can_show=resp_json.get("canShow"),
                        can_feedback=resp_json.get("canFeedback"),
                        session_share=resp_json.get("sessionShare"),
                        session_open=resp_json.get("sessionOpen"),
                    )

                    for content_dict in content_list:
                        content_type = content_dict["contentType"]
                        if content_type == 'text':
                            self.handle_response_text(content_dict)
                        elif content_type == 'text2image':
                            self.handle_response_text2image(content_dict)
                        elif content_type == 'plugin':
                            self.handle_response_plugin(content_dict)
                        elif content_type == 'referenceLink':
                            self.handle_response_reference_link(content_dict)

                    if index == 1 and callable(callback_func):
                        callback_func(self.single_answer)

                    if callable(callback_func):
                        callback_func('<<<end>>>')

                else:  # 处理中间帧数据，部分文本
                    if not callable(callback_func):
                        continue

                    for content_dict in content_list:

                        content_type = content_dict["contentType"]

                        # 中间帧只处理文本
                        if content_type != 'text':
                            continue

                        text = content_dict["content"]

                        self.single_padding = text.replace(self.single_answer, "")
                        callback_func(self.single_padding)
                        self.single_answer = text
            except NeedLoginError:

                raise NeedLoginError('cookies过期，需要重新登录')
            except RequestsError:

                request_url = self.api_base + "/conversation"
                request_data = json.dumps(data)
                request_response = pending
                traceback_info = f"\n--- Error Log Entry ---\n{traceback.format_exc()}\n--- End of Entry ---\n"

                all_data = f"{request_url}\n\n{request_data}\n\n{request_response}\n\n{traceback_info}"
                file_path = self.save_bad_request_data('AI交互请求-官方提示错误', all_data)

                self.logger.error(f"AI交互请求出现官方提示错误，相关数据已写入【{file_path}】", exc_info=True)
            except Exception:

                request_url = self.api_base + "/conversation"
                request_data = json.dumps(data)
                request_response = pending
                traceback_info = f"\n--- Error Log Entry ---\n{traceback.format_exc()}\n--- End of Entry ---\n"

                all_data = f"{request_url}\n\n{request_data}\n\n{request_response}\n\n{traceback_info}"
                file_path = self.save_bad_request_data('AI交互请求-出现未知错误', all_data)

                self.logger.error(f"AI交互请求出现未知错误，相关数据已写入【{file_path}】", exc_info=True)

        answer = AiAnswer(
            content=self.single_answer,
            latest_msg_id=self.parent_id,
            conversation_id=self.session_id,
            reference_link_list=self.single_answer_obj.reference_link_list
        )

        return answer

    def upload(self, file_name: str, file_byte_data: bytes, file_type: str,
               upload_type: Literal['image', 'file'] = 'image'):

        # 获取上传链接
        upload_token = self._get_upload_token()

        files_data = {
            "OSSAccessKeyId": (None, upload_token["data"]["accessId"]),
            "policy": (None, upload_token["data"]["policy"]),
            "signature": (None, upload_token["data"]["signature"]),
            "key": (None, upload_token["data"]["dir"] + file_name),
            "dir": (None, upload_token["data"]["dir"]),
            "success_action_status": (None, "200"),
            "file": (file_name, file_byte_data, file_type)
        }

        headers = self.headers.copy()
        headers.pop("Content-Type")

        # 发送上传请求
        resp = requests.post(
            url=upload_token["data"]["host"] + "/",
            data=None,
            files=files_data,
            headers=headers,
            cookies=self.cookies_dict
        )

        if resp.status_code == 200:

            # 获取下载链接
            if upload_type == 'image':
                data_dict = self._get_download_link_image(upload_token, file_name)
            elif upload_type == 'file':
                data_dict = self._get_download_link_file(upload_token, file_name)
            else:
                raise Exception("upload error")

            return data_dict
        else:

            files_data['file'] = '【这里是二进制数据，写入文件时去除了】'

            request_url = upload_token["data"]["host"] + "/"
            request_data = json.dumps(files_data)
            request_response = '这个请求不需要返回'

            all_data = f"{request_url}\n\n{request_data}\n\n{request_response}"
            file_path = self.save_bad_request_data('上传文件-出现未知错误', all_data)

            self.logger.error(f"上传文件时出现未知错误，相关数据已写入【{file_path}】", exc_info=True)

            raise RequestsError(f"function [upload] got an unexpected response. Status Code: {resp.status_code}")

    def upload_file(self, file_path: str) -> dict:
        """
        上传文档
        :param file_path:
        :return:
        """

        # 判断文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found")

        with open(file_path, 'rb') as f:
            file = f.read()
            file_size = os.path.getsize(file_path)

        # 判断文件大小
        if file_size > self.file_size_limit:
            raise InvalidFileError(f"文件大小不能超过【{self.file_size_limit // 1024 // 1024}】M")

        file_name = os.path.basename(file_path)
        file_type = os.path.splitext(file_path)[1].strip(".")

        error_msg = "不支持的文件类型，目前仅支持【txt,mobi,markdown,word,excel,mobi,epub】"

        if file_type not in ["txt", "mobi", "markdown", "word", "excel", "mobi", "epub"]:
            raise InvalidFileError(error_msg)

        if file_type in ["markdown", "mobi"]:
            file_type = 'application/octet-stream'
        elif file_type == "txt":
            file_type = 'text/plain'
        else:
            file_type = filetype.guess_mime(file)

            if file_type is None:
                raise InvalidFileError("文件类型失败")

            allow_file = False

            if '/pdf' in file_type:
                allow_file = True
            elif 'openxmlformats-officedocument' in file_type:
                allow_file = True
            elif 'epub+zip' in file_type:
                allow_file = True

            if not allow_file:
                raise InvalidFileError(error_msg)

        data = self.upload(file_name, file, file_type, upload_type='file')
        data['file_size'] = file_size
        return data

    def upload_image(self, image_path: str = None, image_url: str = None) -> dict:
        """
        上传图片
        :param image_path: 图片本地路径
        :param image_url: 图片网络地址和
        :return:
        """

        if image_path:
            # 判断图片是否存在
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"{image_path} not found")

            with open(image_path, 'rb') as f:
                image = f.read()
        else:
            image = requests.get(image_url).content
            image_type = imghdr.what(None, image)
            if not image_type:
                self.logger.error(f"传入的image_url存在问题，可能非图片。【{image_url}】")
                raise InvalidFileError("invalid file")

            self.logger.info(f"图像数据为二进制，并且格式为: {image_type}")

        # 类型及名称
        file_type = filetype.guess_mime(image)
        if "image/" not in file_type:
            raise InvalidFileError("invalid file")
        file_name = "image-" + hashlib.md5(image).hexdigest() + "." + file_type[6:]

        data_dict = self.upload(file_name, image, file_type, upload_type='image')

        return data_dict

    def _get_request_data(
            self,
            question: str,
            image_path: str = None,
            image_url: str = None,
            file_path_list: list[str] = None,
    ):

        data = {
            "action": "next",  # 尚未知晓作用
            "contents": [
                {
                    "contentType": "text",
                    "content": question,
                    "role": "user"
                },
            ],
            "mode": "chat",
            "model": "",
            "requestId": self.random_str,
            "parentMsgId": self.parent_id,
            "sessionId": self.session_id,
            "sessionType": "text_chat" if not image_path else "image_chat",
            "userAction": "chat" if self.session_id and self.parent_id else "new_top"
        }

        if image_path:
            self.logger.info("This is a image chat.")

            data_dict = self.upload_image(image_path=image_path)

            data["contents"].append({
                "contentType": "image",
                "content": data_dict['url'],
                "role": "user"
            })
        elif image_url:
            self.logger.info("This is a image chat.")

            data_dict = self.upload_image(image_url=image_url)

            data["contents"].append({
                "contentType": "image",
                "content": data_dict['url'],
                "role": "user"
            })
        elif file_path_list:
            self.logger.info("This is a file chat.")
            self.logger.info(f"There are {len(file_path_list)} files")

            self.check_file_list(file_path_list)

            for file_path in file_path_list:
                data_dict = self.upload_file(file_path)
                item = {
                    "contentType": "file",
                    "content": data_dict['url'],
                    "role": "user",
                    "ext": {
                        "fileSize": data_dict['file_size'],
                        "docId": data_dict['doc_id'],
                    }
                }
                # noinspection PyTypeChecker
                data["contents"].append(item)
        else:
            self.logger.info("This is a text chat.")

        return data

    def _get_upload_token(self) -> dict:
        """
        获取上传token
        :return:
        """

        resp = requests.post(
            url=self.api_base + "/uploadToken",
            headers=self.headers,
            cookies=self.cookies_dict,
            data=json.dumps({})
        )
        resp_json = resp.json()

        if 'success' in resp_json and resp_json['success']:
            return resp_json
        else:

            request_url = self.api_base + "/uploadToken"
            request_data = json.dumps({})
            request_response = resp_json

            all_data = f"{request_url}\n\n{request_data}\n\n{request_response}"
            file_path = self.save_bad_request_data('获取上传文件的token-出现未知错误', all_data)

            self.logger.error(f"获取上传文件的token请求，出现未知错误，相关数据已写入【{file_path}】", exc_info=True)

            # 抛出错误，程序终止
            raise RequestsError("function 【_get_upload_token】got an unexpected response.")

    def _get_download_link_image(self, upload_token: dict, file_name: str) -> dict:
        """
        上传图片之后，获取图片链接
        :param upload_token:
        :param file_name:
        :return:
        """

        request_data = {
            "dir": upload_token["data"]["dir"],
            "fileKey": file_name,
            "fileType": "image"
        }

        resp = requests.post(
            url=self.api_base + "/downloadLink",
            headers=self.headers,
            cookies=self.cookies_dict,
            data=json.dumps(request_data)
        )

        resp_json = resp.json()

        if 'success' in resp_json and resp_json['success']:
            return {"url": resp_json["data"]["url"]}
        else:

            request_url = upload_token["data"]["host"] + "/"
            request_data = json.dumps(request_data)
            request_response = resp.text

            all_data = f"{request_url}\n\n{request_data}\n\n{request_response}"
            file_path = self.save_bad_request_data('获取图片链接-出现未知错误', all_data)
            self.logger.error(f"获取图片链接时出现未知错误，相关数据已写入【{file_path}】")

            raise RequestsError("function [_get_download_link_image] got an unexpected response.")

    def _get_download_link_file(self, upload_token: dict, file_name: str) -> dict:
        """
        上传文档之后，获取文档链接
        :param upload_token:
        :param file_name:
        :return:
        """

        request_data = {
            "dir": upload_token["data"]["dir"],
            "fileKeys": [file_name, ],
            "fileType": "file"
        }

        resp = requests.post(
            url=self.api_base + "/downloadLink/batch",
            headers=self.headers,
            cookies=self.cookies_dict,
            data=json.dumps(request_data)
        )

        resp_json = resp.json()

        if 'success' in resp_json and resp_json['success']:
            results = resp_json["data"]["results"]

            doc_id = results[0]["docId"]
            url = results[0]["url"]
            return {"url": url, "doc_id": doc_id}
        else:

            request_url = self.api_base + "/downloadLink/batch"
            request_data = json.dumps(request_data)
            request_response = resp.text

            all_data = f"{request_url}\n\n{request_data}\n\n{request_response}"
            file_path = self.save_bad_request_data('获取文档链接-出现未知错误', all_data)
            self.logger.error(f"获取文档链接时出现未知错误，相关数据已写入【{file_path}】")

            raise RequestsError("function [_get_download_link_file] got an unexpected response.")

    def handle_response_text(self, data: dict):
        """
        处理回复内容中的AI生成文本
        :param data:
        :return:
        """

        if '抱歉，系统超时，请稍后重试' in data.get('content'):
            return

        content_obj = QwenChatContent(
            id=data.get("id"),
            role=data.get("role"),
            status=data.get("status"),
            content=data.get("content"),
            content_type=data.get("contentType"),
        )
        self.single_answer = data.get("content")
        self.single_answer_obj.content_list.append(content_obj)

    def handle_response_plugin(self, data: dict):
        """
        处理回复内容中的插件结果。
        目前发现两个插件：互联网信息搜索 + 智文文档搜索
        :param data:
        :return:
        """

        plugin_name = data.get("pluginName")
        plugin_code = data.get("pluginCode")
        content = data.get("content")

        # 判断是否为文档检索插件
        if plugin_code == 'zhiwen_doc_search' and plugin_name == '智文文档搜索':
            # TODO 后续需要添加文档问答处理逻辑
            pass

        # 判断是否为网页搜索插件
        if plugin_code == 'tongyi_nlp_web_search' and plugin_name == '互联网信息搜索':

            plugin_result_dict = json.loads(content)
            plugin_result_list = json.loads(plugin_result_dict["pluginResult"])

            for item in plugin_result_list:
                url = item["url"]

                if url == 'expired_url':
                    continue

                obj = QwenPluginWebSearchResult(
                    url=item["url"],
                    title=item["title"],
                    body=item["body"],
                    time=item["time"],
                    host_name=item["host_name"],
                    host_logo=item["host_logo"],
                )
                self.single_answer_obj.web_search_list.append(obj)

        content_obj = QwenChatContent(
            id=data["id"],
            role=data["role"],
            status=data["status"],
            content_type=data.get("contentType"),
            content=content,
            plugin_code=plugin_code,
            plugin_name=plugin_name
        )

        self.single_answer_obj.content_list.append(content_obj)

    def handle_response_reference_link(self, data: dict):
        """
        处理回复内容中记录的相关链接
        :param data:
        :return:
        """

        content = data["content"]
        reference_link_list = json.loads(content)['links']

        for item in reference_link_list:
            obj = ReferenceLink(
                url=item["url"],
                title=item["title"],
            )
            self.single_answer_obj.reference_link_list.append(obj)

        content_obj = QwenChatContent(
            id=data["id"],
            role=data["role"],
            status=data["status"],
            content=data["content"],
            content_type=data.get("contentType")
        )

        self.single_answer_obj.content_list.append(content_obj)

    def handle_response_text2image(self, data: dict):
        """
        文生图中，处理回复内容中的图片链接
        :param data:
        :return:
        """

        self.handle_response_text(data)

        content = data["content"]

        re_path = r"!\[.*\]\((https:\/\/.*?)\)"

        result = re.findall(re_path, content)

        if not result:
            self.logger.warning("AI交互中包含text2image字段，但未找到图片链接，可能是匹配正则出了问题")
            self.logger.info(f"用于匹配图片的正则表达式是：【{re_path}】")
            self.logger.info(f"响应的内容是：【{content}】")
            return

        image_url_list = []
        for url in result:
            image_url_list.append(url)

        self.single_answer_obj.image_url_list = image_url_list

    def get_session_history(self, session_id: str) -> list[QwenChatHistory]:
        """
        根据session_id获取历史会话
        :param session_id:
        :return:
        """

        try:
            resp = requests.post(
                url=self.api_base + "/chat/list",
                cookies=self.cookies_dict,
                headers=self.headers,
                data=json.dumps({
                    "sessionId": session_id
                })
            ).json()
            if 'success' in resp and resp['success']:
                history = []
                for content in resp["data"]:
                    content_list = content.get('contents')
                    chat_list = []
                    for con in content_list:
                        content_type = con.get('contentType')

                        if content_type == 'file':

                            ext = con.get('ext')
                            file_size = ext['fileSize']
                            doc_id = ext['docId']
                        else:
                            file_size = 0
                            doc_id = ''

                        content_obj = QwenChatContent(
                            id=con.get('id'),
                            role=con.get('role'),
                            status=con.get('status'),
                            content=con.get('content'),
                            content_type=content_type,
                            file_size=file_size,
                            doc_id=doc_id
                        )
                        chat_list.append(content_obj)

                    history_obj = QwenChatHistory(
                        sender_type=content.get('senderType'),  # 发送者，用以区分用户与AI
                        create_time=content.get('createTime'),  # 创建时间
                        content_type=content.get('contentType'),  # 消息类型

                        session_id=content.get('sessionId'),
                        msg_id=content.get('msgId'),
                        parent_msg_id=content.get('parentMsgId'),

                        msg_status=content.get('msgStatus'),  # 会话状态：是否完整生成

                        content_list=chat_list,

                        interrupted=content.get('interrupted'),  # AI生成内容时是否被打断
                        ai_disclaimer=content.get('aiDisclaimer'),
                        can_regenerate=content.get('canRegenerate'),
                        can_share=content.get('canShare'),
                        can_show=content.get('canShow'),
                    )
                    history.append(history_obj)

                return history
            else:

                request_url = self.api_base + "/chat/list"
                request_data = json.dumps({
                    "sessionId": session_id
                })
                request_response = resp.text

                all_data = f"{request_url}\n\n{request_data}\n\n{request_response}"
                file_path = self.save_bad_request_data('获取历史会话失败', all_data)
                self.logger.error(f"获取历史会话失败，相关数据已写入【{file_path}】")

        except Exception:
            self.logger.error("get_session_history failed", exc_info=True)

    def get_session_list(self) -> list[QwenSession]:
        """
        获取账号的会话列表
        :return:
        """

        try:
            self.logger.info("获取账号的会话列表")

            resp = requests.post(
                url=self.api_base + "/session/list",
                cookies=self.cookies_dict,
                headers=self.headers,
                json={
                    "keyword": ""
                },
                timeout=10
            )

            resp_json = resp.json()

            if 'success' in resp_json and resp_json['success']:
                session_list = []
                for item in resp_json['data']:
                    session_obj = QwenSession(
                        user_id=item.get('userId'),
                        session_id=item.get('sessionId'),
                        create_time=item.get('createTime'),
                        modified_time=item.get('modifiedTime'),
                        summary=item.get('summary'),
                        session_type=item.get('sessionType'),
                        error_msg=item.get('errorMsg'),
                        status=item.get('status'),
                        can_share=item.get('canShare'),
                    )
                    session_list.append(session_obj)
                self.logger.info(f"获取账号的会话列表成功，共{len(session_list)}个会话")
                return session_list
            else:

                request_url = self.api_base + "/session/list"
                request_data = json.dumps({
                    "keyword": ""
                })
                request_response = resp.text

                all_data = f"{request_url}\n\n{request_data}\n\n{request_response}"
                file_path = self.save_bad_request_data('获取会话列表失败', all_data)
                self.logger.error(f"获取会话列表失败，相关数据已写入【{file_path}】")

        except:
            self.logger.error("get_session_list failed", exc_info=True)

    def delete_session(self, session_id: str) -> bool:
        """
        根据session_id删除会话
        :param session_id:
        :return:
        """

        try:
            resp = requests.post(
                url=self.api_base + "/session/delete",
                cookies=self.cookies_dict,
                headers=self.headers,
                data=json.dumps({
                    "sessionId": session_id
                }),
                timeout=10
            ).json()

            if 'success' in resp and resp['success']:
                self.logger.info(f"删除会话成功！session_id：【{session_id}】")
                return True
            else:
                request_url = self.api_base + "/session/delete"
                request_data = json.dumps({
                    "sessionId": session_id
                })
                request_response = resp.text

                all_data = f"{request_url}\n\n{request_data}\n\n{request_response}"
                file_path = self.save_bad_request_data('获取删除会话失败', all_data)
                self.logger.error(f"获取删除会话失败，相关数据已写入【{file_path}】")
                return False
        except:
            self.logger.error("delete_session unknown error", exc_info=True)
            return False

    def rename_session(self, session_id: str, summary: str) -> bool:
        """
        根据session_id重命名会话
        :param session_id:
        :param summary:
        :return:
        """

        try:
            self.logger.info("根据session_id重命名会话")

            resp = requests.post(
                url=self.api_base + "/session/update",
                cookies=self.cookies_dict,
                headers=self.headers,
                data=json.dumps({
                    "sessionId": session_id,
                    "summary": summary
                }),
                timeout=10
            ).json()

            if 'success' in resp and resp['success']:
                self.logger.info(f"重命名会话成功！session_id：【{session_id}】，summary：【{summary}】")
                return True
            else:
                request_url = self.api_base + "/session/update"
                request_data = json.dumps({
                    "sessionId": session_id,
                    "summary": summary
                })
                request_response = resp.text

                all_data = f"{request_url}\n\n{request_data}\n\n{request_response}"
                file_path = self.save_bad_request_data('重命名会话失败', all_data)
                self.logger.error(f"重命名会话失败，相关数据已写入【{file_path}】")
                return False
        except:
            self.logger.error("function [rename_session] got an unknown error.", exc_info=True)
            return False
