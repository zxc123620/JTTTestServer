#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2026/9/6 21:33
# Author:zhouxiaochuan
# Description:
import logging
import os
import socketserver
from threading import Thread

from jtttestserver.data_quene_manager import DataQueueManager
from jtttestserver.function_tools import FunctionTools
from jtttestserver.jt_type import QueueType


class JtTcpServerHandler(socketserver.BaseRequestHandler):
    """
    用于我们的服务器的请求处理器。
    """

    def extract_message(self, buffer: bytearray):
        """
        从缓冲区中提取消息
        Args:
            buffer: 数据缓冲区

        Returns:

        """
        sign_start = buffer.find(0x7e)
        # 找起始位
        if sign_start == -1:
            logging.debug(f"客户端地址: {self.client_address} 没找到标志位(头) ")
            # 没找到标志位(头),返回None
            buffer.clear() # 清空缓冲区
            return None
        # 找结束位
        sign_end = buffer.find(0x7e, sign_start + 1)
        if sign_end == -1:
            # 没找到标志位(尾),返回None
            logging.debug(f"客户端地址: {self.client_address} 没找到标志位(尾)")
            return None
        logging.info(f"客户端地址: {self.client_address} 起始标志位: {sign_start} 结束标志位: {sign_end}")
        # 判断 起始位是不是结束位
        if sign_end == sign_start + 1:
            # 拿到了结束和开始的标志位
            del buffer[:sign_end] # 把前面的数据都删掉
            # 继续提取消息
            return self.extract_message(buffer)

        # 转换为字节数组 ,并去掉头尾标志位
        message = bytes(buffer[sign_start + 1:sign_end])
        del buffer[:sign_end+1] # 已经提取到数据了，把前面的数据都删掉
        if not message:
            logging.debug(f"客户端地址: {self.client_address} 起始标志位: {sign_start} 结束标志位: {sign_end} 中间消息为空,丢掉数据 ")
            # 消息为空,返回None
            return None
        # 转义解码
        message = FunctionTools.de_escape(message)
        # 校验数据是否有效
        if not FunctionTools.check_valid(message):
            # 校验失败,返回None
            logging.info(f"客户端地址: {self.client_address} 校验失败,丢掉数据 ")
            return None
        return message

    def handle(self):
        client_address = self.client_address
        logging.info(f"客户端地址: {client_address} 连接服务器")
        data_recv_queue = DataQueueManager.get_queue(f"{client_address[0]}_{client_address[1]}",  QueueType.RECV)
        buffer = bytearray()
        try:
            while True:
                # 寻找标志位(头)
                chunk = self.request.recv(1024)
                if not chunk:
                    logging.info(f"关闭 客户端地址: {client_address} 连接")
                    break
                buffer.extend(chunk)
                # 提取消息
                while len(buffer) < 2:
                    message = self.extract_message(buffer)
                    if message is None:
                        break
                    if not message:
                        continue
                    data_recv_queue.put(message)
        except Exception as e:
            logging.error(f"客户端 {client_address} 处理异常: {e}")
        finally:
            logging.info(f"客户端地址: {client_address} 连接结束")


class JtTcpServerThread(Thread):

    def __init__(self):
        Thread.__init__(self, name="JtTcpServer",daemon=True)


    def run(self):
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 37799))
        with socketserver.TCPServer((host, port), JtTcpServerHandler) as server:
            server.serve_forever()
