from enum import Enum

import collections

from core.band_expansion import EXPAND_ALL

BandAlphabet = collections.namedtuple('BandAlphabet', 'chars empty_char')


class BandDirection(Enum):
    '''
    Beschreibt die Laufrichtung eines Turingbandes nachdem der Zustand geandert wurde
    '''
    LEFT = -1
    NONE = 0
    RIGHT = 1


class Band:
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

    def __get_expansion_op_by_direction(self, band_direction):
        if band_direction is BandDirection.LEFT:
            return self.__expansion_strategy.move_left_op

        if band_direction is BandDirection.RIGHT:
            return self.__expansion_strategy.move_right_op

        return lambda position, list: position

    def __get_empty_char(self):
        return self.__alphabet.empty_char if self.__alphabet else None

    def move(self, band_direction):
        '''
        Bewegt das Band in die angegebene Richtung.
        '''
        expansion_op = self.__get_expansion_op_by_direction(band_direction)
        self.__position = expansion_op(self.__position, self.__entries, self.__get_empty_char())

    def read(self):
        '''
        Liest den Buchstaben an der aktuellen Bandposition
        '''
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


class MultiBand:
    '''
    Beschreibt ein mehrdimensionales Turingband als Kollektion eindimensionaler Turingbänder.
    '''

    def __init__(self, dim_1_bands):
        '''
        Initialisiert ein neues n-dimensionales Band.
        :param dim_1_bands: die eindimensionalen Bänder der Turingmaschine.
        '''
        self.__bands = dim_1_bands

    def move(self, band_directions):
        '''
        Bewegt das Band in die angegebene Richtung.
        '''
        for direction, band in zip(band_directions, self.__bands):
            band.move(direction)

    def read(self):
        '''
        Liest die Buchstaben an der aktuellen Bandposition als Liste aus.
        '''
        return [band.read() for band in self.__bands]

    def write(self, chars):
        '''
        Schreibt die Buchstaben an der aktuellen Position auf das Band.
        '''
        for char, band in zip(chars, self.__bands):
            band.write(char)

    def set_alphabet(self, alphabet):
        '''
        Setzt das Bandalphabet
        '''
        for band in self.__bands:
            band.set_alphabet(alphabet)

    def non_alphabet_chars(self):
        '''
        Gibt alle buchstaben des Bandes zurück, die nicht Teil des alphabets sind.
        '''
        return set().union(band.non_alphabet_chars() for band in self.__bands)
