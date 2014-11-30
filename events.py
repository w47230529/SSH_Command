#*--coding: utf-8 *#

import threading
import paramiko
import time
import Queue

class Events:
    """队列处理:
    将一个长队列按每５个一组，生成一个大列表
    """
    def __init__(self, queue, length):
        self.queue = queue
        self.length = length
        self.queue_list = []

    def handle_list(self):
        if len(self.queue) < self.length:
            self.queue_list.append(self.queue)
            return self.queue_list
        else:
            start = 0
            end = self.length
            while True:
                if end <= len(self.queue):
                    self.queue_list.append(self.queue[start:end])
                    start = end
                    end = end + self.length
                else:
                    self.queue_list.append(self.queue[start:])
                    break
            return self.queue_list