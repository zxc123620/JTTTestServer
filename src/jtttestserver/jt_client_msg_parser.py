#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/7 17:36
# Author:zhouxiaochuan
# Description:
import logging
import struct
from dataclasses import dataclass


class FunctionRegister:

    @staticmethod
    def register(func_code):
        """
        客户端函数代码注册器
        Args:
            func_code: 函数代码

        Returns:

        """
        code_map = {}

        def inner(func):
            code_map[func_code] = func

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return inner

    @classmethod
    def parser_msg_body(cls, data: bytes):
        pass

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

class JtClientMsgBodyParser:

    @classmethod
    @FunctionRegister.register(0x0001)
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
