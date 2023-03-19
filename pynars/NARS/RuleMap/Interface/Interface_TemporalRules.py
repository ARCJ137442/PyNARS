'''
这个文件包含了一些用于时间推理的规则，包括序列、并行、类比、归纳等。这些规则可以用于NARS系统中的时间推理，以及其他需要时间推理的应用中。

包依赖关系：
    pynars.NARS.DataStructures
    pynars.Narsese
    pynars.NAL.Inference
    pynars.NAL.Theorems
    pynars.Global
    pynars.Narsese._py.Copula
    pynars.Narsese._py.Term

全局变量名称及其作用：
    无

各函数的依赖关系和主要功能：
    _temporal__deduction_sequence_eliminate__0:
        依赖：temporal__deduction_sequence_eliminate
        功能：将一个时间推理任务中的序列消解为单个语句。
    _temporal__deduction_sequence_eliminate__0_prime:
        依赖：temporal__deduction_sequence_eliminate
        功能：将一个时间推理任务中的序列消解为单个语句。
    _temporal__abduction__1:
        依赖：temporal__abduction
        功能：将一个时间推理任务中的类比转化为推理。
    _temporal__abduction__1_prime:
        依赖：temporal__abduction
        功能：将一个时间推理任务中的类比转化为推理。
    _temporal__deduction_sequence_replace__0_1:
        依赖：temporal__deduction_sequence_replace
        功能：将一个时间推理任务中的序列替换为单个语句。
    _temporal__deduction_sequence_replace__1_0:
        依赖：temporal__deduction_sequence_replace
        功能：将一个时间推理任务中的序列替换为单个语句。
    _temporal__sequence_immediate:
        依赖：temporal__sequence_immediate
        功能：将一个时间推理任务中的立即序列转化为单个语句。
    _temporal__sequence:
        依赖：temporal__sequence
        功能：将一个时间推理任务中的序列转化为单个语句。
    _temporal__sequence_prime:
        依赖：temporal__sequence
        功能：将一个时间推理任务中的序列转化为单个语句。
    _temporal__parallel_immediate:
        依赖：temporal__parallel_immediate
        功能：将一个时间推理任务中的立即并行转化为单个语句。
    _temporal__parallel:
        依赖：temporal__parallel
        功能：将一个时间推理任务中的并行转化为单个语句。
    _temporal__analogy__0_1:
        依赖：temporal__analogy
        功能：将一个时间推理任务中的类比转化为推理。
    _temporal__analogy__1_0:
        依赖：temporal__analogy
        功能：将一个时间推理任务中的类比转化为推理。
    _temporal__analogy__0_0:
        依赖：temporal__analogy
        功能：将一个时间推理任务中的类比转化为推理。
    _temporal__analogy__1_1:
        依赖：temporal__analogy
        功能：将一个时间推理任务中的类比转化为推理。
    _temporal__induction_implication:
        依赖：temporal__induction_implication
        功能：将一个时间推理任务中的序列转化为单个语句。
    _temporal__induction_implication_prime:
        依赖：temporal__induction_implication
        功能：将一个时间推理任务中的序列转化为单个语句。
    _temporal__induction_equivalence:
        依赖：temporal__induction_equivalence
        功能：将一个时间推理任务中的序列转化为单个语句。
    _temporal__induction_composition:
        依赖：temporal__induction_composition
        功能：将一个时间推理任务中的序列转化为单个语句。
    _temporal__induction_predictieve_implication_composition:
        依赖：temporal__induction_predictieve_implication_composition
        功能：将一个时间推理任务中的序列转化为单个语句。
    _temporal__induction_predictive_implication_composition_prime:
        依赖：temporal__induction_predictive_implication_composition
        功能：将一个时间推理任务中的序列转化为单个语句。
    _temporal__induction_predictive_implication_composition_inverse:
        依赖：temporal__induction_predictive_implication_composition
        功能：将一个时间推理任务中的序列转化为单个语句。
    _temporal__induction_predictive_implication_composition_inverse_prime:
        依赖：temporal__induction_predictive_implication_composition
        功能：将一个时间推理任务中的序列转化为单个语句。
各函数的依赖关系和主要功能：
    _temporal__induction_retrospective_implication_composition:
        依赖：temporal__induction_retrospective_implication_composition
        功能：将一个时间推理任务中的序列转化为单个语句。
    _temporal__induction_retrospective_implication_composition_prime:
        依赖：temporal__induction_retrospective_implication_composition
        功能：将一个时间推理任务中的序列转化为单个语句。
    _temporal__induction_retrospective_implication_composition_inverse:
        依赖：temporal__induction_retrospective_implication_composition
        功能：将一个时间推理任务中的序列转化为单个语句。
    _temporal__induction_retrospective_implication_composition_inverse_prime:
        依赖：temporal__induction_retrospective_implication_composition
        功能：将一个时间推理任务中的序列转化为单个语句。
'''
from pynars.NARS.DataStructures import Link, TaskLink, TermLink, LinkType, Task
from pynars.Narsese import Belief
from pynars.NAL.Inference import *
from pynars.NAL.Theorems import *
from pynars import Global
from pynars.Narsese._py.Copula import Copula
from pynars.Narsese._py.Term import Term


def _temporal__deduction_sequence_eliminate__0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<(&/, C, +100, S, ...) =/> P>. C. :|:} |- <S=/>P>. :!105:'''
    return temporal__deduction_sequence_eliminate(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)


def _temporal__deduction_sequence_eliminate__0_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{C. :|: <(&/, C, +100, S, ...) =/> P>.} |- <S=/>P>. :!105:'''
    return temporal__deduction_sequence_eliminate(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)


def _temporal__abduction__1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<(&/, C, +100, S, ...) =/> P>. C. :|:} |- <S=/>P>. :!105:'''
    return temporal__abduction(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)


def _temporal__abduction__1_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{C. :|: <(&/, C, +100, S, ...) =/> P>.} |- <S=/>P>. :!105:'''
    return temporal__abduction(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)

def _temporal__deduction_sequence_replace__0_1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<(&&, C, S, ...) ==> P>. <C ==> P>.} |- P.'''
    return temporal__deduction_sequence_replace(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)

def _temporal__deduction_sequence_replace__1_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{<C ==> P>. <(&&, C, S, ...) ==> P>.} |- P.'''
    return temporal__deduction_sequence_replace(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)


def _temporal__sequence_immediate(task: Task, term_belief: Term, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{(&/, A, B, C)! A} |- A!.'''
    return temporal__sequence_immediate(task, term_belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)

def _temporal__sequence(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{(&/, A, B, C)! A} |- A!.'''
    return temporal__sequence(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)

def _temporal__sequence_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{C! (&/, A, B, C).} |- (&/, A, B)!'''
    return temporal__sequence(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True, inverse_copula=True)

    
def _temporal__parallel_immediate(task: Task, term_belief: Term, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{(&/, A, B, C)! A} |- A!.'''
    return temporal__parallel_immediate(task, term_belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)

def _temporal__parallel(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    '''{(&/, A, B, C)! A} |- A!.'''
    return temporal__parallel(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)

# def _temporal__parallel_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
#     '''{(&/, A, B, C)! A} |- A!.'''
#     return temporal__parallel(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)

'''analogy'''
def _temporal__analogy__0_1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    is_equivalence = belief.term.copula in (Copula.ConcurrentEquivalence, Copula.PredictiveEquivalence)
    return temporal__analogy(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False if is_equivalence else True, inverse_copula=False if is_equivalence else True)


def _temporal__analogy__1_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    is_equivalence = belief.term.copula in (Copula.ConcurrentEquivalence, Copula.PredictiveEquivalence)
    return temporal__analogy(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False if is_equivalence else True, inverse_copula=True if is_equivalence else False)


def _temporal__analogy__0_0(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    is_equivalence = belief.term.copula in (Copula.ConcurrentEquivalence, Copula.PredictiveEquivalence)
    return temporal__analogy(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False if is_equivalence else True, inverse_copula=False)


def _temporal__analogy__1_1(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    is_equivalence = belief.term.copula in (Copula.ConcurrentEquivalence, Copula.PredictiveEquivalence)
    return temporal__analogy(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False if is_equivalence else True, inverse_copula=True)

'''Sequential induction'''
# TODO: the name of each rule may need to be modifed.
def _temporal__induction_implication(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    ''''''
    return temporal__induction_implication(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)


def _temporal__induction_implication_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    ''''''
    return temporal__induction_implication(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True)


def _temporal__induction_equivalence(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    ''''''
    return temporal__induction_equivalence(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)


def _temporal__induction_composition(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    ''''''
    return temporal__induction_composition(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False)

''''''
def _temporal__induction_predictieve_implication_composition(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    ''''''
    return temporal__induction_predictive_implication_composition(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False, inverse_copula=False)


def _temporal__induction_predictive_implication_composition_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    ''''''
    return temporal__induction_predictive_implication_composition(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True, inverse_copula=False)


def _temporal__induction_predictive_implication_composition_inverse(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    ''''''
    return temporal__induction_predictive_implication_composition(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False, inverse_copula=True)


def _temporal__induction_predictive_implication_composition_inverse_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    ''''''
    return temporal__induction_predictive_implication_composition(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True, inverse_copula=True)


''''''
def _temporal__induction_retrospective_implication_composition(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    ''''''
    return temporal__induction_retrospective_implication_composition(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False, inverse_copula=False)


def _temporal__induction_retrospective_implication_composition_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    ''''''
    return temporal__induction_retrospective_implication_composition(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True, inverse_copula=False)


def _temporal__induction_retrospective_implication_composition_inverse(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    ''''''
    return temporal__induction_retrospective_implication_composition(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False, inverse_copula=True)


def _temporal__induction_retrospective_implication_composition_inverse_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    ''''''
    return temporal__induction_retrospective_implication_composition(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True, inverse_copula=True)


def _temporal__induction_predictive_equivalance_composition(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    ''''''
    return temporal__induction_predictive_equivalance_composition(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False, inverse_copula=False)

def _temporal__induction_predictive_equivalance_composition_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    ''''''
    return temporal__induction_predictive_equivalance_composition(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True, inverse_copula=False)

def _temporal__induction_retrospective_equivalance_composition(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    ''''''
    return temporal__induction_retrospective_equivalance_composition(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=False, inverse_copula=False)

def _temporal__induction_retrospective_equivalance_composition_prime(task: Task, belief: Belief, tasklink: TaskLink=None, termlink: TermLink=None):
    ''''''
    return temporal__induction_retrospective_equivalance_composition(task, belief, (tasklink.budget if tasklink is not None else None), (termlink.budget if termlink is not None else None), inverse_premise=True, inverse_copula=False)
