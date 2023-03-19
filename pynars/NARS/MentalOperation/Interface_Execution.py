'''
这个文件是PyNARS中的MentalOperation模块中的Interface_Execution.py文件。该文件提供了一些执行NARS语句的函数，包括believe、doubt、evaluate、wonder、hesitate和want。这些函数都是通过调用MentalOperation模块中的_execute.py文件中的函数来实现的。

包依赖关系：
    pynars.NAL.MentalOperation._execute
    pynars.NARS.DataStructures._py.Concept
    pynars.NARS.DataStructures._py.Memory
    pynars.Narsese
    pynars.NARS.MentalOperation.DataStructures

全局变量名称及其作用：
    无

各函数的依赖关系和主要功能：
    execute__believe:
        依赖：_execute.believe
        功能：执行NARS语句believe

    execute__doubt:
        依赖：_execute.doubt
        功能：执行NARS语句doubt

    execute__evaluate:
        依赖：_execute.evaluate
        功能：执行NARS语句evaluate

    execute__wonder:
        依赖：_execute.wonder
        功能：执行NARS语句wonder

    execute__hesitate:
        依赖：Concept._conceptualize, _execute.hesitate
        功能：执行NARS语句hesitate

    execute__want:
        依赖：_execute.want
        功能：执行NARS语句want
'''

from typing import Iterable, List
import pynars.NAL.MentalOperation._execute as _execute
from pynars.NARS.DataStructures._py.Concept import Concept
from pynars.NARS.DataStructures._py.Memory import Memory
from pynars.Narsese import Task, Term
from ..DataStructures import Bag   
from copy import copy, deepcopy

def execute__believe(arguments: Iterable[Term], task: Task=None, memory: Memory=None):
    ''''''
    statement, truth_term = arguments[1], arguments[2]
    return _execute.believe(statement, truth_term)


def execute__doubt(arguments: Iterable[Term], task: Task=None, memory: Memory=None):
    ''''''
    term = arguments[1]
    concept = Concept._conceptualize(memory.concepts, term, task.budget)
    return _execute.doubt(list(concept.belief_table))


def execute__evaluate(arguments: Iterable[Term], task: Task=None, memory: Memory=None):
    ''''''
    statement = arguments[1]
    return _execute.evaluate(statement)


def execute__wonder(arguments: Iterable[Term], task: Task=None, memory: Memory=None):
    ''''''
    statement = arguments[1]
    return _execute.wonder(statement)


def execute__hesitate(arguments: Iterable[Term], task: Task=None, memory: Memory=None):
    ''''''
    term = arguments[1]
    concept = Concept._conceptualize(memory.concepts, term, task.budget)
    return _execute.hesitate(list(concept.desire_table))
    

def execute__want(arguments: Iterable[Term], task: Task=None, memory: Memory=None):
    ''''''
    statement = arguments[1]
    return _execute.want(statement)
    

