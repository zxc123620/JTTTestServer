#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/7 17:54
# Author:zhouxiaochuan
# Description:
import struct
from dataclasses import dataclass, field

class JTHeaderInfo:
    """
    消息头信息
    """
    msg_id: int = field(doc="消息ID")

@dataclass
class BaseJtMsgInfo:
    sign_byte_head: bytes = field(doc="标志位(头)")
    header_bytes: bytes = field(doc="消息头")
    check_byte: bytes = field(doc="校验位")
    sign_byte_tail: bytes = field(doc="校验位(尾)")
    data_body_bytes: bytes = field(doc="消息体")

    def header_split(self):
        """
        分割消息头
        Returns:

        """
        format = "> H H B 10s H"
        if len(self.header_bytes) > 16:
            pass
        elif len(self.header_bytes) == 16:
            pass
        struct.unpack("> H H B 10s H", self.header_bytes)
