'''
这个文件包含了一些工具函数，用于辅助PyNARS的其他部分。这些函数包括：

包依赖关系：
    无

全局变量名称及其作用：
    getsizeof: 一个函数，用于获取对象的大小。
    list_contains: 一个函数，用于判断一个列表是否包含另一个列表。
    rand_seed: 一个函数，用于设置随机数生成器的种子。

各函数的依赖关系和主要功能：
    get_size:
        依赖：无
        功能：递归地计算对象的大小。
    list_contains:
        依赖：无
        功能：判断一个列表是否包含另一个列表。
    rand_seed:
        依赖：random, numpy
        功能：设置随机数生成器的种子。
    find_var_with_pos:
        依赖：无
        功能：找到具有相同位置头的变量。
    find_pos_with_pos:
        依赖：无
        功能：找到具有相同位置头的位置。
'''

import sys
from typing import Callable, List

try:
    sys.getsizeof(0)
    getsizeof = lambda x: sys.getsizeof(x)
except:
    # import resource
    getsizeof = lambda _: 1#resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = getsizeof(obj)
    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return 0

    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)

    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])

    return size


def list_contains(base_list, obj_list):
    ''''''
    if len(base_list) < len(obj_list): return False

    obj0 = obj_list[0]
    for i, base in enumerate(base_list[:len(base_list)+1 - len(obj_list)]):
        if base == obj0:
            if base_list[i: i+len(obj_list)] == obj_list:
                return True
    return False


def rand_seed(x: int):
    import random
    random.seed(x)
    
    import numpy as np
    np.random.seed(x)

    # if using pytorch, set its seed!
    # # import torch
    # # torch.manual_seed(x)
    # # torch.cuda.manual_seed(x)
    # # torch.cuda.manual_seed_all(x)


find_var_with_pos: Callable[[list, list, List[list]], list] = lambda pos_search, variables, positions: [var for var, pos in zip(variables, positions) if pos[:len(pos_search)] == pos_search] # find those variables with a common head of position. e.g. pos_search=[0], variables=[1, 1, 2, 2], and positions=[[0, 2, 0, 0], [0, 2, 1, 0], [0, 3, 0], [1, 0]], then return [1, 1, 2]
find_pos_with_pos: Callable[[list, List[list]], list] = lambda pos_search, positions: [pos for pos in positions if pos[:len(pos_search)] == pos_search]