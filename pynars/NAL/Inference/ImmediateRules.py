'''
ImmediateRules.py
这个文件包含了一些基本的逻辑规则，如否定、转化和对偶等。这些规则是OpenNARS的基础，用于推理和推导。

## 导入模块路径列表
- pynars.Narsese._py.Sentence
- pynars.Narsese.Copula
- pynars.Narsese.Statement
- pynars.Narsese.Compound
- pynars.Narsese.Connector
- pynars.Narsese.Term
- pynars.Narsese.Task
- pynars.Narsese.Budget
- pynars.Narsese.Stamp
- pynars.Narsese.Judgement
- pynars.Narsese.Truth
- pynars.Narsese.Goal
- pynars.Narsese.Quest
- pynars.Narsese.Question
- pynars.Narsese.F_negation
- pynars.Narsese.F_conversion
- pynars.Narsese.F_contraposition
- pynars.Narsese.fc_to_w_minus
- pynars.Narsese.fc_to_w_plus
- pynars.Narsese.w_to_f
- pynars.Narsese.w_to_c
- pynars.Narsese.Functions.TruthValueFunctions
- pynars.Narsese.Functions.BudgetFunctions

## 全局变量名称及其作用
- 无

## 各函数的依赖关系和主要功能
- negation
    - 依赖：Truth_negation, Budget_forward
    - 主要功能：对一个命题取否定
- conversion
    - 依赖：Truth_conversion, Budget_forward
    - 主要功能：对一个命题进行转化
- contraposition
    - 依赖：Truth_contraposition, Budget_forward, Budget_backward_weak_compound
    - 主要功能：对一个命题进行对偶
'''

from pynars.Narsese._py.Sentence import Sentence
from ..Functions.TruthValueFunctions import *
from pynars.Narsese import Copula, Statement, Compound, Connector, Term, Task, Budget, Stamp
from ..Functions.BudgetFunctions import *

from ..Functions import F_negation, F_conversion, F_contraposition, \
    fc_to_w_minus, fc_to_w_plus, w_to_f, w_to_c
from pynars.Narsese import Judgement, Truth, Goal, Quest, Question

# TODO: <S --> P> |- <S <-> P> OpenNARS 3.0.4 LocalRules.java line 424~441

def negation(task: Task, term_concept: Term, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    '''
    S |- (--, S). %F_neg%
    '''
    stamp_task: Stamp = task.stamp
    premise: Sentence = task.sentence

    term_task = task.term
    term_neg = Compound.Negation(term_task)

    stamp = stamp_task
    if premise.is_judgement:
        truth = Truth_negation(premise.truth)
        sentence_derived = Judgement(term_neg, stamp, truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
    elif premise.is_goal:
        truth = Truth_negation(premise.truth)
        sentence_derived = Goal(term_neg, stamp, truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
    elif premise.is_question:
        sentence_derived = Question(term_neg, stamp)
        budget = Budget_backward_compound(premise.term, budget_tasklink, budget_termlink)
    elif premise.is_quest:
        sentence_derived = Quest(term_neg, stamp)
        budget = Budget_backward_compound(premise.term, budget_tasklink, budget_termlink)
    else: raise 'Invalid case.'

    return Task(sentence_derived, budget)


def conversion(task: Task, term_concept: Term, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    '''
    <S --> P> |- <P --> S>
    <S ==> P> |- <P ==> S>
    '''
    stamp_task: Stamp = task.stamp
    premise: Sentence = task.sentence
    stat: Statement = premise.term

    subject = stat.predicate
    predicate = stat.subject
    statement = Statement(subject, stat.copula.reverse, predicate)

    stamp = stamp_task
    if premise.is_judgement:
        truth = Truth_conversion(premise.truth)
        sentence_derived = Judgement(statement, stamp, truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
    # elif premise.is_goal:
    #     truth = Truth_negation(premise.truth)
    #     sentence_derived = Goal(term_concept, stamp, truth)
    #     budget = Budget_forward(truth, budget_tasklink, budget_termlink)
    # elif premise.is_question:
    #     sentence_derived = Question(term_concept, stamp)
    #     budget = Budget_backward_compound(premise.term, budget_tasklink, budget_termlink)
    # elif premise.is_quest:
    #     sentence_derived = Quest(term_concept, stamp)
    #     budget = Budget_backward_compound(premise.term, budget_tasklink, budget_termlink)
    else: raise 'Invalid case.'

    return Task(sentence_derived, budget)


def contraposition(task: Task, term_concept: Term, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    '''
    <<S ==> P> |- <(--, P) ==> (--, S)>>. %F_cnt%
    '''
    stamp_task: Stamp = task.stamp
    premise: Sentence = task.sentence
    stat: Statement = premise.term

    subject = Compound.Negation(stat.predicate)
    predicate = Compound.Negation(stat.subject)
    statement = Statement(subject, stat.copula, predicate)

    stamp = stamp_task
    if premise.is_judgement:
        truth = Truth_contraposition(premise.truth)
        sentence_derived = Judgement(statement, stamp, truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
    elif premise.is_goal:
        truth = Truth_negation(premise.truth)
        sentence_derived = Goal(term_concept, stamp, truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
    elif premise.is_question or premise.is_quest:
        sentence_derived = Question(term_concept, stamp)
        budget = Budget_backward_weak_compound(statement, budget_tasklink, budget_termlink)
    else: raise 'Invalid case.'

    return Task(sentence_derived, budget)
