# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_LLM
author: 子不语
date: 2024/5/9
contact: 【公众号】思维兵工厂
description: 
--------------------------------------------
"""

from .qwen import QwenWeb
from .xinchen import XinChenWeb
from .xunfei import XunFeiWeb
from .kimi import KimiWeb
from .minmax import MinMaxWeb
from .deepseek import DeepSeekWeb
from .baichuan import BaiChuanWeb
from .wanxiang import WanXiangWeb
from . import errors
from . import types


__all__ = [
    'QwenWeb',
    'XinChenWeb',
    'XunFeiWeb',
    'KimiWeb',
    'MinMaxWeb',
    'DeepSeekWeb',
    'BaiChuanWeb',
    'WanXiangWeb',
    'errors',
    'types'
]
