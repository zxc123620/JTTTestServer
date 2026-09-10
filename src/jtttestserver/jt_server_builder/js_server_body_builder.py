#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/9 16:57
# Author:zhouxiaochuan
# Description:
import datetime
import struct
import uuid
from dataclasses import dataclass

from jtttestserver.jt_type import Jt808ReplyType


class Jt808ServerMsgBodyBuilder:
    """
    服务器消息体构建器
    """

    def to_bytes(self) -> bytes:
        """
        将消息体转换为bytes
        Returns:
        """
        pass

@dataclass
class Jt808ServerBasicReplyBodyBuilder(Jt808ServerMsgBodyBuilder):
    """
    服务器基本回复构建器
    """
    reply_sequence_number: int  # 回复序列号
    replay_msg_id: int  # 回复消息ID
    replay_result: Jt808ReplyType

    def to_bytes(self) -> bytes:
        return struct.pack("> H H B", self.reply_sequence_number, self.replay_msg_id, self.replay_result.value)


@dataclass
class Jt808ServerTimeReplyBodyBuilder(Jt808ServerMsgBodyBuilder):
    """
    服务器时间回复构建器
    0x8004
    """
    server_time: str = datetime.datetime.now().strftime("%y%m%d%H%M%S")

    def to_bytes(self) -> bytes:
        return struct.pack("> 6s", bytes.fromhex(self.server_time))


@dataclass
class Jt808ServerRegisterReplyBodyBuilder(Jt808ServerMsgBodyBuilder):
    """
    服务器注册回复构建器
    0x8100
    """
    reply_sequence_number: int  # 应答流水号
    result: Jt808ReplyType
    authorization_code: str  # 授权码

    def to_bytes(self) -> bytes:
        data = bytearray()
        data.extend(struct.pack("> H B ", self.reply_sequence_number, self.result.value))
        data.extend(self.authorization_code.encode("gbk"))
        return data



