'''
这个文件定义了Operation类，它是Term类的子类，表示Narsese中的操作符。Operation类的实例可以表示Narsese中的操作符，如anticipate、believe等。这个文件还定义了一些全局变量，它们都是Operation类的实例。

包依赖关系：
    无

全局变量名称及其作用：
    Anticipate: Narsese中的anticipate操作符
    Believe: Narsese中的believe操作符
    Doubt: Narsese中的doubt操作符
    Evaluate: Narsese中的evaluate操作符
    Hesitate: Narsese中的hesitate操作符
    Want: Narsese中的want操作符
    Wonder: Narsese中的wonder操作符

各函数的依赖关系和主要功能：
    Operation.__init__:
        依赖：Term.__init__
        功能：初始化Operation实例
    Operation.__str__:
        依赖：无
        功能：返回Operation实例的字符串表示
    Operation.__repr__:
        依赖：无
        功能：返回Operation实例的字符串表示，用于调试
    Operation.do_hashing:
        依赖：无
        功能：计算Operation实例的哈希值
'''

from .Term import Term

class Operation(Term):
    
    is_operation = True

    def __init__(self, word, do_hashing=False, is_mental_operation=False) -> None:
        super().__init__(word, do_hashing=do_hashing)
        self._is_mental_operation = is_mental_operation

    @property
    def is_mental_operation(self):
        return self._is_mental_operation
    
    def __str__(self) -> str:
        return "^" + str(self.word)
    
    def __repr__(self) -> str:
        return f'<Operation: {str(self)}>'

    def do_hashing(self):
        self._hash_value = hash(str(self))
        return self._hash_value


Anticipate = Operation('anticipate', True, is_mental_operation=True)
Believe    = Operation('believe',    True, is_mental_operation=True)
Doubt      = Operation('doubt',      True, is_mental_operation=True)
Evaluate   = Operation('evaluate',   True, is_mental_operation=True)
Hesitate   = Operation('hesitate',   True, is_mental_operation=True)
Want       = Operation('want',       True, is_mental_operation=True)
Wonder     = Operation('wonder',     True, is_mental_operation=True)