import collections
from enum import Enum


class BandDirection(Enum):
    LEFT = -1
    NONE = 0
    RIGHT = 1


class ExpansionStrategy:
    def __init__(self, expand_right=True, expand_left=True):
        self.expand_right = True
        self.expand_left = True


class MultiBand:
    def __init__(self, entries, inital_positions, expansion_strategy=ExpansionStrategy()):
        self.__current_symbols = None
        self.__band_entries = None
        self.__current_positions = None
        self.__expansion_strategy = expansion_strategy

    def move(self, band_directions):
        pass

    def positions(self):
        pass

    def read_chars(self):
        pass

    def wirte_chars(self):
        pass


State = collections.namedtuple('State', 'index name')

StateTransition = collections.namedtuple('StateTransition', 'state_from state_to write_chars move_band')


class TuringGraph:
    def get_transition(self, state, read_chars):
        pass


class MultiBandTuringMachine:
    def __init__(self, initial_state, graph, multiband):
        self.current_state = initial_state
        self.graph = graph
        self.multiband = multiband

    def step(self):
        pass  # move band and return turing step
