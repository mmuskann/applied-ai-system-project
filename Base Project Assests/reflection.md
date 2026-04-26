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

The scheduler considers three main constraints are time, priority, and owner availability. Tasks have scheduled start times and durations, and the system flags any overlapping windows as conflicts. When two tasks share the same start time, priority breaks the tie. The higher priority tasks appear first. Tasks with no time set get pushed to the end. Owners can also set block times and preferred times to reflect when they're actually available.I prioritized time and conflict detection first because a schedule with silent overlaps isn't useful. Priority came after that. Owner availability was also added because the whole point is coordinating around real human schedules, not just the pets'.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff is that the scheduler warns about conflicts but doesn't automatically resolve them. It flags overlapping tasks and tells you to reschedule, but leaves the actual decision to the user. This is reasonable because pet care tasks with certain time can't be changed.You can't just blindly swap a vet appointment with a feeding without knowing the context. We would need to implemnt some sort of ai for that to make the smart decisions. The owner understands their situation better than any algorithm does, so surfacing the problem and letting them fix it makes more sense than having the system guess.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI mostly for debugging and figuring out logic for the conflict detection and sorting features.  I also used it for streamlight because I have no prior experience with that. I would test it and tell ai the problem and have it fix it for me. The most helpful prompts or questions were realted to the logic. Though the one where I desceibe about the stemlit to the ai were also helpful because it fixed the problem for me. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One moment where I didn not accept an AI suggestion as is was when planning the structure. I made the structure my self while taking suggestion.s I evaluated by comapring my idea vs ai and comapring it to see which was better/

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested things like sorting tasks by time, detecting scheduling conflicts, and recurring task logic. I basically tests the parts most likely to break in weird ways. hose felt most important because if sorting or conflict detection is off, the whole schedule is unreliable. I also tested edge cases like tasks with no time or priority since those are easy to overlook and cause silent bugs.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am confident in the core stuff like sorting, conflict detection, and recurring tasks because they all have test coverage including edge cases. If I had more time, I'd test what happens when an owner has block times that conflict with scheduled tasks, and also stress test with a large number of pets and tasks to see if anything breaks at scale.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I was the most satisfied with planning the inital structure. A good foundation is always needed to know what your building and I think I had a pretty good foundation.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve the design. I would want to build this again but in a app format or website instead of a streamlit.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One thing I leanred about desiging systems is the foundation is the most time. I am just taking about this project, or cs. I am taking about everything in genral. YOu can't start anything if you don't have a plan or a good direction or end vision. 
