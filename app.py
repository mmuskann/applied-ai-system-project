import streamlit as st
from pawpal_system import Task, Pet, BlockTime, PreferredTime, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A smart pet care scheduling assistant")

st.divider()

# ── Owner & Pet ──────────────────────────────────────────────────────────────
st.subheader("Owner & Pet")

col_owner, col_pet, col_species = st.columns(3)
with col_owner:
    owner_name = st.text_input("Owner name", value="Jordan")
with col_pet:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_species:
    species = st.selectbox("Species", ["dog", "cat", "other"])

st.divider()

# ── Task entry ───────────────────────────────────────────────────────────────
st.subheader("Add a Task")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    task_time = st.text_input("Time (HH:MM, 24-hr)", value="08:00")
with col3:
    priority = st.number_input("Priority (1 = highest)", min_value=1, max_value=10, value=1)
with col4:
    duration = st.number_input("Duration (min)", min_value=1, max_value=480, value=30)

task_description = st.text_input("Description (optional)", value="")
task_frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"])

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if st.button("➕ Add task", use_container_width=True):
    new_task = Task(task_name=task_title)
    new_task.set_time(task_time)
    new_task.set_priority(int(priority))
    new_task.set_duration(int(duration))
    new_task.set_frequency(task_frequency)
    if task_description:
        new_task.set_description(task_description)
    st.session_state.tasks.append({
        "owner": owner_name,
        "pet": pet_name,
        "species": species,
        "task": new_task,
    })
    st.success(f"Task **{task_title}** added at {task_time}.")

st.divider()

# ── Current task list ────────────────────────────────────────────────────────
st.subheader("Current Tasks")

if any(e["owner"] == owner_name and e["pet"] == pet_name for e in st.session_state.tasks):
    filter_status = st.radio(
        "Show tasks:",
        ["All", "Pending only", "Completed only"],
        horizontal=True,
    )

    # Build a temporary scheduler just for filtering/display of the raw list
    _owner = Owner(name=owner_name)
    _pet = Pet(pet_name=pet_name)
    _pet.set_type(species)
    for entry in st.session_state.tasks:
        if entry["owner"] == owner_name and entry["pet"] == pet_name:
            _pet.add_task(entry["task"])
    _owner.add_pet(_pet)
    _sched = Scheduler(owner=_owner)

    if filter_status == "Pending only":
        display_pairs = _sched.get_tasks_by_status(completed=False)
    elif filter_status == "Completed only":
        display_pairs = _sched.get_tasks_by_status(completed=True)
    else:
        display_pairs = _sched.get_all_tasks_sorted()

    if display_pairs:
        st.caption(f"Showing **{len(display_pairs)}** task(s) for {pet_name}")
        with st.container(border=True):
            st.dataframe(
                [
                    {
                        "Task": t.task_name,
                        "Time": t.time or "—",
                        "Priority": t.priority if t.priority else None,
                        "Frequency": t.frequency or "—",
                        "Description": t.description or "",
                        "Done": t.completed,
                    }
                    for _, t in display_pairs
                ],
                column_config={
                    "Priority": st.column_config.ProgressColumn(
                        "Priority",
                        help="1 = highest priority, 10 = lowest",
                        min_value=1,
                        max_value=10,
                        format="%d",
                    ),
                    "Done": st.column_config.CheckboxColumn(
                        "Done",
                        help="Task completion status",
                    ),
                },
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.info("No tasks match the selected filter.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Edit / Delete Task ────────────────────────────────────────────────────────
st.subheader("Edit / Delete a Task")

_edit_entries = [
    (i, e) for i, e in enumerate(st.session_state.tasks)
    if e["owner"] == owner_name and e["pet"] == pet_name
]

if not _edit_entries:
    st.info("No tasks to edit yet. Add one above.")
else:
    _task_labels = [
        f"{e['task'].task_name} @ {e['task'].time or 'no time'}"
        for _, e in _edit_entries
    ]
    _selected_label = st.selectbox("Select a task to edit", _task_labels, key="edit_select")
    _selected_pos = _task_labels.index(_selected_label)
    _edit_idx, _edit_entry = _edit_entries[_selected_pos]
    _edit_task = _edit_entry["task"]

    with st.form("edit_task_form"):
        e_col1, e_col2, e_col3, e_col4 = st.columns(4)
        with e_col1:
            e_name = st.text_input("Task title", value=_edit_task.task_name)
        with e_col2:
            e_time = st.text_input("Time (HH:MM)", value=_edit_task.time or "")
        with e_col3:
            e_priority = st.number_input(
                "Priority (1 = highest)", min_value=1, max_value=10,
                value=_edit_task.priority or 1,
            )
        with e_col4:
            e_duration = st.number_input(
                "Duration (min)", min_value=1, max_value=480,
                value=_edit_task.duration or 30,
            )
        e_description = st.text_input("Description", value=_edit_task.description or "")
        freq_options = ["daily", "weekly", "as needed"]
        e_freq_idx = freq_options.index(_edit_task.frequency) if _edit_task.frequency in freq_options else 0
        e_frequency = st.selectbox("Frequency", freq_options, index=e_freq_idx)

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            do_update = st.form_submit_button("✏️ Update task", use_container_width=True)
        with btn_col2:
            do_delete = st.form_submit_button("🗑️ Delete task", use_container_width=True)

    if do_update:
        _edit_task.set_task_name(e_name)
        _edit_task.set_time(e_time if e_time else None)
        _edit_task.set_priority(int(e_priority))
        _edit_task.set_duration(int(e_duration))
        _edit_task.set_description(e_description if e_description else None)
        _edit_task.set_frequency(e_frequency)
        st.success(f"Task **{e_name}** updated.")
        st.rerun()

    if do_delete:
        st.session_state.tasks.pop(_edit_idx)
        st.success("Task deleted.")
        st.rerun()

st.divider()

# ── Schedule generation ───────────────────────────────────────────────────────
st.subheader("Generate Schedule")

if st.button("📅 Build schedule", use_container_width=True):
    owner_pet_tasks = [e for e in st.session_state.tasks if e["owner"] == owner_name and e["pet"] == pet_name]
    if not owner_pet_tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        owner = Owner(name=owner_name)
        pet = Pet(pet_name=pet_name)
        pet.set_type(species)
        for entry in st.session_state.tasks:
            if entry["owner"] == owner_name and entry["pet"] == pet_name:
                pet.add_task(entry["task"])
        owner.add_pet(pet)

        scheduler = Scheduler(owner=owner)
        sorted_tasks = scheduler.get_all_tasks_sorted()
        pending = scheduler.get_tasks_by_status(completed=False)
        done = scheduler.get_tasks_by_status(completed=True)
        warnings = scheduler.get_conflict_warnings()

        # ── Summary metrics ──────────────────────────────────────────────────
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total tasks", len(sorted_tasks))
        m2.metric("Pending", len(pending))
        m3.metric("Completed", len(done))
        m4.metric("Conflicts", len(warnings))

        st.divider()

        # ── Conflict warnings ────────────────────────────────────────────────
        if warnings:
            st.error(
                f"⚠️ **{len(warnings)} scheduling conflict(s) detected** — "
                "two or more tasks are set to the same time. "
                "Your pet can only do one thing at a time! Please reschedule the tasks below.",
                icon="🚨",
            )
            for warning_text in warnings:
                parts = warning_text.split(" — ", maxsplit=1)
                detail = parts[1] if len(parts) > 1 else warning_text
                time_part = warning_text.split("time ")[-1].split(" —")[0] if "time " in warning_text else "unknown time"

                with st.container(border=True):
                    st.warning(
                        f"**Conflict at {time_part}**\n\n"
                        f"{detail}\n\n"
                        f"**Tip:** Change the time of one of these tasks above, then rebuild the schedule.",
                        icon="🕐",
                    )
        else:
            st.success("No conflicts — your schedule looks great!", icon="✅")

        # ── Sorted schedule table ────────────────────────────────────────────
        st.markdown(f"### {owner.name}'s Schedule for {pet.pet_name} ({pet.type})")
        st.caption("Tasks sorted earliest to latest. Tasks without a set time appear at the bottom.")

        with st.container(border=True):
            st.dataframe(
                [
                    {
                        "#": i + 1,
                        "Time": t.time or "—",
                        "Duration": f"{t.duration} min" if t.duration else "—",
                        "Task": t.task_name,
                        "Priority": t.priority if t.priority else None,
                        "Frequency": t.frequency or "—",
                        "Description": t.description or "",
                        "Done": t.completed,
                    }
                    for i, (_, t) in enumerate(sorted_tasks)
                ],
                column_config={
                    "#": st.column_config.NumberColumn("#", width="small"),
                    "Priority": st.column_config.ProgressColumn(
                        "Priority",
                        help="1 = highest priority, 10 = lowest",
                        min_value=1,
                        max_value=10,
                        format="%d",
                    ),
                    "Done": st.column_config.CheckboxColumn(
                        "Done",
                        help="Task completion status",
                    ),
                },
                use_container_width=True,
                hide_index=True,
            )

        # ── Scheduling reasoning ─────────────────────────────────────────────
        reasoning = scheduler.get_schedule_reasoning()
        if reasoning:
            with st.expander("📋 How was this schedule built?", expanded=False):
                st.markdown(
                    "Tasks are ordered **earliest start time first**. "
                    "When two tasks share the same start time, the one with **higher priority** "
                    "(lower number) is listed first. Tasks without a set time appear at the end."
                )
                st.markdown("**Per-task reasoning:**")
                for line in reasoning:
                    st.markdown(f"- {line}")
