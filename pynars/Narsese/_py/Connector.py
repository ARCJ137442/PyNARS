'''
这个文件定义了Connector类，它是一个枚举类，包含了Narsese语言中的各种连接符。这个类提供了一些方法，用于检查连接符的类型和有效性。

包依赖关系：
    无

全局变量名称及其作用：
    Conjunction: 逻辑与连接符
    Disjunction: 逻辑或连接符
    Product: 乘法连接符
    ParallelEvents: 并行事件连接符
    SequentialEvents: 顺序事件连接符
    IntensionalIntersection: 内部交集连接符
    ExtensionalIntersection: 外部交集连接符
    ExtensionalDifference: 差集连接符
    IntensionalDifference: 内部差集连接符
    Negation: 否定连接符
    IntensionalSet: 内部集合连接符
    ExtensionalSet: 外部集合连接符
    IntensionalImage: 内部映像连接符
    ExtensionalImage: 外部映像连接符
    List: 列表连接符

各函数的依赖关系和主要功能：
    Connector.check_valid:
        依赖：无
        功能：检查连接符的有效性
    Connector.is_commutative:
        依赖：无
        功能：检查连接符是否是可交换的
    Connector.is_single_only:
        依赖：无
        功能：检查连接符是否只能接受一个参数
    Connector.is_double_only:
        依赖：无
        功能：检查连接符是否只能接受两个参数
    Connector.is_multiple_only:
        依赖：无
        功能：检查连接符是否只能接受多个参数
    Connector.is_temporal:
        依赖：无
        功能：检查连接符是否是时间连接符
'''

# from enum import Enum
from pynars.utils.IdEnum import IdEnum
# from .Term import Term

class Connector(IdEnum):
    Conjunction = "&&"
    Disjunction = "||"
    Product = "*"
    ParallelEvents = "&|"
    SequentialEvents = "&/"
    IntensionalIntersection = "|"
    ExtensionalIntersection = "&"
    ExtensionalDifference = "-"
    IntensionalDifference = "~"
    Negation = "--"
    IntensionalSet = "["
    ExtensionalSet = "{"
    IntensionalImage = "\\"
    ExtensionalImage = "/"
    List = "#"

    @property
    def is_commutative(self):
        return self in (
            Connector.Conjunction, 
            Connector.Disjunction, 
            Connector.ParallelEvents,
            Connector.IntensionalIntersection,
            Connector.ExtensionalIntersection,
            Connector.IntensionalSet,
            Connector.ExtensionalSet
        )
    @property
    def is_single_only(self):
        return self in (
            Connector.Negation,
        )
    
    @property
    def is_double_only(self):
        return self in (
            Connector.ExtensionalDifference, 
            Connector.IntensionalDifference
        )
    
    @property
    def is_multiple_only(self):
        return self in (
            Connector.Conjunction, 
            Connector.Disjunction, 
            Connector.Product, 
            Connector.ParallelEvents,
            Connector.SequentialEvents,
            Connector.IntensionalIntersection,
            Connector.ExtensionalIntersection,
            Connector.ExtensionalDifference,
            Connector.IntensionalDifference,
            Connector.IntensionalImage,
            Connector.ExtensionalImage
        )

    @property
    def is_temporal(self):
        return self in (Connector.SequentialEvents, Connector.ParallelEvents)

    def check_valid(self, len_terms: int):
        if self.is_single_only: return len_terms == 1
        elif self.is_double_only: return len_terms == 2
        elif self.is_multiple_only: return len_terms > 1
        else: return len_terms > 0
    
    # @property
    # def is_higher_order(self):
    #     return self in (
    #         Connector.Conjunction, 
    #         Connector.Disjunction, 
    #         Connector.ParallelEvents,
    #         Connector.IntensionalIntersection,
    #         Connector.ExtensionalIntersection,
    #         Connector.IntensionalSet,
    #         Connector.ExtensionalSet
    #     )

# place_holder = Term('_', True)