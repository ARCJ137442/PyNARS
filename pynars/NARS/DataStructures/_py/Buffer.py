'''
这个文件是PyNARS中的Buffer.py，它定义了一个Buffer类，继承自Bag类，实现了一个时间限制的包，包含新的（输入或派生的）任务。Buffer有以下主要例程：
- put：如包中所定义。
- take：如包中所定义，除了如果所选任务已经过期，则选择将重复多次。此外，在Buffer中，此操作不是直接从外部调用的，而是从内部调用的，作为observe的一部分。
- observe：如果缓冲区不执行时间组合，则此例程只调用take以获取任务，并返回它。否则，它还使用所选任务和每个其他任务来形成包含复合事件的任务。新任务被放入缓冲区。由于它们的高复杂性，大多数任务将被删除。剩下的任务通常对应于内存中的现有概念或缓冲区中的任务。

包依赖关系：
- .Bag：从当前目录导入Bag类
- pynars.Config：从pynars包中导入Config模块
- pynars.Narsese：从pynars包中导入Item类

全局变量名称及其作用：
- 无

各函数的依赖关系和主要功能：
- __init__：
    依赖：Bag.__init__
    功能：初始化Buffer对象
- is_expired：
    依赖：无
    功能：判断任务是否过期
'''

from .Bag import Bag
from pynars.Config import Config
from pynars.Narsese import Item

class Buffer(Bag):
    '''
    According to *the Conceptual Design of OpenNARS 3.1.0*:
        A buffer is a time-restricted bag containing new (input or derived) tasks.
        A buffer has the following major routines:
        **put**: As defined in bag.
        **take**: As defined in bag, except that if the selected task is already expired,
        the selection will repeat up to a predetermined times. Also, in buffer this
        operation is not directly invoked from the outside, but from insider, as
        part of observe.
        **observe**: If the buffer does not carry out temporal composition, this routine
        just call take to get a task, and return it. Otherwise it also uses the selected
        task and every other tasks to form tasks containing compounds events.
        The new tasks are put into the buffers. Given their high complexity,
        most of them will be removed. The remaining ones usually correspond to
        existing concepts in the memory or tasks in the buffer.
    '''

    def __init__(self, capacity: int, n_buckets: int=None, take_in_order: bool=False, max_duration: int=None) -> None:
        Bag.__init__(self, capacity, n_buckets=n_buckets, take_in_order=take_in_order)
        self.max_duration = max_duration if max_duration is not None else Config.max_duration


    def is_expired(self, put_time, current_time):
        return (current_time - put_time) > self.max_duration
