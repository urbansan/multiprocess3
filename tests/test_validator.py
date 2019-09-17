import unittest
from multiprocess3.tests.test_config import config
from multiprocess3.validator import DependencyValidator
from multiprocess3.task import Task
from multiprocess3.exceptions import ValidationError


class TestDependencyValidator(unittest.TestCase):
    def test_cyclic_deps(self):
        t1 = Task('t1', 'g1', 'true')
        t2 = Task('t2', 'g1', 'true')
        t3 = Task('t3', 'g1', 'true')

        deps = dict()
        deps[t1] = {t3}
        deps[t3] = {t2}
        deps[t2] = {t1}

        validator = DependencyValidator(deps)
        with self.assertRaises(ValidationError):
            validator.search_for_cyclic_dependencies()


