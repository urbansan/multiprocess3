from dataclasses import dataclass


class Status:
    not_started = 0
    running = 1
    finished = 2
    error = -1


@dataclass
class Task:
    name: str
    group: str
    command: str
    def __post_init__(self):
        self.status = Status.not_started

    @property
    def unique_name(self):
        return f'{self.group}_{self.name}'

    def __repr__(self):
        return f'{type(self).__name__}(name={self.name}, group={self.group})'

    def __hash__(self):
        return hash((self.name, self.group, self.command, self.status))

    def __eq__(self, other):
        return hash(self) == hash(other)
