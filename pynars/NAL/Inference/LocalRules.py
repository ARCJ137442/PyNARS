'''
这个文件包含了一些本地推理规则，用于在NARS中进行推理。

## 导入模块路径列表
- typing.List
- typing.Union
- pynars.NAL.Functions.BudgetFunctions.Budget_revision
- pynars.NAL.Functions.ExtendedBooleanFunctions.Or
- pynars.NAL.Functions.StampFunctions.Stamp_merge
- pynars.Narsese.Stamp
- pynars.Narsese.Task
- pynars.Narsese._py.Budget.Budget
- pynars.Narsese._py.Sentence.Goal
- pynars.Narsese._py.Sentence.Quest
- pynars.Narsese._py.Sentence.Question
- pynars.Narsese._py.Task.Belief
- pynars.Narsese.Sentence
- pynars.Narsese.Judgement
- pynars.Narsese.Truth
- pynars.Global
- pynars.Config.Enable
- pynars.NAL.Functions.Tools.calculate_solution_quality
- pynars.NAL.Functions.Tools.truth_to_quality
- copy.deepcopy

## 全局变量名称及其作用
- 无

## 各函数的依赖关系和主要功能
- revision: 用于将两个任务的真值进行合并，并返回一个新的任务。
- solution_question: 用于解决一个问题，将问题的答案与一个信念进行比较，如果答案更好，则更新问题的最佳答案，并将信念的真值作为奖励。
- solution_query: 用于解决一个查询，目前未实现。
- solve_query: 用于解决一个查询，目前未实现。
- Truth_revision: 用于将两个真值进行合并，并返回一个新的真值。
- Or: 用于计算两个布尔值的逻辑或。
- Stamp_merge: 用于将两个时间戳进行合并，并返回一个新的时间戳。
- calculate_solution_quality: 用于计算一个问题的答案与一个信念的质量。
- truth_to_quality: 用于将一个真值转换为一个质量值。
'''

from typing import List, Union
from pynars.NAL.Functions.BudgetFunctions import Budget_revision
from pynars.NAL.Functions.ExtendedBooleanFunctions import Or
from pynars.NAL.Functions.StampFunctions import Stamp_merge
from pynars.Narsese import Stamp, Task
from pynars.Narsese._py.Budget import Budget
from pynars.Narsese._py.Sentence import Goal, Quest, Question
from pynars.Narsese._py.Task import Belief
from ..Functions import Truth_revision
from pynars.Narsese import Sentence, Judgement, Truth
# from .TemporalRules import matching_order
from copy import deepcopy
from pynars import Global
from pynars.Config import Enable

from pynars.NAL.Functions.Tools import calculate_solution_quality, truth_to_quality

def revision(task: Task, belief: Task, budget_tasklink: Budget=None, budget_termlink: Budget=None):
    '''
    S. %f1;c1%
    S. %f2;c2%
    |-
    S. %F_rev%
    '''
    premise1: Union[Judgement, Goal] = task.sentence
    premise2: Union[Judgement, Goal] = belief.sentence
    truth1 = premise1.truth
    truth2 = premise2.truth
    if Enable.temporal_rasoning:
        # boolean useNewBeliefTerm = intervalProjection(nal, newBelief.getTerm(), oldBelief.getTerm(), beliefConcept.recent_intervals, newTruth);
        raise 
    truth = Truth_revision(truth1, truth2)
    budget, *_ = Budget_revision(task.budget, truth1, truth2, truth, budget_tasklink=budget_tasklink, budget_termlink=budget_termlink)
    term = premise1.term

    # stamp: Stamp = deepcopy(task.sentence.stamp) # Stamp(Global.time, task.sentence.stamp.t_occurrence, None, (j1.stamp.evidential_base | j2.stamp.evidential_base))
    # stamp.evidential_base.extend(premise2.evidential_base)
    stamp: Stamp = Stamp_merge(premise1.stamp, premise2.stamp)
    if task.is_judgement:
        task = Task(Judgement(term, stamp, truth), budget)
    elif task.is_goal:
        task = Task(Goal(term, stamp, truth), budget)
    else:
        raise "Invalid case."
    return task

def solution_question(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None):
    question: Union[Question, Quest] = task.sentence
    answer: Union[Judgement, Goal] = belief.sentence
    answer_best =  question.answer_best
    if answer_best is None: question.answer_best = answer
    else:
        quality_new = calculate_solution_quality(question, answer)
        quality_old = calculate_solution_quality(question, answer_best)
        if quality_new <= quality_old: answer = None
        else: question.answer_best = answer
    
    if answer is not None and question.answer_best is answer:
        quality = calculate_solution_quality(question, answer, question.term.has_qvar)
        # reward the belief
        budget_answer = Budget(Or(task.budget.priority, quality), task.budget.durability, truth_to_quality(answer.truth))
        belief = Belief(Judgement(answer.term, answer.stamp, answer.truth), budget_answer)

        # de-prioritize the question
        task.budget.priority = min(1-quality, task.budget.priority) # BUG: here, after setting the priority, the level of the task should change within a Bag.
        
    return belief if answer is not None else None

def solution_query(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None):
    '''
    sulution for query
    '''
    # if task.is_query and task.term.equal(belief.term): # BUG: here, variable unification should be executed.
    return solution_question(task, belief, budget_tasklink, budget_termlink)



def solve_query(task: Task, belief: Task, budget_tasklink: Budget=None, budget_termlink: Budget=None):
    raise "TODO"