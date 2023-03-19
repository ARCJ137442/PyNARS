'''
这个文件是Sentence类的实现，Sentence类是Narsese语言中的句子类，包括Judgement、Goal、Question和Quest四种类型。其中Judgement和Goal是陈述句，Question和Quest是疑问句。这个文件中还包括了Punctuation和Stamp两个类。

包依赖关系：
    ordered_set：用于实现有序集合
    pynars.Config：用于获取配置信息
    pynars.Global：用于获取全局变量

全局变量名称及其作用：
    无

各类的依赖关系和主要功能：
    Punctuation类：
        依赖：无
        功能：定义了Judgement、Question、Goal和Quest四种标点符号

    Stamp类：
        依赖：Tense类
        功能：定义了一个时间戳，包括创建时间、事件发生时间、放入缓存的时间和证据基

    Sentence类：
        依赖：Truth类、Term类、Punctuation类、Stamp类、copy函数
        功能：定义了一个句子，包括一个Term、一个标点符号和一个时间戳。其中包括了一些属性和方法，如evidential_base、tense、eternalize、__hash__、__str__、__repr__等。

    Judgement类：
        依赖：Truth类、Term类、Stamp类、Sentence类
        功能：定义了一个陈述句，包括一个Term、一个时间戳和一个Truth。其中包括了一些属性和方法，如__str__、repr等。

    Goal类：
        依赖：Truth类、Term类、Stamp类、Sentence类
        功能：定义了一个目标句，包括一个Term、一个时间戳和一个Truth。其中包括了一些属性和方法，如__str__、repr等。

    Question类：
        依赖：Term类、Stamp类、Sentence类
        功能：定义了一个疑问句，包括一个Term、一个时间戳。其中包括了一些属性和方法，如__str__、repr等。

    Quest类：
        依赖：Term类、Stamp类、Sentence类
        功能：定义了一个Quest句，包括一个Term、一个时间戳。其中包括了一些属性和方法，如__str__、repr等。
'''

from copy import copy
from .Truth import Truth
from .Term import Term
from .Statement import Statement
from enum import Enum
from .Tense import Tense
from typing import Type, Set

from ordered_set import OrderedSet
from .Evidence import *

from pynars.Config import Config, Enable  
from pynars import Global 

class Punctuation(Enum):
    Judgement   = r"."
    Question    = r"?"
    Goal        = r"!"
    Quest       = r"@"
    @property
    def is_judgement(self):
        return self == Punctuation.Judgement

    @property
    def is_question(self):
        return self == Punctuation.Question

    @property
    def is_goal(self):
        return self == Punctuation.Goal

    @property
    def is_quest(self):
        return self == Punctuation.Quest

class Stamp:
    
    def __init__(self, t_creation: int, t_occurrence: int, t_put: int, evidential_base: Type['Base'], is_external: bool=True) -> None:
        '''
        Args:
            t_creation(int): creation time of the stamp
            t_occurrence(int): estimated occurrence time of the event
            t_put(int): the time when it was put into buffer
        '''
        self.t_creation = t_creation
        self.t_occurrence = t_occurrence
        self.t_put = t_put
        self.evidential_base: Type['Base'] = evidential_base
        self.is_external = is_external # whether a sentence is from the external world or the internal world. Only those sentences derived from Mental Operations are internal.


    @property
    def tense(self):
        return Tense.Eternal if self.t_occurrence is None else Tense.Future if self.t_occurrence >= Global.time+Config.temporal_duration else Tense.Past if self.t_occurrence <= Global.time-Config.temporal_duration else Tense.Present
    
    @property
    def is_eternal(self):
        return self.t_occurrence is None

    def eternalize(self):
        self.t_occurrence = None

    def extend_evidenital_base(self, base: Type['Base']):
        if self.evidential_base is None:
            if base is None: return
            elif self.evidential_base is None: self.evidential_base = Base(())
        self.evidential_base.extend(base)

    def __str__(self):
        return f'{self.evidential_base}, {self.tense}'

    def __repr__(self):
        return f'<Stamp: {str(self)}>'
'''
Doubt that are Question and Quest have got a tense?
'''

class Sentence:
    truth: Truth = None
    def __init__(self, term: Term, punct: Punctuation, stamp: Stamp, do_hashing: bool=False) -> None:
        ''''''
        self.term = term
        self.word = term.word + str(punct.value)
        self.punct = punct
        self.stamp: Stamp = stamp
    
    @property
    def evidential_base(self):
        return self.stamp.evidential_base

    @property
    def tense(self):
        return self.stamp.tense

    # @property
    # def temporal_order(self):
    #     return self.term.temporal_order

    def eternalize(self, truth: Truth=None):
        sentence = copy(self)
        if truth is not None:
            sentence.truth = truth
        stamp = copy(sentence.stamp)
        stamp.eternalize()
        sentence.stamp = stamp
        return sentence

    def __hash__(self) -> int:
        return hash(self.term)
    
    def __str__(self) -> str:
        return self.word
    
    def __repr__(self) -> str:
        return f'<{"Sentence" if self.is_eternal else "Event"}: {self.term.repr()}{self.punct.value}>'

    # @property
    def repr(self, is_input=True):
        return self.term.repr(is_input)
    
    @property
    def is_judgement(self) -> bool:
        return self.punct == Punctuation.Judgement
    
    @property
    def is_goal(self) -> bool:
        return self.punct == Punctuation.Goal
    
    @property
    def is_question(self) -> bool:
        return self.punct == Punctuation.Question

    @property 
    def is_quest(self) -> bool:
        return self.punct == Punctuation.Quest
    
    @property
    def is_eternal(self) -> bool:
        return self.stamp.is_eternal
    
    @property
    def is_event(self) -> bool:
        return not self.stamp.is_eternal

    @property
    def is_external_event(self) -> bool:
        return not self.is_eternal and self.stamp.is_external



class Judgement(Sentence):
    def __init__(self, term: Term, stamp: Stamp=None, truth: Truth=None) -> None:
        ''''''
        stamp = stamp if stamp is not None else Stamp(Global.time, None, None, None)
        Sentence.__init__(self, term, Punctuation.Judgement, stamp)
        self.truth = truth if truth is not None else Truth(Config.f, Config.c, Config.k)
        
    def __str__(self) -> str:
        return f'{self.word}{(" " + str(self.tense.value)) if self.tense != Tense.Eternal else ""} {self.truth}'


    def repr(self,is_input=False):
        return f'{self.term.repr(is_input)}{self.punct.value}{(" " + str(self.tense.value)) if self.tense != Tense.Eternal else ""} {self.truth}'

class Goal(Sentence):
    def __init__(self, term: Term, stamp: Stamp=None, desire: Truth=None) -> None:
        ''''''
        stamp = stamp if stamp is not None else Stamp(Global.time, None, None, None, None)
        Sentence.__init__(self, term, Punctuation.Goal, stamp)
        self.truth = desire if desire is not None else Truth(Config.f, Config.c, Config.k)
    
    def __str__(self) -> str:
        return f'{self.word}{(" " + str(self.tense.value)) if self.tense != Tense.Eternal else ""} {str(self.truth)}'


    def repr(self, is_input=False):
        return f'{self.term.repr(is_input)+self.punct.value}{(" " + str(self.tense.value)) if self.tense != Tense.Eternal else ""} {str(self.truth)}'

class Question(Sentence):
    answer_best: Sentence = None
    def __init__(self, term: Term, stamp: Stamp=None, curiosiry: Truth=None) -> None:
        ''''''
        stamp = stamp if stamp is not None else Stamp(Global.time, None, None, None, None)
        # stamp.set_eternal()
        Sentence.__init__(self, term, Punctuation.Question, stamp)
        self.is_query = False # TODO: if there is a query variable in the sentence, then `self.is_query=True`
    
    def __str__(self) -> str:
        return f'{self.word}{(" " + str(self.tense.value)) if self.tense != Tense.Eternal else ""}'
        # return self.word + (str(self.tense.value) if self.tense != Tense.Eternal else "")


    def repr(self, is_input=False):
        return f'{self.term.repr(is_input)+self.punct.value}{(" " + str(self.tense.value)) if self.tense != Tense.Eternal else ""}'


class Quest(Sentence):
    def __init__(self, term: Term, stamp: Stamp=None, curiosiry: Truth=None) -> None:
        ''''''
        stamp = stamp if stamp is not None else Stamp(Global.time, None, None, None, None)
        # stamp.set_eternal()
        Sentence.__init__(self, term,  Punctuation.Quest, stamp)
        self.is_query = False # TODO: if there is a query variable in the sentence, then `self.is_query=True`

    def __str__(self) -> str:
        return f'{self.word}{(" " + str(self.tense.value)) if self.tense != Tense.Eternal else ""}'
        # return self.word + (str(self.tense.value) if self.tense != Tense.Eternal else "")

    def repr(self, is_input=False):
        return f'{self.term.repr(is_input)+self.punct.value}{(" " + str(self.tense.value)) if self.tense != Tense.Eternal else ""}'
