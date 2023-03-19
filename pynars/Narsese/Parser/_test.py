'''
这是一个Narsese解析器的测试文件，用于测试Narsese解析器的各种功能。

包依赖关系：
    无

全局变量名称及其作用：
    re_parser: 用于解析Narsese语句的正则表达式
    parser: Narsese解析器

各函数的依赖关系和主要功能：
    parser.parse:
        依赖：re_parser
        功能：解析Narsese语句并返回解析结果
'''

from .parser import parser
import re
re_parser = re.compile(r'[^<^>^=^"^&^|^!^.^?^@^~^%^;^\,^:^\/^\\^*^#^$^\[^\]^\{^\}^\(^\)^\ ]+')
re_parser.findall('<x-->lock>.')
# result = parser.parse('(&&, <#x --> lock>, <"a"-->"b">).')
result = parser.parse('<x-->lock>.')
print(result.pretty())

result = parser.parse('<"鸟" --> "动-物">. %0.9; 0.9%')
print(result.pretty())
result = parser.parse('<gull <-> swan>. %0.9; 0.9%')
print(result.pretty())
result = parser.parse('<swan --> (&,bird,swimmer)>. %0.9; 0.9%')
print(result.pretty())
result = parser.parse('<planetX --> {Mars,Pluto,Venus}>. %0.9; 0.9%')
print(result.pretty())
result = parser.parse('<(&,bird,swimmer) --> (&,animal,swimmer)>?')
print(result.pretty())
result = parser.parse('<(~, boy, girl) --> [strong]>.')
print(result.pretty())
result = parser.parse('<acid --> (/,reaction,_,base)>.')
print(result.pretty())
result = parser.parse('<(*,acid,base) --> reaction>.')
print(result.pretty())
result = parser.parse('<<$y --> bird> ==> <$y --> flyer>>.')
print(result.pretty())
result = parser.parse('<(&&,<$1 --> [chirping]>,<$1 --> [with_wings]>) ==> <$1 --> bird>>.')
print(result.pretty())
result = parser.parse('<<#x --> lock> ==> <<$y --> key> ==> <#x --> (/,open,$y,_)>>>.')
result = parser.parse('(&&,<#x --> lock>,<<$y --> key> ==> <#x --> (/,open,$y,_)>>).')
result = parser.parse('(&&,<?x --> lock>,<<$y --> key> ==> <#x --> (/,open,$y,_)>>)?')
print(result.pretty())
result = parser.parse('<<(*, $y, door_101) --> open> =\> <(*, $y, key_101) --> hold>>.')
print(result.pretty())
result = parser.parse('<(*,John,room_101) --> enter>. :\: %1.00;0.90%')
print(result.pretty())
result = parser.parse('<<(*,John,door_101) --> open></><(*,John,room_101) --> enter>>.')
print(result.pretty())
result = parser.parse('(&/,<(*,SELF,{t002}) --> hold>,<(*,SELF,{t001}) --> at>,(^open,{t001}))!')
print(result.pretty())
result = parser.parse('<SELF --> (/,at,_,{t003})>. :\:')
print(result.pretty())
result = parser.parse('(&/,<(*,SELF,{t002}) --> reachable>,(^pick,{t002}))!')
print(result.pretty())
result = parser.parse('(^doubt,{SELF},<a --> b>)!')
print(result.pretty())
print('done.')