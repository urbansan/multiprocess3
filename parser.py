from collections import defaultdict
from multiprocess3.task import Task
from typing import Set


class ValidationError(Exception):
    pass


class ConfigParser:
    def __init__(self, config):
        self._config = config
        self._unique_tasks = self._build_tasks()
        self._grouped = self._group_tasks_by_group_and_taskname()

    @property
    def unique_tasks(self):
        return self._unique_tasks

    @property
    def config(self):
        return self._config

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

    def _group_tasks_by_group_and_taskname(self):
        grouping = defaultdict(dict)
        for task in self.unique_tasks:
            grouping[task.group][task.name] = task
        return grouping

    def get_dependencies(self):
        task_to_dependent_task = defaultdict(set)
        for analyzed_task in self.unique_tasks:
            config_deps = self.config[analyzed_task.group]['tasks'] \
                                     [analyzed_task.name].get('dependencies')
            if config_deps:
                dependent_tasks = self._parse_config_dependencies(config_deps)
                dependent_tasks.discard(analyzed_task)
                task_to_dependent_task[analyzed_task].update(dependent_tasks)
        return task_to_dependent_task

    def _parse_config_dependencies(self, deps):
        all_tasks = set()
        for dep_group_name, dep_task_names in deps.items():
            tasks = self._parse_config_dependency_line(dep_group_name, dep_task_names)
            all_tasks.update(tasks)
        return all_tasks

    def _parse_config_dependency_line(self, group, task_names):
        if not task_names:
            dep_tasks = self._get_all_tasks_from_group(group)
        else:
            dep_tasks = self._get_selected_tasks_from_group(group, task_names)
        return dep_tasks

    def _get_selected_tasks_from_group(self, group, task_names):
        dep_tasks = set()
        for dep_task in task_names:
            try:
                dep_task = self._grouped[group][dep_task]
            except KeyError:
                raise ValidationError(f'Invalid group "{group}" and/or '
                                      f'task "{dep_task}" in dependencies.')
            dep_tasks.add(dep_task)

        return dep_tasks

    def _get_all_tasks_from_group(self, group):
        try:
            dep_tasks = self._grouped[group].values()
            dep_tasks = set(dep_tasks)
        except KeyError:
            raise ValidationError(f'Invalid group in dependencies: "{group}"')

        return dep_tasks


if __name__ == '__main__':
    from tests.test_config import config
    parser = ConfigParser(config)
    deps = parser.get_dependencies()
    from pprint import pprint as pp

    # task = Task('start', 'end_group', 'sleep 0')
    # pp(deps[task])
    pp(deps)