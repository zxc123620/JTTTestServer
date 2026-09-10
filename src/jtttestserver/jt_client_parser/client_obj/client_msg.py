#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/10 10:15
# Author:zhouxiaochuan
# Description:
from dataclasses import dataclass
from typing import Generic

from jtttestserver.jt_client_parser.client_obj.basic_client_body import ClientBodyT
from jtttestserver.jt_client_parser.client_obj.msg_header_info import JT808HeaderInfo


@dataclass
class Jt808ClientMsgInfo(Generic[ClientBodyT]):
    """
    JT808客户端消息信息
    """
    sign_byte_head: int  # 标志位(头)
    header: JT808HeaderInfo  # 消息头
    data_body: ClientBodyT  # 消息体
    check_byte: int  # 校验位
    sign_byte_tail: int  # 标志位(尾)