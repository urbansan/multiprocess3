from collections import defaultdict
from multiprocess3.task import Task
from typing import Set


class ValidationError(Exception):
    pass


class ConfigParser:
    def __init__(self, config):
        self._config = config

    @property
    def config(self):
        return self._config

    def get_dependencies(self):

        unique_tasks = self._build_tasks()
        tasks_to_dependencies = self._build_dependencies(unique_tasks)
        return tasks_to_dependencies

    def _build_tasks(self):
        unique_tasks = set()
        for group_name, group_config in self.config.items():
            for task_name, task_config in group_config['tasks'].items():
                task = Task(task_name,
                            group_name,
                            task_config['cmd'])

                if task in unique_tasks:
                    raise ValidationError('There are 2 Task objects with identical signature: {task}')
                else:
                    unique_tasks.add(task)
        return unique_tasks

    def _group_tasks_by_group_and_taskname(self, unique_tasks: Set[Task]):
        grouping = defaultdict(dict)
        for task in unique_tasks:
            grouping[task.group][task.name] = task
        return grouping

    def _build_dependencies(self, unique_tasks):
        grouped = self._group_tasks_by_group_and_taskname(unique_tasks)
        task_to_dependent_task = defaultdict(set)
        for analyzed_task in unique_tasks:
            deps = self.config[analyzed_task.group]['tasks'][analyzed_task.name].get('dependencies')
            if deps:
                for dep_group_name, dep_task_names in deps.items():
                    if not dep_task_names:
                        try:
                            dep_tasks = grouped[dep_group_name].values()
                            dep_tasks = set(dep_tasks)
                            dep_tasks.discard(analyzed_task)
                        except KeyError:
                            raise ValidationError(f'Invalid group in dependencies: "{dep_group_name}"')
                    else:
                        dep_tasks = set()
                        for dep_task in dep_task_names:
                            try:
                                dep_task = grouped[dep_group_name][dep_task]
                            except KeyError:
                                raise ValidationError(f'Invalid group "{dep_group_name}" and/or '
                                                           f'task "{dep_task}" in dependencies.')
                            dep_tasks.add(dep_task)
                        dep_tasks.discard(analyzed_task)
                    task_to_dependent_task[analyzed_task].update(dep_tasks)

        return task_to_dependent_task

if __name__ == '__main__':
    from multiprocess3.test_config import config
    parser = ConfigParser(config)
    deps = parser.get_dependencies()
    from pprint import pprint as pp

    # task = Task('start', 'end_group', 'sleep 0')
    # pp(deps[task])
    pp(deps)