#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/9 16:49
# Author:zhouxiaochuan
# Description:
import logging
import struct

from jtttestserver.jt_client_parser.client_obj.basic_client_body import Jt808ClientBasicBody


class Jt808ClientMsgBodyRegister:

    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.code_map = {}

    @classmethod
    def register(cls, msg_id: int):
        """
        客户端函数代码注册器
        Args:
            msg_id: 消息ID

        Returns:

        """


        def inner(func):
            cls.code_map[msg_id] = func

            def wrapper(*args, **kwargs):
                try:
                    data =  func(*args, **kwargs)
                    if isinstance(data, Jt808ClientBasicBody):
                        logging.info(f"解析消息体成功，消息ID：{msg_id:04x}，消息体数据：{data}")
                    return data
                except struct.error as e:
                    logging.error(f"解析消息体失败，消息ID：{msg_id:04x}，错误信息：{e}")
                    raise e
            return wrapper

        return inner

    @classmethod
    def parser_msg_body(cls, msg_id: int, data: bytes):
        """
        解析消息体
        Args:
            msg_id: 消息ID
            data: 消息体数据

        Returns:

        """
        # func_code = msg_id & 0x0000FFFF
        if msg_id not in cls.code_map:
            raise ValueError(f"未注册消息ID：{msg_id}, 已有注册的消息ID：{cls.code_map.keys()}")
        return cls.code_map[msg_id](data)
