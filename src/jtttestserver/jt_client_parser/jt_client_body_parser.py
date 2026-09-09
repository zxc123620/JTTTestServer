#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/7 17:36
# Author:zhouxiaochuan
# Description:
import logging
import struct
from dataclasses import dataclass

from jtttestserver.jt_client_parser.client_obj.client_reg_body import Jt808ClientRegBody
from jtttestserver.register.client_func_register import ClientMsgBodyRegister


@dataclass
class BasicReplyInfo:
    """

    """
    serial_number: int #流水号
    reply_id: int # 回复ID
    result_code: int # 结果

    def get_result_str(self):
        """

        Returns:

        """
        msg = ["成功", "失败", "消息有误", "不支持"]
        return msg[self.result_code]

class Jt808ClientMsgBodyParser:

    @classmethod
    @ClientMsgBodyRegister.register(0x0001)
    def basic_reply(cls, data: bytes):
        """
        基本回复函数
        Args:
            data: 回复数据
        Returns:
            基本回复信息
        Raises:
            ValueError: 基本回复数据格式错误
        """
        try:
            serial_number, reply_id, result_code = struct.unpack("> H H H", data)
        except struct.error:
            raise ValueError("基本回复数据格式错误")
        basic_reply_info = BasicReplyInfo(serial_number, reply_id, result_code)
        return basic_reply_info

    @classmethod
    @ClientMsgBodyRegister.register(0x0002)
    def heartbeat(cls, data: bytes):
        """
        心跳函数
        Args:
            data: 心跳数据
        Returns:
        """
        return "心跳,没有消息体"

    @classmethod
    @ClientMsgBodyRegister.register(0x0004)
    def get_server_time(cls, data: bytes):
        """
        获取服务器时间函数
        Args:
            data: 获取服务器时间数据
        Returns:
        """
        return "获取服务器时间,没有消息体"


    @classmethod
    @ClientMsgBodyRegister.register(0x0100)
    def client_register(cls, data: bytes):
        """
        客户端注册函数
        Args:
            data: 注册数据
        Returns:

        """
        try:
            province, city, creator_id, client_type, client_id, car_license_plate_color = struct.unpack("> H H 11s 30s 30s B ", data[:76])
            car_license_plate_number = data[76:]
            client_reg_body = Jt808ClientRegBody(province, city, creator_id, client_type, client_id, car_license_plate_color, car_license_plate_number)
            return client_reg_body
        except struct.error:
            raise ValueError("客户端注册数据格式错误")

