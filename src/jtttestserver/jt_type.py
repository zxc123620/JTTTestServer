#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/7 17:43
# Author:zhouxiaochuan
# Description:
from enum import Enum


class Jt808ReplyType(Enum):
    SUCCESS = 0
    FAIL = 1
    ERROR = 2
    UNKNOWN = 3

class QueueType(Enum):
    """
    队列类型
    """
    RECV = "recv"
    SEND = "send"
