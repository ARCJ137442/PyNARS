'''
这个文件是PyNARS中的Interface_Awareness.py，它提供了一些与意识有关的函数。这些函数可以帮助NARS系统更好地理解和处理输入的任务。

包依赖关系：
    typing.List
    pynars.NAL.MentalOperation._aware
    pynars.NARS.DataStructures._py.Concept
    pynars.NARS.DataStructures._py.Memory
    pynars.Narsese.Task
    pynars.Narsese.Term
    pynars.NARS.DataStructures.Bag
    copy.deepcopy

全局变量名称及其作用：
    无

各函数的依赖关系和主要功能：
    aware__believe:
        依赖：pynars.NAL.MentalOperation._aware.believe
        功能：将任务的句子和真值传递给pynars.NAL.MentalOperation._aware.believe函数，并返回结果。

    aware__wonder:
        依赖：pynars.NAL.MentalOperation._aware.wonder
        功能：将任务的句子传递给pynars.NAL.MentalOperation._aware.wonder函数，并返回结果。

    aware__evaluate:
        依赖：pynars.NAL.MentalOperation._aware.evaluate
        功能：将任务的句子传递给pynars.NAL.MentalOperation._aware.evaluate函数，并返回结果。
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
    