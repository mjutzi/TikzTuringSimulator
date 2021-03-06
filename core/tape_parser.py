import re

from core.tape import Tape, MultiTape
from file_import.exceptions import FormatException, assert_format


class _InputParser:
    def __init__(self, full_str_pattern):
        self.__full_str_pattern = re.compile(full_str_pattern)

    def matches(self, string):
        return self.__full_str_pattern.match(string) is not None

    def _parse_tape_list(self, string):
        raise NotImplementedError('abstract method')

    def parse_tape(self, string, num_of_tapes):
        tapes = self._parse_tape_list(string)
        assert_format(len(tapes) > 0, 'expect tapes to be non empty', string)

        if len(tapes) < num_of_tapes:
            num_of_missing_tapes = num_of_tapes - len(tapes)
            tapes.extend([Tape() for _ in range(num_of_missing_tapes)])

        assert_format(len(tapes) == num_of_tapes, 'number of tapes exceeded', string)
        return MultiTape(tapes) if len(tapes) > 1 else tapes[0]


class _SingleCharInputParser(_InputParser):
    '''
    Eignet sich für Input der nur aus einzelnen Charactern besteht
    Input Strings sind von der Form: char1char2 char1char2
    '''
    _VALID_CHAR_PTRN = '[^,;:{}\s]'

    _INPUT_PTRN = '({}+ )*{}*'.format(_VALID_CHAR_PTRN, _VALID_CHAR_PTRN)

    def __init__(self):
        super().__init__(_SingleCharInputParser._INPUT_PTRN)

    def _parse_tape_list(self, string):
        return [Tape(list(chars)) for chars in string.split(' ')]


class _SimpleInputParser(_InputParser):
    '''
    Eignet sich für einfachen Input, der über einzelne Character hinausgeht
    Input Strings sind von der Form: item1,item2;item1,item2
    '''

    _VALID_CHAR_PTRN = '[^,;]'

    _INPUT_PTRN = '(({}+,)+{};?)+'.format(_VALID_CHAR_PTRN, _VALID_CHAR_PTRN)

    def __init__(self):
        super().__init__(_SimpleInputParser._INPUT_PTRN)

    def _parse_single_tape(self, string):
        entries = [e.strip() for e in string.split(',')]
        return Tape(entries)

    def _parse_tape_list(self, string):
        return [self._parse_single_tape(entries) for entries in string.split(';')]


class _GernericInputParser(_InputParser):
    '''
    Eignet sich für Input mit komplexen Sonderzeichen.
    Input Strings sind von der Form: tape:{'item1','item2'}: tape:{'item1','item2'}:
    '''

    _TAPE_PTRN = 'tape:{.*}:'

    _INPUT_PTRN = '(({})\s+)*({})'.format(_TAPE_PTRN, _TAPE_PTRN)

    def __init__(self):
        super().__init__(_GernericInputParser._INPUT_PTRN)
        self.__tape_open_ptrn = re.compile('tape:{')
        self.__tape_close_ptrn = re.compile('}:')
        self.__item_ptrn = re.compile('\'(?P<item>[^\']+),?\'')

    def _parse_single_tape(self, string):
        entries = [match.group('item') for match in self.__item_ptrn.finditer(string)]
        return Tape(entries)

    def _parse_tape_list(self, string):
        open_pos = [match.end() for match in self.__tape_open_ptrn.finditer(string)]
        close_pos = [match.start() for match in self.__tape_close_ptrn.finditer(string)]

        assert_format(len(open_pos) == len(close_pos), 'mismatch of opening an closing tags', string)
        return [self._parse_single_tape(string[l:r]) for l, r in zip(open_pos, close_pos)]


_PARSER = [_GernericInputParser(), _SimpleInputParser(), _SingleCharInputParser()]


def parse_tape(string, num_of_tapes):
    for parser in _PARSER:
        if parser.matches(string):
            return parser.parse_tape(string, num_of_tapes)
    raise FormatException('undefined format', string)


def load_tape(path, num_of_tapes):
    with open(path, 'r') as file:
        tape_str = ''.join(file.readlines())
        return parse_tape(tape_str, num_of_tapes)
