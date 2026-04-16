
class WorldState:
    
    def __init__(self, **kwargs):
        self.facts = kwargs
    
    def __getitem__(self, key):
        return self.facts.get(key, 0)
    
    def __setitem__(self, key, value):
        self.facts[key] = value
    
    def copy(self):
        return WorldState(**self.facts.copy())
    
    def has(self, **conditions):
        for key, needed in conditions.items():
            if self.facts.get(key, 0) < needed:
                return False
        return True
    
    def update(self, **changes):
        for key, delta in changes.items():
            self.facts[key] = self.facts.get(key, 0) + delta
            if self.facts[key] < 0:
                self.facts[key] = 0
    
    def __repr__(self):
        return str(self.facts)

class Action:
    
    def __init__(self, name, requires=None, gives=None, effort=1, time_needed=1):
        self.name = name
        self.requires = requires if requires else {}
        self.gives = gives if gives else {}
        self.effort = effort
        self.time_needed = time_needed
    
    def possible_now(self, world):
        return world.has(**self.requires)
    
    def do_it(self, world):
        new_world = world.copy()
        new_world.update(**self.gives)
        return new_world
    
    def __repr__(self):
        return self.name

def available_actions():
    return [
        Action("Eat something", 
               requires={"food": 1, "hunger": 1},
               gives={"hunger": -30, "food": -1},
               effort=2, time_needed=1),
        
        Action("Get some sleep",
               requires={"fatigue": 1, "at_home": True},
               gives={"fatigue": -40},
               effort=3, time_needed=3),
        
        Action("Drink water",
               requires={"water": 1, "thirst": 1},
               gives={"thirst": -30, "water": -1},
               effort=2, time_needed=1),
        
        Action("Buy groceries",
               requires={"money": 5, "at_shop": True},
               gives={"food": 1, "money": -5},
               effort=3, time_needed=1),
        
        Action("Buy water bottles",
               requires={"money": 3, "at_shop": True},
               gives={"water": 1, "money": -3},
               effort=3, time_needed=1),
        
        Action("Do some work",
               requires={"fatigue": 50},
               gives={"money": 10, "fatigue": 10},
               effort=5, time_needed=2),
        
        Action("Head to the shop",
               gives={"at_shop": True, "at_home": False},
               effort=2, time_needed=1),
        
        Action("Go back home",
               gives={"at_home": True, "at_shop": False},
               effort=2, time_needed=1),
        
        Action("Forage in the woods",
               requires={"in_woods": True, "fatigue": 70},
               gives={"food": 1, "fatigue": 20},
               effort=6, time_needed=3),
        
        Action("Walk to the forest",
               gives={"in_woods": True, "at_home": False},
               effort=3, time_needed=2),
    ]
# planner for actions and goals

class Planner:
    
    def __init__(self, actions):
        self.actions = actions
    
    def guess_effort_to_goal(self, current, goal):
        estimate = 0
        for need, target in goal.items():
            have = current[need]
            if have < target:
                estimate += (target - have) // 10
        return estimate
    
    def make_plan(self, starting_from, trying_to_achieve):
        
        class Thought:
            def __init__(self, situation, action_that_got_here=None, 
                         previous_thought=None, effort_so_far=0, estimated_remaining=0):
                self.situation = situation
                self.action = action_that_got_here
                self.previous = previous_thought
                self.effort_spent = effort_so_far
                self.estimated_left = estimated_remaining
                self.total_estimated = effort_so_far + estimated_remaining
            
            def __lt__(self, other):
                return self.total_estimated < other.total_estimated
        
        first_thought = Thought(
            situation=starting_from.copy(),
            estimated_remaining=self.guess_effort_to_goal(starting_from, trying_to_achieve)
        )
        
        thoughts_to_explore = [first_thought]
        already_considered = set()
        
        while thoughts_to_explore:
            current_thought = thoughts_to_explore.pop(0)
            
            if current_thought.situation.has(**trying_to_achieve):
                return self._trace_back_plan(current_thought)
            
            situation_id = str(current_thought.situation.facts)
            if situation_id in already_considered:
                continue
            already_considered.add(situation_id)
            
            for action in self.actions:
                if action.possible_now(current_thought.situation):
                    after_action = action.do_it(current_thought.situation)
                    
                    new_thought = Thought(
                        situation=after_action,
                        action_that_got_here=action,
                        previous_thought=current_thought,
                        effort_so_far=current_thought.effort_spent + action.effort,
                        estimated_remaining=self.guess_effort_to_goal(after_action, trying_to_achieve)
                    )
                    
                    inserted = False
                    for i, thought in enumerate(thoughts_to_explore):
                        if new_thought.total_estimated < thought.total_estimated:
                            thoughts_to_explore.insert(i, new_thought)
                            inserted = True
                            break
                    if not inserted:
                        thoughts_to_explore.append(new_thought)
        
        return None
    
    def _trace_back_plan(self, final_thought):
        plan = []
        current = final_thought
        while current.previous:
            plan.append(current.action)
            current = current.previous
        plan.reverse()
        return plan

class Agent:
    
    def __init__(self, name, starting_situation, actions):
        self.name = name
        self.situation = starting_situation.copy()
        self.actions = actions
        self.planner = Planner(actions)
        self.current_plan = []
        self.currently_doing = None
        self.time_left_on_action = 0
    
    def set_new_goal(self, goal):
        print(f"\n{self.name} wants to: {self._describe_goal(goal)}")
        
        self.current_plan = self.planner.make_plan(self.situation, goal)
        
        if self.current_plan:
            print(f"Here's what {self.name} decides to do:")
            for i, step in enumerate(self.current_plan):
                print(f"  {i+1}. {step.name}")
            total_time = sum(step.time_needed for step in self.current_plan)
            print(f"This'll take about {total_time} hour{'s' if total_time > 1 else ''}.")
        else:
            print(f"Hmm, {self.name} can't figure out a way to do this.")
        
        return len(self.current_plan) > 0
    
    def _describe_goal(self, goal):
        parts = []
        for need, value in goal.items():
            if need == "hunger" and value == 0:
                parts.append("not be hungry")
            elif need == "fatigue" and value == 0:
                parts.append("feel well rested")
            elif need == "thirst" and value == 0:
                parts.append("not be thirsty")
        return " and ".join(parts) if parts else str(goal)
    
    def take_action(self):
        if not self.current_plan and not self.currently_doing:
            return False
        
        if not self.currently_doing:
            self.currently_doing = self.current_plan.pop(0)
            self.time_left_on_action = self.currently_doing.time_needed
            print(f"\n{self.name} is now: {self.currently_doing.name.lower()}")
        
        self.time_left_on_action -= 1
        
        if self.time_left_on_action <= 0:
            self.situation = self.currently_doing.do_it(self.situation)
            
            hunger = self.situation['hunger']
            fatigue = self.situation['fatigue']
            thirst = self.situation['thirst']
            
            status = []
            if hunger > 0:
                status.append(f"hunger at {hunger}")
            if fatigue > 0:
                status.append(f"energy at {100 - fatigue}%")
            if thirst > 0:
                status.append(f"thirst at {thirst}")
            
            if status:
                print(f"  Done. Now: {', '.join(status)}")
            else:
                print(f"  Done. Feeling good!")
            
            self.currently_doing = None
        
        return True
# finish and add a demo

if __name__ == "__main__":
    run_demo()