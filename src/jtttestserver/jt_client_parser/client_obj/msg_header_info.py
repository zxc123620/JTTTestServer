#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/9 18:01
# Author:zhouxiaochuan
# Description:
import struct
from dataclasses import dataclass
from typing import Optional

from jtttestserver.jt_client_parser.client_obj.basic_client_body import Jt808ClientBasicBody


@dataclass
class JT808MsgBodyProperty(Jt808ClientBasicBody):
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

    def __str__(self) -> str:
        return f"消息体长度: {self.msg_body_length}, 数据加密: {self.data_encryption}, 子包标志: {self.subcontracting_flag}, 版本标志: {self.version_flag}, 保留: {self.other}"


@dataclass
class JT808HeaderInfo(Jt808ClientBasicBody):
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

    def __str__(self) -> str:
        return (f"消息ID: {self.msg_id}, "
                f"消息体属性: ["
                f"{self.body_property}"
                f"],"
                f"版本号: {self.version}, "
                f"手机号: {self.phone_number.hex()}, "
                f"消息序列号: {self.msg_sequence_number}, "
                f"消息包总数: {self.msg_package_total if self.msg_package_total is not None else '无'}, "
                f"消息包当前号: {self.msg_package_current_number if self.msg_package_current_number is not None else '无'}")



