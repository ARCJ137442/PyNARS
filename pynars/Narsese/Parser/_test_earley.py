'''
这个文件是用于测试Earley算法的Python文件。

包依赖关系：
    - lark
    - pynars.Narsese.Parser.parser
    - pathlib.Path

全局变量名称及其作用：
    filepath: 存储文件路径的Path对象
    gramma: 存储Lark语法的字符串
    lark: 存储Lark对象
    content: 存储解析结果的树形结构

各函数的依赖关系和主要功能：
    无

'''

from lark import Lark
from pynars.Narsese.Parser.parser import TreeToNarsese
from pathlib import Path

filepath = Path(r'Narsese\Parser\narsese.lark')
with open(filepath, 'r') as f:
    gramma = ''.join(f.readlines())
lark = Lark(grammar=gramma, parser='lalr')
content = lark.parse(r'$0.90;0.90;0.9$ <robin-->bird>.')

lark = Lark(grammar=gramma, parser='earley')
content = lark.parse(r'$0.90;0.90;0.9$ <robin-->bird>.')


print('done.')