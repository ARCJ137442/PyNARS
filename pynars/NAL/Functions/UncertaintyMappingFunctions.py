'''
这个文件包含了一些用于不确定性映射的函数，包括从w值计算出Truth值，以及从Truth值计算出w值的函数。这些函数可以用于NARS系统中的不确定性推理。

导入模块路径列表：
- pynars.Narsese.Truth

全局变量名称及其作用：
- fc_to_w_plus: 从f和c值计算出w+值的函数
- fc_to_w: 从f和c值计算出w值的函数
- fc_to_w_minus: 从f和c值计算出w-值的函数
- w_to_f: 从w+和w值计算出f值的函数
- w_to_c: 从w和k值计算出c值的函数

各函数的依赖关系和主要功能：
- truth_from_w: 从w+和w值计算出Truth值的函数，依赖于w_to_f和w_to_c函数
- w_from_truth: 从Truth值计算出w+和w-值的函数，依赖于fc_to_w_plus和fc_to_w_minus函数
'''

from pynars.Narsese import Truth

fc_to_w_plus    = lambda f, c, k: k*f*c/(1-c)
fc_to_w         = lambda f, c, k: k*c/(1-c)
fc_to_w_minus   = lambda f, c, k: k*(1-f)*c/(1-c)

w_to_f          = lambda w_plus, w: w_plus/w
w_to_c          = lambda w, k     : w/(w+k)

# lu_to_w_plus    = lambda 

def truth_from_w(w_plus, w, k):
    f, c = (w_to_f(w_plus, w), w_to_c(w, k)) if w != 0 else (0.5, 0.0)
    return Truth(f, c, k)

def w_from_truth(truth: Truth):
    f, c, k = truth.f, truth.c, truth.k
    return fc_to_w_plus(f, c, k), fc_to_w_minus(f, c, k)