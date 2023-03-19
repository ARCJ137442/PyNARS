'''
这个文件是VariableSubstitution模块下的Introduction.py，它是const-to-var的替换操作。

导入模块路径列表：
- List
- pynars.Narsese.Term
- pynars.utils.IndexVar.IntVar
- Substitution

全局变量名称及其作用：
- term_src: 要替换的Term
- term_tgt: 替换后的Term
- iconst_src: 要替换的Term中的immutable constant
- ivar_tgt: 替换后的Term中的immutable variable
- dconst_src: 要替换的Term中的derived constant
- dvar_tgt: 替换后的Term中的derived variable
- qconst_src: 要替换的Term中的query constant
- qvar_tgt: 替换后的Term中的query variable

各函数的依赖关系和主要功能：
- __init__(self, term_src: Term, term_tgt: Term, iconst_src: List[Term]=None, ivar_tgt: List[IntVar]=None, dconst_src: List[Term]=None, dvar_tgt: List[IntVar]=None, qconst_src: List[Term]=None, qvar_tgt: List[IntVar]=None) -> None:
    - 初始化函数，设置要替换的Term和替换后的Term，以及要替换的Term中的各种常量和变量
- apply(self, term_src: Term=None, term_tgt: Term=None):
    - 替换函数，将Term中的常量替换为变量
'''

from typing import List
from pynars.Narsese import Term
from pynars.utils.IndexVar import IntVar

from .Substitution import Substitution

class Introduction(Substitution):
    '''
    the substitution of const-to-var
    '''
    def __init__(self, term_src: Term, term_tgt: Term, iconst_src: List[Term]=None, ivar_tgt: List[IntVar]=None, dconst_src: List[Term]=None, dvar_tgt: List[IntVar]=None, qconst_src: List[Term]=None, qvar_tgt: List[IntVar]=None) -> None:
        super().__init__(term_src, term_tgt, iconst_src, ivar_tgt, dconst_src, dvar_tgt, qconst_src, qvar_tgt)


    def apply(self, term_src: Term=None, term_tgt: Term=None):
        ''''''
        term_src = term_src if term_src is not None else self.term_src
        term_tgt = term_tgt if term_tgt is not None else self.term_tgt
        mapping_ivar = self.mapping_ivar
        mapping_dvar = self.mapping_dvar
        mapping_qvar = self.mapping_qvar
        mapping_const = self.mapping_const

        # TODO: replace const with var

        pass
