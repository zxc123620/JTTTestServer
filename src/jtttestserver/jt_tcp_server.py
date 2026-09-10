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
from jtttestserver.jt_type import QueueType


class JtTcpServerHandler(socketserver.BaseRequestHandler):
    """
    用于我们的服务器的请求处理器。
    """

    def handle(self):
        client_address = self.client_address
        logging.info(f"客户端地址: {client_address} 连接服务器")
        data_recv_queue = DataQueueManager.get_queue(f"{client_address[0]}_{client_address[1]}",  QueueType.RECV)
        sign = bytes([0x7e])
        data = bytearray()
        while True:
            # 寻找标志位(头)
            temp_1 = self.request.recv(1)
            if temp_1 == sign:
                # 如果是头，需要判断是否是上一个的尾 + 下一个的头
                temp_2 = self.request.recv(1)
                if temp_2 == sign:
                    # temp_1 是头 temp_2 是也是标志位 头 表示上一个的尾 + 下一个的头
                    data = bytearray()
                    data.extend(temp_2)
                else:
                    # temp_1 是头 temp_2 不是标志位 头
                    data = bytearray()
                    data.extend(temp_1)
                    data.extend(temp_2)
            else:
                if len(data) == 0:
                    # 没有找到头,只有数据信息
                    logging.info(f"客户端地址: {client_address} 没有头,只有数据信息,丢掉数据 ")
                    continue
                while True:
                    temp = self.request.recv(1)
                    data.extend(temp)
                    if temp == sign:
                        data_recv_queue.put(data)
                        # 找到尾巴了
                        break


class JtTcpServerThread(Thread):

    def __init__(self):
        Thread.__init__(self, name="JtTcpServer",daemon=True)


    def run(self):
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 37799))
        with socketserver.TCPServer((host, port), JtTcpServerHandler) as server:
            server.serve_forever()
