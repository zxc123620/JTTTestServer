#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/9 18:01
# Author:zhouxiaochuan
# Description:
import struct
from dataclasses import dataclass
from typing import Optional



@dataclass
class JT808MsgBodyProperty:
    """
    消息体属性
    """
    msg_body_length: int  # 消息体长度
    data_encryption: int  # 数据加密
    subcontracting_flag: int  # 子包标志
    version_flag: int  # 版本标志
    other: int  # 保留

    def to_int(self) -> int:
        """
        将各字段组合为16位整数
        Returns:

        """
        value = self.msg_body_length & 0x3FF  # 位0-9
        value |= (self.data_encryption & 0x07) << 10  # 位10-12
        value |= (self.subcontracting_flag & 0x01) << 13  # 位13
        value |= (self.version_flag & 0x01) << 14  # 位14
        value |= (self.other & 0x01) << 15  # 位15
        return value

    def to_bytes(self):
        """
        转换为bytes
        Returns:

        """
        return struct.pack("> H", self.to_int())


@dataclass
class JT808HeaderInfo:
    """
    消息头信息
    """
    msg_id: int  # 消息ID
    body_property: JT808MsgBodyProperty  # 消息体属性
    version: int  # 版本号
    phone_number: bytes  # 手机号
    msg_sequence_number: int  # 消息序列号
    msg_package_total: Optional[int] = None  # 消息包总数
    msg_package_current_number: Optional[int] = None  # 消息包当前号

    def get_phone_number(self):
        """
        获取手机号
        Returns:

        """
        return int(self.phone_number.hex(), 16)


    def to_bytes(self):
        """
        转换为bytes
        Returns:

        """
        data = bytearray()
        basic_header = struct.pack("> H H B 10s H", self.msg_id, self.body_property.to_int(), self.version,
                                   self.phone_number, self.msg_sequence_number)
        data.extend(basic_header)
        if self.msg_package_total is not None and self.msg_package_current_number is not None:
            # 消息包总数和当前号
            basic_header_2 =  struct.pack("> H H", self.msg_package_total, self.msg_package_current_number)
            data.extend(basic_header_2)
        return data


@dataclass
class Jt808MsgInfo:
    """
    JT808消息信息
    """
    sign_byte_head: bytes  # 标志位(头)
    header_bytes: bytes  # 消息头
    data_body_bytes: bytes  # 消息体
    check_byte: bytes  # 校验位
    sign_byte_tail: bytes  # 校验位(尾)

