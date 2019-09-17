from multiprocess3.parser import ConfigParser
from multiprocess3.task import Task



class DependencyTracker:


    def __init__(self, config):
        parser = ConfigParser(config)
        self._tasks_to_dependencies = parser.get_dependencies()





    @staticmethod
    def _validate(config):
        validations = [
            isinstance(config, dict),
        ]
        return all(validations)


    def mark_task_as_finished(self, task: Task):
        pass

    def get_available_tasks(self):
        pass


if __name__ == '__main__':
    from tests.test_config import config
    d = DependencyTracker(config)