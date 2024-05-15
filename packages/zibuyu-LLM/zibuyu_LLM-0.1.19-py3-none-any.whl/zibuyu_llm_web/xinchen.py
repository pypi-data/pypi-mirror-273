# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_LLM
author: 子不语
date: 2024/4/28
contact: 【公众号】思维兵工厂
description: 通义星辰web端逆向。


逆向未完全，目前仅实现了与角色的通讯功能，
--------------------------------------------
"""

import json
import logging
import traceback
from typing import Optional

from .base import LLMBase
from .errors import NeedLoginError
from .types import XincChatHistory, XincChatContent, XincMessageIssuer, XincCharacterInfo, XincCharacter, AiAnswer


class XinChenWeb(LLMBase):
    model_name = 'XinChen'

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

        self.request_session.cookies.update(self.cookies_dict)

        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://xingchen.aliyun.com",
            "Referer": "https://xingchen.aliyun.com/xingchen/chat/",
            "User-Agent": self.user_agent,
        }

        self.last_message_id: str = ''  # 上一条消息ID
        self.session_id: str = ''  # 聊天会话ID
        self.character_pk: str = ''  # 角色ID
        self.character_name: str = ''  # 角色名称

        self.single_answer: str = ''  # 流式输出时，累计回复文本
        self.single_answer_obj: Optional[AiAnswer] = None
        self.answer_padding: str = ''  # 流式输出时，每一次的增量文本

    def ask(
            self, prompt: str,
            character_id: str,
            session_id: str = '',
            last_message_id: str = '',
            callback_func=None,
    ) -> AiAnswer:

        host = 'https://xingchen.aliyun.com/api/chat/message/send'

        data = {
            "characterId": character_id,
            "chatRoomId": 1060840,
            "sessionId": session_id,
            "content": prompt,
            "lastMessageId": last_message_id,
            "streaming": True,
            "generateImg": True,
            "generateAsr": True
        }

        headers = self.headers.copy()
        headers['Accept'] = 'text/event-stream'

        response = self.request_session.post(
            host,
            json=data,
            headers=headers,
            stream=True,
            verify=False
        )

        index: str = ''  # 索引
        event: str = ''
        for chunk in response.iter_lines():

            if not chunk:
                continue

            try:
                chunk_str = chunk.decode('utf-8').strip()

                if 'need login' in chunk_str:
                    raise NeedLoginError("cookies过期，需要重新登录")

                content_header, content = [i.strip() for i in chunk_str.split(':', maxsplit=1)]

                if content_header == 'id':
                    index = content
                    self.logger.debug(f"即将接收第【{index}】次数据传送")
                    continue
                elif content_header == 'event':
                    self.logger.debug(f"数据状态：【{content}】")
                    event = content
                    continue
                elif content_header == 'data':
                    single_receive_data = content
                    self.logger.debug(f"接收到第【{index}】数据：【{single_receive_data}】")
                else:
                    raise Exception("响应数据异常，需要重新逆向！")

                content_dict = json.loads(single_receive_data)

                response_content_list = content_dict['choices'][0]['messages']

                if len(response_content_list) == 1:
                    new_content = response_content_list[0]['content']
                    self.answer_padding = new_content.replace(self.single_answer, '')
                    self.single_answer = new_content

                    if callback_func:
                        try:
                            callback_func(self.single_answer, self.answer_padding)
                            self.logger.debug(f"回调函数【{callback_func.__name__}】执行成功")

                            if event == 'stop':
                                callback_func('<<<<end>>>>', '<<<<end>>>>')

                        except:
                            self.logger.error(f"回调函数【{callback_func.__name__}】执行失败")
                            self.logger.error(traceback.format_exc())
                else:
                    all_data = f"响应数据中，messages个数大于1\n\n\n{json.dumps(response_content_list)}"
                    file_path = self.save_bad_request_data('出现新情况', all_data)
                    self.logger.warning("出现新情况：响应数据中，messages个数大于1")
                    self.logger.info(f"相关情况已记录于【{file_path}】")

                self.last_message_id: str = content_dict.get('context', {}).get('answerId')
                self.session_id: str = content_dict.get('context', {}).get('sessionId')
                self.character_pk: str = content_dict.get('context', {}).get('characterPk')
                self.character_name: str = content_dict.get('context', {}).get('characterName')

            except NeedLoginError:
                raise NeedLoginError('cookies过期，需要重新登录')

            except:

                request_response = f"【第{index}次回复】：\n\n{chunk}"
                traceback_info = f"\n--- Error Log Entry ---\n{traceback.format_exc()}\n--- End of Entry ---\n"

                all_data = f"{host}\n\n{json.dumps(data)}\n\n{request_response}\n\n{traceback_info}"
                file_path = self.save_bad_request_data('AI交互出现未知错误', all_data)

                self.logger.error(f"AI交互出现未知错误，请求相关数据已保存于：{file_path}")

        self.single_answer_obj = AiAnswer(
            is_success=True,
            content=self.single_answer
        )
        return self.single_answer_obj

    def get_history(self, chat_room_id: str) -> XincChatHistory:
        """
        根据room_id获取会话历史
        """

        host = "https://xingchen.aliyun.com/api/chat/message/histories"
        headers = self.headers.copy()
        data = {
            "where": {"chatRoomId": chat_room_id},
            "pageSize": 100,
            "pageNum": 1,
            "orderBy": ["gmtCreate desc", "createTimestamp desc"]
        }
        response = self.request_session.post(host,
                                             json=data,
                                             headers=headers)

        try:
            json_resp = response.json()

            if json_resp['code'] != 200:
                raise Exception(f"请求失败，返回状态码：{json_resp['code']}")
            data = json_resp['data']
            content_list = data['list']
            self.logger.debug(f"获取会话历史记录成功，共{len(content_list)}条记录")

            content_obj_list = []
            for content_dict in content_list:
                content_obj = XincChatContent(
                    chat_id=content_dict['chatId'],
                    original_content=content_dict['content'],
                    create_timestamp=content_dict['createTimestamp'],
                    gmt_create=content_dict['gmtCreate'],
                    is_greeting=content_dict['isGreeting'],
                    message_id=content_dict['messageId'],
                    message_type=content_dict['messageType'],
                    session_id=content_dict['sessionId'],
                    message_issuer=XincMessageIssuer(
                        user_id=content_dict['messageIssuer']['userId'],
                        user_name=content_dict['messageIssuer']['userName'],
                        user_type=content_dict['messageIssuer']['userType']
                    )
                )
                content_obj_list.append(content_obj)
            history_obj = XincChatHistory(
                content_list=content_obj_list,
                total=data['total']
            )
            return history_obj
        except:
            request_response = response.content
            traceback_info = f"\n--- Error Log Entry ---\n{traceback.format_exc()}\n--- End of Entry ---\n"

            all_data = f"{host}\n\n{json.dumps(data)}\n\n{request_response}\n\n{traceback_info}"
            file_path = self.save_bad_request_data('获取会话历史记录时出现未知错误', all_data)

            self.logger.error(f"获取会话历史记录时出现未知错误，请求相关数据已保存于：{file_path}")

    def add_session(self, character_id: str, version: int = 1) -> str:
        """
        对同一个角色，只能创建一个会话；多次创建返回相同的room_id
        """

        host = "https://xingchen.aliyun.com/api/chat/character/add?token=undefined"
        data = {"characterId": character_id, "version": version}
        headers = self.headers.copy()
        response = self.request_session.post(host,
                                             json=data,
                                             headers=headers, verify=False, )

        try:
            json_resp = response.json()

            self.logger.debug(f"添加会话成功，响应数据【{response.text}】")

            if json_resp['code'] != 200:
                raise Exception(f"请求失败，返回状态码：{json_resp['code']}")

            self.logger.debug(f"添加会话成功")

            room_id = json_resp['data']

            return room_id
        except:
            request_response = response.content
            traceback_info = f"\n--- Error Log Entry ---\n{traceback.format_exc()}\n--- End of Entry ---\n"
            all_data = f"{host}\n\n{json.dumps(data)}\n\n{request_response}\n\n{traceback_info}"
            file_path = self.save_bad_request_data('添加会话时出现未知错误', all_data)
            self.logger.error(f"添加会话时出现未知错误，请求相关数据已保存于：{file_path}")

    def get_character_info(self, room_id: str) -> XincCharacterInfo:
        """
        获取角色信息
        """

        host = f"https://xingchen.aliyun.com/api/chat/room/{room_id.strip()}"
        response = self.request_session.get(host, headers=self.headers)
        try:
            json_resp = response.json()

            status_code = json_resp['code']
            if status_code != 200:
                self.logger.error(f"获取角色信息失败，返回状态码：{status_code}")
                raise Exception(f"获取角色信息失败，返回状态码：{status_code}")

            data = json_resp['data']

            characters_list = data['characters']

            character_obj_list = []

            for character in characters_list:
                character_obj = XincCharacter(
                    name=character['name'],
                    characterId=character['characterId']
                )
                character_obj_list.append(character_obj)

            chat_history_list = data['histories']
            chat_history_obj_list = []
            for chat_history in chat_history_list:
                chat_history_obj = XincChatContent(
                    chat_id=chat_history['chatId'],
                    original_content=chat_history['content'],
                    create_timestamp=chat_history['createTimestamp'],
                    gmt_create=chat_history['gmtCreate'],
                    is_greeting=chat_history['isGreeting'],
                    message_id=chat_history['messageId'],
                    message_type=chat_history['messageType'],
                    session_id=chat_history['sessionId'],
                    message_issuer=XincMessageIssuer(
                        user_id=chat_history['messageIssuer']['userId'],
                        user_name=chat_history['messageIssuer']['userName'],
                        user_type=chat_history['messageIssuer']['userType']
                    )
                )
                chat_history_obj_list.append(chat_history_obj)

            character_info_obj = XincCharacterInfo(
                character_name=data['name'],
                chat_room_name=data['chatRoomName'],
                is_group_chat=data['isGroupChat'],
                characters=character_obj_list,
                chat_history=XincChatHistory(
                    content_list=chat_history_obj_list,
                    total=len(chat_history_obj_list)
                )
            )

            return character_info_obj

        except:
            request_response = response.content
            traceback_info = f"\n--- Error Log Entry ---\n{traceback.format_exc()}\n--- End of Entry ---\n"
            all_data = f"{host}\n\nget请求，无请求体\n\n{request_response}\n\n{traceback_info}"
            file_path = self.save_bad_request_data('获取角色信息时出现未知错误', all_data)
            self.logger.error(f"获取角色信息时出现未知错误，请求相关数据已保存于：{file_path}")
