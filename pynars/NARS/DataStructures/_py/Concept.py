'''
这个文件是PyNARS中的Concept.py，它定义了Concept类，表示NARS中的概念。Concept是NARS中的一个重要概念，它是对NARS中的Term进行封装，同时还包含了一些与Term相关的信息，如TaskLink、TermLink等。本文件中的Concept类继承自Item类，是NARS中的一个重要的数据结构。

包依赖关系：
    typing.Tuple
    typing.Type
    typing.List
    typing.Union
    pynars.NAL.Functions.Tools.calculate_solution_quality
    pynars.NAL.Functions.Tools.distribute_budget_among_links
    pynars.NAL.Functions.BudgetFunctions.Budget_merge
    pynars.Narsese.Belief
    pynars.Narsese.Task
    pynars.Narsese.Item
    pynars.Narsese.Budget
    pynars.Narsese.Sentence
    pynars.Narsese.Term
    pynars.Narsese.Judgement
    pynars.Narsese.Goal
    pynars.Narsese.place_holder
    pynars.Narsese._py.Quest
    pynars.Narsese._py.Question
    pynars.Config.Config
    pynars.Config.Enable
    pynars.Narsese.place_holder
    pynars.Narsese._py.Sentence.Quest
    pynars.Narsese._py.Sentence.Question
    pynars.NARS.PyNARS.pynars.NARS.DataStructures._py.Link.Link
    pynars.NARS.PyNARS.pynars.NARS.DataStructures._py.Link.TermLink
    pynars.NARS.PyNARS.pynars.NARS.DataStructures._py.Link.TaskLink
    pynars.NARS.PyNARS.pynars.NARS.DataStructures._py.Link.LinkType
    pynars.NARS.PyNARS.pynars.NARS.DataStructures._py.Table.Table
    pynars.NARS.PyNARS.pynars.NARS.DataStructures._py.Bag.Bag
    
全局变量名称及其作用：
    term_links: Bag
        一个Bag，用于存储TermLink，表示与该概念相关的TermLink
    question_table: Table
        一个Table，用于存储直接询问该概念的Pending Question
    quest_table: Table
        一个Table，用于存储直接询问该概念的Pending Quest
    executable_preconditions: Table
        一个Table，用于存储该概念的可执行前提
    belief_table: Table
        一个Table，用于存储直接与该概念相关的Judgment
    general_executable_preconditions: Table
        一个Table，用于存储该概念的一般可执行前提
    desire_table: Table
        一个Table，用于存储直接与该概念相关的Goal
    termLinkTemplates: List[TermLink]
        一个List，用于存储TermLink模板，只有在具有CompoundTerm的概念中才使用，以提高TermLink构建的效率
    _subterms: List[Term]
        一个List，用于存储该概念的子Term

各函数的依赖关系和主要功能：
    __init__:
        依赖：pynars.Config
        功能：初始化Concept实例
    get_belief:
        依赖：无
        功能：获取概念的信念
    match_belief:
        依赖：calculate_solution_quality
        功能：在概念的信念表中匹配一个与给定句子最匹配的信念
    match_desire:
        依赖：calculate_solution_quality
        功能：在概念的愿望表中匹配一个与给定目标最匹配的愿望
    add_belief:
        依赖：无
        功能：向概念的信念表中添加一个信念
    add_desire:
        依赖：无
        功能：向概念的愿望表中添加一个愿望
    accept:
        依赖：_build_task_links, _build_term_links, Concept._conceptualize
        功能：接受一个任务，构建任务链接和项链接
    _build_task_links:
        依赖：Concept._conceptualize
        功能：构建任务链接
    _build_term_links:
        依赖：Concept._conceptualize
    _insert_task_link:
        依赖：无
        功能：将一个任务链接插入到任务链接袋中
    _insert_term_link:
        依赖：无
        功能：将一个项链接插入到项链接袋中
    _conceptualize:
        依赖：pynars.Config, pynars.NAL.Functions.BudgetFunctions.Budget_merge, .Concept, .Link.TermLink, .Link.TaskLink, pynars.Narsese.Term, pynars.Narsese.Budget
        功能：将一个任务概念化，如果概念已经存在于内存中，则将概念合并到已存在的概念中。否则，创建一个新的概念并将其添加到内存中。
'''

from typing import Tuple, Type, List, Union
from pynars.NAL.Functions.Tools import calculate_solution_quality, distribute_budget_among_links
from pynars.NAL.Functions.BudgetFunctions import Budget_merge
from pynars.Narsese import Belief, Task, Item, Budget, Sentence, Term, Task, Judgement, Goal
from pynars.Narsese._py.Sentence import Quest, Question
# from .Link import Link, TermLink, TaskLink, LinkType
from .Link import *
from .Table import Table
from .Bag import Bag
from pynars.Config import Config, Enable
from pynars.Narsese import place_holder


class Concept(Item):
    '''Ref: OpenNARS 3.0.4 Concept.java'''

    # seq_before: Bag # Recent events that happened before the operation the concept represents was executed. 
    task_links: Bag
    term_links: Bag

    # *Note*: since this is iterated frequently, an array should be used. To avoid iterator allocation, use .get(n) in a for-loop
    question_table: Table # Pending Question directly asked about the term
    quest_table: Table # Pending Question directly asked about the term
    executable_preconditions: Table
    belief_table: Table # Judgments directly made about the term Use List because of access and insertion in the middle
    general_executable_preconditions: Table
    
    desire_table: Table # Desire values on the term, similar to the above one

    termLinkTemplates: List[TermLink] # Link templates of TermLink, only in concepts with CompoundTerm Templates are used to improve the efficiency of TermLink building

    _subterms: List[Term]


    def __init__(self, term: Term, budget: Budget, capacity_table: int=None) -> None:
        super().__init__(hash(term), budget)
        self._term = term

        capacity_table = Config.capacity_table if capacity_table is None else capacity_table
        nlevels_term_link_bag = Config.nlevels_term_link
        capacity_term_link_bag = Config.capacity_term_link
        nlevels_task_link_bag = Config.nlevels_task_link
        capacity_task_link_bag = Config.capacity_task_link

        self._term = term
        self.belief_table = Table(capacity_table) 
        self.desire_table = Table(capacity_table) 
        self.question_table = Table(capacity_table)
        self.quest_table = Table(capacity_table)
        self.term_links = Bag(capacity_term_link_bag, nlevels_term_link_bag)
        self.task_links = Bag(capacity_task_link_bag, nlevels_task_link_bag)

        self.executable_preconditions = Table(capacity_table)
        self.general_executable_preconditions = Table(capacity_table)

        self.task_links = Bag(Config.capacity_task_link, Config.nlevels_task_link)
        self.term_links = Bag(Config.capacity_term_link, Config.nlevels_term_link)

        # self._cache_subterms()
        # self.accept(task)

    @property
    def term(self) -> Term:
        return self._term

    def get_belief(self) -> Belief:
        ''''''
        if Enable.temporal_rasoning:
            #  final Sentence belief = beliefT.sentence;
            # nal.emit(BeliefSelect.class, belief);
            # nal.setTheNewStamp(taskStamp, belief.stamp, currentTime);
            
            # final Sentence projectedBelief = belief.projection(taskStamp.getOccurrenceTime(), nal.time.time(), nal.memory);
            # /*if (projectedBelief.getOccurenceTime() != belief.getOccurenceTime()) {
            #    nal.singlePremiseTask(projectedBelief, task.budget);
            # }*/
            
            # return projectedBelief;     // return the first satisfying belief
            raise
        return self.belief_table.first()

    # def match_candidate(self, sentence: Sentence) -> Task | Belief:
    #     if sentence.is_judgement:
    #         return self.match_belief(sentence)
    #     elif sentence.is_goal:
    #         return self.match_desire(sentence)
    #     else:
    #         raise "Invalid type." # TODO: What about question and quest?

    def match_belief(self, sentence: Union[Judgement, Question]) -> Belief:
        '''
        Select a belief with highest quality, within the belief_table, according to the task
        '''
        belief_table: List[Task] = self.belief_table
        if len(belief_table) == 0: return None
        qualities = [(calculate_solution_quality(sentence, task.sentence), task) for task in belief_table]
        _, item_max = max(qualities, key=lambda quality: quality[0])
        return item_max
        
    def match_desire(self, goal: Goal) -> Task:
        '''
        Select a desire with highest quality, within the desire_table, according to the task
        '''
        desire_table: List[Tuple[Task, float]] = self.desire_table
        if len(desire_table) == 0: return None
        qualities = [(calculate_solution_quality(goal, task.sentence), task) for task in desire_table]
        _, item_max = max(qualities, key=lambda quality: quality[0])
        return item_max
        
    def add_belief(self, task: Task) -> Union[Judgement, None]:
        ''''''
        self.belief_table.add(task, task.truth.c)

    def add_desire(self, task: Task) -> Union[Task, None]:
        ''''''
        # goal: Goal = task.sentence
        self.desire_table.add(task, task.truth.c)

    def accept(self, task: Task, concepts: Bag=None, conceptualize: bool=True):
        '''
        Ref: The Conceptual Design of OpenNARS 3.1.0
            **accept task-link:** Pre-process the task using the information local to the con-
            cept, then add the link into the task-link bag so as to process it repeatedly
            in the future.
        '''
        # if task.is_judgement:
        #     self.belief_table.add(task, task.sentence.truth.c)
        if concepts is None: return

        budget = task.budget
        if budget.is_above_thresh:
            if conceptualize:
                concept = Concept._conceptualize(concepts, self.term, budget)
                if concept is None: return # The memroy is full, and the concept fails to get into the memory.
            self._build_task_links(concepts, task)
            self._build_term_links(concepts, task, budget)
    
    def _build_task_links(self, concepts: Bag, task: Task):
        ''''''
        budget = task.budget
        task_link = TaskLink(self, task, budget, True, index=[])
        self._insert_task_link(task_link)
        if self.term.is_atom: return
        sub_budget = budget.distribute(self.term.count()-1) # TODO: It seems that the budget is not the same with that in OpenNARS 3.0.4/3.1.0. Check here.
        for term in self.term.components:
            if term == place_holder: continue # should it skip the `place_holder?`
            concept = Concept._conceptualize(concepts, term, sub_budget)
            if concept is None: continue
            
            indices = Link.get_index(self.term, term)
            for index in indices:
                task_link = TaskLink(concept, task, sub_budget, index=index)
                concept._insert_task_link(task_link)

    def _build_term_links(self, concepts: Bag, task: Task, budget: Budget):
        '''
        Get component-terms to be concepualized and build links by DFS (Depth-Fist-Search).
        '''
        if self.term.count() == 1: return # atomic term

        sub_budget = budget.distribute(self.term.count()-1) # TODO: in the case that there are some terms not being used to build term-links, the count here is not valid, which should be modified.
        if sub_budget.is_above_thresh:
            if self.term.is_atom: return
            
            for term in self.term.components:
                if term == place_holder: continue # should it skip the `place_holder?`
                
                # Option 1
                # # in _build_task_links(...), the terms all have been conceptualized.
                # # therefore, here if a concept is not in memory, it should not be used for term-links construction.
                # sub_concept: Concept = concepts.take_by_key(term, False) 

                # Option 2
                # again, conceptualize
                sub_concept: Concept = Concept._conceptualize(concepts, term, task.budget)
                if sub_concept is None: continue

                indices = Link.get_index(self.term, term)
                for index in indices:
                    self._insert_term_link(TermLink(self, sub_concept, sub_budget, False, index=index))
                    sub_concept._insert_term_link(TermLink(sub_concept, self, sub_budget, True, index=index))

                    sub_concept._build_term_links(concepts, task, sub_budget)
        

    def _insert_task_link(self, task_link: TaskLink):
        self.task_links.put(task_link)
        # TODO: more handling. see OpenNARS 3.1.0 Concept.java line 318~366.
    
    def _insert_term_link(self, term_link: TermLink):
        self.term_links.put(term_link)
        # TODO: more handling. see OpenNARS 3.1.0 Concept.java line 318~366.

    @classmethod
    def _conceptualize(cls, concepts: Bag, term: Term, budget: Budget):
        '''
        Conceptualize a task. 
        If the concept of the task is already in the memory, then merge the concept into the existed one.
        Otherwise, make up a new concept and add it into the memory.
        '''
        if Enable.temporal_rasoning:
            # if(term instanceof Interval) {
            #     return null;
            # }
            # term = CompoundTerm.replaceIntervals(term);
            raise # TODO

        if term.is_var: return None
        
        concept = concepts.take_by_key(term, True) # take the concept from the bag

        if concept is not None:
            Budget_merge(concept.budget, budget) # Merge the term into the concept if the concept has existed
            # Note: The budget handling here is sort of different from that in OpenNARS 3.1.0, see `Memory.java line 207` and `BudgetFunction.java line 167~170` in OpenNARS 3.1.0.
        else:
            concept = Concept(term, budget) # build the current concept if there has not been the concept in the bag

        concept_popped = concepts.put_back(concept) # TODO: Check here. `put` or `put_back`?
        if concept_popped is not None and concept == concept_popped:
            concept = None
        return concept

    def __eq__(self, concept: Type['Concept']):
        return concept.term == self.term
        
    def __hash__(self):
        return hash(self.term)

    def __str__(self):
        return f'{self.budget} {self.term}'

    def __repr__(self):
        return f'<Concept: {self.term.repr()}>'
