from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

# Create owner
owner = Owner("Alex")

# Create pets
buddy = Pet(pet_name="Buddy", age=3, type="Dog")
whiskers = Pet(pet_name="Whiskers", age=5, type="Cat")

# Add tasks OUT OF ORDER to demonstrate sorting
buddy.add_task(Task(task_name="Evening Walk",  description="20-minute walk",                 time="18:00", priority=1, frequency="daily",  due_date=date.today()))
buddy.add_task(Task(task_name="Morning Walk",  description="30-minute walk around the block", time="07:00", priority=1, frequency="daily",  due_date=date.today()))
buddy.add_task(Task(task_name="Vet Check-up",  description="Annual check-up",                 time="09:00", priority=1, frequency="weekly", due_date=date.today()))
buddy.add_task(Task(task_name="Feeding",       description="1 cup of dry food",               time="08:00", priority=2, frequency="daily",  due_date=date.today()))

whiskers.add_task(Task(task_name="Playtime",  description="10 minutes with feather toy", time="17:00", priority=2, frequency="daily",  due_date=date.today()))
whiskers.add_task(Task(task_name="Feeding",   description="Half can of wet food",        time="08:30", priority=1, frequency="weekly", due_date=date.today()))

# ── Deliberate conflicts ───────────────────────────────────────────────────────
# Same pet, same time: Buddy has two tasks at 08:00
buddy.add_task(Task(task_name="Medication",   description="Morning pill",  time="08:00", priority=1))

# Different pets, same time: both pets have something at 17:00
buddy.add_task(Task(task_name="Grooming",     description="Brush coat",    time="17:00", priority=2))

# Add pets to owner
owner.add_pet(buddy)
owner.add_pet(whiskers)

scheduler = Scheduler(owner)

# ── Helper ────────────────────────────────────────────────────────────────────
def print_tasks(label: str, pairs: list) -> None:
    print(f"\n{'=' * 52}")
    print(f"  {label}")
    print('=' * 52)
    if not pairs:
        print("  (no tasks)")
        return
    for pet, task in pairs:
        status = "[DONE]" if task.completed else "[    ]"
        time_str  = task.time     if task.time     else "??:??"
        due_str   = str(task.due_date) if task.due_date else "no date"
        freq_str  = task.frequency if task.frequency else "—"
        print(f"  {status}  {time_str}  due:{due_str}  [{pet.pet_name}]  {task.task_name}  ({freq_str})")

# ── 1. Conflict warnings (checked first, before acting on the schedule) ───────
print(f"\n{'=' * 52}")
print("  Conflict Check")
print('=' * 52)
warnings = scheduler.get_conflict_warnings()
if warnings:
    for w in warnings:
        print(f"  {w}")
else:
    print("  No conflicts detected.")

# ── 2. Sorted by time ─────────────────────────────────────────────────────────
print_tasks("All tasks — sorted by time", scheduler.sort_by_time())

# ── 2. Complete a DAILY task → next occurrence spawned (today + 1 day) ────────
daily_task = buddy.tasks[1]   # Morning Walk
print(f"\n>> Completing daily task: '{daily_task.task_name}' (due {daily_task.due_date})")
next_daily = scheduler.mark_task_complete(buddy, daily_task)
print(f"   New occurrence due: {next_daily.due_date}  (today + 1 day via timedelta)")

# ── 3. Complete a WEEKLY task → next occurrence spawned (today + 7 days) ──────
weekly_task = buddy.tasks[2]  # Vet Check-up
print(f"\n>> Completing weekly task: '{weekly_task.task_name}' (due {weekly_task.due_date})")
next_weekly = scheduler.mark_task_complete(buddy, weekly_task)
print(f"   New occurrence due: {next_weekly.due_date}  (today + 7 days via timedelta)")

# ── 4. Complete a task with no frequency → nothing spawned ────────────────────
one_off = Task(task_name="Bath", time="11:00", frequency="as needed")
buddy.add_task(one_off)
result = scheduler.mark_task_complete(buddy, one_off)
print(f"\n>> Completing one-off task 'Bath': new task spawned? {result is not None}")

# ── 5. Filter by status after completions ────────────────────────────────────
print_tasks("Filter by status: completed",  scheduler.get_tasks_by_status(completed=True))
print_tasks("Filter by status: incomplete", scheduler.get_tasks_by_status(completed=False))

# ── 6. Filter by pet name ─────────────────────────────────────────────────────
print_tasks("Filter by pet name: Buddy",    scheduler.filter_by_pet_name("Buddy"))
print_tasks("Filter by pet name: Whiskers", scheduler.filter_by_pet_name("Whiskers"))

print()
