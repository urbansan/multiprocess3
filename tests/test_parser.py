import unittest
from multiprocess3.test_config import config
from multiprocess3.parser import ConfigParser
from multiprocess3.task import Task


class TestParserDependencies(unittest.TestCase):
    def setUp(self) -> None:
        parser = ConfigParser(config)
        self.deps = parser.get_dependencies()

    def test_endgroup_start(self):
        task = Task('start', 'end_group', 'sleep 0')
        deps_to_test = self.deps[task]
        self.assertEqual(len(deps_to_test), 3)

    def test_group1_end(self):
        task = Task('end', 'group1', 'sleep 0')
        deps_to_test = self.deps[task]
        self.assertEqual(len(deps_to_test), 6)

    def test_group2_end(self):
        task = Task('end', 'group2', 'sleep 0')
        deps_to_test = self.deps[task]
        self.assertEqual(len(deps_to_test), 7)

    def test_group3_end(self):
        task = Task('end', 'group3', 'sleep 0')
        deps_to_test = self.deps[task]
        self.assertEqual(len(deps_to_test), 6)

    def test_dependency_count_without_full_group_deps(self):
        for group, group_config in config.items():
            for task_name, task_config in group_config['tasks'].items():
                config_deps = task_config.get('dependencies')
                if config_deps:
                    try:
                        # A TypeError should be raised when len(None) will be called.
                        # None is a value for full group dependency:
                        # task is dependent to all task in specified group
                        deps_count = sum(len(ts) for g, ts in config_deps.items())
                        with self.subTest(task_name=task_name, group=group):
                            task = Task(task_name, group, task_config['cmd'])
                            task_deps = self.deps[task]
                            self.assertEqual(deps_count, len(task_deps))
                    except TypeError:
                        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
