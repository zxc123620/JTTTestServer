#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/8 17:57
# Author:zhouxiaochuan
# Description:
import logging
from asyncio import log

from geographiclib.geodesic import Geodesic

class FunctionTools:

    @staticmethod
    def de_escape(data: bytes):
        """
        数据转义解码, 把0x7d 0x01 替换为 0x7d。把0x7d 0x02 替换为 0x7e
        Args:
            data: 数据 bytes

        Returns:
            转义后的数据 bytes
        """
        data_new = bytearray(data)
        for i in range(0, len(data_new), 2):
            if data_new[i] == 0x7d and data_new[i+1] == 0x01:
                data_new[i] = 0x7d
            elif data_new[i] == 0x7d and data_new[i+1] == 0x02:
                data_new[i] = 0x7e
        return bytes(data_new)

    @staticmethod
    def escape(data: bytes):
        """
        数据转义编码, 把0x7d 替换为 0x7d 0x01。把0x7e 替换为 0x7d 0x02
        Args:
            data: 数据 bytes

        Returns:
            转义后的数据 bytes
        """
        data_new = bytearray(data)
        for i in range(len(data_new)):
            if data_new[i] == 0x7d:
                data_new[i] = 0x7d
                data_new.insert(i+1, 0x01)
            elif data_new[i] == 0x7e:
                data_new[i] = 0x7d
                data_new.insert(i+1, 0x02)
        return bytes(data_new)

    @staticmethod
    def generate_check_byte(data: bytes):
        """
        生成校验位
        Args:
            data: 头+体bytes

        Returns:
            校验位
        """
        check_byte = 0
        for i in data:
            check_byte ^= i
        return check_byte

    @classmethod
    def check_valid(cls, raw_data: bytes):
        """
        校验数据是否有效
        Args:
            raw_data: 数据 bytes

        Returns:

        """
        raw_check_byte = raw_data[-1] # 校验位
        raw_check_data_body = raw_data[:-1] # 校验数据体
        check_byte = cls.generate_check_byte(raw_check_data_body)
        result = check_byte == raw_check_byte
        logging.info(f"校验结果: {check_byte}(平台计算) == {raw_check_byte}(原始校验) -> {result}")
        return result

    @staticmethod
    def distance_vincenty( lat1, lon1, lat2, lon2):
        """
        计算Vincenty距离，厘米级精度
        Args:
            lat1: 纬度1 单位：十进制度
            lon1: 经度1 单位：十进制度
            lat2: 纬度2 单位：十进制度
            lon2: 经度2 单位：十进制度

        Returns:
            距离（米）

        """
        result = Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)
        return result['s12']  # 距离（米）
