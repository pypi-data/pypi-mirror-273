# 🙋😊😊😊😄👻🛫🚆🚗
"""
File : init.py
Description :
Author : eric.gao
Mood: 😊😊😊
Date : 2024/5/16 18:05
"""

import os, sys, time, builtins
from loguru import logger
logger.remove()
logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS} -</green> <blue>{message}</blue>")
def nb_print(*args, sep=' ', end='\n', file=None):
    """
    超流弊的print补丁
    :param x:
    :return:
    """
    # 获取被调用函数在被调用时所处代码行数
    line = sys._getframe().f_back.f_lineno
    # 获取被调用函数所在模块文件名
    file_name = sys._getframe(1).f_code.co_filename
    file_name = os.path.basename(file_name)
    args = (str(arg) for arg in args)  # REMIND 防止是数字不能被join
    logger.info(f'"{file_name}:{line}"  \033[0;94m{"".join(args)}\033[0m\n')
print = nb_print
