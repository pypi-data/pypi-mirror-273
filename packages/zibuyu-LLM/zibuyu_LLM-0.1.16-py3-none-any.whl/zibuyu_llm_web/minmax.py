# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_LLM
author: 子不语
date: 2024/5/4
contact: 【公众号】思维兵工厂
description: 海螺问问Web逆向。

该平台使用是在请求头中通过Token（JWT）进行鉴权的；cookies无关鉴权。

JWT的载荷部分:

{
  "exp": 1718232417,
  "user": {
    "id": "242935160332279815",
    "name": "小螺帽9815",
    "avatar": "https://cdn.yingshi-ai.com/prod/user_avatar/1706267544389820801-173194570668965896oversize.png",
    "deviceID": "242935159979966466",
    "isAnonymous": false
  }
}
--------------------------------------------
"""

import base64
import os
import re
import uuid
import time
import json
import hashlib
import logging
import asyncio
import traceback
from typing import Dict, Optional, Literal
from urllib.parse import urlencode, quote_plus

import aiohttp
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from .base import LLMBase
from .types import AiAnswer, ReferenceLink
from .errors import RequestsError, NeedLoginError


class MinMaxWeb(LLMBase):
    """
    MinMax Web
    """

    model_name = 'MinMax'

    base_host = 'https://hailuoai.com'

    def __init__(
            self,
            login_phone: str = None,
            token_str: str = None,
            logger_obj: logging.Logger = None,
            error_dir: str = None
    ):
        """
        :param login_phone: 登录手机号
        :param token_str: 登录token
        :param logger_obj: 日志对象
        :param error_dir: 错误日志保存目录
        """

        self.logger = logger_obj
        self.login_phone = login_phone
        self.error_dir = error_dir
        self.token_str = token_str

        super().__init__()

        self.chat_id: str = ''  # 会话ID
        self.user_msg_id: str = ''  # 用户所发送的消息的id，目前无作用
        self.system_msg_id: str = ''  # 系统回复的消息的id，主要用于获取音频

        self.__single_uuid: str = ''  # 单次会话标识ID
        self.__user_id: str = ''  # 用户标识ID
        self.__device_id: str = ''  # 设备标识ID
        self.__device_info_expire: int = 0  # 设备ID过期时间

        self.__voice_info_dict: Optional[dict] = None

        # 语音相关_请求参数
        self.__voice_user_data = {
            'msgID': "",  # 消息ID
            'timbre': "",  # 配音音色
            'device_platform': "web",
            'app_id': "3001",
            'uuid': '',  # uuid，待填充
            'device_id': '',  # 设备ID，待填充
            'version_code': "21200",
            'os_name': "Windows",
            'browser_name': "chrome",
            'server_version': "101",
            'device_memory': 8,
            'cpu_core_num': 8,
            'browser_language': "zh-CN",
            'browser_platform': "Win32",
            'screen_width': 1920,
            'screen_height': 1080,
            'unix': '',  # 时间戳，待填充
        }

        # 公用请求参数
        self.__user_data = {
            'device_platform': "web",
            'app_id': "3001",
            'uuid': '',  # uuid，待填充
            'device_id': '',  # 设备ID，待填充
            'version_code': "21200",
            'os_name': "Windows",
            'browser_name': "chrome",
            'server_version': "101",
            'device_memory': 8,
            'cpu_core_num': 8,
            'browser_language': "zh-CN",
            'browser_platform': "Win32",
            'screen_width': 1920,
            'screen_height': 1080,
            'unix': '',  # 时间戳，待填充
        }

        # 公用请求头
        self.__headers = {
            'Accept': "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            'Origin': "https://hailuoai.com",
            'Pragma': "no-cache",
            'Priority': "u=1, i",
            "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "User-Agent": super().user_agent,
            "Token": self.token_str,
        }

        self.is_anonymous: bool = True  # 是否是匿名用户；默认为匿名用户
        self.single_answer: str = ''
        self.single_answer_obj: AiAnswer = AiAnswer()
        self.single_padding: str = ''  # 流式输出时，每次接收到的回答中的增量部分
        self.single_answer_audio_url_list: Optional[list] = None  # 单次回复时，音频文件的url列表

        if self.token_str:
            self.parse_token_str()
        elif self.anonymity_login():
            self.logger.info(f'未传入Token，进行匿名登录，成功获取token_str')
        else:
            self.logger.error(f'未传入Token，且匿名登录失败')

    @property
    def device_id(self):
        """ 获取设备id，该值存在有效期 """

        now = int(time.time()) * 1000

        if self.__device_id and self.__device_info_expire > now:
            return self.__device_id

        self.update_device_id()

        return self.__device_id

    @property
    def device_info_expire(self):
        """ 获取设备id的过期时间 """
        return self.__device_info_expire

    @property
    def user_id(self):
        """ 获取user_id """

        if self.__user_id:
            return self.__user_id

        self.update_device_id()

        return self.__user_id

    @property
    def single_uuid(self):
        """ 海螺平台未登录也可访问，通过此uuid来唯一标识用户 """

        if self.__single_uuid:
            return self.__single_uuid
        self.__single_uuid = str(uuid.uuid4())
        return self.__single_uuid

    @property
    def voice_info_dict(self):
        """ 获取语音列表 """

        if self.__voice_info_dict:
            return self.__voice_info_dict
        self.__voice_info_dict = {
            "male-botong": {
                "voiceID": "male-botong",
                "voiceName": "思远",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/male-botongccf85929-b9c6-40a3-a66d-8ae734e8fe0c.mp3"
            },
            "Podcast_girl": {
                "voiceID": "Podcast_girl",
                "voiceName": "心悦",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/Podcast_girl9e3c80b6-4f23-4af2-8578-4204161eabd5.mp3"
            },
            "boyan_new_hailuo": {
                "voiceID": "boyan_new_hailuo",
                "voiceName": "子轩",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/boyan_new_hailuo70102124-b4dd-4fe3-8d6e-b57d44f01a90.mp3"
            },
            "female-shaonv": {
                "voiceID": "female-shaonv",
                "voiceName": "灵儿",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/female-shaonv9c5a5aa5-d527-4b8a-adce-d25e911d2fed.mp3"
            },
            "YaeMiko_hailuo": {
                "voiceID": "YaeMiko_hailuo",
                "voiceName": "语嫣",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/YaeMiko_hailuo7384790c-d84b-4c59-9a31-be1a1fe40361.mp3"
            },
            "xiaoyi_mix_hailuo": {
                "voiceID": "xiaoyi_mix_hailuo",
                "voiceName": "少泽",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/xiaoyi_mix_hailuoe47a2c39-fef1-49df-b5b7-7734ab195969.mp3"
            },
            "xiaomo_sft": {
                "voiceID": "xiaomo_sft",
                "voiceName": "芷溪",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/xiaomo_sfta8bb210d-b35a-46d2-9bcd-46f286c0527c.mp3"
            },
            "cove_test2_hailuo": {
                "voiceID": "cove_test2_hailuo",
                "voiceName": "浩翔（英文）",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/cove_test2_hailuob22985f3-277c-442d-bf9c-f28a773ce50d.mp3"
            },
            "scarlett_hailuo": {
                "voiceID": "scarlett_hailuo",
                "voiceName": "雅涵（英文）",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/scarlett_hailuo97649559-1373-4ea8-86dd-b7cfb4aeb029.mp3"
            },
            "Leishen2_hailuo": {
                "voiceID": "Leishen2_hailuo",
                "voiceName": "模仿雷电将军",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/Leishen2_hailuo27ae6370-589e-459f-878d-b6a43c326729.mp3"
            },
            "Zhongli_hailuo": {
                "voiceID": "Zhongli_hailuo",
                "voiceName": "模仿钟离",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/Zhongli_hailuo98dad06d-4e23-49e7-8094-c530c4c05fa5.mp3"
            },
            "Paimeng_hailuo": {
                "voiceID": "Paimeng_hailuo",
                "voiceName": "模仿派蒙",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/Paimeng_hailuo9bda8f9f-3b85-4c76-8c63-cb481980c534.mp3"
            },
            "keli_hailuo": {
                "voiceID": "keli_hailuo",
                "voiceName": "模仿可莉",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/keli_hailuoeb6d70b9-572b-4a15-a1fa-b139a47780ce.mp3"
            },
            "Hutao_hailuo": {
                "voiceID": "Hutao_hailuo",
                "voiceName": "模仿胡桃",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/Hutao_hailuo6c655b82-3c7c-4232-9bdf-64069039dcf5.mp3"
            },
            "Xionger_hailuo": {
                "voiceID": "Xionger_hailuo",
                "voiceName": "模仿熊二",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/Xionger_hailuo4ae3b6b6-a833-45c4-b8d4-659d4a4ca003.mp3"
            },
            "Haimian_hailuo": {
                "voiceID": "Haimian_hailuo",
                "voiceName": "模仿海绵宝宝",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/Haimian_hailuo3afd8572-99e2-420a-bea0-63dd85ffb37f.mp3"
            },
            "Robot_hunter_hailuo": {
                "voiceID": "Robot_hunter_hailuo",
                "voiceName": "模仿变形金刚",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/Robot_hunter_hailuo38ac6dbf-7941-4498-9ed7-5b4bb94c7650.mp3"
            },
            "Linzhiling_hailuo": {
                "voiceID": "Linzhiling_hailuo",
                "voiceName": "小玲玲",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/Linzhiling_hailuo0db5aad6-5c2f-46f5-871f-4f9197a270b1.mp3"
            },
            "huafei_hailuo": {
                "voiceID": "huafei_hailuo",
                "voiceName": "拽妃",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/huafei_hailuoe4d1c4b1-2ea1-4538-b4a7-d97bd68d4915.mp3"
            },
            "lingfeng_hailuo": {
                "voiceID": "lingfeng_hailuo",
                "voiceName": "东北er",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/lingfeng_hailuo044e3100-ec23-435b-8b74-aa1d4ae450c3.mp3"
            },
            "male_dongbei_hailuo": {
                "voiceID": "male_dongbei_hailuo",
                "voiceName": "老铁",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/male_dongbei_hailuo67361485-a4e7-41cc-8592-989667d4c747.mp3"
            },
            "Beijing_hailuo": {
                "voiceID": "Beijing_hailuo",
                "voiceName": "北京er",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/Beijing_hailuoa16df4af-7107-43d7-adb5-30ee80016509.mp3"
            },
            "JayChou_hailuo": {
                "voiceID": "JayChou_hailuo",
                "voiceName": "JayJay",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/JayChou_hailuo654d0644-addf-44f1-8fbc-984d60c519b5.mp3"
            },
            "Daniel_hailuo": {
                "voiceID": "Daniel_hailuo",
                "voiceName": "潇然",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/Daniel_hailuod259f6db-4522-4f1f-8310-d7cbf361d08a.mp3"
            },
            "Bingjiao_zongcai_hailuo": {
                "voiceID": "Bingjiao_zongcai_hailuo",
                "voiceName": "沉韵",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/Bingjiao_zongcai_hailuo924dca88-c6a4-49c6-be19-0c9a30c836c3.mp3"
            },
            "female-yaoyao-hd": {
                "voiceID": "female-yaoyao-hd",
                "voiceName": "瑶瑶",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/female-yaoyao-hdca94aef9-4321-4b3e-a655-8bf0f7d729f2.mp3"
            },
            "murong_sft": {
                "voiceID": "murong_sft",
                "voiceName": "晨曦",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/murong_sft714a221f-30fc-4d1b-9942-d4824f296b9c.mp3"
            },
            "shangshen_sft": {
                "voiceID": "shangshen_sft",
                "voiceName": "沐珊",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/shangshen_sft6ba79922-6a38-4150-bbd0-0570a571f7af.mp3"
            },
            "kongchen_sft": {
                "voiceID": "kongchen_sft",
                "voiceName": "祁辰",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/kongchen_sft3d025ed0-d041-4620-8cd7-f3d09723d275.mp3"
            },
            "shenteng2_hailuo": {
                "voiceID": "shenteng2_hailuo",
                "voiceName": "夏洛特",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/shenteng2_hailuo3922d48b-1edb-4e7e-baa7-bed0131bf20a.mp3"
            },
            "Guodegang_hailuo": {
                "voiceID": "Guodegang_hailuo",
                "voiceName": "郭嘚嘚",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/Guodegang_hailuocba5a5aa-781b-4e0b-96e7-070f0e4e97fb.mp3"
            },
            "yueyue_hailuo": {
                "voiceID": "yueyue_hailuo",
                "voiceName": "小月月",
                "previewAudioUrl": "https://cdn.yingshi-ai.com/audio/example/yueyue_hailuoa518c725-1be1-456f-8274-be18de1c4f34.mp3"
            }
        }
        return self.__voice_info_dict

    @staticmethod
    def md5(value, is_bytes=False):
        """
        md5加密
        :param value: 需要加密的值
        :param is_bytes: 是否已经是二进制数据
        :return:
        """

        hash_object = hashlib.md5()

        if not is_bytes:
            hash_object.update(value.encode('utf-8'))  # 对字符串进行UTF-8编码，因为MD5处理二进制数据
        else:
            hash_object.update(value)
        return hash_object.hexdigest()

    @staticmethod
    def build_query_string(user_data: Dict[str, str]) -> str:
        """
        讲请求参数拼接成query字符串，并进行urlencode处理
        :param user_data: 请求参数字典
        :return:
        """

        query_params = [(k, v) for k, v in user_data.items() if v is not None]
        return urlencode(query_params, doseq=True).lstrip("&")

    @staticmethod
    def get_timestamp():
        """ 获取时间戳 """

        return str(int(time.time()) * 1000)

    def parse_token_str(self) -> bool:
        """海螺使用的Token是JWT格式，可以解析后获取基本信息"""

        if not self.token_str:
            return False

        try:

            data = json.loads(base64.b64decode(self.token_str.split('.')[1]).decode())
            device_id = data.get('user', {}).get('deviceID', '')
            self.is_anonymous = data.get('user', {}).get('isAnonymous', True)
            self.__device_id = device_id
            self.logger.info(f'成功解析JWT\n\n设备ID：【{device_id}】\n用户类型：isAnonymous【{self.is_anonymous}】\n')
            return True
        except:
            self.logger.error(f'解析JWT失败', exc_info=True)
            return False

    def renew_token_str(self) -> bool:

        uri = '/v1/api/user/renewal'
        unix = self.get_timestamp()

        user_data = self.__user_data.copy()
        user_data['device_id'] = self.device_id
        user_data['uuid'] = self.single_uuid
        user_data['unix'] = unix

        headers = self.__headers.copy()

        yy = self.get_yy(
            uri=uri,
            unix=unix,
            data=user_data,
            user_data=user_data,
            jsonfy=True,
        )

        headers["Yy"] = yy
        try:
            response = self.request_session.post(
                self.base_host + uri,
                headers=headers,
                json=user_data
            )

            resp_data = response.json()
            request_status = resp_data.get('statusInfo', {}).get('code', )
            if request_status != 200:
                self.logger.error(f'token_str更新失败，错误码：{request_status}')
                return False

            token = resp_data.get('data', {}).get('token')
            if not token:
                self.logger.error(f'token_str更新失败，token为空')
                return False

            self.token_str = token
        except:
            self.logger.error(f'token_str更新失败', exc_info=True)
            return False

    def anonymity_login(self) -> bool:
        """ 匿名登录，获取token_str """

        uri = '/v1/api/user/login/phone'

        unix = self.get_timestamp()

        user_data = self.__user_data.copy()
        user_data['device_id'] = self.device_id
        user_data['uuid'] = self.single_uuid
        user_data['unix'] = unix

        headers = self.__headers.copy()

        data = {
            "loginType": "3",
            "adInfo": {}
        }

        yy = self.get_yy(
            uri=uri,
            unix=unix,
            data=data,
            user_data=user_data,
            jsonfy=True,
        )

        headers["Yy"] = yy
        headers["server_version"] = ''

        query_str = self.build_query_string(user_data)

        response = self.request_session.post(
            self.base_host + uri + f'?{query_str}',
            headers=headers,
            json=data
        )

        resp_data = response.json()

        token_str = resp_data.get('data', {}).get('token')
        device_id = resp_data.get('data', {}).get('deviceID')
        user_id = resp_data.get('data', {}).get('userID')

        if token_str:
            self.chat_id = None

            self.token_str = token_str
            self.__headers['Token'] = token_str
            self.__device_id = device_id
            self.__user_id = user_id
            self.__device_info_expire = (int(time.time()) + 10800) * 1000

            self.logger.info(f'成功获取到token_str：{token_str}')
            return True

        return False

    def post(
            self,
            url: str,
            headers: dict,
            data: dict,
            stream: bool = False,
            multipart_encode: bool = False,
    ) -> Optional[requests.Response]:
        """
        发送post请求，如果失败，则重新登录后再尝试，尝试两次
        :param url: 请求url
        :param headers: 请求头
        :param data: 请求体
        :param stream: 是否流式传输
        :param multipart_encode: 是否使用multipart/form-data格式
        :return:
        """

        for i in range(3):

            if multipart_encode:
                self.logger.info(f"使用multipart/form-data格式发送POST请求")

                multipart_data = MultipartEncoder(data)
                headers["Content-Type"] = multipart_data.content_type
                headers["Token"] = self.token_str
                response = self.request_session.post(
                    url,
                    headers=headers,
                    data=multipart_data,
                    stream=stream
                )
            else:
                self.logger.info(f"使用json格式发送POST请求")

                headers["Token"] = self.token_str
                response = self.request_session.post(
                    url,
                    headers=headers,
                    data=data,
                    stream=stream
                )

            if response.status_code == 200:
                self.logger.info(f"POST请求成功")
                return response

            self.logger.error(f"POST请求失败，状态码：{response.status_code}")
            self.logger.error(f"POST请求失败，响应内容：{response.text}")

            if not self.is_anonymous:
                self.logger.info(f"并非匿名用户，不进行自动登录")
                return

            result = self.re_login_by_anonymous(data)
            if not result:
                self.logger.error(f"重新匿名登录失败，不再尝试发送POST请求")
                return
            self.logger.info(f"重新匿名登录成功，即将重新发送请求")

        self.logger.error(f"请求3次仍然失败，退出")

    def get(self, url: str, headers: dict, params: dict, stream: bool = False) -> Optional[requests.Response]:
        pass

    def update_device_id(
            self,
            request_uuid: str = None,
            request_device_id: str = None,
    ):
        """ 更新设备id """

        uri = "/v1/api/user/device/register"

        unix = self.get_timestamp()

        user_data = self.__user_data.copy()

        user_data['uuid'] = request_uuid or self.single_uuid
        user_data['device_id'] = request_device_id or self.__device_id
        data = {"uuid": request_uuid or self.single_uuid}

        user_data['unix'] = unix

        headers = self.__headers.copy()

        yy = self.get_yy(
            user_data=user_data,
            uri=uri,
            data=data,
            unix=unix,
            jsonfy=True
        )

        headers["Yy"] = yy

        query_str = self.build_query_string(user_data)
        response = self.request_session.post(
            self.base_host + uri + f'?{query_str}',
            json=data,
            headers=headers
        )

        resp_json = response.json()

        status_code = resp_json.get('statusInfo', {}).get('code')

        if status_code != 0:
            self.logger.error(f'获取设备信息出错')
            self.logger.info(f'响应数据: {resp_json}')
            raise RequestsError(resp_json)

        self.__device_id = resp_json.get('data', {}).get('deviceIDStr')
        self.__user_id = resp_json.get('data', {}).get('userID')

        if self.__device_id:
            self.logger.info(f'成功更新设备ID: 【{self.__device_id}】')

            self.__device_info_expire = (int(time.time()) + 10800) * 1000

            self.logger.info(f'成功更新设备过期时间: 【{self.__device_info_expire}】')

        if self.__user_id:
            self.logger.info(f'成功更新用户ID: 【{self.__user_id}】')

        # 响应数据示例
        """
        {'data':
                 {
                  'deviceID': 242986651646619650,
                  'deviceIDStr': '242986651646619650',
                  'userID': '2Y62maaVyPGK',
                  'realUserID': '242986651696951305'
                  },
             'statusInfo':
                 {
                  'code': 0,
                  'httpCode': 0,
                  'message': '成功',
                  'serviceTime': 1714788676,
                  'requestID': '7e353b60-8462-4488-ae36-42bd62428e5b',
                  'debugInfo': '',
                  'serverAlert': 0
                  }
             }
        """

    def get_yy(
            self,
            uri,
            unix: str,
            user_data: dict,
            data: dict = None,
            jsonfy: bool = False,
            is_file: bool = False
    ):
        """
        获取yy参数
        :param user_data: 请求参数字典
        :param uri: 请求uri，不要忘记开头的 /
        :param data: 请求体数据
        :param unix: 时间戳
        :param jsonfy: 对于data数据，是否仅进行json序列化
        :param is_file: 是否携带文件
        :return:
        """

        query_str = self.build_query_string(user_data)

        if jsonfy:
            data_json = json.dumps(data or {}).replace(' ', '').replace('\r', '').replace('\n', '')
        elif is_file:
            # 计算chatID的MD5哈希
            chat_id_hash = self.md5(data['chatID'])

            # 计算characterID的MD5哈希
            character_id_hash = self.md5(data['characterID'])

            play_speed_level_hash = self.md5(data['playSpeedLevel'])

            file_hash = self.md5(data['voiceBytes'], is_bytes=True)

            # data_json = chat_id_hash + file_hash + character_id_hash + play_speed_level_hash
            data_json = character_id_hash + file_hash + chat_id_hash + play_speed_level_hash

        else:

            # 计算characterID的MD5哈希
            character_id_hash = self.md5(data['characterID'])

            # 移除msgContent中的换行符并计算MD5哈希
            msg_content = re.sub(r'(\r\n|\n|\r)', '', data['msgContent'])
            msg_content_hash = self.md5(msg_content)

            # 计算chatID的MD5哈希
            chat_id_hash = self.md5(data['chatID'])

            # 如果存在form，计算其MD5哈希，否则使用空字符串
            form_hash = self.md5(data.get('form', ''))

            data_json = character_id_hash + msg_content_hash + chat_id_hash + form_hash

        full_uri = f"{uri}{uri.find('?') != -1 and '&' or '?'}{query_str}"

        yy = self.md5(f"{quote_plus(full_uri)}_{data_json}{self.md5(unix)}ooui")

        return yy

    def check_request_info(
            self, request_uuid: str = None,
            request_device_id: str = None,
            device_info_expire: int = 0,
    ) -> bool:

        """MinMax似乎并不检查请求时携带的device_id；但这里仍然带上"""

        if not request_uuid or not request_device_id or not device_info_expire:
            return False

        now = int(time.time()) * 1000

        if device_info_expire < now:
            return False

        self.__device_info_expire = device_info_expire
        self.__device_id = request_device_id
        self.__single_uuid = request_uuid
        return True

    def ask(
            self,
            question: str,
            chat_id: str = None,
            callback_func=None,
            character_id: str = '1',
            search_mode: Literal['0', '1'] = '0',
            audio_output_dir: str = None,
            voice_id: str = 'male-botong',
            request_uuid: str = None,
            request_device_id: str = None,
            device_info_expire: int = None,
    ) -> AiAnswer:
        """
        提问
        :param question: 问题
        :param chat_id: 会话ID
        :param callback_func: 回调函数，处理每一次回答的增量文本
        :param character_id: 角色id，目前固定为1
        :param search_mode: 搜索模式：1表示关闭；0表示开启
        :param audio_output_dir: 音频文件输出目录；不为空时将在AI交互之后生成音频
        :param voice_id: 配音音色ID
        :param request_uuid: 配音音色ID
        :param request_device_id: 配音音色ID
        :param device_info_expire: 配音音色ID
        :return: AiAnswer
        """

        if search_mode not in ['0', '1']:
            raise ValueError("search_mode参数错误，请传入0或1")

        self.check_request_info(request_uuid, request_device_id, device_info_expire)

        if chat_id:
            self.logger.info(f'使用传入的会话ID: 【{chat_id}】')
            self.chat_id = chat_id

        uri = "/v4/api/chat/msg"

        unix = self.get_timestamp()

        # 1. 处理请求参数
        user_data = self.__user_data.copy()

        user_data["uuid"] = self.single_uuid
        user_data["device_id"] = self.device_id
        user_data["unix"] = unix

        # 2. 处理请求体数据
        headers = self.__headers.copy()
        referer = f'https://hailuoai.com/?chat={self.chat_id}' if self.chat_id else 'https://hailuoai.com/'
        headers["Referer"] = referer
        headers["Accept"] = 'text/event-stream'

        data = {
            "characterID": character_id,
            "msgContent": question,
            "chatID": self.chat_id if self.chat_id else '0',  # 为0时将新建对话
            "searchMode": search_mode,
        }

        yy = self.get_yy(
            user_data=user_data,
            uri=uri,
            data=data,
            unix=unix
        )

        headers["Yy"] = yy

        query_str = self.build_query_string(user_data)

        for i in range(3):

            try:
                response = self.post(
                    self.base_host + uri + f'?{query_str}',
                    headers=headers,
                    data=data,
                    stream=True,
                    multipart_encode=True,
                )

                # 请求失败，返回空对象
                if not response:
                    return AiAnswer()

                self.parse_ask_result(
                    response=response,
                    callback_func=callback_func,
                    audio_output_dir=audio_output_dir,
                    voice_id=voice_id
                )

                return self.single_answer_obj
            except NeedLoginError:

                if not self.is_anonymous:
                    self.logger.info('该用户并非匿名用户，不进行自动登录')
                    return AiAnswer()

                result = self.re_login_by_anonymous(data)
                if not result:
                    self.logger.error(f"重新匿名登录失败，AI回答获取失败，返回空对象")
                    return AiAnswer()

        self.logger.error(f"多次获取AI回答都失败，返回空对象")
        return AiAnswer()

    def re_login_by_anonymous(self, data: dict) -> bool:
        """重新进行匿名登录"""

        self.logger.info(f"尝试重新匿名登录...")
        result = self.anonymity_login()

        if not result:
            self.logger.error(f"重新匿名登录失败")
            return False

        self.logger.info(f"重新匿名登录成功")
        self.__headers["Token"] = self.token_str

        # 匿名登录后，就没法保持原来的会话了
        if 'chatID' in data:
            data['chatID'] = '0'
            self.chat_id = None
            self.logger.info(f"原会话ID失效，已清除")

        return True

    def parse_ask_result(
            self,
            response: requests.Response,
            callback_func,
            audio_output_dir,
            voice_id
    ):
        index = 0
        pending = ""
        event = ""

        for chunk in response.iter_lines():

            if not chunk:
                continue

            index += 1
            chunk = chunk.decode("utf-8")
            pending += chunk

            if 'event' in pending:
                """
                在AI的回复中，event一共分成三种类型：
                    - send_result：第一次回复，服务端表示接收到用户请求，返回chatID等信息；
                    - message_result：服务端回复文本；
                    - follow_up_question_result：服务端回复相关联问题推荐；
                """

                event = pending.split(":", maxsplit=1)[-1].strip()
                pending = ""
                continue

            # Incomplete chunk
            if not pending.endswith("}"):
                self.logger.debug("The chunk is incomplete.")
                continue

            self.logger.debug(f"The chunk is complete.")

            # Remove the 'data:' prefix, convert JSON to dict
            pending = pending[5:]
            resp_json = json.loads(pending)
            pending = ""

            message_type = resp_json.get('type')
            status_code = resp_json.get('statusInfo', {}).get('code')
            error_message = resp_json.get('statusInfo', {}).get('message')

            if status_code == 0:
                pass
            else:
                self.logger.error(f"解析请求数据时发送错误，状态码：【{status_code}】，消息：【{error_message}】")
                raise NeedLoginError('error_message')

            if event == "send_result" and message_type == 1:
                self.handle_send_result(resp_json)
                continue
            elif event == "message_result" and message_type == 2:
                self.handle_message_result(resp_json, callback_func)
                continue
            elif event == "follow_up_question_result" and message_type == 4:
                self.handle_follow_up_question_result(resp_json)
                continue
            else:
                self.logger.error(f"MinMax响应出现未知数据，可能需要重新逆向，数据类型：{event}")
                self.logger.info(f"MinMax响应数据：{pending}")

        # 检查是否收到任何响应
        if index == 0:
            self.logger.error("MinMax请求没有收到任何响应")

        if audio_output_dir:
            audio_path_list = self.download_audios(output_dir=audio_output_dir, voice_id=voice_id)

            if not audio_path_list:
                self.logger.error("MinMax音频获取失败")
                return self.single_answer_obj

            self.logger.info(f"已将文本转为音频，存放到【{audio_output_dir}】，共计{len(audio_path_list)}条音频")

            self.single_answer_obj.audio_url_list = audio_path_list
            return self.single_answer_obj

    def handle_follow_up_question_result(self, data: dict):
        """服务端返回最后总结信息"""

        self.single_answer = data.get('data', {}).get('messageResult', {}).get('content')

        reference_link_list = data.get('data', {}).get('extra', {}).get('netSearchStatus', {}).get('linkDetail', [])

        self.single_answer_obj.is_success = True
        self.single_answer_obj.content = self.single_answer
        self.single_answer_obj.conversation_id = self.chat_id
        self.single_answer_obj.reference_link_list = [ReferenceLink(
            title=item['detail'],
            url=item['url'],
        ) for item in reference_link_list]

    def handle_message_result(self, data: dict, callback_func: callable = None):
        """服务端返回响应文本"""

        content = data.get('data', {}).get('messageResult', {}).get('content')
        self.single_padding = content.replace(self.single_answer, '')
        self.single_answer = content

        if callable(callback_func):
            try:
                callback_func(self.single_padding)
            except:
                self.logger.error("回调函数执行失败")

        is_end = data.get('data', {}).get('messageResult', {}).get('isEnd')

        if is_end == 0:
            self.single_answer_obj.is_success = True
            self.single_answer_obj.content = self.single_answer
            self.single_answer_obj.conversation_id = self.chat_id

        if is_end == 0 and callable(callback_func):
            try:
                callback_func(self.end_signal)
            except:
                self.logger.error("回调函数执行失败")

    def handle_send_result(self, data: dict):
        """服务端接收到用户文本，返回chatID等信息"""

        self.user_msg_id = data.get('data', {}).get('sendResult', {}).get('userMsgID')
        self.chat_id = data.get('data', {}).get('sendResult', {}).get('chatID')
        self.system_msg_id = data.get('data', {}).get('sendResult', {}).get('systemMsgID')

    def __get_voice_url(self, msg_id: str = None, voice_id: str = 'male-botong'):

        uri = "/v1/api/chat/msg_tts"

        if voice_id not in self.voice_info_dict:
            raise ValueError("语音ID不存在")

        msg_id = msg_id or self.system_msg_id

        if not msg_id:
            raise ValueError("msg_id不能为空")

        # 1. 处理请求参数
        user_data = self.__voice_user_data.copy()
        unix = self.get_timestamp()
        user_data['msgID'] = msg_id
        user_data['timbre'] = voice_id
        user_data["unix"] = unix
        user_data["uuid"] = self.single_uuid
        user_data["device_id"] = self.device_id

        # 2. 处理请求体数据
        headers = self.__headers.copy()

        headers[
            "Referer"] = f'https://hailuoai.com/?chat={self.chat_id}' if self.chat_id else 'https://hailuoai.com/'

        headers["Accept"] = 'application/json, text/plain, */*'

        yy = self.get_yy(
            user_data=user_data,
            uri=uri,
            unix=unix,
            jsonfy=True,
        )

        headers["Yy"] = yy
        query_str = self.build_query_string(user_data)
        request_status = 1

        while request_status == 1:

            response = self.request_session.get(
                url=self.base_host + uri + f'?{query_str}',
                headers=headers,
            )

            data = response.json()

            if data.get('statusInfo', {}).get('code') != 0:
                self.logger.error(f"配音结果获取失败")
                self.logger.info(f"MinMax响应数据：{data}")
                break

            self.single_answer_audio_url_list = data.get('data', {}).get('result', [])
            request_status = data.get('data', {}).get('requestStatus', 2)
            time.sleep(0.2)

        return self.single_answer_audio_url_list

    async def __download_single_audio(self, session, url, file_name):
        async with session.get(url) as response:
            if response.status == 200:
                with open(file_name, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                self.logger.info(f"{file_name} downloaded successfully.")
                # print(f"{file_name} downloaded successfully.")
            else:
                self.logger.error(f"Failed to download {file_name}. Status code: {response.status}")
                # print(f"Failed to download {file_name}. Status code: {response.status}")

    async def __download_all_audios(self, audio_urls, output_dir):
        """ 并发下载所有音频 """

        async with aiohttp.ClientSession() as session:
            tasks = []
            for index, url in enumerate(audio_urls):
                # 构建保存文件的名称
                file_name = f"{output_dir}/audio_{index}.mp3"
                tasks.append(self.__download_single_audio(session, url, file_name))
            await asyncio.gather(*tasks)

    def download_audios(
            self,
            output_dir,
            msg_id: str = None,
            audio_url_list=None,
            voice_id: str = 'male-botong'
    ) -> Optional[list]:
        """
        下载所有音频
        :param output_dir: 输出目录
        :param msg_id: 消息ID，若为空，则使用最新一次交互的消息ID
        :param audio_url_list: 音频URL列表
        :param voice_id: 配音音色ID
        :return:
        """

        if not msg_id:
            msg_id = self.system_msg_id

        if not msg_id:
            self.logger.error("没有传入消息ID")
            return

        if not audio_url_list:
            audio_url_list = self.__get_voice_url(msg_id=msg_id, voice_id=voice_id)

        if not audio_url_list:
            self.logger.error("没有找到任何音频")
            return

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        asyncio.run(self.__download_all_audios(audio_url_list, output_dir))

        return [f"{output_dir}/audio_{index}.mp3" for index, url in enumerate(audio_url_list)]

    def voice2voice(
            self,
            audio_path: str
    ):
        """
        语音输入 + 语音输出 【未完成】
        :param audio_path: 音频文件路径
        :return:
        """

        if not os.path.exists(audio_path):
            self.logger.error("音频文件不存在")
            return

        uri = "/v1/api/chat/phone_msg"

        unix = self.get_timestamp()

        # 1. 处理请求参数
        user_data = self.__user_data.copy()
        user_data["uuid"] = self.single_uuid
        user_data["device_id"] = self.device_id
        user_data["unix"] = unix

        with open(audio_path, 'rb') as f:
            voice_bytes = f.read()

        data = {
            "chatID": self.chat_id if self.chat_id else '0',  # 为0时将新建对话
            "voiceBytes": voice_bytes,
            # "voiceBytes": base64.b64encode(voice_bytes),
            "characterID": '1',
            "playSpeedLevel": '1',
        }

        yy = self.get_yy(user_data=user_data, uri=uri, unix=unix, is_file=True, data=data)
        headers = self.__headers.copy()
        headers[
            "Referer"] = f'https://hailuoai.com/?chat={self.chat_id}' if self.chat_id else 'https://hailuoai.com/'

        headers["Accept"] = 'text/event-stream'
        headers["Yy"] = yy

        # 3. 将data转换为FormData格式
        multipart_data = MultipartEncoder(data)
        headers['Content-Type'] = multipart_data.content_type

        response = self.request_session.post(
            url=self.base_host + uri,
            headers=headers,
            data=multipart_data
        )

        print(response.status_code)
        print(response.text)

        if response.status_code != 200:
            self.logger.error(f"MinMax音频交互失败，响应数据：{response.text}")
            return

        for line in response.iter_lines():
            line = line.decode('utf-8')
            print(line)

    def send_sms_code(self, phone_num: str) -> bool:
        """
        发送验证码
        :param phone_num: 手机号码
        :return: bool
        """

        uri = '/v1/api/user/login/sms/send'

        unix = self.get_timestamp()

        # 1. 处理请求参数
        user_data = self.__user_data.copy()
        user_data["unix"] = unix
        user_data['device_id'] = self.device_id
        user_data['uuid'] = self.single_uuid

        data = {"phone": phone_num}

        # 1. 处理请求头
        headers = self.__headers.copy()
        headers['Accept'] = 'application/json, text/plain, */*'
        headers['Yy'] = self.get_yy(user_data=user_data, uri=uri, data=data, unix=unix, jsonfy=True)
        headers['Content-Type'] = 'application/json'
        query_str = self.build_query_string(user_data)

        try:
            response = self.request_session.post(
                url=self.base_host + uri + f'?{query_str}',
                headers=headers,
                data=json.dumps(data),
            )

            data = response.json()

            status_code = data.get('statusInfo', {}).get('code')

            if status_code == 0:
                self.logger.info(f"发送验证码成功")
                return True

            self.logger.error(f"发送验证码失败")

        except:
            self.logger.error(f"发送验证码失败")

    def login(
            self,
            phone: str,
            sms_code: str,
    ) -> bool:
        """
        账号登录
        :param phone: 手机号
        :param sms_code: 手机验证码
        :return: 登录成功时返回获取到的Token
        """

        if len(sms_code) != 6:
            self.logger.error(f"验证码长度错误")
            return False

        uri = '/v1/api/user/login/phone'

        data = {
            "phone": phone,
            "code": sms_code,
            "loginType": ""
        }

        unix = self.get_timestamp()

        user_data = self.__user_data.copy()
        user_data["unix"] = unix
        user_data['device_id'] = self.device_id
        user_data['uuid'] = self.single_uuid
        yy = self.get_yy(user_data=user_data, uri=uri, data=data, unix=unix, jsonfy=True)

        headers = self.__headers.copy()
        headers['Accept'] = 'application/json, text/plain, */*'
        headers['Yy'] = yy

        try:
            query_str = self.build_query_string(user_data)
            response = self.request_session.post(
                url=self.base_host + uri + f'?{query_str}',
                headers=headers,
                data=json.dumps(data),
            )

            response_data = response.json()

            status_code = response_data.get('statusInfo', {}).get('code')
            if status_code != 0:
                self.logger.error(f"登录失败")
                return False

            self.logger.info(f"登录成功，已获取到Token")
            token = response_data.get('data', {}).get('token')

            if not token:
                self.logger.error(f"登录失败")
                return False

            self.token_str = token
            return True

        except:
            self.logger.error(f"登录失败")
            return False

    def test(self):
        unix = '1715584452000'

        user_data = {
            'device_platform': "web",
            'app_id': "3001",
            'uuid': 'e63d7053-82b5-4bca-b188-8c21d12b644a',  # uuid，待填充
            'device_id': '246324378819584000',  # 设备ID，待填充
            'version_code': "21200",
            'os_name': "Windows",
            'browser_name': "chrome",
            'server_version': "",
            'device_memory': 8,
            'cpu_core_num': 8,
            'browser_language': "zh-CN",
            'browser_platform': "Win32",
            'screen_width': 1920,
            'screen_height': 1080,
            'unix': unix,  # 时间戳，待填充
        }

        data = {"loginType": "3", "adInfo": {}}

        uri = '/v1/api/user/login/phone'
        yy = self.get_yy(
            uri=uri,
            unix=unix,
            user_data=user_data,
            data=data,
            jsonfy=True,
        )
        print(yy)
