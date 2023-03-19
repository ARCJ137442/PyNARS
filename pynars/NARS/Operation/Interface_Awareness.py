'''
这个文件是pynars.NAL.MentalOperation._aware模块中的Interface_Awareness.py文件，它提供了一些与意识相关的函数，包括aware__believe、aware__wonder和aware__evaluate等。这些函数可以帮助系统进行推理和决策。

包依赖关系：
    pynars.NAL.MentalOperation._aware
    pynars.NARS.DataStructures._py.Concept
    pynars.NARS.DataStructures._py.Memory
    pynars.Narsese
    pynars.NARS.Operation
    copy
    deepcopy

全局变量名称及其作用：
    无

各函数的依赖关系和主要功能：
    aware__believe:
        依赖：pynars.NAL.MentalOperation._aware
        功能：根据任务的句子和真值，返回一个信念
    aware__wonder:
        依赖：pynars.NAL.MentalOperation._aware
        功能：根据任务的句子，返回一个疑问
    aware__evaluate:
        依赖：pynars.NAL.MentalOperation._aware
        功能：根据任务的句子，返回一个评价
'''

from typing import List
import pynars.NAL.MentalOperation._aware as aware
from pynars.NARS.DataStructures._py.Concept import Concept
from pynars.NARS.DataStructures._py.Memory import Memory
from pynars.Narsese import Task, Term
from ..DataStructures import Bag   
from copy import copy, deepcopy

def aware__believe(task: Task, memory: Memory=None):
    ''''''
    return aware.believe(task.sentence, task.truth, task.budget)

def aware__wonder(task: Task, memory: Memory=None):
    ''''''
    return aware.wonder(task.sentence, task.budget)

# def _aware__doubt(arguments: List[Term], task: Task=None, memory: Memory=None):
#     ''''''
#     term = arguments[1]
#     concept = Concept._conceptualize(memory.concepts, term, task.budget)
#     return execute.doubt(list(concept.belief_table))


def aware__evaluate(task: Task, memory: Memory=None):
    ''''''
    return aware.evaluate(task.sentence, task.budget)


# def _aware__hesitate(arguments: List[Term], task: Task=None, memory: Memory=None):
#     ''''''
#     term = arguments[1]
#     concept = Concept._conceptualize(memory.concepts, term, task.budget)
#     return execute.hesitate(list(concept.desire_table))
    

# def _aware__want(arguments: List[Term], task: Task=None, memory: Memory=None):
#     ''''''
#     statement = arguments[1]
#     return execute.want(statement)
    