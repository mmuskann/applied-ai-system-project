# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The three core actions the user should be able to perform are add their pet, add their constraint, and add their pet care task. So, the classes would be the pet class, constraint class and task class. Pet class is reponsible for the pet's information such as name, etc. The constraint class is to allow the owner to add certains times they are not available, their preferences, and prioirty of task or each pet if they have mutliple. The task class is responsible for putting tasks with the pet object/ making a list of tasks. There should be also an owner class to assign the pet to the owner.

Brainstorm:

Owner Class {
    constructor {
        --> name
    }
    method {
        --> delete owner
        --> delete pet from owner
        --> change name
    }
}

Pet Class {
    constructor {
        --> pet_name
    }
    method {
        --> remove pet
        --> pet age
        --> pet type?
    }
}

Constraint Class {
    constructor {
        -->constraint name
    }
    method {
        --> remove constrain
        --> block time (start time, end time)
        --> perfered time (start time, end time)
        --> priority
        --> change block time
        --> change perfered time
        --> change priority
        --> constraint description
    }
}

Task Class {
    constructor {
        -->task name
    }
    method {
        --> delete task 
        --> task description
        --> add task priority
    }
}


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, my design changed during implementation. One change was adding the add_pet method to the owner instead of the pet. I made it because a pet should not be able to remove it self. Also, the remove_pet method should be in the owner class. Another change is, there is now a add_task method to the pet so each pet is assigned a task. Also, delete task logic should be move to pet because it needs to go throught the pet it is assinged to.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff my schedular makes is that it only checks for exact time matches when detecting conflicts. So if two tasks are both set to "08:00" it will flag that as a conflict, but if one task is at "07:00" and another is at "07:20" it wont catch that even if they would overlap in real life.

I decided to do it this way becuase the Task class only stores a start time and not a duration. To actually detect overlaps you would need to know how long each task takes, and adding that felt like too much for now. For a basic pet care schedule most tasks like feeding or a walk are already treated as fixed points in the day anyway, so exact match detection is good enough to catch the most common mistake of putting two things at the same time.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
