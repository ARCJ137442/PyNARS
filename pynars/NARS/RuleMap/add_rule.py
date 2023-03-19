'''
这个文件是RuleMap的一个实现，它提供了一个add_rule函数，用于将规则添加到SparseLUT中。SparseLUT是一个稀疏的多维数组，它可以用于高效地存储和查询规则。此外，这个文件还提供了一些辅助函数，用于判断两个Term是否有公共部分，以及判断两个Statement是否有公共Term等。

包依赖关系：
    numpy
    pynars.Config
    pynars.Narsese
    pynars.Narsese._py
    pynars.Narsese._py.Connector
    pynars.Narsese._py.Sentence
    pynars.Narsese._py.Statement
    pynars.Narsese._py.Term
    pynars.NAL.Inference
    sparse_lut
    pynars.utils.tools
    sty

全局变量名称及其作用：
    _class_convert: 将Judgement, Goal, Question, Quest转换为数字的字典
    CommonId: 用于表示两个Term的公共部分
    add_rule: 将规则添加到SparseLUT中的函数
    _compound_has_common: 判断两个Term是否有公共部分的函数
    _compound_at: 判断一个Term是否在一个Compound中的函数
    _at: 判断一个Term是否在一个Compound中的函数
    _common: 判断两个Statement是否有公共Term的函数

各函数的依赖关系和主要功能：
    task_type_id:
        依赖：Task
        功能：将Task转换为数字
    class_sentence_to_list:
        依赖：无
        功能：将Judgement, Goal, Question, Quest转换为数字列表
    _compound_has_common:
        依赖：Term, Compound, Statement
        功能：判断两个Term是否有公共部分
    _compound_at:
        依赖：Term, Compound, Statement, Connector, _compound_has_common
        功能：判断一个Term是否在一个Compound中
    _at:
        依赖：Compound, Statement, Term
        功能：判断一个Term是否在一个Compound中
    _common:
        依赖：Statement, Statement
        功能：判断两个Statement是否有公共Term
    add_rule:
        依赖：SparseLUT, OrderedDict, List[RuleCallable]
        功能：将规则添加到SparseLUT中
'''

from operator import imod
import os 
from pathlib import Path
from inspect import getmembers, isfunction
import importlib
import re
from typing import Any, List, Tuple, Union
from typing_extensions import Protocol
from collections import OrderedDict

from numpy import product

from pynars.Config import Enable
from pynars.NARS.RuleMap.Interface import Interface_CompositionalRules, Interface_SyllogisticRules, Interface_DecompositionalRules, Interface_TransformRules, Interface_ConditionalRules, Interface_TemporalRules
from pynars.Narsese import Copula, Task
from pynars.Narsese._py.Connector import Connector
from pynars.Narsese._py.Sentence import Goal, Judgement, Quest, Question
from pynars.Narsese._py.Statement import Statement
from pynars.Narsese._py.Term import Term
from pynars.Narsese import Belief, Term, Truth, Compound, Budget
from ..DataStructures import LinkType, TaskLink, TermLink
from pynars.NAL.Inference import *
from sparse_lut import SparseLUT
from pynars.utils.tools import get_size

from pynars.utils.Print import out_print, PrintType

import time
from datetime import datetime
import pickle
import sty
# from ._extract_feature import extract_feature, _compound_has_common, _compound_at
from pynars import Global

class RuleCallable(Protocol):
    def __call__(self, 
        task: Task, 
        belief: Belief, 
        budget_tasklink: Budget=None, 
        budget_termlink: Budget=None
    ) -> Tuple[Task, Tuple[Budget, float, float]]: ...

class RuleMapCallable(Protocol):
    def __call__(self, 
        task: Task, 
        term_belief: Union[Statement, Term],
        truth_belief: Union[Truth, None], 
        task_link: TaskLink, 
        term_link: TermLink
    ) -> List[RuleCallable]: ...


def task_type_id(task: Task):
    if task.is_judgement: return 0
    elif task.is_goal: return 1
    elif task.is_question: return 2
    elif task.is_quest: return 3
    else: raise "Invalid case."

_class_convert = {
    Judgement: 0,
    Goal: 1,
    Question: 2,
    Quest: 3
}
def class_sentence_to_list(*types):
    if isinstance(types, list): types = [types]
    return [_class_convert[t] for t in types]
    
    
class CommonId:
    def __init__(self, first, second=None) -> None:
        self.first = first
        self.second = second

    def __int__(self):
        return self.first*2 + self.second if self.second is not None else self.first


def _compound_has_common(term1: Union[Term, Compound, Statement], term2: Union[Term, Compound, Statement]):
    if term1.is_compound:
        return (term2 in term1.terms) or term1.has_common(term2)
    elif term2.is_compound:
        return (term1 in term2.terms) or term1.has_common(term2)
    else: return False

def _compound_at(term1: Union[Term, Compound, Statement], term2: Compound, compound_has_common: bool=None):
    if term2.is_compound:
        if not term1.is_compound: 
            if term2.connector is Connector.SequentialEvents: 
                return term2.terms[0] == term1
            else: 
                return term2.contains(term1)
        else: 
            empty = True if len(term2.terms - term1.terms) == 0 else False
            if term2.connector is Connector.SequentialEvents: 
                return (not empty) and term2.terms[:len(term1.terms)] == term1.terms
            else: 
                return (not empty) and (compound_has_common if compound_has_common is not None else _compound_has_common(term1, term2))
    else: return False
    
def _at(compound: Union[Compound, Statement], term: Term):
    '''
    To judge whether the `component` is in the `compound`.

    e.g. A@(&&,A,B), then return (True, 0); 
        B@(&&,A,B), then return (True, 1); 
        C@(&&,A,B), then return (False, None)
    '''
    if compound.is_atom:
        return (False, None)
    else:
        if compound.is_compound:
            terms = compound
        elif compound.is_statement:
            terms = (compound.subject, compound.predicate)
        else: raise "Invalid case."

        for i, component in enumerate(terms):
            if component == term:
                return (True, i)
        else:
            return (False, None)
    

def _common(premise1: Statement, premise2: Statement):
    '''
    To judge whether the `premise1` and the `premise2` have common term.

    e.g. <S-->M>, <M-->P>, then return (True, 1, 0);
        <M-->P>, <S-->M>, then return (True, 0, 1);
        <M-->P>, <M-->S>, then return (True, 0, 0);
        <P-->M>, <S-->M>, then return (True, 1, 1);
        <A==>B>, A, then return (True, 0, 0)
        <A==>B>, B, then return (True, 1, 0)

        <A==><B-->C>>, <B-->C>
        <A==>(&, B, C)>, (&, B, C)
        <A==>(&, B, C, D)>, (&, B, C)
        <A-->(|, B, C), <A-->C> |- <A-->B>
        <(&, A, B)-->(|, C, D), <(&, A, B)-->D> |- <(&, A, B)-->C>

    Return:
        has_common_id (bool), common_id_task (int), common_id_belief (int), match_reverse (bool)
    '''
    if premise1.is_statement and premise2.is_statement:
        if premise1.subject == premise2.predicate and premise1.predicate == premise2.subject:
            return True, None, None, True
        if premise1.subject == premise2.subject:
            return True, 0, 0, False
        elif premise1.subject == premise2.predicate:
            return True, 0, 1, False
        elif premise1.predicate == premise2.subject:
            return True, 1, 0, False
        elif premise1.predicate == premise2.predicate:
            return True, 1, 1, False
        else:
            return False, None, None, False
    elif premise1.is_statement and premise2.is_atom:
        if premise1.subject == premise2:
            return True, 0, 0, False
        elif premise1.predicate == premise2:
            return True, 1, 0, False
        else:
            return False, None, None, False
    elif premise2.is_statement and premise1.is_atom:
        if premise2.subject == premise1:
            return True, 0, 0, False
        elif premise2.predicate == premise1:
            return True, 0, 1, False
        else:
            return False, None, None, False
    else:
        return False, None, None, False




def add_rule(sparse_lut: SparseLUT, structure: OrderedDict, rules: List[RuleCallable],**kwargs):
        ''''''
        indices = [kwargs.get(key, None) for key in structure.keys()]

        # convert the indices into a normalized form.
        indices_norm = []
        values = iter(structure.values())
        for index in indices:
            _type, _cnt_type = next(values)
            # if index is Ellipsis or index is None: index = None
            if index is Any: pass
            elif index is None: pass
            elif isinstance(index, tuple): 
                assert 0 < len(index) <= 3, "It shouldn't be bigger than 3, and shouldn't be 0."
                _index = index
                index = []
                for i, idx in enumerate(_index):
                    if i < 2: assert isinstance(idx, _type), "It should be the type identified in `self.structure_map`"
                    idx = int(idx)
                    if i < 2: assert idx < _cnt_type, "It shouldn't be bigger than the maximum index of the type."
                    index.append(index)
                index = slice(*index)
            elif isinstance(index, slice): pass
            elif isinstance(index, list): 
                _index = index
                index = []
                for idx in _index:
                    assert idx is None or isinstance(idx, _type), "It should be the type identified in `self.structure_map`"
                    idx = int(idx) if idx is not None else idx
                    assert (idx if idx is not None else 0) < _cnt_type , "It shouldn't be bigger than the maximum index of the type."
                    index.append(idx)
            else: 
                assert isinstance(index, _type), f"The `{index}` should be the type identified in `self.structure_map`"
                index = int(index)
                assert index < _cnt_type, "It shouldn't be bigger than the maximum index of the type."
            indices_norm.append(index)
        indices = tuple(indices_norm)
        
        # add the rule to the map
        if not(isinstance(rules, tuple) or isinstance(rules, list)):
            rules = (rules,)
        for rule in rules:            
            sparse_lut.add(list(indices), rule)
        return indices