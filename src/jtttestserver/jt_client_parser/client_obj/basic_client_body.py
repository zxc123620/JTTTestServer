#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/10 09:28
# Author:zhouxiaochuan
# Description: 基本客户端消息体
from dataclasses import dataclass
from typing import TypeVar


@dataclass
class Jt808ClientBasicBody:
    pass


ClientBodyT  = TypeVar("ClientBodyT", bound=Jt808ClientBasicBody)

