from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    task_name: str
    description: Optional[str] = None
    priority: Optional[str] = None

    def set_description(self, description: str):
        pass

    def set_priority(self, priority: str):
        pass


@dataclass
class Pet:
    pet_name: str
    age: Optional[int] = None
    type: Optional[str] = None
    tasks: list[Task] = field(default_factory=list)

    def set_age(self, age: int):
        pass

    def set_type(self, type: str):
        pass

    def add_task(self, task: Task):
        pass

    def delete_task(self, task: Task):
        pass


@dataclass
class Constraint:
    constraint_name: str
    description: Optional[str] = None
    priority: Optional[str] = None
    block_start: Optional[str] = None
    block_end: Optional[str] = None
    preferred_start: Optional[str] = None
    preferred_end: Optional[str] = None

    def remove_constraint(self):
        pass

    def set_block_time(self, start_time: str, end_time: str):
        pass

    def set_preferred_time(self, start_time: str, end_time: str):
        pass

    def change_priority(self, priority: str):
        pass

    def set_description(self, description: str):
        pass


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: list[Pet] = []
        self.constraints: list[Constraint] = []

    def delete_owner(self):
        pass

    def add_pet(self, pet: Pet):
        pass

    def delete_pet(self, pet: Pet):
        pass

    def add_constraint(self, constraint: Constraint):
        pass

    def change_name(self, new_name: str):
        pass
