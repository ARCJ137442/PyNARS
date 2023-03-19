'''
这个文件是PyNARS中的一个模块，它实现了NAL-6规则的添加。NAL-6规则是一种基于NARS的推理规则，它可以用于处理复杂的推理任务。本模块提供了一个函数add_rules__NAL6，它可以将NAL-6规则添加到给定的数据结构中。

包依赖关系：
    collections.OrderedDict
    pynars.NARS.DataStructures.LinkType
    pynars.NARS.DataStructures.TaskLink
    pynars.NARS.DataStructures.TermLink
    sparse_lut.SparseLUT
    pynars.Global
    ....RuleMap.add_rule

全局变量名称及其作用：
    无

各函数的依赖关系和主要功能：
    add_rules__NAL6:
        依赖：无
        功能：将NAL-6规则添加到给定的数据结构中
'''

from collections import OrderedDict
from pynars.NARS.DataStructures import LinkType, TaskLink, TermLink
from sparse_lut import SparseLUT
from pynars import Global
from ....RuleMap.add_rule import *


def add_rules__NAL6(sparse_lut: SparseLUT, structure: OrderedDict):
        ''''''

