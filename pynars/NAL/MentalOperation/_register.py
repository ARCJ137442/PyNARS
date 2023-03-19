'''
这个文件是PyNARS中的一个模块，用于注册NARS系统中的各种操作。本文件中定义了一个register函数，用于将操作和对应的函数进行绑定，以便在NARS系统中使用。

- 导入模块路径列表：
    - typing.Callable
    - typing.Dict
    - pynars.Narsese._py.Operation

- 全局变量名称及其作用：
    - registered_operations: 一个字典，用于存储已注册的操作及其对应的函数。

- 各函数的依赖关系和主要功能：
    - register: 将操作和对应的函数进行绑定，以便在NARS系统中使用。
'''

from typing import Callable, Dict
from pynars.Narsese._py.Operation import *

registered_operations: Dict[Operation, Callable] = {}

def register(operation: Operation, callable: Callable):
    ''''''
    global registered_operations
    registered_operations[operation] = callable