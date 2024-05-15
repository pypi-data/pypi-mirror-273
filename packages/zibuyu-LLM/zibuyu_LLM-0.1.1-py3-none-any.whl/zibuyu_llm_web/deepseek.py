# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_LLM
author: 子不语
date: 2024/5/7
contact: 【公众号】思维兵工厂
description: DeepSeek Web端逆向。该AI目前仅支持单窗口会话。

已完全逆向，注册、登录、自动管理Token。

该平台的邮箱注册仅支持海外IP
--------------------------------------------
"""

import json
import logging
import re
from typing import Optional

from .base import LLMBase
from .types import AiAnswer
from .errors import NeedLoginError

# 在发送手机或邮件验证码时，需要携带这个参数；该参数目前为固定值
TURNSTILE_TOKEN = '0.m0l729JxhJEkMRTF3KmaamhsRl0HLUZUVJgQcwaMzJsEHhpZ1YGHhSCPZwP9yWV2N_-rUdwI4P8A5Xm1Kl4ZLxCtFRA5je-3TJhcPkUinVuJwIzBvIah1DILaSEhNo-Ws89CX0TORBX9birCRNY6t3e6Fmsgxvo60mrtmRTkpd5k8jDyRweAqXiILJBkK_EzwwOq9pWHD_HEJjQ5KiId-8FcN18_m3UGUrUQXAQLOMTxqcs9g9tIjseyM81mB-C7HOHrdXhfQqiYX-wdiLa4NqqHgbiZUwP4d_IWWgloS9EAdLtJQQoiMPUjI5gkAGOmtNCFX3RcAQca4jsfod8DzTcYmCd03HJMZsXNr7A8dFegaLxzxWu9-I6TdTMfjaCI-Wzra1KN4BiSP_eWEK_Uz8hYzO3Ohj_Nonm3EpGnABeplDzqiteRunXESzatMv_4.aJXkGwUBtqKoVH0R5DFm3Q.656f25ad10112a3a66a6b5f8a480daedb469eb74c98722855441b164bbdad82c'


class DeepSeekWeb(LLMBase):
    """
    DeepSeek Web端逆向。该AI目前仅支持单窗口会话。
    """

    model_name = 'DeepSeek'

    base_host = 'https://chat.deepseek.com'

    def __init__(
            self,
            account_phone: str = None,
            account_email: str = None,
            password: str = None,
            token: str = None,
            logger_obj: logging.Logger = None,
            error_dir: str = None
    ):
        """
        :param account_phone: 登录手机号
        :param account_email: 登录邮箱
        :param password: 密码
        :param token: 登录Token，若不传入该值，将自行登录获取token
        :param logger_obj: 日志对象
        :param error_dir: 错误日志保存目录
        """

        self.account_phone = account_phone
        self.account_email = account_email
        self.password = password
        self.error_dir = error_dir
        self.logger = logger_obj
        self._token = token

        super().__init__()

        self.__headers = {
            'Accept': "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            'Connection': "keep-alive",
            'Host': "chat.deepseek.com",
            'Origin': "https://chat.deepseek.com",
            'Referer': "https://chat.deepseek.com/",

            'Pragma': "no-cache",
            'Priority': "u=1, i",
            "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "User-Agent": self.user_agent,
        }

        self.single_answer_obj: Optional[AiAnswer] = None
        self.__single_answer: str = ''
        self.__single_padding: str = ''

    @property
    def token(self):

        if self._token:
            return self._token
        self.login()
        return self._token

    def __ask(self, question: str, model: str, callback_func=None):

        uri = '/api/v0/chat/completions'

        headers = self.__headers.copy()
        headers['Authorization'] = f'Bearer {self.token}'
        headers['Content-Type'] = 'application/json'
        headers['Referer'] = 'https://chat.deepseek.com/'

        data = {
            "message": question,
            "stream": True,
            "model_preference": None,
            "model_class": model,
            "temperature": 0
        }

        response = self.request_session.post(
            url=self.base_host + uri,
            headers=headers,
            json=data,
            stream=True,
            timeout=60
        )

        if response.status_code != 200:
            self.logger.error(f'请求失败，响应状态码为：【{response.status_code}】')
            return

        padding = ''
        for line in response.iter_lines():

            if not line:
                continue

            padding += line.decode('utf-8')

            if not padding.endswith('}'):
                continue

            if not padding.startswith('data'):
                self.logger.error(f'请求不正常，响应数据为：【{padding}】')
                raise NeedLoginError("cookies可能过期了，需要重新登录")

            data = json.loads(padding[6:])
            padding = ''

            self.__single_padding = data.get('choices', [])[0].get('delta', {}).get('content', {})

            if callable(callback_func):
                try:
                    callback_func(self.__single_padding)
                except:
                    pass

            finish_reason = data.get('choices', [])[0].get('finish_reason', {})

            if finish_reason == 'stop':
                if callable(callback_func):
                    try:
                        callback_func(self.end_signal)
                    except:
                        self.logger.error(f'回调函数【{callback_func.__name__}】执行失败', exc_info=True)

            if self.__single_padding:
                self.__single_answer += self.__single_padding

        self.single_answer_obj = AiAnswer(
            content=self.__single_answer,
            is_success=True,
        )

        return self.single_answer_obj

    def __get_history(self, model: str, referer: str) -> dict:
        uri = '/api/v0/chat/history'

        params = {
            'model_class': model,
            'filter_server_error': True,
            'forward_query': False,
        }

        headers = self.__headers.copy()
        headers['Authorization'] = f'Bearer {self.token}'
        headers['Referer'] = referer

        try:
            response = self.request_session.get(
                url=self.base_host + uri,
                headers=headers,
                params=params
            )

            resp_json = response.json()
            return resp_json
        except:
            self.logger.error(f'get_history方法请求失败！')

    def login(self) -> bool:
        """登录"""

        uri = '/api/v0/users/login'

        if self.account_email:
            data = {
                "email": self.account_email,
                "password": self.password,
                "mobile": '',
                "area_code": '',
            }
        elif self.account_phone:
            data = {
                "email": "",
                "mobile": self.account_phone,
                "password": self.password,
                "area_code": "+86"
            }
        else:
            raise Exception('未传入账号信息【手机号或邮箱】')

        headers = self.__headers.copy()

        headers['Content-Type'] = 'application/json'

        try:
            response = self.request_session.post(
                url=self.base_host + uri,
                headers=headers,
                json=data
            )

            resp_json = response.json()

            if response.status_code != 200:
                self.logger.error(f'登录失败，响应数据: 【{resp_json}】')
                return False

            self._token = resp_json.get('data', {}).get('user', {}).get('token')

            if not self.token:
                self.logger.error(f'登录失败，响应数据: 【{resp_json}】')
                return False

            self.logger.info(f'登录成功，获取到请求Token')
            return True
        except:
            return False

    def clear_content(self) -> bool:

        uri = '/api/v0/chat/clear_context'

        data = {
            "model_class": "deepseek_chat",
            "append_welcome_message": False
        }

        headers = self.__headers.copy()
        headers['Authorization'] = f'Bearer {self.token}'
        headers['Referer'] = 'https://chat.deepseek.com/'

        response = self.request_session.post(
            url=self.base_host + uri,
            headers=headers,
            json=data
        )

        resp_json = response.json()
        code = resp_json.get('code')

        if code == 0:
            self.logger.info(f'清除上下文成功')
            return True
        else:
            self.logger.error(f'清除上下文失败，响应数据: 【{resp_json}】')
            return False

    def ask_code(self, question: str, callback_func=None) -> AiAnswer:
        """
        代码助手
        :param question:
        :param callback_func:
        :return:
        """

        model = "deepseek_code"
        return self.__ask(question, model, callback_func=callback_func)

    def ask(self, question: str, callback_func=None) -> AiAnswer:
        """
        通用助手
        :param question:
        :param callback_func:
        :return:
        """

        model = "deepseek_chat"
        return self.__ask(question, model, callback_func=callback_func)

    def get_chat_history(self):
        """
        获取通用助手聊天记录
        :return:
        """

        model = "deepseek_chat"
        referer = 'https://chat.deepseek.com/coder'
        data = self.__get_history(model, referer)
        return data

    def get_code_history(self):
        """
        获取代码助手聊天记录
        :return:
        """

        model = "deepseek_code"
        referer = 'https://chat.deepseek.com/coder'
        data = self.__get_history(model, referer)
        return data

    def get_register_header(self):
        """获取注册相关请求时所需的请求头"""

        headers = self.__headers.copy()
        headers['Content-Type'] = 'application/json'
        headers['Referer'] = 'https://chat.deepseek.com/sign_up'
        headers['Origin'] = 'https://chat.deepseek.com'
        headers['Host'] = 'chat.deepseek.com'
        return headers

    def send_code(self, uri: str, data: dict) -> bool:

        headers = self.get_register_header()

        response = self.request_session.post(
            url=self.base_host + uri,
            headers=headers,
            json=data
        )
        response_json = response.json()

        code = response_json.get('data', {}).get('code')
        msg = response_json.get('data', {}).get('msg')

        if code == 0:
            self.logger.info(f'发送验证码成功，返回消息:【{msg}】')
            return True

        self.logger.error(f'发送验证码失败，返回消息:【{msg}】')
        return False

    def send_email_code(self, email: str):
        """
        发送验证码
        :param email:
        :return:
        """

        if not self.is_valid_email(email):
            self.logger.error(f'邮箱格式错误，请检查邮箱格式')
            return False

        uri = '/api/v0/users/create_email_verification_code'
        data = {
            "email": email,
            "locale": "zh_CN",
            "turnstile_token": TURNSTILE_TOKEN,
        }
        return self.send_code(uri=uri, data=data)

    def send_phone_code(self, phone: str):

        if not self.is_valid_phone_number(phone):
            self.logger.error(f'手机号格式错误，请检查手机号格式')
            return False

        uri = '/api/v0/users/create_sms_verification_code'

        data = {
            "mobile_phone_number": phone,
            "locale": "zh_CN",
            "turnstile_token": TURNSTILE_TOKEN,
        }

        return self.send_code(uri=uri, data=data)

    def register(self, uri: str, data: dict) -> str:
        """ 注册，成功时返回Token """

        headers = self.get_register_header()

        try:
            response = self.request_session.post(
                url=self.base_host + uri,
                headers=headers,
                json=data,
            )

            resp_json = response.json()

            token = resp_json.get('data', {}).get('user', {}).get('token')

            if token:
                self.logger.info(f'注册成功，已更新token')
                self.logger.info(f'token:【{token}】')
                self._token = token
                return token

        except:
            self.logger.error(f'注册失败', exc_info=True)

    def register_by_email(self, email: str, code: str, password: str = None):
        """
        通过邮箱注册
        :param email: 邮箱
        :param code: 邮箱验证码
        :param password: 密码
        :return: 注册成功时，返回token
        """

        if not self.is_valid_email(email):
            self.logger.error(f'邮箱格式错误，请检查邮箱格式')
            return

        uri = '/api/v0/users/register'

        data = {
            "locale": "zh_CN",
            "region": "FR",
            "payload": {
                "email": email,
                "email_verification_code": code,
                "password": password or 'ilovedeepseek'
            }
        }

        return self.register(uri=uri, data=data)

    def register_by_phone(self, phone: str, code: str, password: str = None):
        """
        通过手机号注册
        :param phone: 手机号
        :param code: 手机验证码
        :param password: 密码
        :return: 注册成功时，返回token
        """

        if not self.is_valid_phone_number(phone):
            self.logger.error(f'手机号格式错误，请检查手机号格式')
            return

        uri = '/api/v0/users/register_by_mobile'

        data = {
            "locale": "zh_CN",
            "region": "CN",
            "payload": {
                "area_code": "+86",
                "mobile_number": phone,
                "sms_verification_code": code,
                "audit_json_str": "{\"reasons\":[2,1]}",
                "password": password or 'ilovedeepseek'
            }
        }

        return self.register(uri=uri, data=data)

    @staticmethod
    def is_valid_phone_number(phone_number):
        pattern = r'^1[3-9]\d{9}$'
        return bool(re.match(pattern, phone_number))

    @staticmethod
    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
