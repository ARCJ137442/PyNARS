'''
这个文件是PyNARS中的一个模块，它实现了NAL9规则的添加。NAL9是一种基于NARS的推理引擎，它使用了一些特殊的规则来处理任务和概念。这个模块中的函数用于向NAL9中添加规则。

包依赖关系：
    collections.OrderedDict
    pynars.NARS.DataStructures.LinkType
    pynars.NARS.DataStructures.TaskLink
    pynars.NARS.DataStructures.TermLink
    sparse_lut.SparseLUT
    pynars.Global
    ....RuleMap.add_rule
    pynars.NARS.Operation

全局变量名称及其作用：
    无

各函数的依赖关系和主要功能：
    add_rules__NAL9:
        依赖：Believe, Doubt, Evaluate, Hesitate, Want, Wonder
        功能：向NAL9中添加规则
'''

from collections import OrderedDict
from pynars.NARS.DataStructures import LinkType, TaskLink, TermLink
from sparse_lut import SparseLUT
from pynars import Global
from ....RuleMap.add_rule import *
from pynars.NARS.Operation import *

def add_rules__NAL9(sparse_lut: SparseLUT=None, structure: OrderedDict=None):
    ''''''
    register(Believe,    execute__believe)
    register(Doubt,      execute__doubt)
    register(Evaluate,   execute__evaluate)
    register(Hesitate,   execute__hesitate)
    register(Want,       execute__want)
    register(Wonder,     execute__wonder)
    # register(Anticipate, execute__anticipate)
