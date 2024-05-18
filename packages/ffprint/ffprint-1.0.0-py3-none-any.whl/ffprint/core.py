# -*- coding: utf-8 -*-
# 🙋😊😊😊😄👻🛫🚆🚗
"""
File : init.py
Description :
Author : eric.gao
Mood: 😊😊😊
Date : 2024/5/16 18:05
"""

import os
import sys
from loguru import logger

logger.remove()
logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS} -</green> <blue>{message}</blue>")


def nb_print(*args, sep=' ', end='\n', file=None):
    """
    :param x:
    :return:
    """
    line = sys._getframe().f_back.f_lineno
    file_name = sys._getframe(1).f_code.co_filename
    file_name = os.path.basename(file_name)
    args = (str(arg) for arg in args)
    logger.info(f'"{file_name}:{line}" |  \033[0;94m{"".join(args)}\033[0m')


print = nb_print
