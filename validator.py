from multiprocess3.task import Task
from typing import Dict, Set
from multiprocess3.exceptions import ValidationError
from itertools import chain

class DependencyValidator:
    def __init__(self, dependencies: Dict[Task, Set[Task]]):
        self._deps = dependencies

    @property
    def deps(self):
        return self._deps

    def _get_peripherial_tasks(self):
        all_tasks_in_deps = set(chain.from_iterable(self.deps))
        all_tasks_which_have_deps = set(self.deps)
        peripherial = all_tasks_which_have_deps - all_tasks_in_deps
        return peripherial



    def search_for_unavailable_tasks(self):
        pass

    def search_for_cyclic_dependencies(self):
        pass

