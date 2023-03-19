'''
这个文件是Channel类和NarseseChannel类的定义文件，它们都继承了Buffer类。Channel类是一个通用的缓冲区，用于存储Task对象，NarseseChannel类是一个特殊的缓冲区，用于存储Narsese语句。

包依赖关系：
    pynars.Narsese.Sentence
    .Buffer.Buffer
    queue.Queue
    pynars.Narsese.Task
    pynars.Narsese.parser
    pynars.utils.Print.out_print
    pynars.utils.Print.PrintType

全局变量名称及其作用：
    无

各函数的依赖关系和主要功能：
    Channel.put:
        依赖：Buffer.put
        功能：将Task对象放入缓冲区中，返回是否溢出
    Channel.take:
        依赖：Buffer.take_max
        功能：从缓冲区中取出最大的Task对象
    NarseseChannel.put:
        依赖：parser.parse, Buffer.put
        功能：将Narsese语句解析为Task对象并放入缓冲区中，返回是否成功、Task对象和是否溢出
'''

from pynars.Narsese import Sentence
from .Buffer import Buffer
from queue import Queue
from pynars.Narsese import Task
from pynars.Narsese import parser
from pynars.utils.Print import out_print, PrintType

class Channel(Buffer):
    ''''''
    def put(self, task: Task):
        task_overflow = Buffer.put(self, task)
        return task_overflow
    
    def take(self) -> Sentence:
        return Buffer.take_max(self, remove=True)

class NarseseChannel(Channel):
    ''''''
    def put(self, text: str):
        try:
            task: Task = parser.parse(text)
        except:
            task = None
            return False, None, None
        
        task_overflow = Buffer.put(self, task)
        return True, task, task_overflow
            
            
    