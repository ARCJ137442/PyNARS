'''
这个文件是PyNARS中的一个模块，它实现了NAL1规则的添加。NAL1是NARS的一种基本推理规则，它包括了四种基本的推理方式：演绎、归纳、类比和拓展。这个模块中的函数用于向系统中添加NAL1规则。

包依赖关系：
    pynars.NARS.DataStructures
    sparse_lut
    pynars.Global
    ....RuleMap.add_rule

全局变量名称及其作用：
    无

各函数的依赖关系和主要功能：
    add_rules__NAL1:
        依赖：Interface_SyllogisticRules._syllogistic__deduction__0_1, Interface_SyllogisticRules._syllogistic__deduction__1_0, Interface_SyllogisticRules._syllogistic__exemplification__0_1, Interface_SyllogisticRules._syllogistic__exemplification__1_0, Interface_SyllogisticRules._syllogistic__induction__0_0, Interface_SyllogisticRules._syllogistic__induction__0_0_prime, Interface_SyllogisticRules._syllogistic__abduction__1_1, Interface_SyllogisticRules._syllogistic__abduction__1_1_prime, Interface_SyllogisticRules._syllogistic__reversion, LinkType, TaskLink, TermLink, SparseLUT, OrderedDict, Copula, CommonId, add_rule
        功能：向系统中添加NAL1规则
'''

from collections import OrderedDict
from pynars.NARS.DataStructures import LinkType, TaskLink, TermLink
from sparse_lut import SparseLUT
from pynars import Global
from ....RuleMap.add_rule import *

def add_rules__NAL1(sparse_lut: SparseLUT, structure: OrderedDict):

    '''deduction'''
    add_rule(sparse_lut, structure,
        Interface_SyllogisticRules._syllogistic__deduction__0_1, 
        LinkType1 = LinkType.COMPOUND_STATEMENT, 
        LinkType2 = LinkType.COMPOUND_STATEMENT, 
        has_common_id = True,
        Copula1 = Copula.Inheritance,
        Copula2 = Copula.Inheritance,
        match_reverse = False,
        common_id = CommonId(0, 1),
        has_compound_at = False
    )

    add_rule(sparse_lut, structure,
        Interface_SyllogisticRules._syllogistic__deduction__1_0, 
        LinkType1 = LinkType.COMPOUND_STATEMENT, 
        LinkType2 = LinkType.COMPOUND_STATEMENT, 
        has_common_id = True,
        Copula1 = Copula.Inheritance,
        Copula2 = Copula.Inheritance,
        match_reverse = False,
        common_id = CommonId(1, 0),
        has_compound_at = False
    )

    '''exemplification'''
    add_rule(sparse_lut, structure,
        Interface_SyllogisticRules._syllogistic__exemplification__0_1, 
        LinkType1 = LinkType.COMPOUND_STATEMENT, 
        LinkType2 = LinkType.COMPOUND_STATEMENT, 
        has_common_id = True,
        Copula1 = Copula.Inheritance,
        Copula2 = Copula.Inheritance,
        match_reverse = False,
        common_id = CommonId(0, 1),
        has_compound_at = False
    )

    add_rule(sparse_lut, structure,
        Interface_SyllogisticRules._syllogistic__exemplification__1_0, 
        LinkType1 = LinkType.COMPOUND_STATEMENT, 
        LinkType2 = LinkType.COMPOUND_STATEMENT, 
        has_common_id = True,
        Copula1 = Copula.Inheritance,
        Copula2 = Copula.Inheritance,
        match_reverse = False,
        common_id = CommonId(1, 0),
        has_compound_at = False
    )

    '''induction'''
    add_rule(sparse_lut, structure,
        Interface_SyllogisticRules._syllogistic__induction__0_0, 
        LinkType1 = LinkType.COMPOUND_STATEMENT, 
        LinkType2 = LinkType.COMPOUND_STATEMENT, 
        has_common_id = True,
        Copula1 = Copula.Inheritance,
        Copula2 = Copula.Inheritance,
        match_reverse = False,
        common_id = CommonId(0, 0),
        has_compound_at = False
    )

    add_rule(sparse_lut, structure,
        Interface_SyllogisticRules._syllogistic__induction__0_0_prime, 
        LinkType1 = LinkType.COMPOUND_STATEMENT, 
        LinkType2 = LinkType.COMPOUND_STATEMENT, 
        has_common_id = True,
        Copula1 = Copula.Inheritance,
        Copula2 = Copula.Inheritance,
        match_reverse = False,
        common_id = CommonId(0, 0),
        has_compound_at = False
    )

    '''abduction'''
    add_rule(sparse_lut, structure,
        Interface_SyllogisticRules._syllogistic__abduction__1_1, 
        LinkType1 = LinkType.COMPOUND_STATEMENT, 
        LinkType2 = LinkType.COMPOUND_STATEMENT, 
        has_common_id = True,
        Copula1 = Copula.Inheritance,
        Copula2 = Copula.Inheritance,
        match_reverse = False,
        common_id = CommonId(1, 1),
        has_compound_at = False
    )

    add_rule(sparse_lut, structure,
        Interface_SyllogisticRules._syllogistic__abduction__1_1_prime, 
        LinkType1 = LinkType.COMPOUND_STATEMENT, 
        LinkType2 = LinkType.COMPOUND_STATEMENT, 
        has_common_id = True,
        Copula1 = Copula.Inheritance,
        Copula2 = Copula.Inheritance,
        match_reverse = False,
        common_id = CommonId(1, 1),
        has_compound_at = False
    )

    '''reversion'''
    add_rule(sparse_lut, structure,
        Interface_SyllogisticRules._syllogistic__reversion, 
        LinkType1 = LinkType.COMPOUND_STATEMENT, 
        LinkType2 = LinkType.COMPOUND_STATEMENT, 
        has_common_id = True,
        Copula1 = Copula.Inheritance,
        Copula2 = Copula.Inheritance,
        match_reverse = True
    )