# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

### Running the tests

```bash
python -m pytest
```

### What's being tested

The tests are all in `tests/test_pawpal.py`. Here's a quick breakdown:

- **Task** — checks that tasks start with the right defaults and that the setter methods actually update them
- **Pet** — makes sure you can add and remove tasks without issues, including when you try to remove something that was never added
- **Owner** — covers adding/removing pets, setting availability, and wiping all the owner's data clean
- **Scheduler** — the big one. Tests pulling tasks from multiple pets, sorting by time, completing daily tasks (which resets them for the next day), and catching scheduling conflicts

## Smarter Scheduling

Once the basic structure was done I went back and built out the scheduling side more. Here's what I added:

**Sorting by time** — `sort_by_time()` takes all the tasks and puts them in order by their time so the schedule actually makes sense when you print it. If a task doesn't have a time set it just goes at the bottom.

**Filtering** — I added two ways to filter. `filter_by_pet_name()` is useful if you have more than one pet and just want to see what one of them has going on. `get_tasks_by_status()` lets you check what's already done vs what still needs to happen.

**Recurring tasks** — this one took the most thought. When you call `mark_task_complete()` on a daily or weekly task it automatically makes a new copy for the next time. It uses `timedelta` to figure out the date, so daily gets +1 day and weekly gets +7. Tasks that don't repeat just get marked done and thats it.

**Conflict warnings** — `get_conflict_warnings()` scans the schedule and looks for any two tasks at the exact same time. Instead of crashing it just returns a warning message so you know what to fix. If theres no conflicts it returns an empty list.

### Confidence Level

4 out of 5 stars

The unit tests cover all major classes and a wide range of edge cases (None values, multi-pet scenarios, recurring tasks, conflict detection). Confidence is high for the core scheduling logic. One star is held back because there are no integration or UI-level tests for the Streamlit `app.py` layer, so end-to-end behavior remains manually verified.
