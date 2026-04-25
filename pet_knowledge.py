PET_CARE_RULES = [
    {
        "id": "conflicts",
        "keywords": ["conflict", "overlap", "same time", "time"],
        "text": "If two pet tasks overlap, move the lower-priority task or shorten one task. Priority 1 is the highest priority."
    },
    {
        "id": "dog_walks",
        "keywords": ["dog", "walk", "exercise", "potty"],
        "text": "Dog walking tasks are usually easier to schedule in the morning or evening and should not overlap with feeding or medication."
    },
    {
        "id": "feeding",
        "keywords": ["feeding", "food", "meal", "eat"],
        "text": "Feeding tasks should stay at consistent times when possible. Avoid stacking too many tasks at the exact same time."
    },
    {
        "id": "cat_playtime",
        "keywords": ["cat", "playtime", "toy", "feather"],
        "text": "Cat playtime can be flexible and is often a good task to move if there is a schedule conflict."
    },
    {
        "id": "medication",
        "keywords": ["medication", "pill", "medicine"],
        "text": "Medication tasks should be treated as high priority and should not be moved unless the owner confirms it is safe."
    },
    {
        "id": "grooming",
        "keywords": ["grooming", "brush", "coat"],
        "text": "Grooming is usually flexible and can be moved later if it overlaps with feeding, walking, or medication."
    },
]


def retrieve_pet_care_rules(schedule_items, warnings, top_k=5):
    """
    Simple RAG retrieval:
    Looks at the current schedule and pulls the most relevant pet-care rules.
    """

    query_parts = []

    for item in schedule_items:
        query_parts.append(item.get("pet", ""))
        query_parts.append(item.get("species", ""))
        query_parts.append(item.get("task", ""))
        query_parts.append(item.get("description", ""))
        query_parts.append(item.get("frequency", ""))

    query_parts.extend(warnings)

    query = " ".join(str(x).lower() for x in query_parts)

    scored_rules = []

    for rule in PET_CARE_RULES:
        score = 0

        for keyword in rule["keywords"]:
            score += query.count(keyword.lower())

        if score > 0:
            scored_rules.append((score, rule))

    scored_rules.sort(key=lambda pair: pair[0], reverse=True)

    retrieved = [rule for score, rule in scored_rules[:top_k]]

    if not retrieved:
        retrieved = [PET_CARE_RULES[0]]

    return retrieved