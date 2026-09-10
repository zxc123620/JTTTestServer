#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/10 09:24
# Author:zhouxiaochuan
# Description: 客户端位置上传消息体
from dataclasses import dataclass

from jtttestserver.jt_client_parser.client_obj.basic_client_body import Jt808ClientBasicBody

@dataclass
class Jt808ClientPositionBody(Jt808ClientBasicBody):
    alarm_flag: int # 报警标志
    status: int # 状态
    latitude: int # 纬度
    longitude: int # 经度
    altitude: int # 海拔
    speed: int # 速度
    direction: int # 方向
    time_bytes: bytes # 时间
    @property
    def latitude(self) -> float:
        return self.latitude / 1000000

    @property
    def longitude(self) -> float:
        return self.longitude / 1000000


    def get_time_str(self):
        """
        获取时间字符串
        Returns:
        """
        return self.time_bytes.hex()



    def __str__(self) -> str:
        return (f"报警标志: {self.alarm_flag},"
                f"状态标志: {self.status},"
                f"纬度: {self.latitude}, "
                f"经度: {self.longitude}, "
                f"海拔: {self.altitude}m, "
                f"速度: {self.speed}km/h, "
                f"方向: {self.direction}(正北为0度), "
                f"时间: {self.get_time_str()}")
