#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/8 17:57
# Author:zhouxiaochuan
# Description:

class DataFunction:
    @staticmethod
    def data_de_escape(data: bytes):
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
