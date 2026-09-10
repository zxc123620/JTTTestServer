#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/10 09:14
# Author:zhouxiaochuan
# Description: 客户端认证消息体
from dataclasses import dataclass

from jtttestserver.jt_client_parser.client_obj.basic_client_body import Jt808ClientBasicBody


@dataclass
class Jt808ClientAuthBody(Jt808ClientBasicBody):
    auth_len: int # 鉴权码长度
    auth_code_content: bytes # 鉴权码
    client_imei: bytes # 客户端IMEI
    soft_version: bytes # 软件版本

    def get_auth_body_str(self):
        """
        获取认证消息体字符串
        Returns:
        """
        return self.auth_code_content.decode("gbk", "ignore")

    def get_imei_str(self):
        """
        获取客户端IMEI字符串
        Returns:

        """
        return self.client_imei.decode("ascii", "ignore")

    def get_soft_version_str(self):
        """
        获取软件版本字符串
        Returns:

        """
        return self.soft_version.decode("ascii", "ignore")

    def __str__(self) -> str:
        return (f"认证权码长度: {self.auth_len},"
                f"认证权码: {self.get_auth_body_str()},"
                f"客户端IMEI: {self.get_imei_str()},"
                f"软件版本: {self.get_soft_version_str()}")
