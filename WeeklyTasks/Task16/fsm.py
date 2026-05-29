class FSMState:
    def __init__(self, name):
        self.name = name
        self.transitions = {} 
    
    def add_transition(self, trigger, target_state):
        self.transitions[trigger] = target_state
    
    def get_next(self, trigger):
        return self.transitions.get(trigger, None)


class FSM:
    def __init__(self, initial_state_name):
        self.states = {}
        self.current = None
        self.initial_state_name = initial_state_name

    def add_state(self, name):
        state = FSMState(name)
        self.states[name] = state
        if name == self.initial_state_name and self.current is None:
            self.current = state
        return state

    def update(self, agent, delta):
        if self.current:
            self.current.execute(agent, delta)
    
    def trigger(self, trigger):
        if self.current:
            next_state = self.current.get_next(trigger)
            if next_state:
                self.current = next_state
                return True
        return False
    
    @property
    def current_name(self):
        return self.current.name if self.current else None