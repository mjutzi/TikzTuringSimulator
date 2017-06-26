class TuringMachine:
    def __init__(self, initial_state, final_state, transition_graph):
        self.initial_state = initial_state
        self.final_state = final_state
        self.transition_graph = transition_graph

    def as_iterator(self, band):
        current_state = self.initial_state
        while current_state is not self.final_state:
            event, target = self.transition_graph.get_transition(current_state, band.read())
            yield event, target

            if not target:
                break

    def run(self, band, max_iterations=float('inf')):
        pass  # TODO implement logic
