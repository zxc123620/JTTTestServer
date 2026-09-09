#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/7 17:54
# Author:zhouxiaochuan
# Description:
import logging
import struct

from jtttestserver.data_function import DataFunction
from jtttestserver.jt_client_parser.client_obj.msg_header_info import JT808HeaderInfo, JT808MsgBodyProperty


class JT808ClientMessageParser:

    @classmethod
    def parser(cls, data: bytes):
        """
        解析JT808消息
        Args:
            data: 数据

        Returns:

        """
        # 数据转义解码
        data = DataFunction.de_escape(data)
        # 标志位(头)
        sign_byte_head = struct.unpack("B", data[:1])[0]
        # 消息头 解析
        header_info, last_index = cls.parser_header(data[1:])
        # 消息体长度
        msg_body_length = header_info.body_property.msg_body_length
        # 消息ID
        msg_id = header_info.msg_id
        # 消息体
        data_body_bytes = data[last_index:last_index + msg_body_length]
        last_index = last_index + msg_body_length
        # 校验位 (后面再校验)
        check_byte = struct.unpack("B", data[last_index:last_index + 1])[0]
        last_index += 1
        # 校验位(尾)
        sign_byte_tail = struct.unpack("B", data[last_index:last_index + 1])[0]
        # logging.info(
        #     f"标志位(头): {sign_byte_head}, 消息头: {header_bytes}, 校验位: {check_byte}, 校验位(尾): {sign_byte_tail}, 消息体: {data_body_bytes}")

    @classmethod
    def parser_header(cls, data: bytes):
        """
        解析消息头
        Args:
            data: 消息数据, 截断了从消息头开始的数据
        Returns:
        """
        last_index = 17
        # 【消息ID】2字节
        msg_id = struct.unpack("> H", data[:2])[0]
        # 【消息体属性】2字节  检查是否需要分包
        data_body_property = cls.parser_data_body_property(data[2:4])

        # 【版本号】1字节 【手机号】10字节 【消息序列号】2字节

        version, phone_number, msg_serial_number = struct.unpack("> B 10s H", data[4:17])
        header_info = JT808HeaderInfo(
            msg_id=msg_id,
            body_property=data_body_property,
            version=version,
            phone_number=phone_number,
            msg_sequence_number=msg_serial_number,

        )
        # 【消息属性】2字节  【消息包总数】2字节  【消息包当前号】2字节
        if data_body_property.subcontracting_flag == 1:
            last_index += 4
            # 分包
            msg_package_total, msg_package_current_number = struct.unpack("> H H",data[17:21])
            header_info.msg_package_total = msg_package_total
            header_info.msg_package_current_number = msg_package_current_number

        else:
            raise ValueError("消息体属性错误")
        return header_info, last_index

    @classmethod
    def parser_data_body_property(cls, data: bytes):
        """
        解析消息体属性（他在消息头里面）
        Args:
            data: 消息数据, 截断了从消息体属性字节开始的数据到
        Returns:
        """
        data = struct.unpack("> H", data)[0]
        # 提取消息体长度（位0-9，10位）
        msg_body_length = data & 0x3FF
        # 加密方式（位10-12，3位） 修正为 0x07
        data_encryption = (data >> 10) & 0x07
        # 子包标志（位13，1位）
        subcontracting_flag = (data >> 13) & 0x01
        # 版本标志（位14，1位）
        version_flag = (data >> 14) & 0x01
        # 保留（位15，1位）
        other = (data >> 15) & 0x01
        msg_body_property = JT808MsgBodyProperty(
            msg_body_length=msg_body_length,
            data_encryption=data_encryption,
            subcontracting_flag=subcontracting_flag,
            version_flag=version_flag,
            other=other
        )
        return msg_body_property