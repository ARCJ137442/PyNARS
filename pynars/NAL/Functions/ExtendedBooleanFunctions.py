'''

这个文件包含了NARS（非公理化推理系统）中使用的扩展布尔函数。

- 导入列表：
    - numpy as np：用于数学运算。

- 全局变量：
    - Not：一个lambda函数，返回布尔值的否定。
    - And：一个lambda函数，返回布尔值的合取。
    - Or：一个lambda函数，返回布尔值的析取。
    - Average：一个lambda函数，返回数值的平均值。

- 函数：
    - Scalar：一个函数，使用sigmoid函数将数值映射到0.001到0.999之间的值。

'''

import numpy as np

Not = lambda x: (1-x)
And = lambda *x: np.prod(x)
Or  = lambda *x: 1 - np.prod(1-np.array(x))
Average = lambda *x: np.mean(x)

def Scalar(x): 
    x = 0.5 + 4*(x-0.5)**3 
    x = 0.001 if x < 0.001 else 0.999 if x > 0.999 else x
    return x