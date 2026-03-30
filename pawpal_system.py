from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


@dataclass
class Task:
    task_name: str
    description: Optional[str] = None
    priority: Optional[int] = None
    time: Optional[str] = None
    frequency: Optional[str] = None
    completed: bool = False
    due_date: Optional[date] = None

    def set_description(self, description: str):
        self.description = description

    def set_priority(self, priority: int):
        self.priority = priority

    def set_time(self, time: str):
        self.time = time

    def set_frequency(self, frequency: str):
        self.frequency = frequency

    def set_completed(self, completed: bool):
        self.completed = completed

    def set_due_date(self, due_date: date):
        self.due_date = due_date


@dataclass
class Pet:
    pet_name: str
    age: Optional[int] = None
    type: Optional[str] = None
    tasks: list[Task] = field(default_factory=list)

    def set_age(self, age: int):
        self.age = age

    def set_type(self, type: str):
        self.type = type

    def add_task(self, task: Task):
        self.tasks.append(task)

    def delete_task(self, task: Task):
        if task in self.tasks:
            self.tasks.remove(task)

    def task_count(self) -> int:
        return len(self.tasks)


@dataclass
class BlockTime:
    constraint_name: str
    block_start: Optional[str] = None
    block_end: Optional[str] = None
    priority: Optional[int] = None
    description: Optional[str] = None

    def set_block_time(self, start_time: str, end_time: str):
        self.block_start = start_time
        self.block_end = end_time

    def change_priority(self, priority: int):
        self.priority = priority

    def set_description(self, description: str):
        self.description = description


@dataclass
class PreferredTime:
    constraint_name: str
    preferred_start: Optional[str] = None
    preferred_end: Optional[str] = None
    priority: Optional[int] = None
    description: Optional[str] = None

    def set_preferred_time(self, start_time: str, end_time: str):
        self.preferred_start = start_time
        self.preferred_end = end_time

    def change_priority(self, priority: int):
        self.priority = priority

    def set_description(self, description: str):
        self.description = description


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: list[Pet] = []
        self.block_times: list[BlockTime] = []
        self.preferred_times: list[PreferredTime] = []

    def change_name(self, new_name: str):
        self.name = new_name

    def delete_owner(self):
        self.pets.clear()
        self.block_times.clear()
        self.preferred_times.clear()

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def delete_pet(self, pet: Pet):
        if pet in self.pets:
            self.pets.remove(pet)

    def add_block_time(self, block_time: BlockTime):
        self.block_times.append(block_time)

    def delete_block_time(self, block_time: BlockTime):
        if block_time in self.block_times:
            self.block_times.remove(block_time)

    def add_preferred_time(self, preferred_time: PreferredTime):
        self.preferred_times.append(preferred_time)

    def delete_preferred_time(self, preferred_time: PreferredTime):
        if preferred_time in self.preferred_times:
            self.preferred_times.remove(preferred_time)


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        all_tasks = []
        for pet in self.owner.pets:
            for task in pet.tasks:
                all_tasks.append((pet, task))
        return all_tasks

    def sort_by_time(self) -> list[tuple[Pet, Task]]:
        """Return all (Pet, Task) pairs sorted chronologically by HH:MM time string.

        Uses a lambda key of ``(time is None, time)`` so that tasks with a
        time value are sorted lexicographically first (which is correct for
        zero-padded 24-hour strings such as "07:00" < "18:00"), and tasks
        whose ``time`` is ``None`` are pushed to the end.

        Returns:
            A new list of ``(Pet, Task)`` tuples ordered earliest-to-latest,
            with un-timed tasks appended after all timed ones.
        """
        return sorted(
            self.get_all_tasks(),
            key=lambda pair: (pair[1].time is None, pair[1].time),
        )

    def get_all_tasks_sorted(self) -> list[tuple[Pet, Task]]:
        """Return all tasks sorted chronologically by time. Tasks with no time go last."""
        return self.sort_by_time()

    def filter_by_pet_name(self, pet_name: str) -> list[tuple[Pet, Task]]:
        """Return all (Pet, Task) pairs whose pet name matches ``pet_name``.

        The comparison is case-insensitive, so ``"buddy"`` and ``"Buddy"``
        both match a pet named ``"Buddy"``.

        Args:
            pet_name: The name of the pet to filter by.

        Returns:
            A list of ``(Pet, Task)`` tuples for every task belonging to a
            pet whose name matches ``pet_name``.  Returns an empty list if
            no pet with that name exists.
        """
        return [(p, t) for p, t in self.get_all_tasks() if p.pet_name.lower() == pet_name.lower()]

    def mark_task_complete(self, pet: Pet, task: Task) -> Optional[Task]:
        """Mark a task complete and automatically schedule the next occurrence.

        For tasks with a ``frequency`` of ``"daily"`` or ``"weekly"``, a fresh
        ``Task`` is created with the same properties and a ``due_date`` advanced
        by the appropriate ``timedelta`` (1 day or 7 days).  The new task is
        added to ``pet`` and returned.

        If ``task.due_date`` is ``None``, today's date is used as the base for
        the calculation so the result is always a valid future date.

        Args:
            pet:  The ``Pet`` that owns the task.
            task: The ``Task`` being completed.

        Returns:
            The newly created next-occurrence ``Task``, or ``None`` if the
            task's frequency is not ``"daily"`` or ``"weekly"`` (i.e., it does
            not repeat).
        """
        task.set_completed(True)

        delta_map = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}
        delta = delta_map.get(task.frequency)
        if delta is None:
            return None

        base = task.due_date if task.due_date is not None else date.today()
        next_task = Task(
            task_name=task.task_name,
            description=task.description,
            priority=task.priority,
            time=task.time,
            frequency=task.frequency,
            completed=False,
            due_date=base + delta,
        )
        pet.add_task(next_task)
        return next_task

    def complete_daily_task(self, pet: Pet, task: Task) -> Optional[Task]:
        """Mark a daily task complete and add a fresh copy for the next day.
        Returns the new task, or None if the task is not daily."""
        task.set_completed(True)
        if task.frequency != "daily":
            return None
        next_task = Task(
            task_name=task.task_name,
            description=task.description,
            priority=task.priority,
            time=task.time,
            frequency=task.frequency,
            completed=False,
        )
        pet.add_task(next_task)
        return next_task

    def get_time_conflicts(self) -> dict[str, list[tuple[Pet, Task]]]:
        """Return a dict mapping time strings to lists of (Pet, Task) pairs
        that share that time. Only times with more than one task are included."""
        time_map: dict[str, list[tuple[Pet, Task]]] = {}
        for pet, task in self.get_all_tasks():
            if task.time is None:
                continue
            time_map.setdefault(task.time, []).append((pet, task))
        return {t: pairs for t, pairs in time_map.items() if len(pairs) > 1}

    def get_conflict_warnings(self) -> list[str]:
        """Return human-readable warning strings for every conflicting time slot.

        Delegates to :meth:`get_time_conflicts` for the raw conflict data, then
        formats each conflicting slot into a plain sentence that names every
        overlapping task and the pet it belongs to.  The method never raises —
        if the schedule is clean it simply returns an empty list.

        Returns:
            A list of warning strings, one per conflicting time slot.  Each
            string identifies the time, the number of clashing tasks, and
            suggests rescheduling.  Returns ``[]`` when no conflicts exist.
        """
        warnings = []
        for time_slot, pairs in self.get_time_conflicts().items():
            names = ", ".join(
                f"'{task.task_name}' ({pet.pet_name})" for pet, task in pairs
            )
            warnings.append(
                f"WARNING: {len(pairs)} tasks share the same time {time_slot} — {names}. "
                f"Consider rescheduling one of them."
            )
        return warnings

    def get_tasks_for_pet(self, pet: Pet) -> list[tuple[Pet, Task]]:
        """Return all (Pet, Task) pairs belonging to the given pet."""
        return [(p, t) for p, t in self.get_all_tasks() if p is pet]

    def get_tasks_by_status(self, completed: bool) -> list[tuple[Pet, Task]]:
        """Return all (Pet, Task) pairs whose completed flag matches the given value."""
        return [(p, t) for p, t in self.get_all_tasks() if t.completed == completed]

