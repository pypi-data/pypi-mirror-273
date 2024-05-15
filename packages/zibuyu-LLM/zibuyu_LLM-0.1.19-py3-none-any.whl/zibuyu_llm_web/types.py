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

from typing import Literal, Optional, Union
from dataclasses import dataclass


# #################### 公用模型类 ####################

@dataclass
class ReferenceLink:
    """回复中的相关链接"""

    title: str
    url: str


@dataclass
class AiAnswer:
    """AI回复"""

    content: str = ''
    is_success: bool = False
    latest_msg_id: str = ''  # 上一次消息id，有些AI需要用到
    conversation_id: str = ''  # 会话id，不同AI的称呼可能不同，这里统一为conversation_id
    audio_path_list: list[str] = None
    reference_link_list: Optional[list[ReferenceLink]] = None


# #################### ####################

@dataclass
class QwenPluginWebSearchResult:
    """通义千问 - 网页搜索插件结果 """
    url: str
    body: str
    title: str
    time: str
    host_name: str
    host_logo: str


@dataclass
class QwenChatContent:
    """通义千问 - 单次会话"""

    id: str
    role: str
    status: str
    content: str
    content_type: Literal["text", "text2image", "plugin", "referenceLink", "file", "image"]

    file_size: int = 0
    doc_id: str = ''

    # 插件类型特有字段，存储插件信息
    plugin_code: str = None
    plugin_name: str = None


@dataclass
class QwenWebResponse:
    """通义千问 - 对话响应模版 """

    content_type: Literal["text", "text2image",]
    content_from: Literal["text", "text2image",]

    # 回应内容列表，可能包含插件搜索结果、相关网页链接等
    content_list: Union[list[QwenChatContent], None]

    # 插件类型特有字段
    web_search_list: Union[list[QwenPluginWebSearchResult], None]
    reference_link_list: Union[list[ReferenceLink], None]

    # 文生图特有字段，存储图片地址
    image_url_list: Union[list[str], None]

    msg_id: str
    parent_msg_id: str
    session_id: str
    msg_status: str
    params: dict
    stop_reason: dict
    trace_id: dict

    ai_disclaimer: bool = False
    can_regenerate: bool = True
    can_share: bool = True
    can_show: bool = True
    can_feedback: bool = True
    session_warn_new: bool = False
    session_share: bool = True
    session_open: bool = True


@dataclass
class QwenChatHistory:
    """历史会话记录"""

    sender_type: str  # 发送者，用以区分用户与AI
    create_time: int  # 创建时间
    content_type: Literal["text", "text2image",]  # 消息类型

    session_id: str
    msg_id: str
    parent_msg_id: str

    msg_status: str  # 会话状态：是否完整生成

    content_list: Union[list[QwenChatContent], None]

    interrupted: bool = False  # AI生成内容时是否被打断
    ai_disclaimer: bool = False
    can_regenerate: bool = True
    can_share: bool = True
    can_show: bool = True


@dataclass
class QwenSession:
    """通义千问 - 会话"""

    user_id: str  # 用户id
    session_id: str  # 会话id
    create_time: str  # 创建时间
    modified_time: str  # 修改时间
    summary: str  # 标题
    session_type: str  # 会话类型
    error_msg: str  # 错误信息
    status: int  # 状态（未知字段）
    can_share: bool = True  #


@dataclass
class WanXianImage:
    """ 通义万相绘图结果 """

    resource_id: str
    oss_path: str
    url: str
    resize_url: str
    is_security: str
    task_id: str
    vague_url: str
    download_url: str


@dataclass
class XincMessageIssuer:
    """通义星辰聊天类型"""
    user_id: str
    user_name: str
    user_type: str


@dataclass
class XincChatContent:
    """通义星辰聊天内容"""
    chat_id: str
    original_content: str
    create_timestamp: str
    gmt_create: str
    is_greeting: bool
    message_id: str
    message_type: str
    session_id: str

    message_issuer: XincMessageIssuer


@dataclass
class XincChatHistory:
    """通义星辰聊天记录"""
    content_list: list[XincChatContent]
    total: int  # 总数量


@dataclass
class XincCharacter:
    """通义星辰角色"""

    name: str
    characterId: str


@dataclass
class XincCharacterInfo:
    """通义星辰角色信息"""

    character_name: str
    chat_room_name: str
    is_group_chat: bool
    characters: list[XincCharacter]

    chat_history: XincChatHistory


@dataclass
class BaiChuanSession:
    """通义百川会话"""

    id: int
    name: str
    auditStatus: int
    session_id: str
    has_message: int
    created_at: str
    status: int
    withDoc: bool
    createdAt: int


@dataclass
class BaiChuanChat:
    """通义百川聊天内容"""

    id: int
    parentId: int
    data: str
    userId: int
    chat_from: int
    messageId: str
    subId: int
    status: int
    auditStatus: int
    loading: bool
    rating: str
    createdAt: int
    attachments: list
    cites: list
    querys: list
    dragonImage: str
    history: bool
    len: int
