#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/9 16:49
# Author:zhouxiaochuan
# Description:

class MsgBodyRegister:

    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.code_map = {}

    @classmethod
    def register(cls, func_code):
        """
        客户端函数代码注册器
        Args:
            func_code: 函数代码

        Returns:

        """


        def inner(func):
            cls.code_map[func_code] = func

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return inner

    @classmethod
    def parser_msg_body(cls, data: bytes):
        """
        解析消息体
        Args:
            data: 消息体数据

        Returns:

        """
        pass
