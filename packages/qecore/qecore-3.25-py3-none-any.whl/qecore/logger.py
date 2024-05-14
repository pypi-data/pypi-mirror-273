#!/usr/bin/env python3
"""
This file provides loggers.
"""

import sys
import logging
from subprocess import call, STDOUT

# Singleton solution provided by https://stackoverflow.com/a/54209647


class Singleton(type):
    """
    Singleton class used as metaclass by :py:class:`logger.Logging`.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logging(metaclass=Singleton):
    """
    Logging class.
    """

    logger = None

    def __init__(self) -> None:
        """
        Initiating logger class with some basic logging setup.
        """

        if not self.logger:
            call("sudo rm -rf /tmp/qecore_logger.log", shell=True, stderr=STDOUT)

        self.logger = logging.getLogger("general")
        self.logger.setLevel(logging.DEBUG)
        # Disable default handler.
        self.logger.propagate = False

        formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s: [%(filename)s:%(lineno)d] %(func_name)s: %(message)s"  # noqa: E501
        )

        # Setup of file handler.
        # All DEBUG and higher level logs will be going to the file.
        file_handler = logging.FileHandler("/tmp/qecore_logger.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        file_handler.set_name("file_handler")

        # Setup of console handler.
        # All INFO and higher level logs will be going to the console.
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        console_handler.set_name("console_handler")

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.logger.addFilter(FuncFilter())

    def qecore_debug_to_console(self) -> None:
        """
        Set file handler level to DEBUG to get the output to console.
        """

        for handler in self.logger.handlers:
            if handler.get_name() == "console_handler":
                handler.setLevel(logging.DEBUG)
                break


class FuncFilter(logging.Filter):
    def filter(self, record):
        # Have to walk the frame a bit back.
        # 1. filter, 2. handle, 3. _log, 4. debug, 5. Original calling function.
        record.func_name = str(
            sys._getframe().f_back.f_back.f_back.f_back.f_back.f_code.co_name
        )
        return True
