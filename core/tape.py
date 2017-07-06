from enum import Enum

import collections

from core.tape_expansion import EXPAND_ALL

TapeAlphabet = collections.namedtuple('TapeAlphabet', 'chars empty_char')


class Direction(Enum):
    '''
    Beschreibt die Laufrichtung eines Turingbandes nachdem der Zustand geandert wurde
    '''
    LEFT = -1
    NONE = 0
    RIGHT = 1


class Tape:
    '''
    Beschreibt ein eindimensionales Turingband
    '''

    def __init__(self, entries, alphabet=None, expansion_strategy=EXPAND_ALL):
        '''
        Erzeugt ein neues eindimensionales Turingband. Werden die Grenzen des Turingbandes erreicht, so entscheidet die expansion_strategy
        als Stretegy pattern, ob und wie das Band erweitert wird.
        :param entries: die initialien Eintraege des Bandes
        :param expansion_strategy: ein ExpansionStrategy Tupel, dass die Indexverschiebung und ggf. Vergrößerung der Einträge managed.
        Im Modul core.internals sind EXPAND_ALL, EXPAND_NONE, EXPAND_LEFT_ONLY, EXPAND_RIGHT_ONLY vordefiniert
        '''
        self.__position = 0
        self.__entries = entries
        self.__alphabet = alphabet
        self.__expansion_strategy = expansion_strategy

    def __get_expansion_op_by_direction(self, direction):
        if direction is Direction.LEFT:
            return self.__expansion_strategy.move_left_op

        if direction is Direction.RIGHT:
            return self.__expansion_strategy.move_right_op

        return lambda position, list, empty_char: position

    def __get_empty_char(self):
        return self.__alphabet.empty_char if self.__alphabet else None

    def move(self, direction):
        '''
        Bewegt das Band in die angegebene Richtung.
        '''
        expansion_op = self.__get_expansion_op_by_direction(direction)
        self.__position = expansion_op(self.__position, self.__entries, self.__get_empty_char())

    def read(self):
        '''
        Liest den Buchstaben an der aktuellen Bandposition
        '''
        if not self.__entries:
            self.__entries.append(self.__get_empty_char())

        return self.__entries[self.__position]

    def write(self, char):
        '''
        Schreibt den Buchstaben an der aktuellen Position auf das Band.
        '''
        self.__entries[self.__position] = char

    def set_alphabet(self, alphabet):
        '''
        Setzt das Bandalphabet
        '''
        self.__alphabet = alphabet

    def non_alphabet_chars(self):
        '''
        Gibt alle buchstaben des Bandes zurück, die nicht Teil des alphabets sind.
        '''
        if self.__alphabet:
            return set(self.__alphabet.chars) - set(self.__entries)
        else:
            return set(self.__entries)

    @property
    def entries(self):
        return self.__entries

    @property
    def position(self):
        return self.__position

    @property
    def inner_tapes(self):
        return [self]

class MultiTape:
    '''
    Beschreibt ein mehrdimensionales Turingband als Kollektion eindimensionaler Turingbänder.
    '''

    def __init__(self, dim_1_tapes):
        '''
        Initialisiert ein neues n-dimensionales Band.
        :param dim_1_tapes: die eindimensionalen Bänder der Turingmaschine.
        '''
        self.__tapes = dim_1_tapes

    def move(self, direction):
        '''
        Bewegt das Band in die angegebene Richtung.
        '''
        for direction, band in zip(direction, self.__tapes):
            band.move(direction)

    def read(self):
        '''
        Liest die Buchstaben an der aktuellen Bandposition als Liste aus.
        '''
        return [tape.read() for tape in self.__tapes]

    def write(self, chars):
        '''
        Schreibt die Buchstaben an der aktuellen Position auf das Band.
        '''
        for char, tape in zip(chars, self.__tapes):
            tape.write(char)

    def set_alphabet(self, alphabet):
        '''
        Setzt das Bandalphabet
        '''
        for band in self.__tapes:
            band.set_alphabet(alphabet)

    def non_alphabet_chars(self):
        '''
        Gibt alle buchstaben des Bandes zurück, die nicht Teil des alphabets sind.
        '''
        return set().union(tape.non_alphabet_chars() for tape in self.__tapes)

    @property
    def entries(self):
        return [tape.entries() for tape in self.__tapes]

    @property
    def position(self):
        return [tape.position() for tape in self.__tapes]

    @property
    def inner_tapes(self):
        return self.__tapes
