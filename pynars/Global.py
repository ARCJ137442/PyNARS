'''
这个文件是PyNARS中的Global.py，包含了一些全局变量和函数。

包依赖关系：
    无

全局变量名称及其作用：
    time: 记录当前时间
    _input_id: 记录输入的ID

各函数的依赖关系和主要功能：
    get_input_id:
        依赖：无
        功能：返回一个新的输入ID
'''

time = 0
_input_id = 0
def get_input_id():
    global _input_id
    input_id = _input_id
    _input_id += 1
    return input_id