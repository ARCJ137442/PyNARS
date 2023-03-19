'''
First-order syllogism & higher-order syllogism

简介：
    本文件实现了一些一阶和高阶三段论规则，包括强三段论、类比、相似、弱三段论、归纳、举例。这些规则可以用于NARS系统中的推理过程。

导入模块路径列表：
    - math
    - pynars.NAL.Functions.DesireValueFunctions
    - pynars.NAL.Functions.TruthValueFunctions
    - pynars.NAL.Functions.BudgetFunctions
    - pynars.Narsese
    - pynars.Narsese.Punctuation
    - pynars.Narsese.Sentence
    - pynars.Narsese.Judgement
    - pynars.Narsese.Goal
    - pynars.Narsese.Question
    - pynars.Narsese.Quest
    - pynars.NAL.Functions
    - copy
    - pynars.NAL.Functions.StampFunctions

全局变量名称及其作用：
    - 无

各函数的依赖关系和主要功能：
    - deduction: 实现了强三段论规则，包括一阶和高阶。函数的输入为一个任务和一个信念，输出为一个新的任务，其中新任务的语句为强三段论的结论，真值为两个前提的真值的逻辑和。
    - analogy: 实现了类比规则，包括一阶和高阶。函数的输入为一个任务和一个信念，输出为一个新的任务，其中新任务的语句为类比的结论，真值为两个前提的真值的逻辑和。
    - resemblance: 实现了相似规则，包括一阶和高阶。函数的输入为一个任务和一个信念，输出为一个新的任务，其中新任务的语句为相似的结论，真值为两个前提的真值的逻辑和。
    - abduction: 实现了拟合规则，包括一阶和高阶。函数的输入为一个任务和一个信念，输出为一个新的任务，其中新任务的语句为拟合的结论，真值为两个前提的真值的逻辑和。

'''

'''
First-order syllogism & higher-order syllogism

@ Author:   Bowen XU
@ Contact:  bowen.xu@pku.edu.cn
@ Update:   2021.11.6 
@ Comment:
    The general form:
        def syllogistic_rule(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False): ...
    The param `inverse_premise` means whether to inverse the order of term in the task and term in the belief as the two premises, for example, if the terms in the task and the belief are {<S-->M>, <M-->P>}, and the `inverse_premise` equals `True`, then the premises are {<M-->P>, <S-->M>}.
    The param `inverse_copula` means whether to inverse the order of the subject and predicate in the task, for example, if the term in the task is <S-->M>, and the `inverse_copula` equals `True`, then the premise1 is <M-->S>.
    The param `inverse_copula` means whether to inverse the order of the subject and predicate in the task, for example, if the term in the task is <S-->M>, and the `inverse_copula` equals `True`, then the premise1 is <M-->S>.
    
'''
import math
from pynars.NAL.Functions.DesireValueFunctions import Desire_strong, Desire_weak, Desire_deduction, Desire_induction
from pynars.NAL.Functions.TruthValueFunctions import *
from pynars.NAL.Functions.BudgetFunctions import Budget_backward_weak, Budget_forward, Budget_inference, Budget_backward
from pynars.Narsese import Term, Copula, Statement, Truth, Task, Belief, Budget, Stamp
from pynars.Narsese import Punctuation, Sentence, Judgement, Goal, Question, Quest
from ..Functions import F_deduction, fc_to_w_minus, fc_to_w_plus
from copy import deepcopy
from ..Functions.StampFunctions import *




'''
strong syllogism
'''

def deduction(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    '''
    First-order:
        premise1: <M --> P>
        premise2: <S --> M>
        |-
        conclusion: <S --> P>
    Higher-order:
        premise1: <M ==> P>
        premise2: <S ==> M>
        |-
        conclusion: <S ==> P>
    '''
    premise1, premise2 = (task.sentence, belief.sentence) if not inverse_premise else (belief.sentence, task.sentence)

    punct_task: Punctuation = task.sentence.punct
    stamp_task: Stamp = task.stamp
    stamp_belief: Stamp = belief.stamp
    truth_belief: Truth = belief.truth
    
    stat1: Statement = premise1.term
    stat2: Statement = premise2.term
    stamp = Stamp_merge(stamp_task, stamp_belief)

    statement = Statement(stat2.subject, stat1.copula, stat1.predicate)

    if punct_task.is_judgement:
        truth = Truth_deduction(premise1.truth, premise2.truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
        sentence_derived = Judgement(statement, stamp, truth)
    elif punct_task.is_goal:
        truth = Desire_weak(premise1.truth, premise2.truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
        sentence_derived = Goal(statement, stamp, truth)
    elif punct_task.is_question:
        curiosity = None # TODO
        budget = Budget_backward_weak(truth_belief, budget_tasklink, budget_termlink)
        sentence_derived = Question(statement, stamp, curiosity)
    elif punct_task.is_quest:
        curiosity = None # TODO
        budget = Budget_backward(truth_belief, budget_tasklink, budget_termlink)
        sentence_derived = Quest(statement, stamp, curiosity)
    else: raise "Invalid case."

    return Task(sentence_derived, budget)


def analogy(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    '''
    First-order:
        premise1: <M --> P> (inverse: <P --> M>)
        premise2: <S <-> M> (inverse: <S <-> M>)
        |-
        conclusion: <S --> P> (inverse: <P --> S>)

        premise1: <M --> P> (inverse: <P --> M>)
        premise2: <M <-> S> (inverse: <M <-> S>)
        |-
        conclusion: <S --> P> (inverse: <P --> S>)
    
    Higher-order:
        premise1: <M ==> P> (inverse: <P ==> M>)
        premise2: <M <-> S> (inverse: <M <-> S>)
        |-
        conclusion: <S ==> P> (inverse: <P ==> S>)

        premise1: <M ==> P> (inverse: <P ==> M>)
        premise2: <S <-> M> (inverse: <S <-> M>)
        |-
        conclusion: <S ==> P> (inverse: <P ==> S>)
        
        -------------

        premise1: <M ==> P> (inverse: <P ==> M>)
        premise2: <S <=> M> (inverse: <S <=> M>)
        |-
        conclusion: <S ==> P> (inverse: <P ==> S>)

        premise1: <M ==> P> (inverse: <P ==> M>)
        premise2: <M <=> S> (inverse: <M <=> S>)
        |-
        conclusion: <S ==> P> (inverse: <P ==> S>)
    '''
    # premise1, premise2 = (task.sentence, belief.sentence) if belief.term.is_commutative else (belief.sentence, task.sentence)
    premise1, premise2 = (task.sentence, belief.sentence) if not inverse_premise else (belief.sentence, task.sentence) # to ensure that the copula of premise1 is inheritence, and that the copula of premise2 is similarity.

    punct_task: Punctuation = task.sentence.punct
    stamp_task: Stamp = task.stamp
    stamp_belief: Stamp = belief.stamp
    truth_belief: Truth = belief.truth
    
    stat1: Statement = premise1.term
    stat2: Statement = premise2.term
    stamp = Stamp_merge(stamp_task, stamp_belief)
    
    # TODO
    if not inverse_copula:
        if stat2.predicate == stat1.subject:
            statement = Statement(stat2.subject, stat1.copula, stat1.predicate)
        elif stat2.subject == stat1.subject:
            statement = Statement(stat2.predicate, stat1.copula, stat1.predicate)
        else: raise "Invalid case."
    else:
        if stat2.predicate == stat1.predicate:
            statement = Statement(stat1.subject, stat1.copula, stat2.subject)
        elif stat2.subject == stat1.predicate:
            statement = Statement(stat1.subject, stat1.copula, stat2.predicate)
        else: raise "Invalid case."
            

    if punct_task.is_judgement:
        truth = Truth_analogy(premise1.truth, premise2.truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
        sentence_derived = Judgement(statement, stamp, truth)
    elif punct_task.is_goal:
        Desire_function = Desire_weak if task.term.is_commutative else Desire_strong
        truth = Desire_function(premise1.truth, premise2.truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
        sentence_derived = Goal(statement, stamp, truth)
    elif punct_task.is_question:
        curiosity = None # TODO
        budget = Budget_backward_weak(truth_belief, budget_tasklink, budget_termlink)
        sentence_derived = Question(statement, stamp, curiosity)
    elif punct_task.is_quest:
        curiosity = None # TODO
        budget = Budget_backward(truth_belief, budget_tasklink, budget_termlink)
        sentence_derived = Quest(statement, stamp, curiosity)
    else: raise "Invalid case."

    return Task(sentence_derived, budget)


def resemblance(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    '''
    First-order:
        premise1: <M <-> P> (inverse: <P <-> M>)
        premise2: <S <-> M> (inverse: <S <-> M>)
        |-
        conclusion: <S <-> P> (inverse: <P <-> S>)

        premise1: <M <-> P> (inverse: <P <-> M>)
        premise2: <M <-> S> (inverse: <M <-> S>)
        |-
        conclusion: <S <-> P> (inverse: <P <-> S>)
    
    Higher-order:
        premise1: <M <-> P> (inverse: <P <-> M>)
        premise2: <M <=> S> (inverse: <M <=> S>)
        |-
        conclusion: <S <=> P> (inverse: <P <=> S>)

        premise1: <M <-> P> (inverse: <P <-> M>)
        premise2: <S <=> M> (inverse: <S <=> M>)
        |-
        conclusion: <S <=> P> (inverse: <P <=> S>)
        
        -------------

        premise1: <M <=> P> (inverse: <P <=> M>)
        premise2: <M <-> S> (inverse: <M <-> S>)
        |-
        conclusion: <S <-> P> (inverse: <P <-> S>)

        premise1: <M <=> P> (inverse: <P <=> M>)
        premise2: <S <-> M> (inverse: <S <-> M>)
        |-
        conclusion: <S <-> P> (inverse: <P <-> S>)
        
        -------------

        premise1: <M <=> P> (inverse: <P <=> M>)
        premise2: <S <=> M> (inverse: <S <=> M>)
        |-
        conclusion: <S <=> P> (inverse: <P <=> S>)

        premise1: <M <=> P> (inverse: <P <=> M>)
        premise2: <M <=> S> (inverse: <M <=> S>)
        |-
        conclusion: <S <=> P> (inverse: <P <=> S>)
    '''

    premise1, premise2 = (task.sentence, belief.sentence) if not inverse_premise else (belief.sentence, task.sentence) # to ensure that the premise2 is a higher-order statement.

    punct_task: Punctuation = task.sentence.punct
    stamp_task: Stamp = task.stamp
    stamp_belief: Stamp = belief.stamp
    truth_belief: Truth = belief.truth
    
    stat1: Statement = premise1.term
    stat2: Statement = premise2.term
    stamp = Stamp_merge(stamp_task, stamp_belief)

    if not inverse_copula:
        if stat2.predicate == stat1.subject:
            statement = Statement(stat2.subject, stat2.copula, stat1.predicate)
        elif stat2.subject == stat1.subject:
            statement = Statement(stat2.predicate, stat2.copula, stat1.predicate)
        else: raise "Invalid case."
    else:
        if stat2.predicate == stat1.predicate:
            statement = Statement(stat1.subject, stat2.copula, stat2.subject)
        elif stat2.subject == stat1.predicate:
            statement = Statement(stat1.subject, stat2.copula, stat2.predicate)
        else: raise "Invalid case."

    if punct_task.is_judgement:
        truth = Truth_resemblance(premise1.truth, premise2.truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
        sentence_derived = Judgement(statement, stamp, truth)
    elif punct_task.is_goal:
        truth = Desire_strong(premise1.truth, premise2.truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
        sentence_derived = Goal(statement, stamp, truth)
    elif punct_task.is_question:
        curiosity = None # TODO
        budget = Budget_backward(truth_belief, budget_tasklink, budget_termlink)
        sentence_derived = Question(statement, stamp, curiosity)
    elif punct_task.is_quest:
        curiosity = None # TODO
        budget = Budget_backward(truth_belief, budget_tasklink, budget_termlink)
        sentence_derived = Quest(statement, stamp, curiosity)
    else: raise "Invalid case."

    return Task(sentence_derived, budget)


'''
weak syllogism
'''

def abduction(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    '''
    First-order:
        premise1: <P --> M>
        premise2: <S --> M>
        |-
        conclusion: <S --> P>
    Higher-order:
        premise1: <P ==> M>
        premise2: <S ==> M>
        |-
        conclusion: <S ==> P>

        premise1: <P =/> M>
        premise2: <S =\> M>
        |-
        conclusion: <S =\> P>

        premise1: <P =\> M>
        premise2: <S =/> M>
        |-
        conclusion: <S =\> P>
    '''
    premise1, premise2 = (task.sentence, belief.sentence) if not inverse_premise else (belief.sentence, task.sentence)

    punct_task: Punctuation = task.sentence.punct
    stamp_task: Stamp = task.stamp
    stamp_belief: Stamp = belief.stamp
    truth_belief: Truth = belief.truth
    
    stat1: Statement = premise1.term
    stat2: Statement = premise2.term
    stamp = Stamp_merge(stamp_task, stamp_belief)

    statement = Statement(stat2.subject, stat2.copula, stat1.subject)

    if punct_task.is_judgement:
        truth = Truth_abduction(premise1.truth, premise2.truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
        sentence_derived = Judgement(statement, stamp, truth)
    elif punct_task.is_goal:
        Desire_function = Desire_strong if not inverse_premise else Desire_weak
        truth = Desire_function(premise1.truth, premise2.truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
        sentence_derived = Goal(statement, stamp, truth)
    elif punct_task.is_question:
        curiosity = None # TODO
        Budget_function = Budget_backward if not inverse_premise else Budget_backward_weak
        budget = Budget_function(truth_belief, budget_tasklink, budget_termlink)
        sentence_derived = Question(statement, stamp, curiosity)
    elif punct_task.is_quest:
        curiosity = None # TODO
        Budget_function = Budget_backward_weak if not inverse_premise else Budget_backward
        budget = Budget_function(truth_belief, budget_tasklink, budget_termlink)
        sentence_derived = Quest(statement, stamp, curiosity)
    else: raise "Invalid case."

    return Task(sentence_derived, budget)


def induction(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    '''
    First-order:
        premise1: <M --> P>
        premise2: <M --> S>
        |-
        conclusion: <S --> P>
    Higher-order:
        premise1: <M ==> P>
        premise2: <M ==> S>
        |-
        conclusion: <S ==> P>

        premise1: <M =/> P>
        premise2: <M =\> S>
        |-
        conclusion: <S =/> P>

        premise1: <M =\> P>
        premise2: <M =/> S>
        |-
        conclusion: <S =/> P>
    '''
    premise1, premise2 = (task.sentence, belief.sentence) if not inverse_premise else (belief.sentence, task.sentence)

    punct_task: Punctuation = task.sentence.punct
    stamp_task: Stamp = task.stamp
    stamp_belief: Stamp = belief.stamp
    truth_belief: Truth = belief.truth
    
    stat1: Statement = premise1.term
    stat2: Statement = premise2.term
    stamp = Stamp_merge(stamp_task, stamp_belief)

    statement = Statement(stat2.predicate, stat1.copula, stat1.predicate)

    if task.is_judgement:
        truth = Truth_induction(premise1.truth, premise2.truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
        sentence_derived = Judgement(statement, stamp, truth)
    elif task.is_goal:
        Desire_function = Desire_strong if not inverse_premise else Desire_weak
        truth = Desire_function(premise1.truth, premise2.truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
        sentence_derived = Goal(statement, stamp, truth)
    elif task.is_question:
        curiosity = None # TODO
        Budget_function = Budget_backward if not inverse_premise else Budget_backward_weak
        budget = Budget_function(truth_belief, budget_tasklink, budget_termlink)
        sentence_derived = Question(statement, stamp, curiosity)
    elif task.is_quest:
        curiosity = None # TODO
        Budget_function = Budget_backward_weak if not inverse_premise else Budget_backward
        budget = Budget_function(truth_belief, budget_tasklink, budget_termlink)
        sentence_derived = Quest(statement, stamp, curiosity)
    else: raise "Invalid case."

    return Task(sentence_derived, budget)


def exemplification(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    '''
    First-order:
        premise2: <P --> M>
        premise1: <M --> S>
        |-
        conclusion: <S --> P>
    Higher-order:
        premise1: <P ==> M>
        premise2: <M ==> S>
        |-
        conclusion: <S ==> P>

        premise1: <P =\> M>
        premise2: <M =\> S>
        |-
        conclusion: <S =/> P>
    '''
    premise1, premise2 = (task.sentence, belief.sentence) if not inverse_premise else (belief.sentence, task.sentence)

    punct_task: Punctuation = task.sentence.punct
    stamp_task: Stamp = task.stamp
    stamp_belief: Stamp = belief.stamp
    truth_belief: Truth = belief.truth
    
    stat1: Statement = premise1.term
    stat2: Statement = premise2.term
    stamp = Stamp_merge(stamp_task, stamp_belief)

    statement = Statement(stat2.predicate, stat1.copula.reverse, stat1.subject)
    
    if punct_task.is_judgement:
        truth = Truth_exemplification(premise1.truth, premise2.truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
        sentence_derived = Judgement(statement, stamp, truth)
    elif punct_task.is_goal:
        truth = Desire_weak(premise1.truth, premise2.truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
        sentence_derived = Goal(statement, stamp, truth)
    elif punct_task.is_question:
        curiosity = None # TODO
        budget = Budget_backward_weak(truth_belief, budget_tasklink, budget_termlink)
        sentence_derived = Question(statement, stamp, curiosity)
    elif punct_task.is_quest:
        curiosity = None # TODO
        budget = Budget_backward(truth_belief, budget_tasklink, budget_termlink)
        sentence_derived = Quest(statement, stamp, curiosity)
    else: raise "Invalid case."

    return Task(sentence_derived, budget)


def comparison(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    ''''''
    '''
    First-order:
        premise1: <M --> P> (inverse_copula: <P --> M>)
        premise2: <M --> S> (inverse_copula: <S --> M>)
        |-
        conclusion: <S <-> P>
    Higher-order:
        premise1: <M ==> P>  (inverse_copula: <P ==> M>)
        premise2: <M ==> S>  (inverse_copula: <S ==> M>)
        |-
        conclusion: <S <=> P>

        premise1: <M =/> P>  (inverse_copula: <P =\> M>)
        premise2: <M =\> S>  (inverse_copula: <S =/> M>)
        |-
        conclusion: <S </> P>
    '''
    premise1, premise2 = (task.sentence, belief.sentence) if not (inverse_copula ^ inverse_premise) else (belief.sentence, task.sentence)

    punct_task: Punctuation = task.sentence.punct
    stamp_task: Stamp = task.stamp
    stamp_belief: Stamp = belief.stamp
    truth_belief: Truth = belief.truth
    
    stat1: Statement = premise1.term
    stat2: Statement = premise2.term
    stamp = Stamp_merge(stamp_task, stamp_belief)

    copula = stat1.copula.symmetrize() if not inverse_copula else stat2.copula.symmetrize()
    statement = Statement(stat2.predicate, copula, stat1.predicate) if not inverse_copula else Statement(stat2.subject, copula, stat1.subject)

    if punct_task.is_judgement:
        truth = Truth_comparison(premise1.truth, premise2.truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
        sentence_derived = Judgement(statement, stamp, truth)
    elif punct_task.is_goal:
        truth = Desire_strong(premise1.truth, premise2.truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
        sentence_derived = Goal(statement, stamp, truth)
    elif punct_task.is_question:
        curiosity = None # TODO
        budget = Budget_backward(truth_belief, budget_tasklink, budget_termlink)
        sentence_derived = Question(statement, stamp, curiosity)
    elif punct_task.is_quest:
        curiosity = None # TODO
        budget = Budget_backward_weak(truth_belief, budget_tasklink, budget_termlink)
        sentence_derived = Quest(statement, stamp, curiosity)
    else: raise "Invalid case."

    return Task(sentence_derived, budget)


'''Other rules out of the book'''

# This is a special rule, which is different from those of the syllogystic rules above. The form of the derived task differs between those derived from different types of sentence.
def reversion(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    ''''''
    '''
    First-order:
        For Judgement:
        premise1: <S --> P>. 
        premise2: <P --> S>.
        |-
        conclusion: <S <-> P>.

        For Goal, Question, and Quest
        premise1: <S --> P>?
        premise2: <P --> S>.
        |-
        conclusion: <S --> P>.
    Higher-order:
        For Judgement:
        premise1: <S ==> P>.  
        premise2: <P ==> S>.  
        |-
        conclusion: <S <=> P>.

        For Goal, Question, and Quest
        premise1: <S ==> P>?  
        premise2: <P ==> S>.  
        |-
        conclusion: <S ==> P>.
    Proof:
        For a judgement,
        Given `<S --> P>.` and `<P --> S>.`,
        according to the rule `intersection_composition` in `CompositionalRules`, that is `{T1. T2.} |- (&&, T1, T2). %F_int%`,
        it is derived that `(&&, <S --> P>, <P --> S>)`.
        According to the theorem `equivalence_theorem1` in `StructuralRules`, that is `<S <-> P> <=> (&&, <S --> P>, <P --> S>)`,
        it is derived that <S <-> P>.
        Hence, {<S --> P>. <P --> S>.} |- <S <-> P>.
        This is essentially a 2-step inference.

        For other cases, the rule is obviously right.
    '''
    premise1, premise2 = (task.sentence, belief.sentence) if not inverse_premise else (belief.sentence, task.sentence)

    # punct_task: Punctuation = task.sentence.punct
    stamp_task: Stamp = task.stamp
    stamp_belief: Stamp = belief.stamp
    truth_belief: Truth = belief.truth
    
    stat1: Statement = premise1.term
    stat2: Statement = premise2.term
    stamp = Stamp_merge(stamp_task, stamp_belief)

    if task.is_judgement:
        statement = Statement(stat2.subject, stat1.copula.symmetrize(), stat1.subject)
        truth = Truth_intersection(premise1.truth, premise2.truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
        sentence_derived = Judgement(statement, stamp, truth)
    elif task.is_goal or task.is_question or task.is_quest: 
        statement = task.term
        truth = Truth_conversion(belief.truth)
        budget = Budget_forward(truth, budget_tasklink, budget_termlink)
        sentence_derived = Judgement(statement, stamp, truth)
    else: raise "Invalid case."

    return Task(sentence_derived, budget)


