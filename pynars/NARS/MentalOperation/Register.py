'''
这个文件是PyNARS中的一个模块，用于实现NARS系统中的心理操作的注册。该模块提供了一个register函数，用于将心理操作和对应的函数进行注册。

包依赖关系：
    无

全局变量名称及其作用：
    registered_operations: 一个字典，用于存储心理操作和对应的函数。

各函数的依赖关系和主要功能：
    register:
        依赖：无
        功能：将心理操作和对应的函数进行注册。
'''

from typing import Callable, Dict
from pynars.Narsese._py.Operation import *

registered_operations: Dict[Operation, Callable] = {}

def register(operation: Operation, callable: Callable):
    ''''''
    global registered_operations
    registered_operations[operation] = callable