# AI Responsibility Reflection

## What are the limitations or biases in your system?

One limitation is that my system only works with the information the user enters into the schedule and the small set of rules I created in `pet_knowledge.py`. If the user enters vague task names like “care” or “thing to do,” the AI may not retrieve the best rule or give the most helpful advice. The system also depends on the rules I wrote, so it may favor certain tasks like medication or feeding because I marked them as more important. In real life, every pet and owner may have different needs, so the AI advice should be treated as a helpful suggestion, not a perfect answer.

## Could your AI be misused, and how would you prevent that?

The biggest misuse would be someone treating the AI like a veterinarian, especially for medication or health-related tasks. For example, a user might ask the AI if they should move a medication time or skip a task, which could be unsafe. To prevent that, I added guardrails in the AI prompt telling the model not to give medical or veterinary diagnosis. The AI is supposed to focus on scheduling only, and if medication is involved, it should remind the user to confirm timing with a vet if they are unsure. I also made the AI use only the schedule data and retrieved rules instead of inventing extra information.

## What surprised you while testing your AI's reliability?

What surprised me was how much better the AI responses became when I gave it structured information. When the AI received the task list, conflict warnings, priorities, and retrieved rules, the answers were more specific and actually connected to the app. I also noticed that small changes in the task names or descriptions could affect the quality of the response. For example, if I used clear names like “Medication” or “Feeding,” the AI gave better advice than when the task name was too general. This showed me that AI reliability depends a lot on the quality of the input data.

## How did you collaborate with AI during this project?

I used AI as a coding and planning assistant during this project. It helped me break the feature into smaller steps, such as creating a knowledge base, retrieving rules, building the AI prompt, and connecting the response back into Streamlit. One helpful suggestion was to create a separate `pet_knowledge.py` file for the RAG rules. That made the project easier to organize and also made it easier to explain how retrieval works.

One flawed suggestion was that the first AI integration was written for the OpenAI API, but I ended up using a Google/Gemini API key instead. That meant the original code and requirements did not fully match what I needed. I had to change the package, environment variable names, and API call so the project worked with Gemini. This taught me that AI can be very helpful, but I still need to understand and check the code instead of copying it blindly.