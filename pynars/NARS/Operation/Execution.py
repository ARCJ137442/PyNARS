'''
这个文件是PyNARS中的一个模块，它实现了执行任务的功能。该模块提供了两个函数：executed_task和execute。其中，executed_task函数用于执行任务，而execute函数用于执行任务并将结果添加到概念中。

包依赖关系：
    pynars.Config
    pynars.NARS.DataStructures._py.Concept
    pynars.NARS.DataStructures._py.Memory
    pynars.Narsese._py.Budget
    pynars.Narsese._py.Operation
    pynars.Narsese._py.Sentence
    pynars.Narsese._py.Statement
    pynars.Narsese._py.Task
    pynars.Narsese._py.Truth
    pynars.NAL.Functions.Tools
    pynars.Narsese
    pynars.Global
    .Register

全局变量名称及其作用：
    Global.time: 当前时间
    Config.c_judgement: 判断的置信度
    Config.k: 时间常数
    Config.p_feedback: 反馈概率
    Config.d_feedback: 反馈延迟

各函数的依赖关系和主要功能：
    executed_task:
        依赖：Global.get_input_id, Truth, Stamp, Budget, Task
        功能：执行任务并返回一个Judgement任务
    execute:
        依赖：memory.take_by_key, registered_operations
        功能：执行任务并将结果添加到概念中
'''

from typing import Callable, List
from pynars.Config import Config
from pynars.NARS.DataStructures._py.Concept import Concept
from pynars.NARS.DataStructures._py.Memory import Memory
from pynars.Narsese._py.Budget import Budget
from pynars.Narsese._py.Operation import *
from pynars.Narsese._py.Sentence import Goal, Judgement, Quest, Question, Sentence, Stamp
from pynars.Narsese._py.Statement import Statement
from pynars.Narsese._py.Task import Belief, Desire, Task
from pynars.Narsese._py.Truth import Truth
from .Register import registered_operations
from pynars.Narsese import Term
from pynars.NAL.Functions.Tools import truth_from_term, truth_to_quality
from pynars.Narsese import Base
from pynars import Global

def executed_task(task: Task):
    '''
    '''
    input_id = Global.get_input_id()
    truth = Truth(1.0, Config.c_judgement, Config.k)
    stamp = Stamp(Global.time, Global.time, None, Base((input_id,)))
    budget = Budget(Config.p_feedback, Config.d_feedback, truth_to_quality(task.truth))
    
    return Task(Judgement(task.term, stamp, truth), budget, input_id)



def execute(task: Task, concept: Concept, memory: Memory):
    '''
    it should be ensured that the task is executable, i.e., `task.is_executable == True`.
    '''
    if task.term != concept.term:
        concept = memory.take_by_key(task.term, remove=False)
    stat: Statement = task.term
    operation: Operation = stat.predicate
    args = stat.subject.terms
    function_op: Callable = registered_operations.get(operation, None)

    if function_op is not None: 
        belief = executed_task(task)
        if concept is not None: 
            concept.add_belief(belief)
        return function_op(args, task, memory), belief
    else: 
        return None, None