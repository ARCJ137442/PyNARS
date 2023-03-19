'''
这个模块包含与NARS印章操作相关的函数。

- 导入列表:
    - Union
    - Config
    - Stamp
    - deepcopy
    - Connector
    - Copula

- 全局变量:
    - _temporal_interval: 一个字典，将给定联结词或连接词的时间间隔映射到它的值。

- 函数依赖关系和主要功能:
    - Stamp_merge: 合并两个印章并返回结果。它接受两个印章作为输入，以及一个可选的顺序标记、一个布尔标志以反转印章的顺序和一个时间偏差。它返回一个新的印章，它是合并两个输入印章的结果。
'''

from typing import Union
from pynars.Config import Config
from pynars.Narsese import Stamp
from copy import deepcopy
from pynars.Narsese import Connector, Copula


_temporal_interval = {
    Connector.SequentialEvents: Config.temporal_duration,
    Copula.PredictiveImplication: Config.temporal_duration,
    Copula.PredictiveEquivalence: Config.temporal_duration,
    Copula.RetrospectiveImplication: -Config.temporal_duration,
}

def Stamp_merge(stamp1: Stamp, stamp2: Stamp, order_mark: Union[Copula, Connector]=None, reverse_order=False, t_bias=0):
    stamp: Stamp = deepcopy(stamp1)
    # stamp.is_external = stamp1.is_external
    if stamp is not None:
        stamp.extend_evidenital_base(stamp2.evidential_base)
        if not stamp1.is_eternal and not stamp2.is_eternal:
            stamp.t_occurrence = max(stamp1.t_occurrence, stamp2.t_occurrence)
        if not stamp1.is_eternal:
            # occurrence time interval
            interval = _temporal_interval.get(order_mark, 0)
            if reverse_order: interval = -interval
            stamp.t_occurrence += interval + t_bias
    return stamp