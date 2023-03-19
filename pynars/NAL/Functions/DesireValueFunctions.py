'''
包依赖关系：
   typing.Callable
   pyNars.Narsese.Truth
   .ExtendedBooleanFunctions
   .UncertaintyMappingFunctions.w_to_c

全局变量名称及其作用：
    DesireFuncion: 一个函数类型，用于表示欲望函数
    Desire_strong: 一个欲望函数，表示两个欲望的强合取
    Desire_weak: 一个欲望函数，表示两个欲望的弱合取
    Desire_deduction: 一个欲望函数，表示两个欲望的蕴含
    Desire_induction: 一个欲望函数，表示两个欲望的归纳

各函数的依赖关系和主要功能：
    Desire_strong:
        依赖：And函数
        功能：计算两个欲望的强合取
    Desire_weak:
        依赖：And函数，w_to_c函数
        功能：计算两个欲望的弱合取
    Desire_deduction:
        依赖：And函数
        功能：计算两个欲望的蕴含
    Desire_induction:
        依赖：And函数，w_to_c函数
        功能：计算两个欲望的归纳
'''

from typing import Callable
from pynars.Narsese import Truth
from .ExtendedBooleanFunctions import *
from .UncertaintyMappingFunctions import w_to_c

DesireFuncion = Callable[[Truth, Truth], Truth]


Desire_strong: DesireFuncion = lambda desire1, desire2: Truth(And(desire1.f, desire2.f), And(desire1.c, desire2.c, desire2.f), desire1.k)

Desire_weak: DesireFuncion = lambda desire1, desire2: Truth(And(desire1.f, desire2.f), And(desire1.c, desire2.c, desire2.f, w_to_c(1.0, desire1.k)), desire1.k)

Desire_deduction: DesireFuncion = lambda desire1, desire2: Truth(And(desire1.f, desire2.f), And(desire1.c, desire2.c), desire1.k)

Desire_induction: DesireFuncion = lambda desire1, desire2: Truth(desire1.f, w_to_c(And(desire2.f, desire1.c, desire2.c), desire1.k), desire1.k)
