'''
这个文件定义了Variable类，它是Term类的子类，表示Narsese中的变量。Variable类有三种前缀：Independent、Dependent和Query，分别对应独立变量、依赖变量和查询变量。Variable类的实例可以用于表示Narsese中的变量，例如"$x"、"#y"和"?z"。

包依赖关系：
    - copy
    - enum
    - typing
    - pynars.Config
    - pynars.utils.IndexVar
    - pynars.Narsese._py.Term

全局变量名称及其作用：
    - VarPrefix: 枚举类型，表示Variable类的前缀。
    - Variable.is_var: 类属性，表示Variable类的实例是否为变量。
    - Variable.has_var: 类属性，表示Variable类的实例是否包含变量。
    - Variable.prefix: 实例属性，表示Variable类的实例的前缀。
    - Variable.name: 实例属性，表示Variable类的实例的名称。
    - Variable.dependents: 实例属性，表示Variable类的实例的依赖变量。
    - Variable.is_ivar: 实例属性，表示Variable类的实例是否为独立变量。
    - Variable.has_ivar: 实例属性，表示Variable类的实例是否包含独立变量。
    - Variable.is_dvar: 实例属性，表示Variable类的实例是否为依赖变量。
    - Variable.has_dvar: 实例属性，表示Variable类的实例是否包含依赖变量。
    - Variable.is_qvar: 实例属性，表示Variable类的实例是否为查询变量。
    - Variable.has_qvar: 实例属性，表示Variable类的实例是否包含查询变量。

各函数的依赖关系和主要功能：
    - __init__:
        依赖：Term.__init__
        功能：初始化Variable类的实例。
    - __repr__:
        依赖：无
        功能：返回Variable类的实例的字符串表示。
    - repr_with_var:
        依赖：无
        功能：返回Variable类的实例的字符串表示，包含变量的值。
    - Independent:
        依赖：无
        功能：创建一个独立变量的Variable类的实例。
    - Dependent:
        依赖：无
        功能：创建一个依赖变量的Variable类的实例。
    - Query:
        依赖：无
        功能：创建一个查询变量的Variable类的实例。
    - clone:
        依赖：copy.deepcopy
        功能：创建Variable类的实例的深拷贝。
'''

from copy import copy, deepcopy
from enum import Enum
from typing import Type
from pynars.Config import Config

from pynars.utils.IndexVar import IndexVar
from .Term import Term

class VarPrefix(Enum):
    Independent = "$"
    Dependent = "#"
    Query = "?"


class Variable(Term):
    is_var: bool = True
    has_var: bool = True
    
    def __init__(self, prefix: VarPrefix, word: str, do_hashing=False, is_input=False) -> None:
        self.prefix = prefix
        self.name = str(word)
        word = prefix.value
        super().__init__(word, do_hashing=do_hashing)
        self.dependents = [] # only for dependent variable. TODO: implement son classes of Variable, including DependentVar, IndependentVar, QueryVar.
        # self.has_variable: bool = True

        self.is_ivar = self.has_ivar = self.prefix == VarPrefix.Independent
        self.is_dvar = self.has_dvar = self.prefix == VarPrefix.Dependent
        self.is_qvar = self.has_qvar = self.prefix == VarPrefix.Query
    

    def __repr__(self) -> str:
        # return f'<Variable: {self.repr}>'
        return self.word + self.name


    # @property
    # def repr(self):
    #     return self.word + self.name

    def repr_with_var(self, index_var: IndexVar, pos: list):
        ''''''
        if not self.is_var: raise "Invalide case."
        if self.is_ivar:
            try: idx = index_var.positions_ivar.index(pos)
            except: raise "Invalid case: The `pos` is not in `index_var.positions_ivar`"
            var = index_var.postions_normalized[0][idx] if Config.variable_repr_normalized else index_var.var_independent[idx]
        elif self.is_dvar:
            try: idx = index_var.positions_dvar.index(pos)
            except: raise "Invalid case: The `pos` is not in `index_var.positions_dvar`"
            var = index_var.postions_normalized[1][idx] if Config.variable_repr_normalized else index_var.var_dependent[idx]
        elif self.is_qvar:
            try: idx = index_var.positions_qvar.index(pos)
            except: raise "Invalid case: The `pos` is not in `index_var.positions_qvar`"
            var = index_var.postions_normalized[2][idx] if Config.variable_repr_normalized else index_var.var_query[idx]
        else: raise "Invalide case."
        prefix = self.prefix.value
            
        return prefix + str(var)


    @classmethod
    def Independent(cls, word: str, do_hashing=False, is_input=False):
        return Variable(VarPrefix.Independent, word, do_hashing, is_input)


    @classmethod
    def Dependent(cls, word: str, do_hashing=False, is_input=False):
        return Variable(VarPrefix.Dependent, word, do_hashing, is_input)


    @classmethod
    def Query(cls, word: str, do_hashing=False, is_input=False):
        return Variable(VarPrefix.Query, word, do_hashing, is_input)

    
    def clone(self) -> Type['Variable']:
        clone = copy(self)
        clone._index_var = deepcopy(self._index_var)
        return clone