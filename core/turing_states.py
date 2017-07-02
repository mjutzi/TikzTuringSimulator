import collections

State = collections.namedtuple('State', 'index name')

TransitionEvent = collections.namedtuple('TransitionEvent', 'current_state read_chars')

TransitionTarget = collections.namedtuple('TransitionTarget', 'new_state new_chars move_directions')


class TransitionGraph:
    '''
    Repräsentiert Menge der zulässigen Zustandsänderungen einer Turingmaschine.
    '''

    def __init__(self, transitions_map=None):
        self.__transitions_map = transitions_map if transitions_map is not None else {}

    def register_transition(self, current_state, read_chars, transition_target):
        '''
        Registriert die aktuelle Zustandsänderung als zulässig.
        :param current_state: der aktuelle Zustand der Turingmaschine
        :param read_chars: die gelesenen Character
        :param transition_target: der Zustandsübergang
        '''
        event = TransitionEvent(state_from=current_state, read_chars=read_chars)
        self.__transitions_map[event] = transition_target

    def get_transition(self, current_state, read_chars):
        '''
        Gibt die zulässige Zustandsänderung zurück, die durch den gegebenen Zustand und die gelesenen Character entstehen.
        :param current_state: der aktuelle Zustand der Turingmaschine
        :param read_chars: die gelesenen Character
        :return: das zugehörige Tupel TransitionEvent, TransitionTarget sofern dieses registriert wurde oder
        TransitionEvent,None sofern die Zustansänderung nicht zulässig ist.
        '''
        event = TransitionEvent(state_from=current_state, read_chars=read_chars)
        target = self.__transitions_map[event] if event in self.__transitions_map[event] else None
        return event, target
