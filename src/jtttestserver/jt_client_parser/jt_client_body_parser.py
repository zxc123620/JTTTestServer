#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/7 17:36
# Author:zhouxiaochuan
# Description:
import logging
import struct
from dataclasses import dataclass

from jtttestserver.jt_client_parser.client_obj.client_auth_body import Jt808ClientAuthBody
from jtttestserver.jt_client_parser.client_obj.client_position_body import Jt808ClientPositionBody
from jtttestserver.jt_client_parser.client_obj.client_reg_body import Jt808ClientRegBody
from jtttestserver.register.client_func_register import Jt808ClientMsgBodyRegister


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
    @Jt808ClientMsgBodyRegister.register(0x0001)
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
    @Jt808ClientMsgBodyRegister.register(0x0002)
    def heartbeat(cls, data: bytes):
        """
        心跳函数
        Args:
            data: 心跳数据
        Returns:
        """
        return "心跳,没有消息体"
    @classmethod
    @Jt808ClientMsgBodyRegister.register(0x0003)
    def client_log_out(cls, data: bytes):
        """
        客户端注销函数
        Args:
            data: 注销数据
        Returns:
        """
        return "注销客户端,没有消息体"


    @classmethod
    @Jt808ClientMsgBodyRegister.register(0x0004)
    def get_server_time(cls, data: bytes):
        """
        获取服务器时间函数
        Args:
            data: 获取服务器时间数据
        Returns:
        """
        return "获取服务器时间,没有消息体"



    @classmethod
    @Jt808ClientMsgBodyRegister.register(0x0100)
    def client_register(cls, data: bytes):
        """
        客户端注册函数
        Args:
            data: 注册数据
        Returns:

        """
        province, city, creator_id, client_type, client_id, car_license_plate_color = struct.unpack("> H H 11s 30s 30s B ", data[:76])
        car_license_plate_number = data[76:]
        client_reg_body = Jt808ClientRegBody(province, city, creator_id, client_type, client_id, car_license_plate_color, car_license_plate_number)
        return client_reg_body


    @classmethod
    @Jt808ClientMsgBodyRegister.register(0x0102)
    def client_login(cls, data: bytes):
        """
        客户端登录函数
        Args:
            data: 登录数据

        Returns:

        """
        # 鉴权码长度
        auth_len = struct.unpack("> B", data[:1])[0]
        # 鉴权码
        auth_code_content = data[1:auth_len+1]
        # auth_code_content_str = auth_code_content.decode("gbk")
        # 客户端IMEI 版本号
        client_imei, soft_version = struct.unpack("> 15s 20s", data[auth_len+1:])
        client_auth_body = Jt808ClientAuthBody(auth_len, auth_code_content, client_imei, soft_version)
        return client_auth_body

    @classmethod
    @Jt808ClientMsgBodyRegister.register(0x0200)
    def client_position_upload(cls, data: bytes):
        """
        客户端位置上传函数
        Args:
            data: 位置上传数据

        Returns:

        """
        alarm_flag , status, latitude, longitude, altitude, speed, direction, time_bytes = struct.unpack("> I I I I H H H 6s", data)
        client_position_body = Jt808ClientPositionBody(alarm_flag, status, latitude, longitude, altitude, speed, direction, time_bytes)
        return client_position_body
