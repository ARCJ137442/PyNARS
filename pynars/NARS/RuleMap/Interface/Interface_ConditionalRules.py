'''
这个文件包含了一些条件规则的推理函数，包括演绎、归纳、类比和拟类推理。这些函数可以用于NARS系统中的推理过程。

包依赖关系：
    pynars.NARS.DataStructures
    pynars.Narsese
    pynars.NAL.Inference
    pynars.NAL.Theorems
    pynars.Global

全局变量名称及其作用：
    无

各函数的依赖关系和主要功能：
    _conditional__deduction__0:
        依赖：conditional__deduction
        功能：推导出一个条件语句的结论，其中前提是一个简单语句。
    _conditional__deduction__0_prime:
        依赖：conditional__deduction
        功能：推导出一个条件语句的结论，其中前提是一个简单语句。
    _conditional__deduction_compound_eliminate__0:
        依赖：conditional__deduction_compound_eliminate
        功能：推导出一个条件语句的结论，其中前提是一个复合语句。
    _conditional__deduction_compound_eliminate__0_prime:
        依赖：conditional__deduction_compound_eliminate
        功能：推导出一个条件语句的结论，其中前提是一个复合语句。
    _conditional__deduction_compound_replace__0_1:
        依赖：conditional__deduction_compound_replace
        功能：推导出一个条件语句的结论，其中前提是一个复合语句。
    _conditional__deduction_compound_replace__1_0:
        依赖：conditional__deduction_compound_replace
        功能：推导出一个条件语句的结论，其中前提是一个复合语句。
    _conditional__abduction__1:
        依赖：conditional__abduction
        功能：从一个条件语句中推断出前提。
    _conditional__abduction__1_prime:
        依赖：conditional__abduction
        功能：从一个条件语句中推断出前提。
    _conditional__abduction_compound_eliminate__1_1:
        依赖：conditional__abduction_compound_eliminate
        功能：从一个条件语句中推断出前提，其中前提是一个复合语句。
    _conditional__abduction_compound_eliminate__1_1_prime:
        依赖：conditional__abduction_compound_eliminate
        功能：从一个条件语句中推断出前提，其中前提是一个复合语句。
    _conditional__abduction_compound_eliminate2__1_1:
        依赖：conditional__abduction_compound_eliminate2
        功能：从一个条件语句中推断出前提，其中前提是一个复合语句。
    _conditional__abduction_compound_eliminate2__1_1_prime:
        依赖：conditional__abduction_compound_eliminate2
        功能：从一个条件语句中推断出前提，其中前提是一个复合语句。
    _conditional__induction_compound_replace__0_0:
        依赖：conditional__induction_compound_replace
        功能：从一个条件语句中推断出结论，其中前提是一个复合语句。
    _conditional__induction_compound_replace__0_0_prime:
        依赖：conditional__induction_compound_replace
        功能：从一个条件语句中推断出结论，其中前提是一个复合语句。
    _conditional__analogy__0:
        依赖：conditional__analogy
        功能：从一个条件语句中推断出结论，其中前提是一个简单语句。
    _conditional__analogy__0_prime:
        依赖：conditional__analogy
        功能：从一个条件语句中推断出结论，其中前提是一个简单语句。
    _conditional__analogy__1:
        依赖：conditional__analogy
        功能：从一个条件语句中推断出结论，其中前提是一个简单语句。
    _conditional__analogy__1_prime:
        依赖：conditional__analogy
        功能：从一个条件语句中推断出结论，其中前提是一个简单语句。
'''

from pynars.NARS.DataStructures import Link, TaskLink, TermLink, LinkType, Task
from pynars.Narsese import Belief
from pynars.NAL.Inference import *
from pynars.NAL.Theorems import *
from pynars import Global

'''deduction'''
def _conditional__deduction__0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<S ==> P>. S.} |- P.'''
    return conditional__deduction(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)


def _conditional__deduction__0_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{S. <S ==> P>.} |- P.'''
    return conditional__deduction(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)


def _conditional__deduction_compound_eliminate__0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<(&&, C, S, ...) ==> P>. <C ==> P>.} |- P.'''
    return conditional__deduction_compound_eliminate(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)

def _conditional__deduction_compound_eliminate__0_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<C ==> P>. <(&&, C, S, ...) ==> P>.} |- P.'''
    return conditional__deduction_compound_eliminate(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)


def _conditional__deduction_compound_replace__0_1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<(&&, C, S, ...) ==> P>. <C ==> P>.} |- P.'''
    return conditional__deduction_compound_replace(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)

def _conditional__deduction_compound_replace__1_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<C ==> P>. <(&&, C, S, ...) ==> P>.} |- P.'''
    return conditional__deduction_compound_replace(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)


'''abduction'''
def _conditional__abduction__1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return conditional__abduction(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)


def _conditional__abduction__1_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return conditional__abduction(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)

def _conditional__abduction_compound_eliminate__1_1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<(&&, C, S, ...) ==> P>. <C ==> P>.} |- (&&, S, ...).'''
    return conditional__abduction_compound_eliminate(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)

def _conditional__abduction_compound_eliminate__1_1_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<(&&, C, S, ...) ==> P>. <C ==> P>.} |- (&&, S, ...).'''
    return conditional__abduction_compound_eliminate(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)


def _conditional__abduction_compound_eliminate2__1_1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<(&&, C, S, ...) ==> P>. <C ==> P>.} |- (&&, S, ...).'''
    return conditional__abduction_compound_eliminate2(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)

def _conditional__abduction_compound_eliminate2__1_1_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<(&&, C, S, ...) ==> P>. <C ==> P>.} |- (&&, S, ...).'''
    return conditional__abduction_compound_eliminate2(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)


'''induction'''
def _conditional__induction_compound_replace__0_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<(&&, C, M, ...) ==> P>. <M ==> S>.} |- <(&&, C, S, ...)  ==> P>.%'''
    return conditional__induction_compound_replace(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)

def _conditional__induction_compound_replace__0_0_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<M ==> S>. <(&&, C, M, ...) ==> P>.} |- <(&&, C, S, ...)  ==> P>.%'''
    return conditional__induction_compound_replace(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)


'''analogy'''
def _conditional__analogy__0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{S. <S<=>P>.} |- P.'''
    return conditional__analogy(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False, inverse_copula=False)


def _conditional__analogy__0_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<S<=>P>. S.} |- P.'''
    return conditional__analogy(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True, inverse_copula=False)

def _conditional__analogy__1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{S. <P<=>S>.} |- P.'''
    return conditional__analogy(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False, inverse_copula=True)


def _conditional__analogy__1_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<P<=>S>. S.} |- P.'''
    return conditional__analogy(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True, inverse_copula=True)

# def _syllogistic__analogy__1_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
#     return syllogistic__analogy(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False if belief.term.is_commutative else True, inverse_copula=True if belief.term.is_commutative else False)


# def _syllogistic__analogy__0_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
#     return syllogistic__analogy(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False if belief.term.is_commutative else True, inverse_copula=False)


# def _syllogistic__analogy__1_1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
#     return syllogistic__analogy(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False if belief.term.is_commutative else True, inverse_copula=True)


# '''resemblance'''
# def _syllogistic__resemblance__0_1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
#     inverse_premise = True if (task.term.is_higher_order and (not belief.term.is_higher_order)) else False
#     return syllogistic__resemblance(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=inverse_premise, inverse_copula=inverse_premise)


# def _syllogistic__resemblance__1_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
#     inverse_premise = True if (task.term.is_higher_order and (not belief.term.is_higher_order)) else False
#     return syllogistic__resemblance(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=inverse_premise, inverse_copula=(not inverse_premise))


# def _syllogistic__resemblance__0_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
#     inverse_premise = True if (task.term.is_higher_order and (not belief.term.is_higher_order)) else False
#     return syllogistic__resemblance(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=inverse_premise, inverse_copula=False)


# def _syllogistic__resemblance__1_1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
#     inverse_premise = True if (task.term.is_higher_order and (not belief.term.is_higher_order)) else False
#     return syllogistic__resemblance(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=inverse_premise, inverse_copula=True)


# def _syllogistic__resemblance__0_1_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
#     inverse_premise = True if ((not task.term.is_higher_order) and belief.term.is_higher_order) else False
#     return syllogistic__resemblance(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=inverse_premise, inverse_copula=inverse_premise)


# def _syllogistic__resemblance__1_0_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
#     inverse_premise = True if ((not task.term.is_higher_order) and belief.term.is_higher_order) else False
#     return syllogistic__resemblance(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=inverse_premise, inverse_copula=(not inverse_premise))


# def _syllogistic__resemblance__0_0_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
#     inverse_premise = True if ((not task.term.is_higher_order) and belief.term.is_higher_order) else False
#     return syllogistic__resemblance(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=inverse_premise, inverse_copula=False)


# def _syllogistic__resemblance__1_1_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
#     inverse_premise = True if ((not task.term.is_higher_order) and belief.term.is_higher_order) else False
#     return syllogistic__resemblance(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=inverse_premise, inverse_copula=True)

# '''reversion'''
# def _syllogistic__reversion(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
#     return syllogistic__reversion(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None))