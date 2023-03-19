'''
这个文件定义了一个名为IdEnum的类，它继承自Python内置的Enum类。IdEnum类的实例可以用于表示一个枚举类型的值，同时还会自动分配一个唯一的整数ID。这个文件的详细说明如下：

包依赖关系：
    无

全局变量名称及其作用：
    无

各函数的依赖关系和主要功能：
    IdEnum.__new__:
        依赖：无
        功能：创建一个新的枚举成员，并为其分配一个唯一的整数ID。
    IdEnum.__int__:
        依赖：无
        功能：返回该枚举成员的整数ID。
'''

from enum import Enum

class IdEnum(Enum):
    def __new__(cls, value):
        if not hasattr(cls, '_copula_id'): cls._copula_id = 0
        member = object.__new__(cls)
        member._value_ = value
        member._copula_id = cls._copula_id
        cls._copula_id += 1
        return member

    def __int__(self):
        return self._copula_id