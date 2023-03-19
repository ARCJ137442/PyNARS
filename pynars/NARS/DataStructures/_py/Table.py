'''
这个文件是用于实现`Table`类的，该类用于在`Concept`中实现信念表、欲望表等。

包依赖关系：
    typing.Union
    depq.DEPQ
    pynars.Narsese.Task
    pynars.Narsese.Belief

全局变量名称及其作用：
    无

各函数的依赖关系和主要功能：
    __init__:
        依赖：DEPQ
        功能：初始化一个DEPQ对象作为Table的_table属性
    add:
        依赖：无
        功能：向Table中添加一个Task对象和一个float类型的概率值
    empty:
        依赖：无
        功能：判断Table是否为空
    first:
        依赖：无
        功能：返回Table中的第一个元素
    last:
        依赖：无
        功能：返回Table中的最后一个元素
    __iter__:
        依赖：无
        功能：返回一个迭代器，用于遍历Table中的元素
    values:
        依赖：__iter__
        功能：返回Table中所有元素的值
    items:
        依赖：无
        功能：返回Table中所有元素的键值对
    keys:
        依赖：无
        功能：返回Table中所有元素的键
    __getitem__:
        依赖：无
        功能：返回Table中指定索引的元素
    __len__:
        依赖：无
        功能：返回Table中元素的数量
    __str__:
        依赖：无
        功能：返回Table的字符串表示形式
    __repr__:
        依赖：__str__
        功能：返回Table的字符串表示形式
'''

from typing import Union
from depq import DEPQ
from pynars.Narsese import Task, Belief

class Table:
    '''
    Utilized for belief table, desire table, etc. in the `Concept`.
    '''
    def __init__(self, capacity):
        self._table = DEPQ(maxlen=capacity)

    def add(self, task: Task, p: float):
        if task in self:
            self._table.remove(task)
        self._table.insert(task, p)


    # def remove(self, task: Task):
    #     self._table.elim(task)

    @property
    def empty(self):
        return self._table.is_empty()
    
    def first(self):
        return self._table.first() if len(self._table) > 0 else None
    
    def last(self):
        return self._table.last() if len(self._table) > 0 else None

    def __iter__(self):
        return (value for value, _ in self._table)
    
    def values(self):
        return tuple(iter(self))
    
    def items(self):
        return tuple(iter(self._table))

    def keys(self):
        return tuple(key for _, key in self._table)

    def __getitem__(self, idx: int) -> Union[Task, Belief]:
        return self._table[idx][0]

    def __len__(self):
        return len(self._table)

    def __str__(self):
        return f'<Table: #items={len(self._table)}, capacity={self._table.maxlen}>'

    def __repr__(self):
        return str(self)