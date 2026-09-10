#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time: 2026/9/10 11:10
# Author:zhouxiaochuan
# Description: 队列管理类
import queue

from jtttestserver.jt_type import QueueType


class DataQueueManager:
    queue_map: dict[str, dict[str, queue.Queue]] = {}

    @classmethod
    def get_queue(cls, que_id: str, que_type: QueueType):
        """
        获取队列

        Args:
            que_id: 队列ID
            que_type: 队列类型

        Returns:
            队列对象

        """
        if que_id not in cls.queue_map or (que_type.value not in cls.queue_map[que_id]):
            # 如果队列ID不存在，或队列类型不存在，创建一个新的队列 并添加到队列映射中
            cls.queue_map[que_id][que_type.value] = queue.Queue()
        return cls.queue_map[que_id][que_type.value]
