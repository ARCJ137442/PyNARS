'''
这个文件包含了一些用于处理NARS逻辑中真值的函数，包括本地推理和直接推理。其中本地推理是指只考虑两个命题之间的关系，而直接推理是指考虑多个命题之间的关系。这些函数的具体作用和依赖关系如下：

导入模块路径列表：
- typing.Callable
- pynars.Narsese.Truth
- pynars.Narsese.truth_analytic
- .ExtendedBooleanFunctions
- .UncertaintyMappingFunctions

全局变量名称及其作用：
- F_rev: 本地推理中的反转函数，将两个命题的正反面进行反转
- F_exp: 本地推理中的期望函数，计算命题的期望值
- F_dec: 本地推理中的决策函数，计算命题的决策值
- F_neg: 直接推理中的否定函数，将命题的正反面进行反转
- F_cnv: 直接推理中的转换函数，将命题的正面和置信度进行合并
- F_cnt: 直接推理中的对偶函数，将命题的正面和负面进行对偶
- F_ded: 直接推理中的演绎函数，计算两个命题的演绎结果
- F_ana: 直接推理中的类比函数，计算两个命题的类比结果
- F_res: 直接推理中的相似函数，计算两个命题的相似结果
- F_abd: 直接推理中的引入函数，计算两个命题的引入结果
- F_ind: 直接推理中的归纳函数，计算两个命题的归纳结果
- F_exe: 直接推理中的举例函数，计算两个命题的举例结果
- F_com: 直接推理中的比较函数，计算两个命题的比较结果
- F_ddj: 直接推理中的析取消解函数，计算两个命题的析取消解结果
- F_dcj: 直接推理中的合取消解函数，计算两个命题的合取消解结果
- F_int: 术语组合中的交集函数，计算两个命题的交集结果
- F_uni: 术语组合中的并集函数，计算两个命题的并集结果
- F_dif: 术语组合中的差集函数，计算两个命题的差集结果

'''
from typing import Callable
from pynars.Narsese import Truth, truth_analytic
from .ExtendedBooleanFunctions import *
# from .Tools import *
from .UncertaintyMappingFunctions import *
TruthFunction = Callable[[Truth, Truth], Truth]
TruthImmedFunction = Callable[[Truth], Truth]

'''local inference'''
# F_rev
F_rev = F_revision          = lambda w_p_1, w_p_2, w_m_1, w_m_2: (w_p_1+w_p_2, w_m_1+w_m_2)  # return: w+, w-

def Truth_revision(truth1: Truth, truth2: Truth):
    w_p_1 = fc_to_w_plus(truth1.f, truth1.c, truth1.k)
    w_p_2 = fc_to_w_plus(truth2.f, truth2.c, truth2.k)
    w_m_1 = fc_to_w_minus(truth1.f, truth1.c, truth1.k)
    w_m_2 = fc_to_w_minus(truth2.f, truth2.c, truth2.k)
    w_p, w_m = F_revision(w_p_1, w_p_2, w_m_1, w_m_2)
    truth = truth_from_w(w_p, w_m+w_p, truth1.k)
    return truth
    
# F_exp
F_exp = F_expectation       = lambda f, c: (c*(f - 0.5) + 0.5)  # return: e

# F_dec
F_dec = F_decision          = lambda p, d: p*(d - 0.5)          # return: g

'''immediate inference'''
# F_neg
F_neg = F_negation          = lambda w_plus, w_minus: (w_minus, w_plus)     # return: w+, w-
def Truth_negation(truth: Truth) -> Truth: 
    k = truth.k
    w_plus, w_minus = F_negation(*w_from_truth(truth))
    w = w_plus + w_minus
    return Truth(w_to_f(w_plus, w), w_to_c(w, k) , k)

# F_cnv 
F_cnv = F_conversion        = lambda f, c: (And(f, c), 0)                   # return: w+, w-
def Truth_conversion(truth: Truth) -> Truth: 
    w_plus, w_minus = F_conversion(truth.f, truth.c)
    return truth_from_w(w_plus, w_plus + w_minus, truth.k)


# F_cnt
F_cnt = F_contraposition    = lambda f, c: (0, And(Not(f), c))              # return: w+, w-
def Truth_contraposition(truth: Truth) -> Truth: 
    w_plus, w_minus = F_contraposition(truth.f, truth.c)
    return truth_from_w(w_plus, w_plus + w_minus, truth.k)

'''strong syllogism'''
# F_ded
F_ded = F_deduction         = lambda f1, c1, f2, c2: (And(f1, f2), And(f1, f2, c1, c2))     # return: f, c
Truth_deduction: TruthFunction = lambda truth1, truth2: Truth(*F_deduction(truth1.f, truth1.c, truth2.f, truth2.c), truth1.k)

# F_ana
F_ana = F_analogy           = lambda f1, c1, f2, c2: (And(f1, f2), And(f2, c1, c2))         # return: f, c
Truth_analogy: TruthFunction = lambda truth1, truth2: Truth(*F_analogy(truth1.f, truth1.c, truth2.f, truth2.c), truth1.k)

# F_res
F_res = F_resemblance       = lambda f1, c1, f2, c2: (And(f1, f2), And(Or(f1, f2), c1, c2)) # return: f, c
Truth_resemblance: TruthFunction = lambda truth1, truth2: Truth(*F_resemblance(truth1.f, truth1.c, truth2.f, truth2.c), truth1.k)

'''weak syllogism'''
# F_abd
F_abd = F_abduction         = lambda f1, c1, f2, c2:(And(f1, f2, c1, c2), And(f1, c1, c2))      # return: w+, w
Truth_abduction: TruthFunction = lambda truth1, truth2: truth_from_w(*F_abduction(truth1.f, truth1.c, truth2.f, truth2.c), truth1.k)

# F_ind
F_ind = F_induction         = lambda f1, c1, f2, c2: (And(f1, f2, c1, c2), And(f2, c1, c2))     # return: w+, w
Truth_induction: TruthFunction = lambda truth1, truth2: truth_from_w(*F_induction(truth1.f, truth1.c, truth2.f, truth2.c), truth1.k)

# F_exe
F_ind = F_exemplification   = lambda f1, c1, f2, c2: (And(f1, f2, c1, c2), And(f1, f2, c1, c2))     # return: w+, w
Truth_exemplification: TruthFunction = lambda truth1, truth2: truth_from_w(*F_exemplification(truth1.f, truth1.c, truth2.f, truth2.c), truth1.k)
# def Truth_exemplification(truth1: Truth, truth2: Truth) -> Truth: 
#     return truth_from_w(*F_exemplification(truth1.f, truth1.c, truth2.f, truth2.c), truth1.k)
    
# F_com
F_com = F_comparison        = lambda f1, c1, f2, c2: (And(f1, f2, c1, c2), And(Or(f1, f2), c1, c2)) # return: w+, w
Truth_comparison: TruthFunction = lambda truth1, truth2: truth_from_w(*F_comparison(truth1.f, truth1.c, truth2.f, truth2.c), truth1.k)

'''term composition'''
# F_int
F_int = F_intersection      = lambda f1, c1, f2, c2: (And(f1, f2), And(c1, c2))                  # return: f, c
Truth_intersection: TruthFunction = lambda truth1, truth2: Truth(*F_intersection(truth1.f, truth1.c, truth2.f, truth2.c), truth1.k)

# F_uni
F_uni = F_union             = lambda f1, c1, f2, c2: (Or(f1, f2), And(c1, c2))                   # return: f, c 
Truth_union: TruthFunction = lambda truth1, truth2: Truth(*F_union(truth1.f, truth1.c, truth2.f, truth2.c), truth1.k)

# F_dif
F_dif = F_difference        = lambda f1, c1, f2, c2: (And(f1, Not(f2)), And( c1, c2))            # return: f, c 
Truth_difference: TruthFunction = lambda truth1, truth2: Truth(*F_difference(truth1.f, truth1.c, truth2.f, truth2.c), truth1.k)

# F_dcj     {(&&, A, B).; B.} |- A.
Truth_deconjuntion: TruthFunction = lambda truth1, truth2: Truth_negation(Truth_deduction(Truth_intersection(Truth_negation(truth1), truth2), truth_analytic)) 

# F_ddj     {(||, A, B).; B.} |- A.
Truth_dedisjunction: TruthFunction = lambda truth1, truth2: Truth_deduction(Truth_intersection(truth1, Truth_negation(truth2)), truth_analytic)