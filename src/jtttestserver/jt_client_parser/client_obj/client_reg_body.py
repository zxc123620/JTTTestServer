#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/9 18:04
# Author:zhouxiaochuan
# Description: 客户端注册消息体
from dataclasses import dataclass


@dataclass
class Jt808ClientRegBody:
    province: int  # 省份
    city: int  # 城市
    creator_id: bytes  # 制造商ID
    client_type: bytes # 终端类型
    client_id: bytes  # 终端ID
    car_license_plate_color: bytes  # 车牌颜色
    car_license_plate_number: bytes  # 车牌号或者车架号
