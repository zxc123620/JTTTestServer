#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/9 16:54
# Author:zhouxiaochuan
# Description:
from jtttestserver.register.func_code_register import MsgBodyRegister


class Jt808ServerMsgBodyRegister(MsgBodyRegister):

    @classmethod
    def parser_msg_body(cls, data: bytes):
        pass