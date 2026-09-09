#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/8 17:50
# Author:zhouxiaochuan
# Description:
from jtttestserver.jt_client_parser.jt_client_msg_parser import JTHeaderInfo


class Jt808ServerMsgBuilder:

    @classmethod
    def combine_msg(cls, header_info: JTHeaderInfo):
        """
        组合消息
        Args:
            header_info: 消息头
        Returns:
            组合后的消息 bytes
        """
        msg = bytearray()
        # 标识位(头)
        # msg.append(0x7e)
        # 消息头
        msg.extend(header_info.to_bytes())
        # 标识位(尾)
        # msg.append(0x7e)


    @staticmethod
    def parser_basic_reply(self):
        pass