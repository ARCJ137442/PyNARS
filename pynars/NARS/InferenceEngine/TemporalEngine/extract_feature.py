'''
这个文件是PyNARS中的一个模块，提供了从NARSese语句中提取特征的功能。

包依赖关系：
    typing.Union
    collections.namedtuple
    pynars.Narsese._py.Connector.Connector
    pynars.Narsese._py.Copula.Copula
    pynars.NAL.Inference
    pynars.Narsese.Statement
    pynars.Narsese.Term
    pynars.Narsese.Compound

全局变量名称及其作用：
    Feature: 一个namedtuple，包含了从NARSese语句中提取的特征。

各函数的依赖关系和主要功能：
    extract_feature:
        依赖：Union, namedtuple, pynars.Narsese._py.Connector.Connector, pynars.NAL.Inference, pynars.Narsese.Statement, pynars.Narsese.Term, pynars.Narsese.Compound, pynars.Narsese._py.Copula.Copula
        功能：从两个NARSese语句中提取特征，返回一个Feature对象。
    _mirorr_feature:
        依赖：Union, extract_feature
        功能：从两个NARSese语句中提取特征，返回一个Feature对象，但是交换了两个语句的顺序。
'''

from typing import Union
from collections import namedtuple

from pynars.Narsese._py.Connector import Connector
from pynars.NAL.Inference import *
from pynars.Narsese import Statement, Term, Compound
from pynars.Narsese._py.Copula import Copula

Feature = namedtuple(
    'Feature', 
    [
        'is_temporal_copula1',
        'is_temporal_copula2',
        'is_temporal_connector1',
        'is_temporal_connector2'
    ],
    defaults=[None, None, None, None]
)

def _mirorr_feature(premise1: Union[Term, Compound, Statement], premise2: Union[Term, Compound, Statement]):
    feature = extract_feature(premise2, premise1)
    return Feature(
        feature.is_temporal_copula2,
        feature.is_temporal_copula1,
        feature.is_temporal_connector2,
        feature.is_temporal_connector1
    )


def extract_feature(premise1: Union[Term, Compound, Statement], premise2: Union[Term, Compound, Statement]) -> Feature:
    '''
    It should be ensured that premise1 and premise2 aren't identical.    
    '''
    is_temporal_copula1 = premise1.is_statement and premise1.copula.is_temporal
    is_temporal_copula2 = premise2.is_statement and premise2.copula.is_temporal
    is_temporal_connector1 = premise1.is_compound and premise1.connector.is_temporal
    is_temporal_connector2 = premise2.is_compound and premise2.connector.is_temporal
    return Feature(
        is_temporal_copula1=is_temporal_copula1,
        is_temporal_copula2=is_temporal_copula2,
        is_temporal_connector1=is_temporal_connector1,
        is_temporal_connector2=is_temporal_connector2,

    )

