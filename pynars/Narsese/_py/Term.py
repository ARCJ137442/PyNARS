'''
这个文件定义了一个名为Term的类，它是Narsese中的一个基本元素。Term类的实例可以是原子、语句或复合项。Term类的实例可以包含变量，可以是可执行的语句，可以是高阶的。Term类的实例可以被哈希，可以被比较，可以被克隆。Term类的实例可以被序列化，可以被打印。

包依赖关系：
    numpy
    ordered_set
    pynars.Config
    pynars.Narsese._py.Connector
    pynars.Narsese._py.Copula
    typing
    enum
    pynars.utils.IndexVar

全局变量名称及其作用：
    place_holder: 一个占位符，用于哈希。

各函数的依赖关系和主要功能：
    Term.__init__:
        依赖：无
        功能：初始化Term类的实例，包括设置word、word_sorted、_components、_hash_value等属性。
    Term.sub_terms:
        依赖：无
        功能：返回包括self和_components的所有Term类实例。
    Term.components:
        依赖：无
        功能：返回_components属性，即包括self的所有Term类实例。
    Term.count:
        依赖：无
        功能：返回包括self和_components的Term类实例的数量。
    Term.complexity:
        依赖：无
        功能：返回self的复杂度。
    Term.is_statement:
        依赖：无
        功能：判断self是否为语句。
    Term.is_compound:
        依赖：无
        功能：判断self是否为复合项。
    Term.is_atom:
        依赖：无
        功能：判断self是否为原子。
    Term.is_commutative:
        依赖：无
        功能：判断self的组成部分是否可交换。
    Term.is_higher_order:
        依赖：无
        功能：判断self是否为高阶项。
    Term.is_executable:
        依赖：无
        功能：判断self是否为可执行语句。
    Term.terms:
        依赖：无
        功能：返回包括self的所有Term类实例。
    Term.index_var:
        依赖：无
        功能：返回self的IndexVar实例。
    Term.is_mental_operation:
        依赖：无
        功能：判断self是否为心理操作。
    Term.identical:
        依赖：无
        功能：判断self和o是否相同。
    Term.equal:
        依赖：无
        功能：判断self和o是否相等。
    Term.has_common:
        依赖：无
        功能：判断term是否与self有公共部分，如果same_term为True，则term与self相同时也返回True。
    Term.__hash__:
        依赖：无
        功能：返回self的哈希值。
    Term.__eq__:
        依赖：Term.identical
        功能：判断self和o是否相同。
    Term.__contains__:
        依赖：无
        功能：判断term是否在self的子项中。
    Term.__str__:
        依赖：无
        功能：返回self的字符串表示。
    Term.__repr__:
        依赖：无
        功能：返回self的字符串表示，用于调试。
    Term.__len__:
        依赖：无
        功能：返回self的子项数量。
    Term.__getitem__:
        依赖：无
        功能：返回self的第一个子项。
    Term.repr:
        依赖：Term.repr_with_var
        功能：返回self的字符串表示，如果self包含变量，则使用Term.repr_with_var。
    Term.repr_with_var:
        依赖：无
        功能：返回self的字符串表示，包括变量。
    Term.handle_variables:
        依赖：无
        功能：处理self的变量信息。
    Term.handle_index_var:
        依赖：Term.handle_variables
        功能：处理self的IndexVar实例。
    Term.clone:
        依赖：无
        功能：返回self的克隆。
'''

from pynars.Narsese._py.Connector import Connector
from .Copula import Copula
from pynars.Config import Enable
from typing import Iterable, List, Set, Type
from enum import Enum
from pynars.utils.IndexVar import IndexVar
from numpy import prod
from ordered_set import OrderedSet
# from pynars.utils.tools import find_pos_with_pos, find_var_with_pos
from copy import copy, deepcopy

class TermType(Enum):
    ATOM = 0
    STATEMENT = 1
    COMPOUND = 2

class Term:

    type = TermType.ATOM
    copula: Copula = None
    connector: Connector = None
    _complexity: float = 1.0 # The complexity of the term. Read only.
    has_var: bool = False # Whether the term contains variable(s).
    has_ivar: bool = False # Whether the term contains independent variable(s).
    has_dvar: bool = False # Whether the term contains dependent variable(s).
    has_qvar: bool = False # Whether the term contains query variable(s).
    is_var: bool = False
    is_ivar: bool = False
    is_dvar: bool = False
    is_qvar: bool = False
    is_closed: bool = True # Whether the term is closed or open in terms of variable.

    is_interval: bool = False

    is_operation = False 
    _index_var: IndexVar = None
    
    def __init__(self, word, do_hashing=False, word_sorted=None, is_input=False) -> None:
        self.word = word
        self.word_sorted = word_sorted if word_sorted is not None else word
        self._components: Set[Term] = None

        if Enable.variable:
            if self._index_var is None: self._index_var = IndexVar()

        if do_hashing:
            self.do_hashing()
        else:
            self._hash_value = None
        

    @property
    def sub_terms(self) -> Set[Type['Term']]:
        return (self, *self._components) if self._components is not None else set((self, ))

    @property
    def components(self) ->Set[Type['Term']]:
        return self._components
    

    def count(self):
        '''the number of sub-terms (including this term itself)'''
        return len(self._components)+1 if self._components is not None else 1

    # @property
    # def temporal_order(self):
    #     return TemporalOrder.NONE

    @property
    def complexity(self):
        return self._complexity

    @property
    def is_statement(self):
        return self.type == TermType.STATEMENT
    
    @property
    def is_compound(self):
        return self.type == TermType.COMPOUND
    
    @property
    def is_atom(self):
        return self.type == TermType.ATOM

    @property
    def is_commutative(self):
        '''whether the components of the term is commutative'''
        return False
    
    @property
    def is_higher_order(self):
        '''whether the term is higher-ordered'''
        return False

    @property
    def is_executable(self):
        return self.is_statement and self.is_operation

    @property
    def terms(self):
        return (self, )

    @property
    def index_var(self):
        return self._index_var
    
    @property
    def is_mental_operation(self):
        return False

    def identical(self, o: Type['Term']) -> bool:
        return hash(o) == hash(self) # and hash(o.index_var) == hash(self.index_var)

    def equal(self, o: Type['Term']) -> bool:
        '''
        Return:
            is_equal (bool), is_replacable(bool)
        '''
        
        if o.is_atom:
            if self.is_var ^ o.is_var: # one of them is variable, while the other is not
                return True
            elif self.is_var and o.is_var: # the two are both variables
                if (self.is_ivar and o.is_ivar) or (self.is_dvar and o.is_dvar) or (self.is_qvar and o.is_qvar): # the two, to be equal, should be the same type of variable 
                    return True
                else: 
                    return False, False
            elif not self.is_var and not o.is_var: # the two are neither variables:
                return self.identical(o)
        elif (o.is_compound or o.is_statement) and self.is_var:
            return True
        else: return False

    def has_common(self, term: Type['Term'], same_term: bool=True) -> bool:
        if not term.is_atom: return False
        return self == term

    def do_hashing(self):
        self._hash_value = hash(self.word_sorted+str(self.index_var.postions_normalized))
        return self._hash_value

    def __hash__(self) -> int:
        return self._hash_value if self._hash_value is not None else self.do_hashing()
    
    def __eq__(self, o: Type['Term']) -> bool:
        return self.identical(o)

    def __contains__(self, term: Type['Term']) -> bool:
        return term in self.sub_terms

    def __str__(self) -> str:
        return self.word
    
    def __repr__(self) -> str:
        return f'<Term: {str(self)}>'
    
    def __len__(self):
        return len(self._components)

    def __getitem__(self, index: List[int]) -> Type['Term']:
        if len(index) > 0 or not (len(index)==0 or index[0]== 0 or index[0] == -1): raise "Out of bounds."
        return self

    def repr(self, is_input=False):
        return str(self) if not self.has_var else self.repr_with_var(self.index_var, [])

    def repr_with_var(self, index_var: IndexVar, pos: list):
        ''''''
        # raise "Invalid case."
        return str(self)

    def handle_variables(self, terms: Iterable['Term']):
        ''''''
        self.has_var = bool(sum(tuple(term.has_var for term in terms)))
        self.has_ivar = bool(sum(tuple(term.has_ivar for term in terms)))
        self.has_dvar = bool(sum(tuple(term.has_dvar for term in terms)))
        self.has_qvar = bool(sum(tuple(term.has_qvar for term in terms)))

    def handle_index_var(self, terms: Iterable['Term'], is_input: bool):
        if self.index_var is None: self._index_var = IndexVar()
        self.handle_variables(terms)
        
        indices_var_to_merge = []
        for i, component in enumerate(terms):
            if component.is_atom and component.is_var: 
                if component.is_ivar: self.index_var.add_ivar([i], name=repr(component))
                elif component.is_dvar: self.index_var.add_dvar([i], name=repr(component))
                elif component.is_qvar: self.index_var.add_qvar([i], name=repr(component))
            elif component.has_var: # but component itself is not variable
                if component.has_ivar:
                    for index in component.index_var.positions_ivar:
                        self.index_var.add_ivar([i]+index)
                if component.has_dvar:
                    for index in component.index_var.positions_dvar:
                        self.index_var.add_dvar([i]+index)
                if component.has_qvar:
                    for index in component.index_var.positions_qvar:
                        self.index_var.add_qvar([i]+index)
                indices_var_to_merge.append(component.index_var)
        self.index_var.merge(*indices_var_to_merge, is_input=is_input)
        self.index_var.normalize()

    def clone(self):
        # clone = copy(self)
        return self
        

place_holder = Term('_', True)