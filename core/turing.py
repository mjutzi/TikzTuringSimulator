import collections
from enum import Enum


class BandDirection(Enum):
    '''
    Beschreibt die Laufrichtung eines Turingbandes nachdem der Zustand geandert wurde
    '''
    LEFT = -1
    NONE = 0
    RIGHT = 1


class ExpansionStrategy:
    '''
    Strategie, die angibt wie das Turingband in die Linke und rechte Laufrichtung erweitert wird, sofern die
    Grenzen des Turingbandes ueberschritten werden.
    '''

    def __init__(self, expand_right=True, expand_left=False):
        self.expand_right = True
        self.expand_left = True


class MultiBand:
    '''
    Beschreibt ein mehrdimensionales Turingband.
    '''

    def __init__(self, entries, inital_positions, expansion_strategy=ExpansionStrategy()):
        self.__current_symbols = None
        self.__band_entries = None
        self.__current_positions = None
        self.__expansion_strategy = expansion_strategy

    def move(self, band_directions):
        '''
        Bewegt das Turingband in die angegebenen Richtungen.
        '''
        pass

    def positions(self):
        '''
        Gibt die aktuelle Position oder Positionen zurück.
        '''
        pass

    def read_chars(self):
        '''
        Liest die Buchstaben an der aktuellen Bandposition.
        '''
        pass

    def wirte_chars(self):
        '''
        Schreibt die Buchstaben an der aktuellen Bandposition.
        '''
        pass


State = collections.namedtuple('State', 'index name')

StateTransition = collections.namedtuple('StateTransition', 'state_from state_to write_chars move_band')


class TuringGraph:
    '''
    Repräsentiert die Zulässigen Zustandsänderungen einer Turingmaschine.
    '''

    def get_transition(self, state, read_chars):
        pass


class MultiBandTuringMachine:
    '''
    Repräsentiert eine Mehrbandturingmaschine.
    '''

    def __init__(self, initial_state, graph, multiband):
        self.current_state = initial_state
        self.graph = graph
        self.multiband = multiband

    def step(self):
        '''
        Bewegt das Band und gibt die Zustandsänderung zurück.
        :return: die Zustandsänderung als StateTransition Tupel
        '''
        pass  # move band and return turing step
