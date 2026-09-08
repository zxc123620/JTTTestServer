#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/8 17:50
# Author:zhouxiaochuan
# Description:

class JtServerMsgParser:

    @classmethod
    def combine_msg(cls, func_code: int, data_body_bytes: bytes):
        """
        组合消息
        Args:
            func_code: 函数码
            data_body_bytes: 消息体
        Returns:
            组合后的消息 bytes
        """
        msg = bytearray()
        msg.append(0x7d)


    @staticmethod
    def parser_basic_reply(self):
        pass