'''
这个文件是Budget类的实现，它定义了一个Budget类，用于表示NARS系统中的预算。Budget类包含了优先级、耐久性和质量三个属性，以及一些方法用于计算预算的摘要、判断预算是否超过阈值、将预算分配为n个部分等。此外，Budget类还定义了一些静态方法，用于从Truth对象中计算质量值。

包依赖关系：
    - math
    - pynars.Config
    - typing
    - .Truth

全局变量名称及其作用：
    - priority: 预算的优先级
    - durability: 预算的耐久性
    - quality: 预算的质量

各函数的依赖关系和主要功能：
    - __init__:
        依赖：Config
        功能：初始化Budget对象
    - summary:
        依赖：无
        功能：计算预算的摘要
    - is_above_thresh:
        依赖：Config
        功能：判断预算是否超过阈值
    - __str__:
        依赖：无
        功能：返回Budget对象的字符串表示
    - __repr__:
        依赖：无
        功能：返回Budget对象的字符串表示
    - __iter__:
        依赖：无
        功能：返回Budget对象的迭代器
    - quality_from_truth:
        依赖：无
        功能：从Truth对象中计算质量值
    - reduce_by_achieving_level:
        依赖：无
        功能：根据实现水平减少预算
    - distribute:
        依赖：无
        功能：将预算分配为n个部分
'''

from math import sqrt
from pynars.Config import Config
from typing import Type
from .Truth import Truth

class Budget:
    priority: float = 0.9
    durability: float = 0.9
    quality: float = 0.5
    
    def __init__(self, priority: float, durability: float, quality: float):
        self.priority = priority if priority is not None else Budget.priority
        self.durability = durability if durability is not None else  Budget.durability
        self.quality = quality if durability is not None else  Budget.quality    

    @property
    def summary(self) -> float:
        return self.durability*(self.priority+self.quality)/2.0

    @property
    def is_above_thresh(self) -> bool:
        return self.summary > Config.budget_thresh


    def __str__(self) -> str:
        return f'${float(self.priority):.3f};{float(self.durability):.3f};{float(self.quality):.3f}$'
        
    def __repr__(self) -> str:
        return str(self)

    def __iter__(self):
        '''return (p, d, q)'''
        return iter((self.priority, self.durability, self.quality))


    @classmethod
    def quality_from_truth(cls, t: Truth):
        exp: float = t.e
        return max(exp, (1 - exp)*0.75)

    def reduce_by_achieving_level(self, h: float):
        self.priority = self.priority * (1 - h)
    
    def distribute(self, n: int):
        '''
        distribute the budget into n parts.
        Ref. OpenNARS 3.1.0 BudgetFunctions.java line 144~146:
            ```
            final float priority = (float) (b.getPriority() / sqrt(n));
            return new BudgetValue(priority, b.getDurability(), b.getQuality(), narParameters);
            ```
        '''
        return Budget(self.priority/sqrt((n if n > 0 else 1)), self.durability, self.quality)