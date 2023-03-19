'''
这个文件是PyNARS中的一个模块，它实现了NAL7规则。NAL7规则是一种基于时间的推理规则，它可以用于推理和学习。这个模块中的函数实现了NAL7规则的不同变体，以及它们之间的组合。这个模块中的函数都是为了实现NAL7规则而设计的。

包依赖关系：
    collections.OrderedDict
    pynars.NARS.DataStructures
    sparse_lut
    pynars.Global
    ....RuleMap.add_rule

全局变量名称及其作用：
    无

各函数的依赖关系和主要功能：
    add_rules__NAL7:
        依赖：Interface_TemporalRules
        功能：实现NAL7规则的不同变体和它们之间的组合，将它们添加到给定的稀疏查找表和有序字典结构中。这些规则是基于时间的推理规则，可以用于推理和学习。这个函数依赖于Interface_TemporalRules模块。
'''

from collections import OrderedDict
from pynars.NARS.DataStructures import LinkType, TaskLink, TermLink
from sparse_lut import SparseLUT
from pynars import Global
from ....RuleMap.add_rule import *


def add_rules__NAL7(sparse_lut: SparseLUT, structure: OrderedDict):
    ''''''
    ''''''
    add_rule(sparse_lut, structure,
        [
            Interface_TemporalRules._temporal__induction_composition,
            Interface_TemporalRules._temporal__induction_implication,
            Interface_TemporalRules._temporal__induction_implication_prime,
            Interface_TemporalRules._temporal__induction_equivalence,
        ],
        is_temporal_copula1 = False,
        is_temporal_copula2 = False
    )
    add_rule(sparse_lut, structure,
        Interface_TemporalRules._temporal__induction_composition,
        is_temporal_copula1 = False,
        is_temporal_copula2 = True
    )
    add_rule(sparse_lut, structure,
        Interface_TemporalRules._temporal__induction_composition,
        is_temporal_copula1 = True,
        is_temporal_copula2 = False
    )

    ''''''
    add_rule(sparse_lut, structure,
        Interface_TemporalRules._temporal__induction_implication,
        is_temporal_copula1 = False,
        is_temporal_copula2 = False
    )
    add_rule(sparse_lut, structure,
        Interface_TemporalRules._temporal__induction_implication_prime,
        is_temporal_copula1 = False,
        is_temporal_copula2 = False
    )

    ''''''
    add_rule(sparse_lut, structure,
        [
            Interface_TemporalRules._temporal__induction_predictieve_implication_composition,
            Interface_TemporalRules._temporal__induction_predictive_implication_composition_inverse,
            Interface_TemporalRules._temporal__induction_predictive_equivalance_composition
        ],
        is_temporal_copula1 = False,
        is_temporal_copula2 = True,
        copula2 = [
            Copula.PredictiveImplication,
            Copula.ConcurrentImplication
        ]
    )
    add_rule(sparse_lut, structure,
        [
            Interface_TemporalRules._temporal__induction_predictive_implication_composition_prime,
            Interface_TemporalRules._temporal__induction_predictive_implication_composition_inverse_prime,
            Interface_TemporalRules._temporal__induction_predictive_equivalance_composition_prime
        ],
        is_temporal_copula1 = True,
        is_temporal_copula2 = False,
        copula1 = [
            Copula.PredictiveImplication,
            Copula.ConcurrentImplication
        ]
    )

    ''''''
    add_rule(sparse_lut, structure,
        [
            Interface_TemporalRules._temporal__induction_retrospective_implication_composition,
            Interface_TemporalRules._temporal__induction_retrospective_implication_composition_inverse,
            Interface_TemporalRules._temporal__induction_retrospective_equivalance_composition

        ],
        is_temporal_copula1 = False,
        is_temporal_copula2 = True,
        copula2 = Copula.RetrospectiveImplication
    )
    add_rule(sparse_lut, structure,
        [
            Interface_TemporalRules._temporal__induction_retrospective_implication_composition_prime,
            Interface_TemporalRules._temporal__induction_retrospective_implication_composition_inverse_prime,
            Interface_TemporalRules._temporal__induction_retrospective_equivalance_composition_prime
        ],
        is_temporal_copula1 = True,
        is_temporal_copula2 = False,
        copula1 = Copula.RetrospectiveImplication
    )

    # add_rule(sparse_lut, structure,
    #     Interface_TemporalRules._temporal__induction_predictive_implication_composition_inverse,
    #     is_temporal_copula1 = False,
    #     is_temporal_copula2 = True,
    #     coupla2 = [Copula.RetrospectiveImplication]
    # )
    # add_rule(sparse_lut, structure,
    #     Interface_TemporalRules._temporal__induction_predictive_implication_composition_inverse_prime,
    #     is_temporal_copula1 = True,
    #     is_temporal_copula2 = False,
    #     coupla1 = [Copula.RetrospectiveImplication]
    # )


    # add_rule(sparse_lut, structure,
    #     Interface_TemporalRules._temporal__induction_implication_composition,
    #     connector1 = [None, Connector.SequentialEvents, Connector.ParallelEvents],
    #     copula2 = Copula.PredictiveImplication
    # )

    # add_rule(sparse_lut, structure,
    #     [
    #         Interface_TemporalRules._temporal__induction_implication,
    #         Interface_TemporalRules._temporal__induction_implication_prime
    #     ], 
    #     is_temporal_copula1 = False,
    #     is_temporal_copula2 = False
    # )
    # add_rule(sparse_lut, structure,
    #     [
    #         Interface_TemporalRules._temporal__induction_implication,
    #         Interface_TemporalRules._temporal__induction_implication_prime,
    #         Interface_TemporalRules._temporal__induction_composition,
    #     ], 
    #     is_temporal_copula1 = False,
    #     is_temporal_copula2 = False,
    #     is_temporal_connector1 = False,
    #     is_temporal_connector2 = False
    # )