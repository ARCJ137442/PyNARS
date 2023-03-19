'''
这个文件包含了用于处理三段论的接口函数。这些函数可以用于推理、类比、归纳、演绎、比较和类比推理。这些函数都是在syllogistic.py中定义的，但是这个文件提供了一些额外的功能，例如在不同的前提顺序下进行推理。

包依赖关系：
    pynars.NARS.DataStructures
    pynars.Narsese
    pynars.NAL.Inference
    pynars.NAL.Theorems
    pynars.Global

全局变量名称及其作用：
    无

各函数的依赖关系和主要功能：
    _syllogistic__deduction__0_1:
        依赖：syllogistic__deduction
        功能：{<M-->P>, <S-->M>} |- <S-->P>
    _syllogistic__deduction__1_0:
        依赖：syllogistic__deduction
        功能：{<S-->M>, <M-->P>} |- <S-->P>
    _syllogistic__exemplification__0_1:
        依赖：syllogistic__exemplification
        功能：{<M-->S>, <P-->M>} |- <S-->P>
    _syllogistic__exemplification__1_0:
        依赖：syllogistic__exemplification
        功能：{<P-->M>, <M-->S>} |- <S-->P>
    _syllogistic__induction__0_0:
        依赖：syllogistic__induction
        功能：归纳推理
    _syllogistic__induction__0_0_prime:
        依赖：syllogistic__induction
        功能：归纳推理
    _syllogistic__abduction__1_1:
        依赖：syllogistic__abduction
        功能：类比推理
    _syllogistic__comparison__0_0:
        依赖：syllogistic__comparison
        功能：{<M-->P>, <S-->P>} |- <S-->M>
    _syllogistic__comparison__0_0_prime:
        依赖：syllogistic__comparison
        功能：{<M-->P>, <S-->P>} |- <M-->S>
    _syllogistic__comparison__1_1:
        依赖：syllogistic__comparison
        功能：{<M-->P>, <S-->M>} |- <S-->P>
    _syllogistic__comparison__1_1_prime:
        依赖：syllogistic__comparison
        功能：{<M-->P>, <S-->M>} |- <P-->S>
    _syllogistic__analogy__0_1:
        依赖：syllogistic__analogy
        功能：{<M-->P>, <S-->M>} |- <S-->P>
    _syllogistic__analogy__1_0:
        依赖：syllogistic__analogy
        功能：{<M-->P>, <M-->S>} |- <S-->P>
各函数的依赖关系和主要功能：
    _syllogistic__analogy__0_0:
        依赖：syllogistic__analogy
        功能：{<M-->P>, <S-->M>} |- <M-->S>
    _syllogistic__analogy__1_1:
        依赖：syllogistic__analogy
        功能：{<M-->P>, <S-->M>} |- <P-->S>
    _syllogistic__resemblance__0_1:
        依赖：syllogistic__resemblance
        功能：{<M-->P>, <S-->M>} |- <S-->P>
    _syllogistic__resemblance__1_0:
        依赖：syllogistic__resemblance
        功能：{<M-->P>, <M-->S>} |- <S-->P>
    _syllogistic__resemblance__0_0_prime:
        依赖：syllogistic__resemblance
        功能：{<P-->M>, <S-->M>} |- <S-->P>
    _syllogistic__resemblance__1_1_prime:
        依赖：syllogistic__resemblance
        功能：{<P-->M>, <M-->S>} |- <P-->S>
    _syllogistic__reversion:
        依赖：无
        功能：反演推理
'''

from pynars.NARS.DataStructures import Link, TaskLink, TermLink, LinkType, Task
from pynars.Narsese import Belief
from pynars.NAL.Inference import *
from pynars.NAL.Theorems import *
from pynars import Global

'''deduction'''
def _syllogistic__deduction__0_1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<M-->P>, <S-->M>} |- <S-->P>'''
    return syllogistic__deduction(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)


def _syllogistic__deduction__1_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<S-->M>, <M-->P>} |- <S-->P>'''
    return syllogistic__deduction(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)


'''exemplification'''
def _syllogistic__exemplification__0_1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<M-->S>, <P-->M>} |- <S-->P>'''
    return syllogistic__exemplification(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)


def _syllogistic__exemplification__1_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<P-->M>, <M-->S>} |- <S-->P>'''
    return syllogistic__exemplification(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)


'''induction'''
def _syllogistic__induction__0_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return syllogistic__induction(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)


def _syllogistic__induction__0_0_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return syllogistic__induction(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)


'''abduction'''
def _syllogistic__abduction__1_1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return syllogistic__abduction(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)


def _syllogistic__abduction__1_1_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return syllogistic__abduction(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)


def _syllogistic__comparison__0_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return syllogistic__comparison(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False,inverse_copula=False)

def _syllogistic__comparison__0_0_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return syllogistic__comparison(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True, inverse_copula=False)

def _syllogistic__comparison__1_1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return syllogistic__comparison(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False, inverse_copula=True)

def _syllogistic__comparison__1_1_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return syllogistic__comparison(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True, inverse_copula=True)


'''analogy'''
def _syllogistic__analogy__0_1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return syllogistic__analogy(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False if belief.term.is_commutative else True, inverse_copula=False if belief.term.is_commutative else True)


def _syllogistic__analogy__1_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return syllogistic__analogy(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False if belief.term.is_commutative else True, inverse_copula=True if belief.term.is_commutative else False)


def _syllogistic__analogy__0_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return syllogistic__analogy(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False if belief.term.is_commutative else True, inverse_copula=False)


def _syllogistic__analogy__1_1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return syllogistic__analogy(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False if belief.term.is_commutative else True, inverse_copula=True)


'''resemblance'''
def _syllogistic__resemblance__0_1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    inverse_premise = True if (task.term.is_higher_order and (not belief.term.is_higher_order)) else False
    return syllogistic__resemblance(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=inverse_premise, inverse_copula=inverse_premise)


def _syllogistic__resemblance__1_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    inverse_premise = True if (task.term.is_higher_order and (not belief.term.is_higher_order)) else False
    return syllogistic__resemblance(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=inverse_premise, inverse_copula=(not inverse_premise))


def _syllogistic__resemblance__0_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    inverse_premise = True if (task.term.is_higher_order and (not belief.term.is_higher_order)) else False
    return syllogistic__resemblance(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=inverse_premise, inverse_copula=False)


def _syllogistic__resemblance__1_1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    inverse_premise = True if (task.term.is_higher_order and (not belief.term.is_higher_order)) else False
    return syllogistic__resemblance(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=inverse_premise, inverse_copula=True)


def _syllogistic__resemblance__0_1_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    inverse_premise = True if ((not task.term.is_higher_order) and belief.term.is_higher_order) else False
    return syllogistic__resemblance(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=inverse_premise, inverse_copula=inverse_premise)


def _syllogistic__resemblance__1_0_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    inverse_premise = True if ((not task.term.is_higher_order) and belief.term.is_higher_order) else False
    return syllogistic__resemblance(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=inverse_premise, inverse_copula=(not inverse_premise))


def _syllogistic__resemblance__0_0_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    inverse_premise = True if ((not task.term.is_higher_order) and belief.term.is_higher_order) else False
    return syllogistic__resemblance(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=inverse_premise, inverse_copula=False)


def _syllogistic__resemblance__1_1_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    inverse_premise = True if ((not task.term.is_higher_order) and belief.term.is_higher_order) else False
    return syllogistic__resemblance(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=inverse_premise, inverse_copula=True)

'''reversion'''
def _syllogistic__reversion(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    return syllogistic__reversion(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None))