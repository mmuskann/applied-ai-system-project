import json
import logging
import os
from typing import Any

from dotenv import load_dotenv
from google import genai

from pawpal_system import Scheduler
from pet_knowledge import retrieve_pet_care_rules


load_dotenv()

logging.basicConfig(
    filename="pawpal_ai.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def _task_to_dict(pet, task) -> dict[str, Any]:
    return {
        "pet": pet.pet_name,
        "species": pet.type,
        "task": task.task_name,
        "description": task.description or "",
        "time": task.time or "no time",
        "duration_minutes": task.duration,
        "priority": task.priority,
        "frequency": task.frequency or "none",
        "completed": task.completed,
        "due_date": str(task.due_date) if task.due_date else "no date",
    }


def build_ai_schedule_advice(owner, scheduler: Scheduler, user_goal: str):
    """
    Main AI feature for PawPal+.

    This is RAG because it:
    1. Reads the current PawPal schedule.
    2. Retrieves relevant pet-care rules.
    3. Sends the schedule and retrieved rules to Gemini.
    4. Returns AI-generated schedule advice.
    """

    sorted_pairs = scheduler.get_all_tasks_sorted()
    schedule_items = [_task_to_dict(pet, task) for pet, task in sorted_pairs]

    warnings = scheduler.get_conflict_warnings()
    reasoning = scheduler.get_schedule_reasoning()

    retrieved_rules = retrieve_pet_care_rules(schedule_items, warnings)

    debug_info = {
        "schedule_items": schedule_items,
        "warnings": warnings,
        "retrieved_rules": retrieved_rules,
    }

    logging.info(
        "AI schedule advice requested for owner=%s, tasks=%s, conflicts=%s",
        owner.name,
        len(schedule_items),
        len(warnings),
    )

    if not schedule_items:
        return "Add at least one task before asking the AI for advice.", debug_info

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        logging.warning("Missing GEMINI_API_KEY.")
        return (
            "AI is not set up yet. Add your GEMINI_API_KEY to the .env file, "
            "then restart the Streamlit app."
        ), debug_info

    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    prompt_payload = {
        "owner": owner.name,
        "user_goal": user_goal,
        "current_schedule": schedule_items,
        "conflict_warnings": warnings,
        "scheduler_reasoning": reasoning,
        "retrieved_pet_care_rules": retrieved_rules,
    }

    prompt = f"""
You are PawPal+, an AI pet care scheduling assistant.

Use the current schedule, conflict warnings, scheduler reasoning, and retrieved pet-care rules.

Rules:
- Do not invent tasks that do not exist.
- Do not give medical or veterinary diagnosis.
- If medication is involved, say the owner should confirm timing with a vet if unsure.
- Give practical schedule advice based only on the data provided.

Return your answer with these sections:
1. Schedule Summary
2. Problems Found
3. Suggested Fixes
4. Why These Fixes Help

Here is the PawPal schedule data:

{json.dumps(prompt_payload, indent=2)}
"""

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )

        logging.info("AI schedule advice completed successfully.")

        if response.text:
            return response.text, debug_info

        return "The AI returned an empty response. Try again.", debug_info

    except Exception as e:
        logging.exception("AI schedule advice failed.")

        fallback = "The AI request failed, but PawPal still checked your schedule.\n\n"

        if warnings:
            fallback += "Conflicts found:\n"
            for warning in warnings:
                fallback += f"- {warning}\n"
        else:
            fallback += "No conflicts were found by the regular scheduler."

        fallback += f"\n\nError: {e}"

        return fallback, debug_info