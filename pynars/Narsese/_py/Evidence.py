'''
这个文件包含了Evidential Base类，它是一个证据库的基类，用于存储证据。此外，还包含了interleave函数，用于将两个证据库合并。


包依赖关系：
    - ordered_set: 用于实现有序集合
    - pynars.Narsese._py.Truth: 用于实现Truth类
    - pynars.Narsese._py.Term: 用于实现Term类
    - pynars.Narsese._py.Statement: 用于实现Statement类
    - pynars.Narsese._py.Tense: 用于实现Tense类
    - typing: 用于类型提示
    - pynars.Config: 用于读取配置文件
    - pynars.Global: 用于读取全局变量


全局变量名称及其作用：
    - Config: 用于读取配置文件
    - Global: 用于读取全局变量


各函数的依赖关系和主要功能：
    - Base:
        依赖：ordered_set, pynars.Narsese._py.Truth, pynars.Narsese._py.Term, pynars.Narsese._py.Statement, pynars.Narsese._py.Tense, typing, pynars.Config, pynars.Global
        功能：Evidential Base类，用于存储证据。
    - Base.interleave:
        依赖：无
        功能：将两个证据库合并。
    - Base.add:
        依赖：无
        功能：向证据库中添加证据。
    - Base.extend:
        依赖：无
        功能：将另一个证据库中的证据添加到当前证据库中。
    - Base.is_overlaped:
        依赖：无
        功能：检查另一个证据库是否与当前证据库重叠。
    - Base.do_hashing:
        依赖：无
        功能：计算证据库的哈希值。
    - Base.__eq__:
        依赖：无
        功能：判断两个证据库是否相等。
    - Base.__or__:
        依赖：无
        功能：将两个证据库合并。
    - Base.__ior__:
        依赖：无
        功能：将另一个证据库中的证据添加到当前证据库中。
    - Base.__hash__:
        依赖：无
        功能：计算证据库的哈希值。
    - Base.__len__:
        依赖：无
        功能：返回证据库中证据的数量。
    - Base.__repr__:
        依赖：无
        功能：返回证据库的字符串表示形式。

'''
# from pynars.Narsese._py.Task import Task
from .Truth import Truth
from .Term import Term
from .Statement import Statement
from enum import Enum
from .Tense import Tense
from typing import Tuple, Type, Set, List, Union

from ordered_set import OrderedSet
# from .Evidence import Base
# from .Task import *

from pynars.Config import Config, Enable
from pynars import Global 

# class Evidence:
#     def __init__(self, task) -> None:
#         self._hash_task = hash(task)
#         self._input_id = task.input_id
    
#     def __eq__(self, evidence: Type['Evidence']):
#         return (self._hash_task==evidence._hash_task) and (self._input_id==evidence._input_id)

class Base:
    '''Evidential Base'''
    def __init__(self, terms: Tuple[int]=tuple()) -> None:
        # TODO: DOUBT --
        # IF `<A-->B>.`, `<B-->C>.`, `<C--D>.`, THEN it can be derived in a single that `<A-->C>.`, `<B-->D>.`.
        # In the second step, it can be derived that `{<A-->B>. <B-->D>.} |- (1) <A-->D>.`, and `{<A-->C>. <C-->D>.} |- (2) <A-->D>.`
        # Is it reasonable theoretically to apply revision rules between (1) and (2)?

        self._set: Set[int] = OrderedSet(terms)
        self._hash = None
    
    @classmethod
    def interleave(self, base1, base2) -> Type['Base']:
        '''interleave two bases'''
        # TODO: DOUBT --
        # What if some evidence is lost (because of forgetting)?

        # TODO: DOUBT --
        # Is the base ordered? What kind of evidence should overflow?
        

        # TODO: Ref: OpenNARS 3.1.0 Stamp.java line 178~187.
        # TODO: Optimize this loop with cython (with python-style).
        # while (j < baseLength) {
        #     if(i2 < secondLength) {
        #         evidentialBase[j++] = secondBase[i2++];
        #     }
        #     if(i1 < firstLength) {
        #         evidentialBase[j++] = firstBase[i1++];
        #     }
        # }

    def add(self, id_evidence: int):
        self._hash = None
        self._set.add(id_evidence)
        return self
    
    def extend(self, base: Union[Type['Base'] , None]):
        self._hash = None
        self._set = self._set.union(base._set)
        return self

    def is_overlaped(self, base: Union[Type['Base'], None]) -> bool:
        ''' Check whether another `Base` object is overlapped with `self`.
        Complexity: O(N) N=min(len(self), len(o))
        '''
        return not self._set.isdisjoint(base._set) if base is not None else False
    
    def do_hashing(self):
        self._hash = hash(frozenset(self._set))
        return self._hash

    def __eq__(self, o: Type['Base']) -> bool:
        # TODO: Ref: OpenNARS 3.1.0 Stamp.Java line 334~335, 346~349, 461~516
        if id(o) == id(self):
            return True
        elif hash(self) != hash(o):
            return False
        return self._set == o._set
    
    def __or__(self, base: Type['Base']) -> Type['Base']:
        return Base(self._set | base._set)

    def __ior__(self, base: Type['Base']) -> Type['Base']:
        self._hash = None
        self._set |= base._set
        return self

    def __hash__(self) -> int:
        return self._hash if self._hash is not None else self.do_hashing()

    def __len__(self) -> int:
        return len(self._set)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({len(self._set)})"
