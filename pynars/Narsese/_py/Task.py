'''
这个文件定义了一个名为Task的类，它是Item的子类，表示一个任务。Task类包含了一个Sentence对象，它是Judgement、Goal、Question或Quest的子类，表示一个句子。Task类还包含了一个Budget对象，表示任务的预算。Task类的实例可以通过achieving_level方法计算出它的完成度，通过reduce_budget_by_achieving_level方法减少它的预算。Task类还包含了一些属性和方法，用于判断任务的类型、是否可执行等。

包依赖关系：
    copy
    typing
    .Sentence
    .Item
    .Budget
    .Term
    .Truth

全局变量名称及其作用：
    Task.input_id: 任务的输入ID

各函数的依赖关系和主要功能：
    __init__:
        依赖：hash, super
        功能：初始化Task对象
    achieving_level:
        依赖：is_judgement, is_goal, is_question
        功能：计算Task对象的完成度
    reduce_budget_by_achieving_level:
        依赖：achieving_level
        功能：减少Task对象的预算
    eternalize:
        依赖：copy
        功能：将Task对象的Sentence对象永久化
    __str__:
        依赖：repr
        功能：返回Task对象的字符串表示
    __repr__:
        依赖：str
        功能：返回Task对象的字符串表示
'''

from copy import copy
from typing import Type, Union
from .Sentence import Sentence, Judgement, Goal, Quest, Question, Stamp
from .Item import Item
from .Budget import Budget
from .Term import Term
from .Truth import Truth

class Task(Item):
    input_id = -1

    def __init__(self, sentence: Sentence, budget: Budget=None, input_id: int=None) -> None:
        super().__init__(hash(sentence), budget)
        self.sentence: Sentence = sentence
        self.input_id = self.input_id if input_id is None else input_id

    def achieving_level(self, truth_belief: Truth=None):
        if self.is_judgement:
            e_belief = truth_belief.e if truth_belief is not None else 0.5
            judgement: Judgement=self.sentence
            return 1-abs(judgement.truth.e-e_belief)
        elif self.is_goal:
            e_belief = truth_belief.e if truth_belief is not None else 0.5
            goal: Goal=self.sentence
            return 1-abs(goal.truth.e-e_belief)
        elif self.is_question:
            question: Question = self.sentence
            return truth_belief.e if question.is_query else truth_belief.c
        elif self.is_quest:
            quest: Quest = self.sentence
            return truth_belief.e if quest.is_query else truth_belief.c
        else:
            raise f'Invalid type! {type(self.sentence)}'

    def reduce_budget_by_achieving_level(self, belief_selected: Union[Type['Belief'], None]):
        truth = belief_selected.truth if belief_selected is not None else None
        self.budget.reduce_by_achieving_level(self.achieving_level(truth))

    @property
    def stamp(self) -> Stamp:
        return self.sentence.stamp
    
    @property
    def evidential_base(self):
        return self.sentence.evidential_base

    @property
    def term(self) -> Term:
        return self.sentence.term
    
    @property
    def truth(self) -> Truth:
        return self.sentence.truth
    
    @property
    def is_judgement(self) -> bool:
        return self.sentence.is_judgement
    
    @property
    def is_goal(self) -> bool:
        return self.sentence.is_goal
    
    @property
    def is_question(self) -> bool:
        return self.sentence.is_question

    @property 
    def is_quest(self) -> bool:
        return self.sentence.is_quest


    @property
    def is_query(self) -> bool:
        return self.term.has_qvar and (self.is_question or self.is_quest)

    @property
    def is_eternal(self) -> bool:
        return self.sentence.is_eternal
    
    @property
    def is_event(self) -> bool:
        return self.sentence.is_event

    @property
    def is_external_event(self) -> bool:
        return self.sentence.is_external_event

    @property
    def is_operation(self) -> bool:
        return self.term.is_operation
    
    @property
    def is_mental_operation(self) -> bool:
        return self.term.is_mental_operation

    @property
    def is_executable(self):
        return self.is_goal and self.term.is_executable
    
    def eternalize(self, truth: Truth=None):
        task = copy(self)
        task.sentence = task.sentence.eternalize(truth)
        return task

    def __str__(self) -> str:
        '''$p;d;q$ sentence %f;c%'''
        return f'{(str(self.budget) if self.budget is not None else "$-;-;-$") + " "}{self.sentence.repr(False)}'

    def __repr__(self) -> str:
        return str(self)

Belief = Task
Desire = Task
