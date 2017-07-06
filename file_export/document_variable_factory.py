from file_export.template_variables import *


def _create_tape_item_vars(value, item_index, current_item_index, tape_index):
    item_type = 'selected_item' if item_index == current_item_index else 'regular_item'
    return TapeItemTemplateVariables(tape_index=tape_index, value=value, type=item_type)


def _create_tape_vars(entries, current_item_index, tape_index, offset=0):
    def item_var(value, item_index):
        return _create_tape_item_vars(value, item_index, current_item_index, tape_index)

    items = [item_var(value, index + offset) for index, value in enumerate(entries)]
    return TapeTemplateVariables(index=tape_index, items=items, current_item_index=current_item_index)


def _clamp(entries, left, right):
    l = max(0, left)
    r = min(len(entries), right)
    return entries[l:r], left, right


def _create_single_tape_vars(d1_tape, tape_index, limit):
    item_index = d1_tape.position
    entries = d1_tape.entries
    offset = 0

    if item_index <= limit:
        entries, offset, _ = _clamp(entries, 0, limit)
    else:
        entries, offset, _ = _clamp(entries, item_index - limit // 2, item_index + limit // 2)

    return _create_tape_vars(entries, item_index, tape_index, offset)


def create_tape_vars(tape, limit_items_to):
    return [_create_single_tape_vars(d1_tape, tape_index, limit_items_to)
            for tape_index, d1_tape in enumerate(tape.inner_tapes)]


def _create_state_vars(states, current_state):
    def state_type(state):
        return 'selected_state' if state.index == current_state.index else 'regular_state'

    return [StateTemplateVariables(name=state.name, type=state_type(state)) for state in states]


class DocumentVariableFactory:
    def __init__(self, tape, states, tape_item_limit=12):
        self.__tape = tape
        self.__states = states
        self.__tape_item_limit = tape_item_limit

        self.__iterations = []

    def add_iteration(self, transition_target):
        turing_var = TuringMachineTemplateVariables(
            states=_create_state_vars(self.__states, transition_target.new_state),
            tapes=create_tape_vars(self.__tape, self.__tape_item_limit))

        iter_var = IterationTemplateVariables(
            iteration_count=len(self.__iterations),
            new_chars=transition_target.new_chars,
            move_directions=transition_target.move_directions,
            turing_machine=turing_var)

        self.__iterations.append(iter_var)

    def document_variables(self, remark=''):
        return DocumentTemplateVariables(iterations=self.__iterations, remark=remark)
