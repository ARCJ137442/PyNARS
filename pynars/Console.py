'''
这是一个NARS的控制台程序，可以通过命令行或文件输入Narsese语句，然后输出推理结果。本程序主要包括以下几个部分：

包依赖关系：
    - copy: 用于深拷贝对象
    - typing: 用于类型提示
    - pathlib: 用于处理文件路径
    - pynars.Narsese: Narsese语句的解析和生成
    - pynars.NAL: NAL的实现
    - pynars.NARS: NARS的实现
    - time: 用于等待一段时间
    - multiprocessing: 用于多进程
    - os: 用于获取进程信息
    - argparse: 用于解析命令行参数

全局变量名称及其作用：
    - None

各函数的依赖关系和主要功能：
    - info:
        依赖：os
        功能：输出进程信息
    - run_line:
        依赖：pynars.Narsese, pynars.NARS.Reasoner, pynars.utils.Print
        功能：运行一行Narsese语句
    - handle_lines:
        依赖：run_line
        功能：处理多行Narsese语句
    - run_file:
        依赖：handle_lines
        功能：运行一个Narsese文件
    - run_nars:
        依赖：run_file, pynars.NARS.Reasoner, pynars.utils.Print
        功能：运行NARS控制台程序
'''

from copy import deepcopy
from typing import Tuple, Union
from pathlib import Path
from pynars import Narsese, NAL, NARS
from time import sleep
from multiprocessing import Process
import os
from pynars.Narsese.Parser.parser import TreeToNarsese
from pynars.Narsese import Sentence
import random
from pynars.NARS import Reasoner as Reasoner
from pynars.utils.Print import out_print, PrintType
from pynars.Narsese import Task
from typing import List
from pynars.utils.tools import rand_seed
import argparse

def info(title):
    print(f'''
============= {title} =============
module name: {__name__}
parent process: {os.getppid()}
process id: {os.getpid()}
============={'='*(len(title)+2)}=============
    ''')

def run_line(nars: Reasoner, line: str):
    ''''''
    line = line.strip(' \n')
    if line.startswith("//"):
        return None
    elif line.startswith("''"):
        if line.startswith("''outputMustContain('"):
            line = line[len("''outputMustContain('"):].rstrip("')\n")
            if len(line) == 0: return
            try:
                content_check = Narsese.parser.parse(line)
                out_print(PrintType.INFO, f'OutputContains({content_check.sentence.repr()})')
            except:
                out_print(PrintType.ERROR, f'Invalid input! Failed to parse: {line}')
                # out_print(PrintType.ERROR, f'{file}, line {i}, {line}')
        return 
    elif line.startswith("'"):
        return None
    elif line.isdigit():
        n_cycle = int(line)
        out_print(PrintType.INFO, f'Run {n_cycle} cycles.')
        tasks_all_cycles = []
        for _ in range(n_cycle):
            tasks_all = nars.cycle()
            tasks_all_cycles.append(deepcopy(tasks_all))
        return tasks_all_cycles
    else:
        line = line.rstrip(' \n')
        if len(line) == 0:
            return None
        try:
            success, task, _ = nars.input_narsese(line, go_cycle=False)
            if success: out_print(PrintType.IN, task.sentence.repr(), *task.budget)
            else: out_print(PrintType.ERROR, f'Invalid input! Failed to parse: {line}')

            tasks_all = nars.cycle()
            return [deepcopy(tasks_all)]
        except:
            out_print(PrintType.ERROR, f'Unknown error: {line}')


def handle_lines(nars: Reasoner, lines: str):
    tasks_lines = []
    for line in lines.split('\n'):
        if len(line) == 0: continue

        tasks_line = run_line(nars, line)
        if tasks_line is not None:
            tasks_lines.extend(tasks_line)

    tasks_lines: List[Tuple[List[Task], Task, Task, List[Task], Task, Tuple[Task, Task]]]
    for tasks_line in tasks_lines: 
        tasks_derived, judgement_revised, goal_revised, answers_question, answers_quest, (task_operation_return, task_executed) = tasks_line
        for task in tasks_derived: out_print(PrintType.OUT, task.sentence.repr(), *task.budget)
        
        if judgement_revised is not None: out_print(PrintType.OUT, judgement_revised.sentence.repr(), *judgement_revised.budget)
        if goal_revised is not None: out_print(PrintType.OUT, goal_revised.sentence.repr(), *goal_revised.budget)
        if answers_question is not None: 
            for answer in answers_question: out_print(PrintType.ANSWER, answer.sentence.repr(), *answer.budget)
        if answers_quest is not None: 
            for answer in answers_quest: out_print(PrintType.ANSWER, answers_quest.sentence.repr(), *answers_quest.budget)
        if task_executed is not None:
            out_print(PrintType.EXE, f'{task_executed.term.repr()} = {str(task_operation_return) if task_operation_return is not None else None}')


def run_file(nars: Reasoner, filepath: str=None):
    # handle the file
    if filepath is not None:
        filepath: Path = Path(filepath)
        filename = filepath.name
        out_print(PrintType.COMMENT, f'Run file <{filename}>.', comment_title='NARS')
        with open(filepath, 'r') as f:
            lines = f.read()
            handle_lines(nars, lines)

    

def run_nars(filepath: str):
    ''''''
    # info('Console')
    seed = 137
    rand_seed(seed)
    out_print(PrintType.COMMENT, f'rand_seed={seed}', comment_title='Setup')
    nars = Reasoner(100, 100)
    out_print(PrintType.COMMENT, 'Init...', comment_title='NARS')
    out_print(PrintType.COMMENT, 'Run...', comment_title='NARS')
    run_file(nars, filepath)
    # console
    out_print(PrintType.COMMENT, 'Console.', comment_title='NARS')
    while True:
        out_print(PrintType.COMMENT, '', comment_title='Input', end='')
        lines = input()
        handle_lines(nars, lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse NAL files.')
    parser.add_argument('filepath', metavar='Path', type=str, nargs='*',
        help='file path of an *.nal file.')
    args = parser.parse_args()
    filepath: Union[list, None] = args.filepath
    filepath = filepath[0] if (filepath is not None and len(filepath) > 0) else None

    try:
        run_nars(filepath)
    except KeyboardInterrupt:
        out_print(PrintType.COMMENT, 'Stop...', comment_title='\n\nNARS')

    print('Done.')

# if __name__ == '__main__':
#     # Process
#     info('main')
#     try:
#         p_console = Process(target=run_console, args=())
#         p_nars = Process(target=run_nars, args=())
#         p_console.start()
#         p_nars.start()
#         p_nars.join()
#         p_console.close()
#     except KeyboardInterrupt:
#         print('\n\nStop NARS...')

#     print('Done.')