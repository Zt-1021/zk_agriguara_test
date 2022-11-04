#!/usr/bin/python3.8
# -*- coding:utf-8 -*-
# @DateTime　　: 2020/10/27 15:11
# @Author　: wanghr

import logging
import time
import os

"""
在工程中多个地方要实例化该TestLog类的时，注意使用不同的名字，及log=TestLog(logger='不同值')，否则会出错
"""
project_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class TestLog(object):
    """
    封装后的logging
    """

    def __init__(self, logger=None):
        """
        :param logger:
            指定保存日志的文件路径，日志级别，以及调用文件
        """

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)  # 日志级别 DEBUG 10 < INFO 20 < WARNING 30 < ERROR 40 < CRITICAL 50

        # 创建一个handler，用于写入日志文件
        self.log_time = time.strftime("%Y_%m_%d")
        self.log_path = os.path.join(project_path, 'log', (self.log_time + '.log'))

        # fh = logging.FileHandler(self.log_name, 'a')  # 追加模式  这个是python2的
        fh = logging.FileHandler(self.log_path, 'a', encoding='utf-8')  # 这个是python3的
        fh.setLevel(logging.INFO)

        # 再创建一个handler，用于输出到控制台
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.INFO)

        # 定义handler的输出格式,console和file不同的ri
        # formatter_console = logging.Formatter('%(message)s')
        formatter_file = logging.Formatter(
            '[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s]%(message)s')
        fh.setFormatter(formatter_file)
        # ch.setFormatter(formatter_console)

        # 给logger添加handler
        self.logger.addHandler(fh)
        # self.logger.addHandler(ch)

        #  添加下面一句，在记录日志之后移除句柄
        # self.logger.removeHandler(ch)
        # self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()
        # ch.close()

    def get_log(self):
        return self.logger


if __name__ == '__main__':
    log = TestLog().get_log()
    log.info("info message")
    log.debug("debug message")
    log.error("error message")
    log.critical("critical message")