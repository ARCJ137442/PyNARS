'''
这个文件是PyNARS中的一个模块，它实现了NAL4推理引擎的规则。本文件中的函数实现了NAL4推理引擎的规则，包括转换规则和组合规则。这些规则是NAL4推理引擎的核心部分，用于推理和推断。本文件中的函数实现了NAL4推理引擎的规则，包括转换规则和组合规则。这些规则是NAL4推理引擎的核心部分，用于推理和推断。

包依赖关系：
    pynars.NARS.DataStructures
    sparse_lut
    pynars.Global
    ....RuleMap.add_rule

全局变量名称及其作用：
    无

各函数的依赖关系和主要功能：
    add_rules__NAL4:
        依赖：Interface_TransformRules._transform__product_to_image, Interface_TransformRules._transform__image_to_product, Interface_TransformRules._transform__image_to_image, Interface_CompositionalRules._structural__bi_composition__0, Interface_CompositionalRules._structural__bi_composition__1, Interface_CompositionalRules._structural__bi_composition__0_prime, Interface_CompositionalRules._structural__bi_composition__1_prime
        功能：实现NAL4推理引擎的规则，包括转换规则和组合规则。
'''

from collections import OrderedDict
from pynars.NARS.DataStructures import LinkType, TaskLink, TermLink
from sparse_lut import SparseLUT
from pynars import Global
from ....RuleMap.add_rule import *


def add_rules__NAL4(sparse_lut: SparseLUT, structure: OrderedDict):
    ''''''
    '''transform'''
    add_rule(sparse_lut, structure,
        Interface_TransformRules._transform__product_to_image, 
        LinkType1 = LinkType.TRANSFORM, 
        LinkType2 = None,
        has_common_id = True,
        Connector1 = Connector.Product
    )

    add_rule(sparse_lut, structure,
        Interface_TransformRules._transform__image_to_product, 
        LinkType1 = LinkType.TRANSFORM, 
        LinkType2 = None,
        has_common_id = True,
        Connector1 = [
            Connector.IntensionalImage, 
            Connector.ExtensionalImage
        ]
    )

    add_rule(sparse_lut, structure,
        Interface_TransformRules._transform__image_to_image, 
        LinkType1 = LinkType.TRANSFORM, 
        LinkType2 = [None],
        has_common_id = True,
        Connector1 = [
            Connector.IntensionalImage, 
            Connector.ExtensionalImage
        ]
    )
    '''Theorems'''

    '''bi-composition'''

    add_rule(sparse_lut, structure,
        Interface_CompositionalRules._structural__bi_composition__0,
        LinkType1 = LinkType.COMPOUND_STATEMENT, 
        LinkType2 = LinkType.COMPOUND, 
        has_common_id = True,
        Copula1 = Copula.Inheritance,
        Copula2 = None,
        match_reverse = False,
        sentence_type = class_sentence_to_list(Judgement),
        Connector1 = None,
        Connector2 = Connector.Product,
        has_compound_common_id = True,
        compound_common_id = CommonId(0),
        is_belief_valid = False,
        # at_compound_pos = 0
    )

    add_rule(sparse_lut, structure,
        Interface_CompositionalRules._structural__bi_composition__1,
        LinkType1 = LinkType.COMPOUND_STATEMENT, 
        LinkType2 = LinkType.COMPOUND, 
        has_common_id = True,
        Copula1 = Copula.Inheritance,
        Copula2 = None,
        match_reverse = False,
        sentence_type = class_sentence_to_list(Judgement),
        Connector1 = None,
        Connector2 = Connector.Product,
        has_compound_common_id = True,
        compound_common_id = CommonId(1),
        is_belief_valid = False,
        # at_compound_pos = 0
    )

    add_rule(sparse_lut, structure,
        Interface_CompositionalRules._structural__bi_composition__0,
        LinkType1 = LinkType.COMPOUND_STATEMENT, 
        LinkType2 = LinkType.COMPOUND, 
        has_common_id = True,
        Copula1 = Copula.Inheritance,
        Copula2 = None,
        match_reverse = False,
        sentence_type = class_sentence_to_list(Judgement),
        Connector1 = None,
        Connector2 = [
            # Connector.Product,
            Connector.ExtensionalImage,
            Connector.IntensionalImage
        ],
        has_compound_common_id = True,
        compound_common_id = CommonId(0),
        is_belief_valid = False,
        at_compound_pos = 0
    )

    add_rule(sparse_lut, structure,
        Interface_CompositionalRules._structural__bi_composition__1,
        LinkType1 = LinkType.COMPOUND_STATEMENT, 
        LinkType2 = LinkType.COMPOUND, 
        has_common_id = True,
        Copula1 = Copula.Inheritance,
        Copula2 = None,
        match_reverse = False,
        sentence_type = class_sentence_to_list(Judgement),
        Connector1 = None,
        Connector2 = [
            # Connector.Product,
            Connector.ExtensionalImage,
            Connector.IntensionalImage
        ],
        has_compound_common_id = True,
        compound_common_id = CommonId(1),
        is_belief_valid = False,
        at_compound_pos = 0
    )

    add_rule(sparse_lut, structure,
        Interface_CompositionalRules._structural__bi_composition__0_prime,
        LinkType1 = LinkType.COMPOUND_STATEMENT, 
        LinkType2 = LinkType.COMPOUND, 
        has_common_id = True,
        Copula1 = Copula.Inheritance,
        Copula2 = None,
        match_reverse = False,
        sentence_type = class_sentence_to_list(Judgement),
        Connector1 = None,
        Connector2 = [
            Connector.ExtensionalImage,
            Connector.IntensionalImage
        ],
        has_compound_common_id = True,
        compound_common_id = CommonId(0),
        is_belief_valid = False,
        at_compound_pos = 1
    )

    add_rule(sparse_lut, structure,
        Interface_CompositionalRules._structural__bi_composition__1_prime,
        LinkType1 = LinkType.COMPOUND_STATEMENT, 
        LinkType2 = LinkType.COMPOUND, 
        has_common_id = True,
        Copula1 = Copula.Inheritance,
        Copula2 = None,
        match_reverse = False,
        sentence_type = class_sentence_to_list(Judgement),
        Connector1 = None,
        Connector2 = [
            Connector.ExtensionalImage,
            Connector.IntensionalImage
        ],
        has_compound_common_id = True,
        compound_common_id = CommonId(1),
        is_belief_valid = False,
        at_compound_pos = 1
    )