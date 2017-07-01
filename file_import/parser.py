from file_import.file_elements import Header, Command, compile_turing_machine
from file_import.file_formats import DEFAULT_COMMAND_PATTERN, DEFAULT_HEADER_PATTERN, DEFAULT_IGNORE_LINE
from file_import.file_formats import CUSTOM_COMMAND_PATTERN, CUSTOM_HEADER_PATTERN, CUSTOM_IGNORE_LINE


def _value(group_name, match):
    return match.group(group_name).strip()


def _optional(group_name, match):
    if group_name in match.groups():
        return match.group(group_name).strip()
    else:
        return None


def _sequence(group_name, match, sequence_length=None):
    if sequence_length == 1:
        return _value(group_name, match)
    else:
        seq = [char.strip() for char in _value(group_name, match).split(',')]
        assert not sequence_length or len(seq) == sequence_length, \
            'expected length n={} got n\'={}'.format(sequence_length, len(seq))
        return seq


def _parse_header(str, pattern):
    match = pattern.match(str)
    assert match, '\'{}\' does not match command pattern'.format(str)

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
    assert match, '\'{}\' does not match command pattern'.format(str)

    return Command(
        current_state=_value('current_state', match),
        read_chars=_sequence('read_chars', match, num_of_bands),
        new_state=_value('new_state', match),
        new_chars=_sequence('new_chars', match, num_of_bands),
        move_directions=_sequence('move_directions', match, num_of_bands)
    )


def _patterns_by_format(fromat):
    if format == 'custom':
        return CUSTOM_IGNORE_LINE, CUSTOM_HEADER_PATTERN, CUSTOM_COMMAND_PATTERN
    else:
        return DEFAULT_IGNORE_LINE, DEFAULT_HEADER_PATTERN, DEFAULT_COMMAND_PATTERN


def parse_file(path, file_format='default'):
    ignore_pattern, header_pattern, command_pattern = _patterns_by_format(file_format)

    with open(path, 'r') as file:
        lines = [line for line in file.readlines() if not ignore_pattern.match(line)]
        header = _parse_header(lines[0], header_pattern)
        commands = [_parse_command(line, header.num_of_bands, command_pattern) for line in lines[1:]]

        return compile_turing_machine(header, commands)
