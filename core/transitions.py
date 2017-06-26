import collections

State = collections.namedtuple('State', 'index name')

StateTransition = collections.namedtuple('StateTransition', 'state_from state_to write_chars move_band')


class TuringGraph:
    '''
    Repräsentiert die Zulässigen Zustandsänderungen einer Turingmaschine.
    '''

    def get_transition(self, state, read_chars):
        pass
