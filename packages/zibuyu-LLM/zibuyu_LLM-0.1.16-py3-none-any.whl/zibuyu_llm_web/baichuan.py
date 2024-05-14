# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_LLM
author: 子不语
date: 2024/4/28
contact: 【公众号】思维兵工厂
description: 逆向百川大模型。

逆向尚未完成文件上传部分。
该平台的cookies有效期是一个月
--------------------------------------------
"""

import json
import logging
from typing import Optional

from .base import LLMBase
from .errors import NeedLoginError
from .types import BaiChuanSession, BaiChuanChat, AiAnswer


class BaiChuanWeb(LLMBase):
    """
    百川大模型Web版调用
    """

    model_name = 'BaiChuan'

    base_host = 'https://www.baichuan-ai.com'

    def __init__(
            self,
            cookies_str: str = None,
            cookies_dict: dict = None,
            logger_obj: logging.Logger = None,
            error_dir: str = None
    ):
        """
        QwenWeb初始化
        :param cookies_str: cookies字符串
        :param cookies_dict: cookies字典
        :param logger_obj: 日志记录对象
        :param error_dir: 错误请求记录的保存目录，当出现请求失败时，会将关于该请求的URL、请求参数、响应数据整理成TXT文件，存放于此目录
        """

        if not cookies_str and not cookies_dict:
            raise ValueError("cookies_str和cookies_dict不能同时为空")

        # 1. 日志记录对象
        if logger_obj:
            self.logger = logger_obj

        # 2. 错误请求记录的保存目录
        self.error_dir = error_dir

        self.cookies_str = cookies_str
        self.cookies_dict = cookies_dict

        super().__init__()

        self.headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "User-Agent": self.user_agent,
            "Cookie": self.cookies_str,
            "Connection": "keep-alive"
        }

        self.history: list = []
        self.single_answer: str = ""
        self.single_answer_obj: Optional[AiAnswer] = None
        self.input_tokens: int = 0
        self.output_tokens: int = 0
        self.request_session.cookies.update(self.cookies_dict)

    def ask(
            self,
            question: str,
            parent_id: str = None,
            session_id: str = None,
            callback_func=None,
    ) -> AiAnswer:
        """
        提问
        :param question: 问题
        :param parent_id: 上一次会话的id，用来确保上下文
        :param session_id: 会话窗口的id，用来确保上下文
        :param callback_func: 回调函数
        :return: 回答
        """

        uri = "/api/chat/v1/chat"

        payload = {
            "app_info": {
                "id": 10001,  # 固定值
                "name": 'baichuan_web',  # 固定值
            },
            "type": "input",  # 固定值
            "stream": True,  # 固定值：是否流式输出
            "prompt": {
                "id": '',
                "messageId": '',
                "from": 0,
                "parent_id": parent_id,
                "data": question,
            },
            "session_info": {
                "id": session_id,
                "name": '',
                "created_at": 0,
            },
            "parameters": {
                "repetition_penalty": -1,
                "temperature": -1,
                "top_k": -1,
                "top_p": -1,
                "max_new_tokens": -1,
                "do_sample": -1,
                "regenerate": 0
            },
            "history": self.history,  # 历史会话信息
            "retry": 3  # 固定值
        }

        response = self.request_session.post(
            self.base_host + uri,
            json=payload,
            headers=self.headers,
            stream=True
        )

        pending = ""
        for chunk in response.iter_lines(decode_unicode=True):

            if not chunk:
                continue

            # 正常AI交互时接收的是bytes类型数据，如果出现str类型数据，说明cookies过期或cookies不合法
            # if isinstance(chunk, bytes):
            #     print('接收到bytes数据')

            if isinstance(chunk, str):
                self.logger.error("cookies过期，需要重新登录")
                raise NeedLoginError("cookies过期，需要重新登录")

            chunk_str = chunk.decode().strip()
            pending += chunk_str

            # Incomplete chunk
            if not chunk_str.endswith("}"):
                self.logger.debug("The chunk is incomplete.")
                continue

            self.logger.debug(f"Receive a chunk and this chunk is complete.")

            resp_json = json.loads(pending)
            pending = ''

            if 'answer' not in resp_json:
                continue

            answer_chunk = resp_json.get("answer", {}).get("data", "")
            self.single_answer += answer_chunk

            if callable(callback_func):
                try:
                    callback_func(answer_chunk)
                    self.logger.debug(f"{callback_func.__name__} be executed successfully.")
                except:
                    pass

            if 'usage' in resp_json:
                self.input_tokens += resp_json.get("usage", {}).get("prompt_tokens", 0)
                self.output_tokens += resp_json.get("usage", {}).get("answer_tokens", 0)

        self.history.append({"from": 0, "data": question})
        self.history.append({"from": 1, "data": self.single_answer})

        self.single_answer_obj = AiAnswer(
            is_success=True,
            content=self.single_answer
        )

        return self.single_answer_obj

    def get_session_list(self, page: int = 1, limit: int = 50) -> list[BaiChuanSession]:

        uri = '/api/session/get'

        params = {
            "page": page,
            "limit": limit,
        }

        result = self.request_session.get(
            self.base_host + uri,
            params=params,
            headers=self.headers
        )

        data = result.json()
        code = data.get("code")

        if code != 200:
            self.logger.error(f"获取会话列表失败，错误码：{code}")

        session_list = []
        data = data.get("data", {})
        for session in data:
            session_obj = BaiChuanSession(**session)
            session_list.append(session_obj)

        return session_list

    def get_history(self, session_id: str) -> list[BaiChuanChat]:
        # TODO 待完成

        uri = '/api/message/messages'

        result = self.request_session.post(
            self.base_host + uri,
            json={"sessionId": session_id},
            headers=self.headers
        )

        resp_data = result.json()

        code = resp_data.get("code")

        if code != 200:
            self.logger.error(f"获取会话历史记录失败，错误码：{code}")
            return []

        data = resp_data.get("data", [])
        chat_list = []
        for chat in data:
            chat_obj = BaiChuanChat(**chat)
            chat_list.append(chat_obj)

        return chat_list
