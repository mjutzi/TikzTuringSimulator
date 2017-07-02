class TuringMachine:
    def __init__(self, initial_state, final_states, transition_graph):
        self.initial_state = initial_state
        self.final_states = final_states
        self.transition_graph = transition_graph

    def as_iterator(self, band):
        current_state = self.initial_state
        while not current_state in self.final_states:
            event, target = self.transition_graph.get_transition(current_state, band.read())
            yield event, target

            if not target:
                break
