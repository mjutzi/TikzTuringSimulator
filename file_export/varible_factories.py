from file_export.template_variables import *


def _create_tape_item_var(value, item_index, current_item_index, tape_index):
    item_type = 'selected_item' if item_index == current_item_index else 'regular_item'
    return TapeItemTemplateVariables(tape_index=tape_index, value=value, type=item_type)


def _create_tape_var(entries, current_item_index, tape_index, offset=0):
    def item_var(value, item_index):
        return _create_tape_item_var(value, item_index, current_item_index, tape_index)

    items = [item_var(value, index + offset) for index, value in enumerate(entries)]
    return TapeTemplateVariables(index=tape_index, items=items, current_item_index=current_item_index)


def _clamp(entries, left, right):
    l = max(0, left)
    r = min(len(entries), right)
    return entries[l:r], left, right


def _create_tape_var_d1(d1_tape, tape_index, limit):
    item_index = d1_tape.position
    entries = d1_tape.entries
    offset = 0

    if item_index <= limit:
        entries, offset, _ = _clamp(entries, 0, limit)
    else:
        entries, offset, _ = _clamp(entries, item_index - limit // 2, item_index + limit // 2)

    return _create_tape_var(entries, item_index, tape_index, offset)


def create_tape_variables(tape, limit_items_to):
    return [_create_tape_var_d1(d1_tape, tape_index, limit_items_to)
            for tape_index, d1_tape in enumerate(tape.inner_tapes)]


def create_state_variables(states, current_state):
    def state_type(state):
        return 'selected_state' if state.index == current_state.index else 'regular_state'

    return [StateTemplateVariables(name=state.name, type=state_type(state)) for state in states]


def create_iteration_variables(iteration_count, tape, current_state, states, tape_item_limit=12):
    return IterationTemplateVariables(
        iteration_count=iteration_count,
        turing_machine=TuringMachineTemplateVariables(
            states=create_state_variables(states, current_state),
            tapes=create_tape_variables(tape, tape_item_limit)))
