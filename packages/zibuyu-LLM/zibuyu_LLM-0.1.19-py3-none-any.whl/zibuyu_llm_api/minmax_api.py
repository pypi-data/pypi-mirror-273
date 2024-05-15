# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: mind_workshop
author: 子不语
date: 2024/3/12
contact: 【公众号】思维兵工厂
description: MinMax平台大模型api调用【官网：https://www.minimaxi.com/】

分析：
    1. 该平台的语音合成效果非常好，
    2. 文本生成能力，只有abab5.5和abab6模型让人满意；同时在参数中指定示例对话、限制返回格式等功能
--------------------------------------------
"""

import time
import json
import asyncio
import requests
import aiohttp
from dataclasses import dataclass
from typing import Literal, Optional, List

start = time.time()

# 官方模型列表，如若更新，可以自行添加
MODEL = {
    # 文本大模型
    'text': {
        'abab5.5s-chat': '',
        'abab5.5-chat': '',
        'abab6-chat': '',
        'abab6.5-chat': '',
        'abab6.5s-chat': '',
    },
    # 语音大模型，用于文本转语音功能
    'voice': {

        'speech-01': '',  # 中文
        'speech-02': '',  # 中文、英文、中英混合、日文、韩文
        'voice_choice': {
            "male-qn-qingse": "青涩青年音色",
            "male-qn-jingying": "精英青年音色",
            "male-qn-badao": "霸道青年音色",
            "male-qn-daxuesheng": "青年大学生音色",
            "female-shaonv": "少女音色",
            "female-yujie": "御姐音色",
            "female-chengshu": "成熟女性音色",
            "female-tianmei": "甜美女性音色",
            "presenter_male": "男性主持人",
            "presenter_female": "女性主持人",
            "audiobook_male_1": "男性有声书1",
            "audiobook_male_2": "男性有声书2",
            "audiobook_female_1": "女性有声书1",
            "audiobook_female_2": "女性有声书2",
            "male-qn-qingse-jingpin": "青涩青年音色-beta",
            "male-qn-jingying-jingpin": "精英青年音色-beta",
            "male-qn-badao-jingpin": "霸道青年音色-beta",
            "male-qn-daxuesheng-jingpin": "青年大学生音色-beta",
            "female-shaonv-jingpin": "少女音色-beta",
            "female-yujie-jingpin": "御姐音色-beta",
            "female-chengshu-jingpin": "成熟女性音色-beta",
            "female-tianmei-jingpin": "甜美女性音色-beta",
        }
    }
}


@dataclass
class Glyph:
    msg_type: Literal['json_value', 'raw2', '1']
    json_properties: dict = None
    raw_glyph: str = None
    property_list: list = None

    def __post_init__(self):
        if self.msg_type not in ['json_value', 'raw2', '1']:
            raise ValueError(f"Invalid msg_type '{self.msg_type}'. Must be one of ['json_value', 'raw2', '1']")

        if self.msg_type == 'json_value':
            if self.json_properties is None:
                raise ValueError("json_properties must be set when msg_type is 'json_value'")

        if self.msg_type == 'raw2':
            if self.raw_glyph is None:
                raise ValueError("raw_glyph must be set when msg_type is 'raw2'")


@dataclass
class MessageNormal:
    sender_type: str
    text: str


@dataclass
class MessagePro:
    sender_type: str
    sender_name: str
    text: str


@dataclass
class Bot:
    """定义bot：传入bot名称和prompt"""
    bot_name: str
    content: str


@dataclass
class ReplyBot:
    """指定回复的bot"""

    sender_name: str
    bot_list: List[Bot]
    sender_type: str = 'BOT'

    def __post_init__(self):
        if self.sender_name not in self.bot_list:
            raise ValueError(f"Invalid bot name '{self.bot_name}'. Must be one of {self.bot_list}")


class MinMaxGPT(object):
    base_host = 'https://api.minimax.chat'

    def __init__(self, group_id: str, api_key: str):
        self.group_id = group_id
        self.api_key = api_key

        # 文本转语音接口
        self.text2voice_url = f'{self.base_host}/v1/text_to_speech'

        # 文本转语音接口，支持长文本，长度限制<50000字符
        self.text2voice_pro_url = f'{self.base_host}/v1/t2a_pro'

        # 文本生成接口
        self.text2text_url_pro = f'{self.base_host}/v1/text/chatcompletion_pro'

        # 文本生成接口，支持超级文本，异步合成，长度最大支持1000万字符
        self.text2text_large_url = f'{self.base_host}/v1/t2a_async'

        # 文本生成接口，旧版。官方推荐使用上面那个，计费一样
        self.text2text_url = f'{self.base_host}/v1/text/chatcompletion'

        self.temperature: float = 0.9  # 设置随机性
        self.top_p: float = 0.9  # 设置随机性
        self.single_answer: str = ''  # 单次回答的文本
        self.total_tokens: int = 0  # 消耗总tokens数
        self.single_tokens: int = 0  # 消耗总tokens数
        self.messages_normal: list = []  # 历史会话记录
        self.messages_pro: list = []  # 历史会话记录

        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        self.start = 0

    @staticmethod
    def check_request_data(
            text: Optional[str] = None,
            pitch: int = 0,
            vol: float = 2.0,
            speed: float = 1.0,
            output_format: str = 'mp3',
            voice_id: str = 'male-qn-qingse',
            model: str = 'speech-02',
            char_to_pitch: list[str] = None,
            timber_weights: list[dict] = None,
    ):

        if model not in MODEL['voice'].keys():
            raise ValueError(f'输入模型不支持，请从以下模型选择： {[model for model in MODEL["voice"].keys()]}')

        if voice_id not in MODEL['voice']['voice_choice'].keys():
            raise ValueError(f'输入的语音id不支持！')

        data = {
            "voice_id": voice_id,
            "output_format": output_format,
            "text": text,
            "model": model,
            "speed": speed,
            "vol": vol,
            "pitch": pitch,
        }

        if timber_weights:
            if not isinstance(timber_weights, list):
                raise TypeError(f'timber_weights参数类型错误，应为list类型！')

            for item in timber_weights:
                if not isinstance(item, dict):
                    raise TypeError(f'timber_weights参数类型错误，应为list[dict]类型！')
                if 'voice_id' not in item:
                    raise KeyError(f'timber_weights参数格式错误，字典元素需包含voice_id项')
                if 'weight' not in item:
                    raise KeyError(f'timber_weights参数格式错误，字典元素需包含weight项')
            data['timber_weights'] = timber_weights

        if char_to_pitch:
            if not isinstance(char_to_pitch, list):
                raise TypeError(f'char_to_pitch参数类型错误，应为list类型！')
            data['char_to_pitch'] = char_to_pitch

        return data

    async def _async_text2voice(self, file_path: str, data: dict, task_type: Literal['long_text', 'text'] = 'text'):

        if task_type == 'long_text':
            host = self.text2voice_pro_url
        else:
            host = self.text2voice_url

        async with aiohttp.ClientSession() as session:
            async with session.post(host, headers=self.headers, json=data) as response:
                if response.status != 200 or "json" in response.headers["Content-Type"]:
                    print("调用失败！", f"状态码为：【{response.status_code}】")
                    print(response.text)
                    return False
                with open(file_path, "wb") as f:
                    f.write(await response.content.read())

    async def async_text2voice(self, text: str,
                               file_path: str,
                               pitch: int = 0,
                               vol: float = 2.0,
                               speed: float = 1.0,
                               output_format: str = 'mp3',
                               voice_id: str = 'male-qn-qingse',
                               model: str = 'speech-02',
                               char_to_pitch: list[str] = None,
                               timber_weights: list[dict] = None,
                               ):

        data = self.check_request_data(text, pitch, vol, speed, output_format, voice_id, model,
                                       char_to_pitch, timber_weights)
        return await self._async_text2voice(file_path, data)

    async def _text2voice_list(self, text_list: list[str],
                               file_path_list: list[str],
                               pitch: int = 0,
                               vol: float = 2.0,
                               speed: float = 1.0,
                               output_format: str = 'mp3',
                               voice_id: str = 'male-qn-qingse',
                               model: str = 'speech-02',
                               char_to_pitch: list[str] = None,
                               timber_weights: list[dict] = None):

        if len(text_list) != len(file_path_list):
            raise ValueError(f'输入的文本和文件路径数量不匹配！')

        task_list = []
        for text, file_path in zip(text_list, file_path_list):
            task = asyncio.create_task(
                self.async_text2voice(text, file_path, pitch, vol, speed, output_format, voice_id, model,
                                      char_to_pitch, timber_weights))
            task.add_done_callback(lambda t: None)
            task_list.append(task)

        while True:

            if all([task.done() for task in task_list]):
                return True
            else:
                await asyncio.sleep(0.2)

    def text2voice_list(self, text_list: list[str],
                        file_path_list: list[str],
                        pitch: int = 0,
                        vol: float = 2.0,
                        speed: float = 1.0,
                        output_format: str = 'mp3',
                        voice_id: str = 'male-qn-qingse',
                        model: str = 'speech-02',
                        char_to_pitch: list[str] = None,
                        timber_weights: list[dict] = None):

        """
        异步合成多个语音
        :param text_list: 需合成的文本列表
        :param file_path_list: 合成语音的存放路径，列表个数需与text_list一致
        :param pitch:
        :param vol:
        :param speed:
        :param output_format:
        :param voice_id:
        :param model:
        :param char_to_pitch:
        :param timber_weights:
        :return:
        """

        return asyncio.run(
            self._text2voice_list(text_list, file_path_list, pitch, vol, speed, output_format, voice_id, model,
                                  char_to_pitch, timber_weights))

    # #################### 下面为同步请求 ####################

    def _text2voice(self, file_path: str, data: dict, task_type: Literal['long_text', 'text'] = 'text'):
        """
        语音合成公用方法
        :param file_path: 音频文件的保存路径
        :param data: 请求体
        :return:
        """

        if task_type == 'long_text':
            response = requests.post(self.text2voice_pro_url, headers=self.headers, json=data)
        else:
            response = requests.post(self.text2voice_url, headers=self.headers, json=data)

        if response.status_code != 200 or "json" in response.headers["Content-Type"]:
            print("调用失败！", f"状态码为：【{response.status_code}】")
            print(response.text)
            return False
        with open(file_path, "wb") as f:
            f.write(response.content)
        return True

    def text2voice(self, text: str,
                   file_path: str,
                   pitch: int = 0,
                   vol: float = 2.0,
                   speed: float = 1.0,
                   output_format: str = 'mp3',
                   voice_id: str = 'male-qn-qingse',
                   model: str = 'speech-02',
                   char_to_pitch: list[str] = None,
                   timber_weights: list[dict] = None, ):
        """
        文本转语音
        :param text: 文本
        :param file_path: 音频路径
        :param pitch: 音调大小，范围[-12, 12]，0为原音色输出，取值需为整数
        :param vol: 音量大小，范围(0, 10]，取值越大，音量越高
        :param speed: 语速大小，范围[0.5, 2]，取值越大，语速越高
        :param output_format: 生成声音的音频格式,可选范围：mp3、wav、pcm、flac、aac
        :param voice_id: 语音id
        :param model: 模型
        :param timber_weights: 音色混合相关信息，传入将会覆盖voice_id
        :param char_to_pitch: 替换需要特殊标注的文字、符号及对应的注音，声调用数字代替，
            一声（阴平）为1，二声（阳平）为2，三声（上声）为3，四声（去声）为4），轻声为5。
            ["燕少飞/(yan4)(shao3)(fei1)"]  ["omg/oh my god","=/等于"]
        """

        data = self.check_request_data(text, pitch, vol, speed, output_format, voice_id, model,
                                       char_to_pitch, timber_weights)
        return self._text2voice(file_path, data)

    def check_task_status(self, task_id: str):
        """检查提交的文本配音任务是否完成"""

        url = f"https://api.minimax.chat/query/t2a_async_query?GroupId={self.group_id}&task_id={task_id}"

        payload = {}

        response = requests.request("GET", url, headers=self.headers, data=payload)

        print(response.text)

    def text2voice_async(self, text_file_path: str,
                         pitch: int = 0,
                         vol: float = 2.0,
                         speed: float = 1.0,
                         audio_sample_rate: Literal[16000, 24000, 32000] = 32000,
                         bitrate: Literal[32000, 64000, 128000] = 128000,
                         output_format: str = 'mp3',
                         voice_id: str = 'male-qn-qingse',
                         char_to_pitch: list[str] = None,
                         timber_weights: list[dict] = None,
                         ):
        """
        文本转语音，超长文本版，最高支持1000万字符。仅支持speech-01
        :param text_file_path: 长度限制<10000000字符，格式为zip。打包上传，包里应只包含txt或json文件（压缩包内为同一格式文件），
            json文件会有三个字段，["title", "content", "extra"]，分别表示标题，正文，作者。
            json里会有三个字段，["title", "content", "extra"]，分别是标题，正文，作者的话，
            需要产出三份结果，一共9个文件放在一个文件夹里。如果某字段不存在，或者内容为空，则不生成相应文件。
        :param pitch: 音调大小，范围[-12, 12]，0为原音色输出，取值需为整数
        :param vol: 音量大小，范围(0, 10]，取值越大，音量越高
        :param speed: 语速大小，范围[0.5, 2]，取值越大，语速越高
        :param audio_sample_rate: 生成声音的采样率，范围[16000,24000,32000]，默认为32000
        :param bitrate: 生成声音的比特率，范围[32000, 64000，128000]，默认为128000
        :param output_format: 生成声音的音频格式,可选范围：mp3、wav、pcm、flac、aac
        :param voice_id: 语音id
        :param model: 模型
        :param timber_weights: 音色混合相关信息，传入将会覆盖voice_id
        :param char_to_pitch: 替换需要特殊标注的文字、符号及对应的注音，声调用数字代替，
            一声（阴平）为1，二声（阳平）为2，三声（上声）为3，四声（去声）为4），轻声为5。
            ["燕少飞/(yan4)(shao3)(fei1)"]  ["omg/oh my god","=/等于"]
        """

        text = open(text_file_path, 'r', encoding='utf-8')

        data = self.check_request_data(text, pitch, vol, speed, output_format, voice_id, 'speech-01',
                                       char_to_pitch, timber_weights)
        data['audio_sample_rate'] = audio_sample_rate
        data['bitrate'] = bitrate

        result = requests.post(self.text2text_large_url, headers=self.headers, json=data)

        print(result.text)
        with open(text_file_path.replace('.zip', '(任务记录).txt'), mode='w', encoding='utf-8') as f:
            f.write(result.text)

    def text2voice_long_text(self, text: str,
                             file_path: str,
                             pitch: int = 0,
                             vol: float = 2.0,
                             speed: float = 1.0,
                             audio_sample_rate: Literal[16000, 24000, 32000] = 32000,
                             bitrate: Literal[32000, 64000, 128000] = 128000,
                             output_format: str = 'mp3',
                             voice_id: str = 'male-qn-qingse',
                             model: str = 'speech-02',
                             char_to_pitch: list[str] = None,
                             timber_weights: list[dict] = None,
                             ):
        """
        文本转语音，长文本版，长度限制<50000字符
        :param text: 文本
        :param file_path: 音频路径
        :param pitch: 音调大小，范围[-12, 12]，0为原音色输出，取值需为整数
        :param vol: 音量大小，范围(0, 10]，取值越大，音量越高
        :param speed: 语速大小，范围[0.5, 2]，取值越大，语速越高
        :param audio_sample_rate: 生成声音的采样率，范围[16000,24000,32000]，默认为32000
        :param bitrate: 生成声音的比特率，范围[32000, 64000，128000]，默认为128000
        :param output_format: 生成声音的音频格式,可选范围：mp3、wav、pcm、flac、aac
        :param voice_id: 语音id
        :param model: 模型
        :param timber_weights: 音色混合相关信息，传入将会覆盖voice_id
        :param char_to_pitch: 替换需要特殊标注的文字、符号及对应的注音，声调用数字代替，
            一声（阴平）为1，二声（阳平）为2，三声（上声）为3，四声（去声）为4），轻声为5。
            ["燕少飞/(yan4)(shao3)(fei1)"]  ["omg/oh my god","=/等于"]
        """

        if audio_sample_rate not in [16000, 24000, 32000]:
            raise ValueError(f'audio_sample_rate参数错误，应为16000、24000、32000之一！')
        if bitrate not in [32000, 64000, 128000]:
            raise ValueError(f'bitrate参数错误，应为32000、64000、128000之一！')

        data = self.check_request_data(text, pitch, vol, speed, output_format, voice_id, model,
                                       char_to_pitch, timber_weights)
        data['audio_sample_rate'] = audio_sample_rate
        data['bitrate'] = bitrate
        return self._text2voice(file_path, data, task_type='long_text')

    def parse_chunk_delta(self, chunk_str: str, handle_type: Literal['new', 'normal'] = 'new') -> str:
        """
        处理文本大模型流式输出时的数据
        :param chunk_str: 单次返回的数据，字符串格式
        :param handle_type: 指定接口类型，新旧接口逻辑不同
        :return:
        """

        try:
            error_dict = json.loads(chunk_str)
            print("error_msg: ", error_dict)
            return ''
        except:
            pass

        parsed_data = json.loads(chunk_str[6:])

        # 最后一次通讯，将会回复所有文本以及通讯信息，这里将文本全部内容保存到single_answer中
        if "usage" in parsed_data:
            self.single_answer = parsed_data['reply']
            total_tokens = parsed_data["usage"]["total_tokens"]
            self.total_tokens += total_tokens
            self.single_tokens = total_tokens
            return ''  # 最后一次通讯，返回空字符串

        try:
            if handle_type == 'old':
                delta_content = parsed_data["choices"][0]["delta"]
            else:
                delta_content = parsed_data["choices"][0]["messages"][0]["text"]
            return delta_content
        except:
            print(parsed_data)

    def set_temperature(self, value):
        if not isinstance(value, float):
            raise TypeError(f'temperature参数类型错误，应为float！')
        if not 0 < value <= 1:
            raise ValueError(f'temperature参数范围错误，应为(0,1]！')
        self.temperature = value
        return self.temperature

    def set_top_p(self, value):
        if not isinstance(value, float):
            raise TypeError(f'top_p参数类型错误，应为float！')
        if not 0 < value <= 1:
            raise ValueError(f'top_p参数范围错误，应为(0,1]！')
        self.top_p = value
        return self.top_p

    def check_params(self,
                     prompt: str = "",
                     model: str = "abab5.5s-chat",
                     tokens_to_generate: int = 1024,
                     temperature: float = 0.9,
                     top_p: float = 0.9,
                     stream: bool = False, ) -> dict:
        """
        检查输入的各个参数是否符合要求
        :param stream:
        :param prompt:
        :param model:
        :param tokens_to_generate:
        :param temperature:
        :param top_p:
        :return:
        """

        if model not in MODEL['text'].keys():
            raise ValueError(f"model参数错误，目前支持的模型有：{[model for model in MODEL['text'].keys()]}")

        # 将之前的单次回答清零
        self.single_answer = ''

        self.set_temperature(temperature)
        self.set_top_p(top_p)

        payload = {
            "model": model,
            "tokens_to_generate": tokens_to_generate,
            "stream": stream,
            "use_standard_sse": True,  # 结果分批返回，以一个换行为分割符
            "temperature": self.temperature,  # 控制输出的随机性
            "top_p": self.top_p,  # 控制输出的随机性
            "messages": self.messages_normal
        }

        if prompt:
            payload['prompt'] = prompt

        return payload

    def ask_normal(self, question: str,
                   prompt: str = "",
                   stream: bool = False,
                   model: str = "abab5.5s-chat",
                   tokens_to_generate: int = 1024,
                   temperature: float = 0.9,
                   top_p: float = 0.9,
                   messages: list[MessageNormal] = None,
                   callback_func=None,
                   ) -> str:
        """
        文本生成普通接口，基于自然语言交互的文本生成能力接口
        不包含功能支持，比如：多人对话、对话示例，支持集合搜索引擎、调用自定义函数、限制返回格式等。
        :param question: 提问的文本
        :param prompt: prompt，不提供时将使用内置prompt
        :param stream: 是否流式输出
        :param model: 大模型的版本
        :param tokens_to_generate: 允许输出的最大tokens数。这个参数不会影响模型本身的生成效果，而是仅仅截断生成文本。
        :param temperature: float，(0,1]  较高的值将使输出更加随机，而较低的值将使输出更加集中和确定。
        :param top_p: float，(0,1]  数值越小结果确定性越强；数值越大，结果越随机。建议temperature和top_p同时只调整其中一个
        :param messages: 历史信息
        :param callback_func: 流式输出时，每次接收到信息的处理函数
        :return:
        """

        if not prompt:
            prompt = "你是一个非常出色的人工智能助手，帮助用户解决各方面问题。"

        # 检查历史会话信息
        if messages:
            for message_obj in messages:
                if not isinstance(message_obj, MessageNormal):
                    raise TypeError(f"messages参数类型错误，应为list[MessageNormal]！")
                self.messages_normal.append({"sender_type": message_obj.sender_type,
                                             "text": message_obj.text})
        self.messages_normal.append({"sender_type": 'USER',
                                     "text": question})

        payload = self.check_params(prompt, model, tokens_to_generate, temperature, top_p, stream)

        payload["role_meta"] = {"user_name": "我", "bot_name": "专家"}
        payload["messages"] = self.messages_normal

        if stream:
            response = requests.post(self.text2text_url, headers=self.headers, json=payload, stream=True)
        else:
            response = requests.post(self.text2text_url, headers=self.headers, json=payload)

        if callback_func and callable(callback_func):

            for chunk in response.iter_lines():
                if chunk:
                    chunk_str = chunk.decode("utf-8")
                    chunk_content = self.parse_chunk_delta(chunk_str, handle_type='normal')
                    callback_func(chunk_content)
        else:
            data = json.loads(response.text)
            print(data)
            self.single_answer = data['reply']
            self.single_tokens = data['usage']['total_tokens']
            self.total_tokens += self.single_tokens

        return self.single_answer

    def ask(
            self,
            question: str,
            messages: list[MessagePro] = None,
            prompt: str = "",
            stream: bool = False,
            bot_setting: list[Bot] = None,
            reply_bot: Bot = None,
            model: str = "abab5.5s-chat",
            tokens_to_generate: int = 1024,
            temperature: float = 0.9,
            top_p: float = 0.9,
            sample_messages: list[MessagePro] = None,
            glyph: Glyph = None,
            callback_func=None,
    ) -> str:
        """
        文本生成新接口，提供了更强大的问答和文本生成能力，
        包括多人对话、对话示例，支持集合搜索引擎、调用自定义函数、限制返回格式，
        适合于复杂的对话交互和深度内容创作设计的场景。
        :param question: 提问的文本
        :param messages: 历史会话信息
        :param prompt: 不提供时将使用内置prompt
        :param stream: 是否流式输出
        :param bot_setting: 机器人列表
        :param reply_bot: 指定回复机器人
        :param model: 大模型的版本
        :param tokens_to_generate: 允许输出的最大tokens数
        :param temperature:
        :param top_p:
        :param sample_messages: 数据示例
        :param glyph: 数据格式要求
        :param callback_func: 流式输出时，每次接收到信息的处理函数
        :return:
        """

        payload = self.check_params('', model, tokens_to_generate, temperature, top_p, stream)
        payload["sample_messages"] = [
            # {
            #     "sender_type": "USER",
            #     "sender_name": "小明",
            #     "text": "把A5处理成红色，并修改内容为minimax"
            # },
            # {
            #     "sender_type": "BOT",
            #     "sender_name": "MM智能助理",
            #     "text": "select A5 color red change minimax"
            # }
        ]

        if not bot_setting:
            payload["bot_setting"] = [{"bot_name": "Mark", "content": prompt, }]
            payload["reply_constraints"] = {"sender_type": "BOT", "sender_name": "Mark"}
        else:

            # if not reply_bot_name:
            #     raise ValueError(f"bot_setting不为空时，reply_bot_name必须为指定范围内的值")

            payload["bot_setting"] = []
            for bot_obj in bot_setting:
                if not isinstance(bot_obj, Bot):
                    raise TypeError(f"bot_setting参数类型错误，应为list[Bot]！")
                payload["bot_setting"].append({"bot_name": bot_obj.bot_name, "content": bot_obj.content, })
            payload["reply_constraints"] = {"sender_type": "BOT", "sender_name": reply_bot.bot_name}

        # 设定历史会话
        payload["messages"] = []
        if messages:
            for message_obj in messages:
                if not isinstance(message_obj, MessagePro):
                    raise TypeError(f"messages参数类型错误，应为list[MessagePro]！")
                payload["messages"].append({"sender_type": message_obj.sender_type,
                                            "sender_name": message_obj.sender_name,
                                            "text": message_obj.text})
        # 添加本次提问
        payload["messages"].append({"sender_type": "USER",
                                    "sender_name": "小明",
                                    "text": question})

        # 设定回复示例
        payload['sample_messages'] = []
        if sample_messages:
            for sample_message_obj in sample_messages:
                if not isinstance(sample_message_obj, MessagePro):
                    raise TypeError(f"sample_messages参数类型错误，应为list[MessagePro]！")

                payload["sample_messages"].append({"sender_type": sample_message_obj.sender_type,
                                                   "sender_name": sample_message_obj.sender_name,
                                                   "text": sample_message_obj.text})

        # 设置回复文本的格式
        if glyph:
            payload["reply_constraints"]['glyph'] = {'type': glyph.msg_type}

            if glyph.msg_type == 'raw2':
                payload["reply_constraints"]['glyph']['type'] = glyph.raw_glyph
            if glyph.msg_type == 'json_value':
                payload["reply_constraints"]['glyph']['json_properties'] = glyph.json_properties

            payload["stream"] = False  # glyph和stream不能同时使用

        if stream:
            response = requests.post(self.text2text_url_pro, headers=self.headers, json=payload, stream=True)
        else:
            response = requests.post(self.text2text_url_pro, headers=self.headers, json=payload)

        if callback_func and callable(callback_func) and payload["stream"]:

            for chunk in response.iter_lines():
                if chunk:
                    chunk_str = chunk.decode("utf-8")
                    chunk_content = self.parse_chunk_delta(chunk_str)
                    callback_func(chunk_content)
        else:
            data = json.loads(response.text)

            self.single_answer = data['reply']
            self.single_tokens = data['usage']['total_tokens']
            self.total_tokens += self.single_tokens

        return self.single_answer
