import os

from core.band import BandAlphabet
from file_import.file_elements import Header, Command, compile_turing_machine
from file_import.file_formats import DEFAULT_COMMAND_PATTERN, DEFAULT_HEADER_PATTERN, DEFAULT_IGNORE_LINE
from file_import.file_formats import CUSTOM_COMMAND_PATTERN, CUSTOM_HEADER_PATTERN, CUSTOM_IGNORE_LINE
from file_import.exceptions import assert_format, FormatException


def _value(group_name, match):
    return match.group(group_name).strip()


def _optional(group_name, match):
    return match.group(group_name).strip() if group_name in match.groups() else None


def _sequence(group_name, match, sequence_length=None):
    raw_string = _value(group_name, match)
    if sequence_length == 1:
        return raw_string
    else:
        seq = [char.strip() for char in raw_string.split(',')]

        has_required_len = not sequence_length or len(seq) == sequence_length
        error_message = 'expected length n={} got n\'={}'.format(sequence_length, len(seq))
        assert_format(has_required_len, error_message, raw_string)

        return seq


def _parse_header(str, pattern):
    match = pattern.match(str)
    assert_format(match, 'does not match header pattern', str)

    return Header(
        num_of_bands=_value('num_of_bands', match),
        num_of_states=_optional('num_of_states', match),
        chars_in=_sequence('chars_in', match),
        chars_out=_sequence('chars_out', match),
        empty_char=_value('empty_char', match),
        accepted_states=_sequence('accepted_states', match),
        initial_state=_optional('initial_state', match)
    )


def _parse_command(str, num_of_bands, pattern):
    match = pattern.match(str)
    assert_format(match, 'does not match command pattern', str)

    return Command(
        current_state=_value('current_state', match),
        read_chars=_sequence('read_chars', match, num_of_bands),
        new_state=_value('new_state', match),
        new_chars=_sequence('new_chars', match, num_of_bands),
        move_directions=_sequence('move_directions', match, num_of_bands)
    )


def _get_format_by_name(parse_format):
    if not parse_format or parse_format == 'default':
        return DEFAULT_IGNORE_LINE, DEFAULT_HEADER_PATTERN, DEFAULT_COMMAND_PATTERN

    if parse_format == 'custom':
        return CUSTOM_IGNORE_LINE, CUSTOM_HEADER_PATTERN, CUSTOM_COMMAND_PATTERN

    raise ValueError('unknown format: {}'.format(parse_format))


def parse_lines(all_lines, parse_format='default'):
    ignore_pattern, header_pattern, command_pattern = _get_format_by_name(parse_format)

    lines = [line for line in all_lines if not ignore_pattern.match(line)]
    assert_format(len(lines) > 1, 'not enough lines', None)

    header = _parse_header(lines[0], header_pattern)
    commands = [_parse_command(line, header.num_of_bands, command_pattern) for line in lines[1:]]

    band_alphabet = BandAlphabet(chars=set(header.chars_in), empty_char=header.empty_char)
    turing_machine = compile_turing_machine(header, commands)

    return band_alphabet, turing_machine


def parse_file(path):
    _, file_extension = os.path.splitext(path)
    format = 'custom' if file_extension == 'tur' else 'default'

    with open(path, 'r') as file:
        return parse_lines(file.readlines(), format)
