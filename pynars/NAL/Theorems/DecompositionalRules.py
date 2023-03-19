'''
这个文件包含了NARS的分解规则，包括以下规则：
    1. <M --> (&, T1, T2)>.  <M --> T1>. |-  <M --> T2>.
    2. <M --> (|, T1, T2)>.  <M --> T1>. |-  <M --> T2>.
    3. <M --> (-, T1, T2)>). <M --> T1>. |-  <M --> T2>.
    4. <M --> (-, T1, T2)>). <M --> T1>. |-  <M --> T2>.
    5. (--, <(|, T1, T2) --> M>).  <T1 --> M>. |-  (--, <T2 --> M>).
    6. <(&, T1, T2) --> M>.        (--, <T1 --> M>). |-  (--, <T2 --> M>).
    7. (--, <(~, T1, T2) --> M>).  <T1 --> M>. |-  <T2 --> M>.
    8. (--, <(~, T2, T1) --> M>).  (--, <T1 --> M>). |-  (--, <T2 --> M>).
    9. (&&, T2, T1).        T1. |- T2.
    10. (||, T1, T2).       T1. |- T2.

【导入模块路径列表】
    - Copula
    - Statement
    - Compound
    - Connector
    - Term
    - Truth
    - Task
    - Belief
    - Budget
    - Judgement
    - Goal
    - Quest
    - Question
    - truth_analytic
    - Functions

【全局变量名称及其作用】
    - truth_analytic: 用于计算分解规则的分析真值。

【各函数的依赖关系和主要功能】
    - decomposition_theorem1:
        依赖：无
        功能：实现分解规则1——将一个复合语句分解为两个子语句，其中一个是复合语句的谓词，另一个是复合语句的主语。
    - decomposition_theorem2:
        依赖：无
        功能：实现分解规则2——将一个复合语句分解为两个子语句，其中一个是复合语句的主语，另一个是复合语句的谓词。
    - decomposition_theorem3:
        依赖：无
        功能：实现分解规则3——将一个复合语句分解为两个子语句，其中一个是复合语句的主语，另一个是复合语句的谓词的否定。
    - decomposition_theorem4:
        依赖：无
        功能：实现分解规则4——将一个复合语句分解为两个子语句，其中一个是复合语句的谓词的否定，另一个是复合语句的主语的否定。
    - decomposition_theorem5:
        依赖：无
        功能：实现分解规则5——将一个复合语句分解为两个子语句，其中一个是复合语句的主语，另一个是复合语句的谓词的两个子语句的析取的否定。
    - decomposition_theorem6:
        依赖：无
        功能：实现分解规则6——将一个复合语句分解为两个子语句，其中一个是复合语句的主语的两个子语句的合取，另一个是复合语句的谓词。
    - decomposition_theorem7:
        依赖：无
        功能：实现分解规则7——将一个复合语句分解为两个子语句，其中一个是复合语句的主语，另一个是复合语句的谓词的否定的主语。
    - decomposition_theorem8:
        依赖：无
        功能：实现分解规则8——将一个复合语句分解为两个子语句，其中一个是复合语句的谓词的否定的主语，另一个是复合语句的主语的否定。
    - decomposition_theorem9:
        依赖：无
        功能：实现分解规则9——将一个复合语句分解为两个子语句，其中一个是复合语句的两个子语句的合取，另一个是复合语句的其中一个子语句。
    - decomposition_theorem10:
        依赖：无
        功能：实现分解规则10——将一个复合语句分解为两个子语句，其中一个是复合语句的其中一个子语句，另一个是复合语句的另一个子语句的否定。
'''

from pynars.Narsese import Copula, Statement, Compound, Connector, Term, Truth, Task, Belief, Budget
from pynars.Narsese import Judgement, Goal, Quest, Question
from pynars.Narsese import truth_analytic
from ..Functions import *

'''
Decompositional rules

Including,
        S1                          S2                      S
        -----------------------------------------------------------------------
1 ok    (--, <M --> (&, T1, T2)>).  <M --> T1>.         |-  (--, <M --> T2>).
2 ok    <M --> (|, T1, T2)>.        (--, <M --> T1>).   |-  <M --> T2>.
3       (--, <M --> (-, T1, T2)>).  <M --> T1>.         |-  <M --> T2>.
4       (--, <M --> (-, T2, T1)>).  (--, <M --> T1>).   |-  (--, <M --> T2>).
5       (--, <(|, T2, T1) --> M>).  <T1 --> M>.         |-  (--, <T2 --> M>).
6       <(&, T1, T2) --> M>.        (--, <T1 --> M>).   |-  (--, <T2 --> M>).
7       (--, <(~, T1, T2) --> M>).  <T1 --> M>.         |-  <T2 --> M>.
8       (--, <(~, T2, T1) --> M>).  (--, <T1 --> M>).   |-  (--, <T2 --> M>).

9       (--, (&&, T1, T2)).         T1.                 |-  (--, T2).
10      (||, T1, T2).               (--, T1).           |-  T2.

Each rule corresponds to a knowledge (with analytics truth) following the form 
    <(&&, S1, S2) ==> S>. %1.0;1.0%

TODO Doubt:
When any task comes into the reasoner, any theorem can be used to derive an analytically true knowledge.
Then, which rule should be took?

TODO:
    Make a general check function to get the valid knowledge according to the two premises.
    And in each rule function, do no checking and get the derived knowedge directly.
'''

def decomposition_theorem1(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    '''
    Original:   (--, <M --> (&, T1, T2)>).  <M --> T1>. |-  (--, <M --> T2>).
    Practical:  <M --> (&, T1, T2)>.        <M --> T1>. |-  <M --> T2>.
    '''
    premise1, premise2 = (task.sentence, belief.sentence) if not inverse_premise else (belief.sentence, task.sentence)

    stamp_task: Stamp = task.stamp
    stamp_belief: Stamp = belief.stamp

    stamp = Stamp_merge(stamp_task, stamp_belief)

    stat1: Statement = premise1.term[0]
    stat2: Statement = premise2.term
    compound: Compound = stat1.predicate

    statement = Statement(stat2.subject, Copula.Inheritance, compound - stat2.predicate)

    if task.is_judgement:
        truth = Truth_negation(Truth_deduction(Truth_intersection(Truth_negation(premise1.truth), premise2.truth), truth_analytic))
        budget = Budget_forward_compound(statement, truth, budget_tasklink, budget_termlink)
        sentence_derived = Judgement(statement, stamp, truth)
    else: raise "Invalid case."

    return Task(sentence_derived, budget)


def decomposition_theorem2(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    '''
    Original:   <M --> (|, T1, T2)>.        (--, <M --> T1>).   |-  <M --> T2>.
    Practical:  <M --> (|, T1, T2)>.        <M --> T1>.         |-  <M --> T2>.

    Proof (of Theorem 7.8 in the NAL book):
        According to propositional logic, implication of the definition of extensional intersection ((M → T1)∧(M → T2)) =⇒ (M → (T1∩T2)) can be rewritten equivalently into ((M → T1) ∧ ¬(M → (T1 ∩ T2))) =⇒ ¬(M → T2), and ((T1 ∩ T2) → M) =⇒ (((T1 → M) ∨ (T2 → M)) into (¬(T1 → M) ∧ (T1 ∩ T2) → M) =⇒ (T2 → M). The conclusions on intensional intersection can be proved in parallel.
    According to the proof, similarly,  {<M --> (|, T1, T2)>. (--, (<M --> (|, T1, T3)>).} |-  <M --> T2>.
    
    ((M → T1)∧(M → T2)∧(M → T3)∧(M → T3)) =⇒ (M → (T1∩T2∩T3∩T4))
    ((M → (T1∩T2))∧¬(M → (T1∩T2∩T3∩T4)) =⇒ ¬(M → (T3∩T4))


    '''
    premise1, premise2 = (task.sentence, belief.sentence) if not inverse_premise else (belief.sentence, task.sentence)

    stamp_task: Stamp = task.stamp
    stamp_belief: Stamp = belief.stamp

    stamp = Stamp_merge(stamp_task, stamp_belief)

    stat1: Statement = premise1.term
    stat2: Statement = premise2.term
    compound: Compound = stat1.predicate

    statement = Statement(stat2.subject, stat1.copula, compound - stat2.predicate)

    if task.is_judgement:
        # # As a theorem to apply, the truth should be calculated with the analytic truth using the deduction rule, isn't it?
        # truth = Truth_deduction(Truth_intersection(premise1.truth, Truth_negation(premise2.truth)), truth_analytic)
        truth = Truth_intersection(premise1.truth, Truth_negation(premise2.truth))
        budget = Budget_forward_compound(statement, truth, budget_tasklink, budget_termlink)
        sentence_derived = Judgement(statement, stamp, truth)
    else: raise "Invalid case."

    return Task(sentence_derived, budget)


def decomposition_theorem3(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    '''
    Original:   (--, <M --> (-, T1, T2)>).  <M --> T1>. |-  <M --> T2>.
    Practical:  <M --> (-, T1, T2)>).  <M --> T1>.      |-  <M --> T2>.
    '''
    premise1, premise2 = (task.sentence, belief.sentence) if not inverse_premise else (belief.sentence, task.sentence)

    stamp_task: Stamp = task.stamp
    stamp_belief: Stamp = belief.stamp

    stamp = Stamp_merge(stamp_task, stamp_belief)

    stat1: Statement = premise1.term
    stat2: Statement = premise2.term
    compound: Compound = stat1.predicate

    statement = Statement(stat2.subject, stat1.copula, compound - stat2.predicate)

    if task.is_judgement:
        truth = Truth_intersection(Truth_negation(premise1.truth), premise2.truth)
        budget = Budget_forward_compound(statement, truth, budget_tasklink, budget_termlink)
        sentence_derived = Judgement(statement, stamp, truth)
    else: raise "Invalid case."

    return Task(sentence_derived, budget)


def decomposition_theorem4(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    '''
    Original:   (--, <M --> (-, T2, T1)>).  (--, <M --> T1>).   |-  (--, <M --> T2>).
    Practical:  <M --> (-, T1, T2)>).  <M --> T1>.              |-  <M --> T2>.
    '''
    premise1, premise2 = (task.sentence, belief.sentence) if not inverse_premise else (belief.sentence, task.sentence)

    stamp_task: Stamp = task.stamp
    stamp_belief: Stamp = belief.stamp

    stamp = Stamp_merge(stamp_task, stamp_belief)

    stat1: Statement = premise1.term
    stat2: Statement = premise2.term
    compound: Compound = stat1.predicate

    statement = Statement(stat2.subject, Copula.Inheritance, compound - stat2.predicate)

    if task.is_judgement:
        truth = Truth_negation(Truth_intersection(Truth_negation(premise1.truth), Truth_negation(premise2.truth)))
        budget = Budget_forward_compound(statement, truth, budget_tasklink, budget_termlink)
        sentence_derived = Judgement(statement, stamp, truth)
    else: raise "Invalid case."

    return Task(sentence_derived, budget)

def decomposition_theorem5(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    '''(--, <(|, T1, T2) --> M>).  <T1 --> M>.         |-  (--, <T2 --> M>).'''
    premise1, premise2 = (task.sentence, belief.sentence) if not inverse_premise else (belief.sentence, task.sentence)

    stamp_task: Stamp = task.stamp
    stamp_belief: Stamp = belief.stamp

    stamp = Stamp_merge(stamp_task, stamp_belief)

    stat1: Statement = premise1.term[0]
    stat2: Statement = premise2.term
    compound: Compound = stat1.subject

    statement = Compound.Negation(Statement(compound - stat2.subject, Copula.Inheritance, stat2.subject))

    if task.is_judgement:
        truth = Truth_deduction(Truth_intersection(premise1.truth, premise2.truth), truth_analytic)
        budget = Budget_forward_compound(statement, truth, budget_tasklink, budget_termlink)
        sentence_derived = Judgement(statement, stamp, truth)
    else: raise "Invalid case."

    return Task(sentence_derived, budget)


def decomposition_theorem6(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    '''<(&, T1, T2) --> M>.        (--, <T1 --> M>)   |-  (--, <T2 --> M>).'''
    premise1, premise2 = (task.sentence, belief.sentence) if not inverse_premise else (belief.sentence, task.sentence)

    stamp_task: Stamp = task.stamp
    stamp_belief: Stamp = belief.stamp

    stamp = Stamp_merge(stamp_task, stamp_belief)

    stat1: Statement = premise1.term
    stat2: Statement = premise2.term[0]
    compound: Compound = stat1.subject

    statement = Compound.Negation(Statement(compound - stat2.subject, Copula.Inheritance, stat2.subject))

    if task.is_judgement:
        truth = Truth_deduction(Truth_intersection(premise1.truth, premise2.truth), truth_analytic)
        budget = Budget_forward_compound(statement, truth, budget_tasklink, budget_termlink)
        sentence_derived = Judgement(statement, stamp, truth)
    else: raise "Invalid case."

    return Task(sentence_derived, budget)


def decomposition_theorem7(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    '''(--, <(~, T1, T2) --> M>).  <T1 --> M>.         |-  <T2 --> M>.'''
    premise1, premise2 = (task.sentence, belief.sentence) if not inverse_premise else (belief.sentence, task.sentence)

    stamp_task: Stamp = task.stamp
    stamp_belief: Stamp = belief.stamp

    stamp = Stamp_merge(stamp_task, stamp_belief)

    stat1: Statement = premise1.term[0]
    stat2: Statement = premise2.term
    compound: Compound = stat1.subject

    statement = Statement(compound - stat2.subject, Copula.Inheritance, stat2.subject)

    if task.is_judgement:
        truth = Truth_deduction(Truth_intersection(premise1.truth, premise2.truth), truth_analytic)
        budget = Budget_forward_compound(statement, truth, budget_tasklink, budget_termlink)
        sentence_derived = Judgement(statement, stamp, truth)
    else: raise "Invalid case."

    return Task(sentence_derived, budget)


def decomposition_theorem8(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    '''(--, <(~, T2, T1) --> M>).  (--, <T1 --> M>).   |-  (--, <T2 --> M>).'''
    premise1, premise2 = (task.sentence, belief.sentence) if not inverse_premise else (belief.sentence, task.sentence)

    stamp_task: Stamp = task.stamp
    stamp_belief: Stamp = belief.stamp

    stamp = Stamp_merge(stamp_task, stamp_belief)

    stat1: Statement = premise1.term[0]
    stat2: Statement = premise2.term[0]
    compound: Compound = stat1.subject

    statement = Compound.Negation(Statement(compound - stat2.subject, Copula.Inheritance, stat2.subject))

    if task.is_judgement:
        truth = Truth_deduction(Truth_intersection(premise1.truth, premise2.truth), truth_analytic)
        budget = Budget_forward_compound(statement, truth, budget_tasklink, budget_termlink)
        sentence_derived = Judgement(statement, stamp, truth)
    else: raise "Invalid case."

    return Task(sentence_derived, budget)


def decomposition_theorem9(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    '''
    Original:  (--, (&&, T2, T1)).  T1. |- (--, T2).
    Practical: (&&, T2, T1).        T1. |- T2.
    '''
    premise1, premise2 = (task.sentence, belief.sentence) if not inverse_premise else (belief.sentence, task.sentence)

    stamp_task: Stamp = task.stamp
    stamp_belief: Stamp = belief.stamp

    stamp = Stamp_merge(stamp_task, stamp_belief)

    stat1: Statement = premise1.term
    stat2: Statement = premise2.term
    compound: Compound = stat1

    statement = compound - stat2

    if task.is_judgement:
        truth = Truth_negation(Truth_intersection(Truth_negation(premise1.truth), premise2.truth))
        budget = Budget_forward_compound(statement, truth, budget_tasklink, budget_termlink)
        sentence_derived = Judgement(statement, stamp, truth)
    else: raise "Invalid case."

    return Task(sentence_derived, budget)


def decomposition_theorem10(task: Task, belief: Belief, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False):
    '''
    Original:  (||, T1, T2).    (--, T1).   |-  T2.
    Practical: (||, T1, T2).    T1.         |-  T2.
    '''
    premise1, premise2 = (task.sentence, belief.sentence) if not inverse_premise else (belief.sentence, task.sentence)

    stamp_task: Stamp = task.stamp
    stamp_belief: Stamp = belief.stamp

    stamp = Stamp_merge(stamp_task, stamp_belief)

    stat1: Statement = premise1.term
    stat2: Statement = premise2.term
    compound: Compound = stat1

    statement = compound - stat2

    if task.is_judgement:
        truth = Truth_intersection(premise1.truth, Truth_negation(premise2.truth))
        budget = Budget_forward_compound(statement, truth, budget_tasklink, budget_termlink)
        sentence_derived = Judgement(statement, stamp, truth)
    else: raise "Invalid case."

    return Task(sentence_derived, budget)
