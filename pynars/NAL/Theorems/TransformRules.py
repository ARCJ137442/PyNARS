'''
这个文件实现了一些关于转换的通用函数，包括从积到像、从像到积、从像到像。这些函数的实现与参数略有不同，但是都是通用的。

包依赖关系：
    pynars.Narsese.Copula
    pynars.Narsese.Statement
    pynars.Narsese.Compound
    pynars.Narsese.Connector
    pynars.Narsese.Term
    pynars.Narsese.Judgement
    pynars.Narsese.Truth
    pynars.Narsese.Task
    pynars.Narsese.Belief
    pynars.Narsese.Budget
    pynars.Narsese.Stamp
    pynars.Narsese.Goal
    pynars.Narsese.Quest
    pynars.Narsese.Question
    pynars.Narsese.place_holder
    pynars.Narsese._py.Sentence
    ..Functions.TruthValueFunctions
    ..Functions.DesireValueFunctions
    ..Functions.StampFunctions
    ..Functions.BudgetFunctions

全局变量名称及其作用：
    无

各函数的依赖关系和主要功能：
    product_to_image:
        依赖：无
        功能：将积转换为像

    image_to_product:
        依赖：无
        功能：将像转换为积

    image_to_image:
        依赖：无
        功能：将像转换为像
'''

'''Although there are some theorems about transform between product and image, they are highly specialized, which can only handle some special forms or cases, e.g. `equivalence_theorem13()` in `StructuralRules.py`.
In this file, some more generalized functions of transform are implemented, though with a little differences in terms of parameters.
'''
from typing import List
from pynars.Narsese import Copula, Statement, Compound, Connector, Term, Judgement, Truth, Task, Belief, Budget, Stamp, Goal, Quest, Question
from pynars.Narsese import place_holder
from pynars.Narsese._py.Sentence import Sentence

from ..Functions.TruthValueFunctions import *
from ..Functions.DesireValueFunctions import *
from ..Functions.StampFunctions import *
from ..Functions.BudgetFunctions import *


def product_to_image(task: Task, term_concept: Term, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False, index: tuple=None):
    '''
    it should be ensured that `len(index) >= 2`
    e.g. <(&&,<(*,a,b) --> R>,...) ==> C>. |- <(&&,<a --> (/,R,_,b)>,...) ==> C>
    '''
    term_task = task.term
    stat_product: Statement = term_task[index[:-2]] # <(*,a,b) --> R>
    compound_product: Compound = stat_product[index[-2]] # (*,a,b)
    idx_relation = 1-index[-2]
    idx_product = index[-1]
    term_relation = stat_product[idx_relation] # R
    if idx_relation == 0: # intensional image
        predicate = compound_product[idx_product]
        subject = Compound.IntensionalImage(term_relation, compound_product=compound_product, idx=idx_product)
    elif idx_relation == 1: # extensional image
        subject = compound_product[idx_product]
        predicate = Compound.ExtensionalImage(term_relation, compound_product=compound_product, idx=idx_product)
    else: raise "Invalid case."
    stat_image = Statement(subject, stat_product.copula, predicate) # BUG: the statment input should be replaced with `stat_image`, not using the stat_image as the statement output.
    budget = task.budget
    stamp = task.stamp
    # term_task

    if task.is_judgement:
        truth = task.truth
        sentence_derived = Judgement(stat_image, stamp, truth)
    elif task.is_goal:
        truth = task.truth
        sentence_derived = Goal(stat_image, stamp, truth)
    elif task.is_question:
        sentence_derived = Question(stat_image, stamp)
    elif task.is_quest:
        sentence_derived = Quest(stat_image, stamp)
    else: raise "Invalid case."
    
    return Task(sentence_derived, budget)


def image_to_product(task: Task, term_concept: Term, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False, index=None):
    """Created By Cursor.so
    image_to_product(task, term_concept, budget_tasklink=None, budget_termlink=None, inverse_premise=False, inverse_copula=False, index=None)
    
    Transforms a given task into a product of a term and a compound image.
    
    Parameters:
        task (Task): The task to be transformed.
        term_concept (Term): The term concept.
        budget_tasklink (Budget): The budget for the tasklink.
        budget_termlink (Budget): The budget for the termlink.
        inverse_premise (bool): Whether to inverse the premise.
        inverse_copula (bool): Whether to inverse the copula.
        index (int): The index of the compound image.
    
    Returns:
        Task: The transformed task.
    """
    term_task = task.term
    stat_image: Statement = term_task[index[:-2]] # <a --> (/,R,_,b)>
    compound_image: Compound = stat_image[index[-2]] # (/,R,_,b)
    idx_term = 1-index[-2]
    idx_image = index[-1]
    term_relation = compound_image[0] # R
    term = stat_image[1-index[-2]]

    compound_product = Compound.Product(term, compound_image=compound_image)

    if idx_term == 0: 
        subject = compound_product
        predicate = term_relation
    elif idx_term == 1: 
        subject = term_relation
        predicate = compound_product
        
    else: raise "Invalid case."

    stat_image = Statement(subject, stat_image.copula, predicate)
    budget = task.budget
    stamp = task.stamp

    if task.is_judgement:
        truth = task.truth
        sentence_derived = Judgement(stat_image, stamp, truth)
    elif task.is_goal:
        truth = task.truth
        sentence_derived = Goal(stat_image, stamp, truth)
    elif task.is_question:
        sentence_derived = Question(stat_image, stamp)
    elif task.is_quest:
        sentence_derived = Quest(stat_image, stamp)
    else: raise "Invalid case."
    
    return Task(sentence_derived, budget)


def image_to_image(task: Task, term_concept: Term, budget_tasklink: Budget=None, budget_termlink: Budget=None, inverse_premise: bool=False, inverse_copula: bool=False, index=None):
    """Created By Cursor.so
    image_to_image(task, term_concept, budget_tasklink=None, budget_termlink=None, inverse_premise=False, inverse_copula=False, index=None)
    
    Transforms a given task by replacing a term in the task's statement with an image of the given term_concept.
    
    Parameters:
        task (Task): The task to be transformed.
        term_concept (Term): The term to be replaced in the task's statement.
        budget_tasklink (Budget): The budget of the tasklink.
        budget_termlink (Budget): The budget of the termlink.
        inverse_premise (bool): Whether to inverse the premise.
        inverse_copula (bool): Whether to inverse the copula.
        index (list): The index of the term to be replaced.
    
    Returns:
        Task: The transformed task.
    """
    term_task = task.term
    stat_image: Statement = term_task[index[:-2]] # <a --> (/,R,_,b)>
    compound_image: Compound = stat_image[index[-2]] # (/,R,_,b)
    idx_term = 1-index[-2]
    idx_image = index[-1]
    term = stat_image[1-index[-2]]
    term_replaced = compound_image[idx_image]
    compound_image = Compound.Image(term, compound_image, idx_image)
    if idx_term == 0: 
        subject = term_replaced
        predicate = compound_image
    elif idx_term == 1: 
        subject = compound_image
        predicate = term_replaced

    stat_image = Statement(subject, stat_image.copula, predicate)
    budget = task.budget
    stamp = task.stamp

    if task.is_judgement:
        truth = task.truth
        sentence_derived = Judgement(stat_image, stamp, truth)
    elif task.is_goal:
        truth = task.truth
        sentence_derived = Goal(stat_image, stamp, truth)
    elif task.is_question:
        sentence_derived = Question(stat_image, stamp)
    elif task.is_quest:
        sentence_derived = Quest(stat_image, stamp)
    else: raise "Invalid case."
    
    return Task(sentence_derived, budget)