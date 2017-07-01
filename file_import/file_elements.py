import collections

from core.turing_machine import TuringMachine
from core.turing_states import TransitionGraph, TransitionTarget, State

Header = collections.namedtuple('Header',
                                'num_of_bands num_of_states chars_in chars_out empty_char accepted_states initial_state')

Command = collections.namedtuple('Command', 'current_state read_chars new_state new_chars move_directions')


def _compile_states(commands):
    states1 = set(command.state_old for command in commands)
    states2 = set(command.state_new for command in commands)

    states = list(states1 | states2)
    sorted(states)

    state_dict = {name: State(index=index, name=name) for index, name in enumerate(states)}
    first_state = state_dict[states[0]]

    return first_state, state_dict


def _compile_transition_graph(states, commands):
    transition_graph = TransitionGraph()

    for command in commands:
        state_old = states[command.state_old]
        read_chars = command.chars_read

        target = TransitionTarget(
            new_state=states[command.state_new],
            new_chars=command.chars_write,
            move_directions=command.head_directions)

        transition_graph.register_transition(state_old, read_chars, target)

    return transition_graph


def compile_turing_machine(header, commands):
    first_state, state_dict = _compile_states(commands)
    transition_graph = _compile_transition_graph(state_dict, commands)

    initial_state = header.initial_state if header.initial_state else first_state
    final_states = header.accepted_states

    return TuringMachine(initial_state, final_states, transition_graph)
