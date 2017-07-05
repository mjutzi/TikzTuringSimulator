import collections

from core.tape import Direction
from core.turing_machine import TuringMachine
from core.turing_states import TransitionGraph, TransitionTarget, State
from file_import.exceptions import FormatException

Header = collections.namedtuple('Header',
                                'num_of_bands num_of_states chars_in chars_out empty_char accepted_states initial_state')

Command = collections.namedtuple('Command', 'current_state read_chars new_state new_chars move_directions')


def _compile_states(commands):
    states1 = {command.current_state for command in commands}
    states2 = {command.new_state for command in commands}

    state_names = list(states1 | states2)
    state_names.sort()

    states = [State(index=index, name=name) for index, name in enumerate(state_names)]

    find_by_name = {state.name: state for state in states}
    find_by_index = states

    return find_by_name, find_by_index


def _compile_transition_graph(commands, find_state):
    transition_graph = TransitionGraph()
    directions = {'L': Direction.LEFT, 'R': Direction.RIGHT, 'N': Direction.NONE}

    for command in commands:
        current_state = find_state(command.current_state)
        read_chars = command.read_chars

        target = TransitionTarget(
            new_state=find_state(command.new_state),
            new_chars=command.new_chars,
            move_directions=directions[command.move_directions])

        transition_graph.register_transition(current_state, read_chars, target)

    return transition_graph


def compile_turing_machine(header, commands, band_alphabet):
    find_by_name, find_by_index = _compile_states(commands)

    def find_state(name_or_index):
        if name_or_index in find_by_name:
            return find_by_name[name_or_index]

        try:
            index = int(name_or_index)
            return find_by_index[index]

        except (ValueError, IndexError) as error:
            raise FormatException('state is unknown', name_or_index)

    transition_graph = _compile_transition_graph(commands, find_state)

    initial_state = find_state(header.initial_state) if header.initial_state else find_by_index[0]
    final_states = {find_state(descriptor) for descriptor in header.accepted_states}

    return TuringMachine(initial_state, final_states, transition_graph, band_alphabet)
