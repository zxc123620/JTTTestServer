#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/7 17:36
# Author:zhouxiaochuan
# Description:
import logging


class ClientDataTool:

    @classmethod
    def split_data(cls, data:bytes):
        """
        分割客户端请求数据
        Args:
            data: 数据

        Returns:

        """
        sign_byte_head = data[0]
        header_bytes = data[1:19]
        check_byte = data[-2]
        sign_byte_tail = data[-1]
        data_body_bytes = data[19:-2]
        logging.info(f"标志位(头): {sign_byte_head}, 消息头: {header_bytes}, 校验位: {check_byte}, 校验位(尾): {sign_byte_tail}, 消息体: {data_body_bytes}")


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

class JtClientFunction:


    @classmethod
    @ClientDataTool.register(0x0001)
    def basic_reply(cls, data):
        """
        基本回复函数
        Args:
            data: 回复数据

        Returns:

        """
        return data
