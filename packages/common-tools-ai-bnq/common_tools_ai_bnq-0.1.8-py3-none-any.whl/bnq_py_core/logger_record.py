#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/3/27 17:36
# Author:Zhang HongTao
# @File:logger_record.py

import logging
import logging.config
import logging.handlers
import os
import pathlib
import sys
import time

from structlog import configure, processors, stdlib
from termcolor import colored


class _LoggingF(object):
    """
    日志记录父类
    """

    def __init__(self, log_dir=None, max_bytes=20 * 1024 * 1024, backup_count=10, log_level=logging.INFO):
        self.record_info = None
        self.logger = None
        self.log_record_path = log_dir  # 日志记录路径
        self.max_bytes = max_bytes  # 日志文件大小
        self.backup_count = backup_count  # 日志文件备份数量
        self.level = log_level  # 日志级别
        self.level_third = logging.WARNING  # 第三方库日志级别

    def get_logging_config(self, log_filename):
        """获取logging配置

        :param log_filename:
        :return:
        """
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
                },
                "console": {
                    "format": colored(f'[%(asctime)s][%(levelname)1.1s][%(process)d][%(name)s]', 'green') + colored(
                        f'(%(filename)s %(lineno)d)', 'yellow') + ': %(message)s'
                }
            },
            "handlers": {
                "console_handler": {
                    "class": "logging.StreamHandler",
                    "level": self.level,
                    "formatter": "console",
                    "stream": sys.stdout
                },
                "file_handler": {
                    "level": self.level,
                    "formatter": "default",
                    "class": "concurrent_log_handler.ConcurrentTimedRotatingFileHandler",
                    "filename": log_filename,
                    "when": "midnight",
                    "maxBytes": self.max_bytes,
                    "backupCount": self.backup_count,
                    "encoding": "UTF-8"
                },
            },
            "loggers": {
                "": {
                    "handlers": ["console_handler"],
                    "level": self.level_third
                }
            },
            "root": {
                "level": self.level,
                "handlers": ["file_handler", "console_handler"]
            }
        }


class LoggingRecord(_LoggingF):
    """日志记录类，用于记录运行中的信息

    """
    __instance = None  # 单例
    __filename = None  # 日志文件名

    def __new__(cls, log_dir=None, *args, **kwargs):
        """保证日志模块是单例模式"""
        if not cls.__instance:
            cls.__instance = super(LoggingRecord, cls).__new__(cls)
        __now_time = int(round(time.time()))
        __time_record = time.strftime("%Y%m%d", time.localtime(__now_time))
        cls.__filename = __time_record + "_BNQ_AI.log"
        return cls.__instance

    def __init__(self, max_bytes=20 * 1024 * 1024, backup_count=10, log_level=logging.INFO, log_dir=None):
        super().__init__(log_dir, max_bytes, backup_count, log_level)
        self.init_log()

    def init_log(self):
        """初始化log模块

        Returns:

        """
        if self.log_record_path is None:
            # 获取根目录路径，并创建日志文件夹
            # self.log_record_path = os.path.join(os.getcwd(), "logs")
            self.log_record_path = "/bnq/logs"

        pathlib.Path(self.log_record_path).mkdir(parents=True, exist_ok=True)
        log_filename = os.path.join(self.log_record_path, self.__filename)
        logging.config.dictConfig(self.get_logging_config(log_filename))
        configure(
            context_class=dict,
            logger_factory=stdlib.LoggerFactory(),
            wrapper_class=stdlib.BoundLogger,
            processors=[
                stdlib.filter_by_level,
                stdlib.PositionalArgumentsFormatter(),
                processors.StackInfoRenderer(),
                processors.format_exc_info,
                processors.UnicodeDecoder(),
                stdlib.render_to_log_kwargs
            ]
        )
        self.logger = logging.getLogger("BNQ-AI")
        self.logger.level = self.level

    def debug(self, record_info):
        """debug级别的日志记录

        :param record_info:
        :return:
        """
        self.logger.debug(record_info)

    def info(self, record_info):
        """

        Args:
            record_info:

        Returns:

        """
        self.logger.info(record_info)

    def error(self, error_info, exc_info_=True):
        """

        Args:
            error_info:
            exc_info_:

        Returns:

        """
        self.logger.error(error_info, exc_info=exc_info_)

    def warning(self, warning_info):
        """

        Args:
            warning_info:

        Returns:

        """
        self.logger.warning(warning_info)

    def exception(self, exception_info):
        self.logger.exception(exception_info)


class LoggingRecordTimeRotation(_LoggingF):
    """日志记录类，用于记录运行中的信息, 日志文件按时间切割

    """
    __instance = None  # 单例

    def __new__(cls, log_dir=None, *args, **kwargs):
        """保证日志模块是单例模式"""
        if not cls.__instance:
            cls.__instance = super(LoggingRecordTimeRotation, cls).__new__(cls)
        return cls.__instance

    def __init__(self, max_bytes=20 * 1024 * 1024, backup_count=10, log_level=logging.INFO, log_dir=None):
        super().__init__(log_dir, max_bytes, backup_count, log_level)
        self.init_log()

    def init_log(self):
        """初始化log模块

        Returns:

        """
        if self.log_record_path is None:
            # 获取根目录路径，并创建日志文件夹
            self.log_record_path = "/bnq/logs"

        pathlib.Path(self.log_record_path).mkdir(parents=True, exist_ok=True)
        log_filename = os.path.join(self.log_record_path, "access.log")
        logging.config.dictConfig(self.get_logging_config(log_filename))
        self.logger = logging.getLogger("BNQ-AI")
        self.logger.level = self.level

    def debug(self, record_info):
        """debug级别的日志记录

        :param record_info:
        :return:
        """
        self.logger.debug(record_info)

    def info(self, record_info):
        """

        Args:
            record_info:

        Returns:

        """
        self.logger.info(record_info)

    def error(self, error_info, exc_info_=True):
        """

        Args:
            error_info:
            exc_info_:

        Returns:

        """
        self.logger.error(error_info, exc_info=exc_info_)

    def warning(self, warning_info):
        """

        Args:
            warning_info:

        Returns:

        """
        self.logger.warning(warning_info)

    def exception(self, exception_info):
        self.logger.exception(exception_info)


if __name__ == "__main__":

    for i in range(10):
        testLog = LoggingRecordTimeRotation(log_level=logging.DEBUG)
        print(testLog, "testLog")
        testLog.debug(i)
        testLog.info("中文测试")
        testLog.error(i)
        testLog.warning(i)
        testLog.exception(i)
