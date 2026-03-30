from pawpal_system import Task, Pet, BlockTime, PreferredTime, Owner, Scheduler


def make_owner_with_tasks(*task_defs) -> tuple[Owner, Pet, Scheduler]:
    """Helper: build an owner/pet/scheduler with tasks from (name, time, priority) tuples."""
    owner = Owner("Jordan")
    pet = Pet(pet_name="Mochi")
    for name, time, priority in task_defs:
        t = Task(task_name=name, time=time, priority=priority)
        pet.add_task(t)
    owner.add_pet(pet)
    return owner, pet, Scheduler(owner)


# --- Task ---

def test_task_defaults():
    t = Task(task_name="Feed")
    assert t.description is None
    assert t.priority is None
    assert t.time is None
    assert t.frequency is None
    assert t.completed is False


def test_task_setters():
    t = Task(task_name="Walk")
    t.set_description("Morning walk")
    t.set_priority(2)
    t.set_time("08:00")
    t.set_frequency("daily")
    t.set_completed(True)
    assert t.description == "Morning walk"
    assert t.priority == 2
    assert t.time == "08:00"
    assert t.frequency == "daily"
    assert t.completed is True


# --- Pet ---

def test_pet_add_task():
    pet = Pet(pet_name="Mochi")
    t = Task(task_name="Feed")
    pet.add_task(t)
    assert t in pet.tasks
    assert pet.task_count() == 1


def test_pet_delete_task():
    pet = Pet(pet_name="Mochi")
    t = Task(task_name="Feed")
    pet.add_task(t)
    pet.delete_task(t)
    assert pet.task_count() == 0


def test_pet_delete_task_not_in_list():
    pet = Pet(pet_name="Mochi")
    t = Task(task_name="Feed")
    # Should not raise
    pet.delete_task(t)
    assert pet.task_count() == 0


def test_pet_task_count_after_add_and_delete():
    pet = Pet(pet_name="Mochi")
    t1 = Task(task_name="Feed")
    t2 = Task(task_name="Walk")
    pet.add_task(t1)
    pet.add_task(t2)
    assert pet.task_count() == 2
    pet.delete_task(t1)
    assert pet.task_count() == 1


def test_pet_add_same_task_twice():
    pet = Pet(pet_name="Mochi")
    t = Task(task_name="Feed")
    pet.add_task(t)
    pet.add_task(t)
    assert pet.task_count() == 2


def test_pet_no_tasks_by_default():
    pet = Pet(pet_name="Mochi")
    assert pet.task_count() == 0
    assert pet.tasks == []


# --- Owner ---

def test_owner_add_and_delete_pet():
    owner = Owner("Jordan")
    pet = Pet(pet_name="Mochi")
    owner.add_pet(pet)
    assert pet in owner.pets
    owner.delete_pet(pet)
    assert pet not in owner.pets


def test_owner_delete_pet_not_in_list():
    owner = Owner("Jordan")
    pet = Pet(pet_name="Mochi")
    # Should not raise
    owner.delete_pet(pet)


def test_owner_add_and_delete_block_time():
    owner = Owner("Jordan")
    bt = BlockTime(constraint_name="Sleep")
    owner.add_block_time(bt)
    assert bt in owner.block_times
    owner.delete_block_time(bt)
    assert bt not in owner.block_times


def test_owner_delete_block_time_not_in_list():
    owner = Owner("Jordan")
    bt = BlockTime(constraint_name="Sleep")
    owner.delete_block_time(bt)  # Should not raise


def test_owner_add_and_delete_preferred_time():
    owner = Owner("Jordan")
    pt = PreferredTime(constraint_name="Morning")
    owner.add_preferred_time(pt)
    assert pt in owner.preferred_times
    owner.delete_preferred_time(pt)
    assert pt not in owner.preferred_times


def test_owner_delete_owner_clears_all():
    owner = Owner("Jordan")
    owner.add_pet(Pet(pet_name="Mochi"))
    owner.add_block_time(BlockTime(constraint_name="Sleep"))
    owner.add_preferred_time(PreferredTime(constraint_name="Morning"))
    owner.delete_owner()
    assert owner.pets == []
    assert owner.block_times == []
    assert owner.preferred_times == []


def test_owner_change_name():
    owner = Owner("Jordan")
    owner.change_name("Alex")
    assert owner.name == "Alex"


# --- Scheduler ---

def test_scheduler_no_pets():
    owner = Owner("Jordan")
    scheduler = Scheduler(owner)
    assert scheduler.get_all_tasks() == []


def test_scheduler_pet_with_no_tasks():
    owner = Owner("Jordan")
    owner.add_pet(Pet(pet_name="Mochi"))
    scheduler = Scheduler(owner)
    assert scheduler.get_all_tasks() == []


def test_scheduler_single_pet_single_task():
    owner = Owner("Jordan")
    pet = Pet(pet_name="Mochi")
    t = Task(task_name="Feed")
    pet.add_task(t)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    result = scheduler.get_all_tasks()
    assert len(result) == 1
    assert result[0] == (pet, t)


def test_scheduler_multiple_pets():
    owner = Owner("Jordan")
    pet1 = Pet(pet_name="Mochi")
    pet2 = Pet(pet_name="Luna")
    t1 = Task(task_name="Feed")
    t2 = Task(task_name="Walk")
    pet1.add_task(t1)
    pet2.add_task(t2)
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    scheduler = Scheduler(owner)
    result = scheduler.get_all_tasks()
    assert len(result) == 2
    assert (pet1, t1) in result
    assert (pet2, t2) in result


def test_scheduler_multiple_pets_overlapping_task_names():
    owner = Owner("Jordan")
    pet1 = Pet(pet_name="Mochi")
    pet2 = Pet(pet_name="Luna")
    t1 = Task(task_name="Feed")
    t2 = Task(task_name="Feed")
    pet1.add_task(t1)
    pet2.add_task(t2)
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    scheduler = Scheduler(owner)
    result = scheduler.get_all_tasks()
    assert len(result) == 2


def test_scheduler_returns_all_tasks_for_multiple_tasks_per_pet():
    owner = Owner("Jordan")
    pet = Pet(pet_name="Mochi")
    tasks = [Task(task_name=f"Task{i}") for i in range(3)]
    for t in tasks:
        pet.add_task(t)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    result = scheduler.get_all_tasks()
    assert len(result) == 3
    for t in tasks:
        assert (pet, t) in result


# --- Sorting edge cases (priority) ---

def test_tasks_sorted_by_priority():
    tasks = [
        Task(task_name="Low", priority=3),
        Task(task_name="High", priority=1),
        Task(task_name="Mid", priority=2),
    ]
    sorted_tasks = sorted(tasks, key=lambda t: t.priority)
    assert [t.task_name for t in sorted_tasks] == ["High", "Mid", "Low"]


def test_tasks_equal_priority_preserves_order():
    tasks = [
        Task(task_name="First", priority=1),
        Task(task_name="Second", priority=1),
        Task(task_name="Third", priority=1),
    ]
    sorted_tasks = sorted(tasks, key=lambda t: t.priority)
    assert [t.task_name for t in sorted_tasks] == ["First", "Second", "Third"]


def test_tasks_sort_none_priority_last():
    tasks = [
        Task(task_name="NoPriority", priority=None),
        Task(task_name="High", priority=1),
        Task(task_name="Low", priority=5),
    ]
    sorted_tasks = sorted(tasks, key=lambda t: (t.priority is None, t.priority))
    assert sorted_tasks[0].task_name == "High"
    assert sorted_tasks[1].task_name == "Low"
    assert sorted_tasks[2].task_name == "NoPriority"


def test_tasks_all_none_priority_no_crash():
    tasks = [Task(task_name=f"Task{i}") for i in range(3)]
    # Should not raise when all priorities are None
    sorted_tasks = sorted(tasks, key=lambda t: (t.priority is None, t.priority))
    assert len(sorted_tasks) == 3


# --- Recurring task edge cases ---

def test_completed_task_can_be_reset():
    t = Task(task_name="Walk", frequency="daily")
    t.set_completed(True)
    assert t.completed is True
    t.set_completed(False)
    assert t.completed is False


def test_daily_task_frequency_value():
    t = Task(task_name="Walk")
    t.set_frequency("daily")
    assert t.frequency == "daily"


def test_task_frequency_none_by_default():
    t = Task(task_name="Walk")
    assert t.frequency is None


# --- BlockTime / PreferredTime ---

def test_block_time_set_times():
    bt = BlockTime(constraint_name="Sleep")
    bt.set_block_time("22:00", "06:00")
    assert bt.block_start == "22:00"
    assert bt.block_end == "06:00"


def test_block_time_change_priority():
    bt = BlockTime(constraint_name="Sleep")
    bt.change_priority(1)
    assert bt.priority == 1


def test_preferred_time_set_times():
    pt = PreferredTime(constraint_name="Morning")
    pt.set_preferred_time("07:00", "09:00")
    assert pt.preferred_start == "07:00"
    assert pt.preferred_end == "09:00"


def test_preferred_time_change_priority():
    pt = PreferredTime(constraint_name="Morning")
    pt.change_priority(2)
    assert pt.priority == 2


# --- Sorting Correctness: chronological order ---

def test_sorted_tasks_chronological_order():
    _, _, scheduler = make_owner_with_tasks(
        ("Dinner",  "18:00", 1),
        ("Walk",    "07:00", 1),
        ("Lunch",   "12:00", 1),
    )
    result = scheduler.get_all_tasks_sorted()
    times = [task.time for _, task in result]
    assert times == ["07:00", "12:00", "18:00"]


def test_sorted_tasks_already_in_order():
    _, _, scheduler = make_owner_with_tasks(
        ("Feed",  "08:00", 1),
        ("Walk",  "10:00", 1),
        ("Meds",  "20:00", 1),
    )
    result = scheduler.get_all_tasks_sorted()
    times = [task.time for _, task in result]
    assert times == ["08:00", "10:00", "20:00"]


def test_sorted_tasks_none_time_goes_last():
    _, _, scheduler = make_owner_with_tasks(
        ("Unknown", None,    1),
        ("Walk",    "07:00", 1),
        ("Dinner",  "18:00", 1),
    )
    result = scheduler.get_all_tasks_sorted()
    times = [task.time for _, task in result]
    assert times == ["07:00", "18:00", None]


def test_sorted_tasks_all_none_times_no_crash():
    _, _, scheduler = make_owner_with_tasks(
        ("A", None, 1),
        ("B", None, 1),
    )
    result = scheduler.get_all_tasks_sorted()
    assert len(result) == 2


def test_sorted_tasks_across_multiple_pets():
    owner = Owner("Jordan")
    pet1 = Pet(pet_name="Mochi")
    pet2 = Pet(pet_name="Luna")
    t1 = Task(task_name="EarlyTask", time="06:00")
    t2 = Task(task_name="LateTask",  time="20:00")
    pet1.add_task(t2)   # added late task to first pet
    pet2.add_task(t1)   # added early task to second pet
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    scheduler = Scheduler(owner)
    result = scheduler.get_all_tasks_sorted()
    assert result[0][1].task_name == "EarlyTask"
    assert result[1][1].task_name == "LateTask"


# --- Recurrence Logic: daily task spawns next-day task on completion ---

def test_complete_daily_task_marks_original_done():
    _, pet, scheduler = make_owner_with_tasks(("Walk", "08:00", 1))
    task = pet.tasks[0]
    task.set_frequency("daily")
    scheduler.complete_daily_task(pet, task)
    assert task.completed is True


def test_complete_daily_task_adds_new_task():
    _, pet, scheduler = make_owner_with_tasks(("Walk", "08:00", 1))
    task = pet.tasks[0]
    task.set_frequency("daily")
    scheduler.complete_daily_task(pet, task)
    assert pet.task_count() == 2


def test_complete_daily_task_new_task_is_not_completed():
    _, pet, scheduler = make_owner_with_tasks(("Walk", "08:00", 1))
    task = pet.tasks[0]
    task.set_frequency("daily")
    new_task = scheduler.complete_daily_task(pet, task)
    assert new_task is not None
    assert new_task.completed is False


def test_complete_daily_task_new_task_inherits_properties():
    _, pet, scheduler = make_owner_with_tasks(("Walk", "08:00", 2))
    task = pet.tasks[0]
    task.set_frequency("daily")
    task.set_description("Morning walk")
    new_task = scheduler.complete_daily_task(pet, task)
    assert new_task.task_name == "Walk"
    assert new_task.time == "08:00"
    assert new_task.priority == 2
    assert new_task.frequency == "daily"
    assert new_task.description == "Morning walk"


def test_complete_non_daily_task_does_not_add_new_task():
    _, pet, scheduler = make_owner_with_tasks(("Vet", "10:00", 1))
    task = pet.tasks[0]
    task.set_frequency("as needed")
    result = scheduler.complete_daily_task(pet, task)
    assert result is None
    assert pet.task_count() == 1   # no new task added


def test_complete_task_with_no_frequency_does_not_add_new_task():
    _, pet, scheduler = make_owner_with_tasks(("Vet", "10:00", 1))
    task = pet.tasks[0]
    # frequency remains None
    result = scheduler.complete_daily_task(pet, task)
    assert result is None
    assert pet.task_count() == 1


# --- Conflict Detection: duplicate time slots ---

def test_no_conflicts_when_all_times_unique():
    _, _, scheduler = make_owner_with_tasks(
        ("Feed", "08:00", 1),
        ("Walk", "10:00", 1),
    )
    assert scheduler.get_time_conflicts() == {}


def test_detects_conflict_same_time_same_pet():
    _, _, scheduler = make_owner_with_tasks(
        ("Feed",  "08:00", 1),
        ("Meds",  "08:00", 2),
        ("Walk",  "10:00", 1),
    )
    conflicts = scheduler.get_time_conflicts()
    assert "08:00" in conflicts
    assert len(conflicts["08:00"]) == 2
    assert "10:00" not in conflicts


def test_detects_conflict_same_time_different_pets():
    owner = Owner("Jordan")
    pet1 = Pet(pet_name="Mochi")
    pet2 = Pet(pet_name="Luna")
    pet1.add_task(Task(task_name="Feed", time="08:00"))
    pet2.add_task(Task(task_name="Meds", time="08:00"))
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    scheduler = Scheduler(owner)
    conflicts = scheduler.get_time_conflicts()
    assert "08:00" in conflicts
    assert len(conflicts["08:00"]) == 2


def test_no_conflict_for_none_times():
    _, _, scheduler = make_owner_with_tasks(
        ("Unknown1", None, 1),
        ("Unknown2", None, 1),
    )
    # None times are excluded from conflict detection
    conflicts = scheduler.get_time_conflicts()
    assert conflicts == {}


def test_multiple_conflict_slots():
    _, _, scheduler = make_owner_with_tasks(
        ("A", "08:00", 1),
        ("B", "08:00", 2),
        ("C", "12:00", 1),
        ("D", "12:00", 2),
        ("E", "18:00", 1),
    )
    conflicts = scheduler.get_time_conflicts()
    assert "08:00" in conflicts
    assert "12:00" in conflicts
    assert "18:00" not in conflicts


# --- Duration field ---

def test_task_duration_default_none():
    t = Task(task_name="Walk")
    assert t.duration is None


def test_task_set_duration():
    t = Task(task_name="Walk")
    t.set_duration(45)
    assert t.duration == 45


# --- Priority as secondary sort key ---

def test_sort_by_priority_when_times_equal():
    """When two tasks share the same start time, higher priority (lower number) comes first."""
    _, _, scheduler = make_owner_with_tasks(
        ("Meds",  "08:00", 3),
        ("Feed",  "08:00", 1),
        ("Walk",  "08:00", 2),
    )
    result = scheduler.get_all_tasks_sorted()
    names = [t.task_name for _, t in result]
    assert names == ["Feed", "Walk", "Meds"]


def test_sort_priority_none_last_within_same_time():
    """Tasks with no priority sort after prioritized tasks at the same time."""
    _, _, scheduler = make_owner_with_tasks(
        ("NoPriority", "08:00", None),
        ("High",       "08:00", 1),
    )
    result = scheduler.get_all_tasks_sorted()
    assert result[0][1].task_name == "High"
    assert result[1][1].task_name == "NoPriority"


# --- Duration-based overlap conflict detection ---

def test_overlap_conflict_detected_via_duration():
    """A 60-minute task starting at 08:00 overlaps a 30-minute task starting at 08:30."""
    owner = Owner("Jordan")
    pet = Pet(pet_name="Mochi")
    long_task = Task(task_name="Long", time="08:00")
    long_task.set_duration(60)
    short_task = Task(task_name="Short", time="08:30")
    short_task.set_duration(30)
    pet.add_task(long_task)
    pet.add_task(short_task)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    conflicts = scheduler.get_time_conflicts()
    assert len(conflicts) > 0


def test_no_overlap_when_tasks_are_sequential():
    """A 30-minute task at 08:00 and a 30-minute task at 08:30 do NOT overlap."""
    owner = Owner("Jordan")
    pet = Pet(pet_name="Mochi")
    t1 = Task(task_name="First", time="08:00")
    t1.set_duration(30)
    t2 = Task(task_name="Second", time="08:30")
    t2.set_duration(30)
    pet.add_task(t1)
    pet.add_task(t2)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    assert scheduler.get_time_conflicts() == {}


def test_existing_exact_time_conflict_still_detected():
    """Backward compat: two tasks at the exact same time still conflict (no duration)."""
    _, _, scheduler = make_owner_with_tasks(
        ("A", "09:00", 1),
        ("B", "09:00", 2),
    )
    conflicts = scheduler.get_time_conflicts()
    assert "09:00" in conflicts
    assert len(conflicts["09:00"]) == 2


# --- set_task_name ---

def test_set_task_name():
    t = Task(task_name="OldName")
    t.set_task_name("NewName")
    assert t.task_name == "NewName"


# --- get_schedule_reasoning ---

def test_schedule_reasoning_returns_one_entry_per_task():
    _, _, scheduler = make_owner_with_tasks(
        ("Walk",  "08:00", 1),
        ("Feed",  "12:00", 2),
    )
    reasons = scheduler.get_schedule_reasoning()
    assert len(reasons) == 2


def test_schedule_reasoning_no_tasks_returns_empty():
    owner = Owner("Jordan")
    scheduler = Scheduler(owner)
    assert scheduler.get_schedule_reasoning() == []


def test_schedule_reasoning_untimed_task_mentions_end():
    _, _, scheduler = make_owner_with_tasks(
        ("NoTime", None, 1),
    )
    reasons = scheduler.get_schedule_reasoning()
    assert len(reasons) == 1
    assert "end" in reasons[0].lower() or "no scheduled time" in reasons[0].lower()
