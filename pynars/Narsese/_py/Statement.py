'''
这个文件定义了一个名为Statement的类，它是Term的子类，表示一个语句。Statement类有多个方法，包括__init__、__getitem__、equal、has_common、__repr__、repr_with_var、Inheritance、Implication、Similarity、Equivalence、PredictiveImplication、ConcurrentImplication、RetrospectiveImplication、PredictiveEquivalence、ConcurrentEquivalence和clone。Statement类的实例可以表示一个语句，包括主语、谓语和谓词。Statement类的实例可以进行比较、克隆等操作。

包依赖关系：
    - copy
    - enum
    - lib2to3.pgen2.tokenize
    - pynars.Config
    - pynars.utils.IndexVar
    - pynars.Narsese._py.Term
    - pynars.Narsese._py.Copula
    - typing
    - ordered_set

全局变量名称及其作用：
    - Enable: 一个类，表示NARS系统的配置。包括是否启用变量、是否启用时间等。

各函数的依赖关系和主要功能：
    - __init__:
        依赖：Term、Copula、OrderedSet
        功能：初始化一个Statement实例。
    - __getitem__:
        依赖：无
        功能：获取Statement实例的子项。
    - equal:
        依赖：无
        功能：比较两个Statement实例是否相等。
    - has_common:
        依赖：无
        功能：判断两个Statement实例是否有公共部分。
    - __repr__:
        依赖：无
        功能：返回Statement实例的字符串表示。
    - repr_with_var:
        依赖：无
        功能：返回Statement实例的字符串表示，包括变量。
    - Inheritance:
        依赖：__init__
        功能：创建一个表示继承关系的Statement实例。
    - Implication:
        依赖：Term、Copula
        功能：创建一个表示蕴含关系的Statement实例。
    - Similarity:
        依赖：Term、Copula
        功能：创建一个表示相似关系的Statement实例。
    - Equivalence:
        依赖：Term、Copula
        功能：创建一个表示等价关系的Statement实例。
    - PredictiveImplication:
        依赖：Term、Copula
        功能：创建一个表示预测蕴含关系的Statement实例。
    - ConcurrentImplication:
        依赖：Term、Copula
        功能：创建一个表示并发蕴含关系的Statement实例。
    - RetrospectiveImplication:
        依赖：Term、Copula
        功能：创建一个表示回顾蕴含关系的Statement实例。
    - PredictiveEquivalence:
        依赖：Term、Copula
        功能：创建一个表示预测等价关系的Statement实例。
    - ConcurrentEquivalence:
        依赖：Term、Copula
        功能：创建一个表示并发等价关系的Statement实例。
    - clone:
        依赖：copy
        功能：克隆一个Statement实例。
'''

from copy import copy
import enum
from lib2to3.pgen2.tokenize import StopTokenizing
from pynars.Config import Enable
from pynars.utils.IndexVar import IndexVar
from .Term import Term, TermType
from .Copula import Copula
from typing import List, Type
# from .Compound import *f
from ordered_set import OrderedSet

class Statement(Term):
    type = TermType.STATEMENT
    
    def __init__(self, subject: Term, copula: Copula, predicate: Term, is_input: bool=False) -> None:
        self._is_commutative = copula.is_commutative
        word = "<"+str(subject)+str(copula.value)+str(predicate)+">"
        if self.is_commutative:
            subject_word, predicate_word = sorted((subject, predicate), key=hash)
            word_sorted = "<"+subject_word.word_sorted+str(copula.value)+predicate_word.word_sorted+">"
        else: word_sorted = "<"+subject.word_sorted+str(copula.value)+predicate.word_sorted+">"
        super().__init__(word, word_sorted=word_sorted)

        self.subject = subject
        self.copula = copula
        self.predicate = predicate

        self._components = OrderedSet((*self.subject.sub_terms, *self.predicate.sub_terms))
        self._complexity += (subject.complexity + predicate.complexity)
        self._is_higher_order = copula.is_higher_order

        self.is_operation = self.predicate.is_operation

        if Enable.variable:
            self.handle_index_var((self.subject, self.predicate), is_input)

        pass
        
    def __getitem__(self, index: List[int]) -> Term:
        if isinstance(index, int): index = (index,)
        if len(index) == 0: return self
        
        idx = index[0]
        if idx > 1: raise "Out of bounds."

        index = index[1:]
        term = self.subject if idx == 0 else self.predicate
        return term.__getitem__(index)

    @property
    def is_commutative(self):
        return self._is_commutative
    
    @property
    def is_higher_order(self):
        return self._is_higher_order

    @property
    def terms(self):
        return (self.subject, self.predicate)

    def equal(self, o: Type['Statement']) -> bool:
        '''
        Return:
            is_equal (bool), is_replacable(bool)
        '''

        if o.is_statement:
            if not self.copula is o.copula: return False

            if self.subject.equal(o.subject) and self.predicate.equal(o.predicate): return True
            elif not o.is_commutative: return False
            else: return self.subject.equal(o.predicate) and self.predicate.equal(o.subject)

        elif o.is_atom and o.is_var:
            return True
        else: return False
            

    def has_common(self, statement: Type['Statement'], same_copula: bool=True) -> bool:
        if not statement.is_statement: return False
        return ((statement.copula is self.copula) if same_copula else True) and (not {self.subject, self.predicate}.isdisjoint({statement.subject, statement.predicate}))


    def __repr__(self) -> str:
        return  f'<Statement: {self.repr()}>'
    
    def repr_with_var(self, index_var: IndexVar, pos: list):
        '''
        index_var (IndexVar): the `index_var` of the root/topmost term.
        pos (list): the position of the current term within the root/topmost term.
        '''
        word_subject = str(self.subject) if not self.subject.has_var else self.subject.repr_with_var(index_var, pos+[0])
        word_predicate = str(self.predicate) if not self.predicate.has_var else self.predicate.repr_with_var(index_var, pos+[1])
        
        return f'<{word_subject+str(self.copula.value)+word_predicate}>'

    @classmethod
    def Inheritance(cls, subject: Term, predicate: Term, is_input: bool=False):
        return cls(subject, Copula.Inheritance, predicate, is_input)
    
    
    @classmethod
    def Implication(cls, subject: Term, predicate: Term, is_input: bool=False):
        return cls(subject, Copula.Implication, predicate, is_input)


    @classmethod
    def Similarity(cls, subject: Term, predicate: Term, is_input: bool=False):
        return cls(subject, Copula.Similarity, predicate, is_input)

    
    @classmethod
    def Equivalence(cls, subject: Term, predicate: Term, is_input: bool=False):
        return cls(subject, Copula.Equivalence, predicate, is_input)


    @classmethod
    def PredictiveImplication(cls, subject: Term, predicate: Term, is_input: bool=False):
        return cls(subject, Copula.PredictiveImplication, predicate, is_input)


    @classmethod
    def ConcurrentImplication(cls, subject: Term, predicate: Term, is_input: bool=False):
        return cls(subject, Copula.ConcurrentImplication, predicate, is_input)


    @classmethod
    def RetrospectiveImplication(cls, subject: Term, predicate: Term, is_input: bool=False):
        return cls(subject, Copula.RetrospectiveImplication, predicate, is_input)


    @classmethod
    def PredictiveEquivalence(cls, subject: Term, predicate: Term, is_input: bool=False):
        return cls(subject, Copula.PredictiveEquivalence, predicate, is_input)


    @classmethod
    def ConcurrentEquivalence(cls, subject: Term, predicate: Term, is_input: bool=False):
        return cls(subject, Copula.ConcurrentEquivalence, predicate, is_input)

    def clone(self):
        if not self.has_var: return self
        # now, not self.has_var
        clone = copy(self)
        clone.subject = self.subject.clone()
        clone.predicate = self.predicate.clone()
        clone._index_var = self._index_var.clone()
        
        return clone
