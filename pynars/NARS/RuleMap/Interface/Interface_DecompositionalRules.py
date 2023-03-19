'''
这个文件是Interface_DecompositionalRules.py，它包含了一些用于分解规则的接口函数。这些函数都是以_decompositional__开头的，它们的主要功能是将一个复杂的任务分解成更小的子任务，以便更好地处理。这些函数都是内部函数，不应该被直接调用。

包依赖关系：
    pynars.NARS.DataStructures
    pynars.Narsese
    pynars.NAL.Inference
    pynars.NAL.Theorems
    pynars.Global

全局变量名称及其作用：
    无

各函数的依赖关系和主要功能：
    _decompositional__decomposition_theorem2__0_0:
        依赖：decompositional__decomposition_theorem2
        功能：将一个复杂的任务分解成更小的子任务，以便更好地处理。
    _decompositional__decomposition_theorem2__0_0_prime:
        依赖：decompositional__decomposition_theorem2
        功能：将一个复杂的任务分解成更小的子任务，以便更好地处理。
    _decompositional__decomposition_theorem3__0_0:
        依赖：decompositional__decomposition_theorem3
        功能：将一个复杂的任务分解成更小的子任务，以便更好地处理。
    _decompositional__decomposition_theorem3__0_0_prime:
        依赖：decompositional__decomposition_theorem3
        功能：将一个复杂的任务分解成更小的子任务，以便更好地处理。
    _decompositional__decomposition_theorem9:
        依赖：decompositional__decomposition_theorem9
        功能：将一个复杂的任务分解成更小的子任务，以便更好地处理。
    _decompositional__decomposition_theorem9_prime:
        依赖：decompositional__decomposition_theorem9
        功能：将一个复杂的任务分解成更小的子任务，以便更好地处理，同时反转前提。
    _decompositional__decomposition_theorem10:
        依赖：decompositional__decomposition_theorem10
        功能：将一个复杂的任务分解成更小的子任务，以便更好地处理。
    _decompositional__decomposition_theorem10_prime:
        依赖：decompositional__decomposition_theorem10
        功能：将一个复杂的任务分解成更小的子任务，以便更好地处理，同时反转前提。
'''

from pynars.NARS.DataStructures import Link, TaskLink, TermLink, LinkType, Task
from pynars.Narsese import Belief
from pynars.NAL.Inference import *
from pynars.NAL.Theorems import *
from pynars import Global

def _decompositional__decomposition_theorem2__0_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return decompositional__decomposition_theorem2(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)

def _decompositional__decomposition_theorem2__0_0_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return decompositional__decomposition_theorem2(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)

def _decompositional__decomposition_theorem3__0_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return decompositional__decomposition_theorem3(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)

def _decompositional__decomposition_theorem3__0_0_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return decompositional__decomposition_theorem3(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)

# def _decompositional__decomposition_theorem4__0_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
#     return decomposition_theorem4(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)

# def _decompositional__decomposition_theorem4__0_0_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
#     return decomposition_theorem4(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)


def _decompositional__decomposition_theorem9(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return decompositional__decomposition_theorem9(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)

def _decompositional__decomposition_theorem9_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return decompositional__decomposition_theorem9(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)


def _decompositional__decomposition_theorem10(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return decompositional__decomposition_theorem10(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)

def _decompositional__decomposition_theorem10_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return decompositional__decomposition_theorem10(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)
