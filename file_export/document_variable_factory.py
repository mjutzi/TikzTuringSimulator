from file_export.template_variables import *


def _create_tape_item_vars(value, item_index, current_item_index, tape_index):
    item_type = 'selected_item' if item_index == current_item_index else 'regular_item'
    return TapeItemTemplateVariables(tape_index=tape_index, value=value, type=item_type)


def _create_tape_vars(entries, current_item_index, tape_index, offset=0):
    def item_var(value, item_index):
        return _create_tape_item_vars(value, item_index, current_item_index, tape_index)

    items = [item_var(value, index + offset) for index, value in enumerate(entries)]
    return TapeTemplateVariables(index=tape_index, items=items, current_item_index=current_item_index)


def _clamp(entries, view_point, max_length):
    n = len(entries)
    limit = min(max_length, n)

    half = (limit + 1) // 2
    mid_l = view_point - half
    mid_r = view_point + half

    if mid_l < 0:
        return entries[0:limit], 0

    if mid_r > n:
        return entries[n - limit:n], n - limit

    return entries[mid_l:mid_r], mid_l


def _create_single_tape_vars(d1_tape, tape_index, limit):
    entries, offset = _clamp(d1_tape.entries, d1_tape.position, limit)
    return _create_tape_vars(entries, d1_tape.position, tape_index, offset)


def create_tape_vars(tape, limit_items_to):
    return [_create_single_tape_vars(d1_tape, tape_index, limit_items_to)
            for tape_index, d1_tape in enumerate(tape.inner_tapes)]


def _create_state_vars(states, current_state, limit):
    current_state_idx = current_state.index if current_state else 0

    def state_type(state):
        return 'selected_state' if state.index == current_state_idx  else 'regular_state'

    state_list, _ = _clamp(list(states), current_state_idx, limit)
    return [StateTemplateVariables(name=state.name, type=state_type(state)) for state in state_list]


class DocumentVariableFactory:
    def __init__(self, tape, states, tape_item_limit=12, state_item_limit=12):
        self.__tape = tape
        self.__states = states
        self.__tape_item_limit = tape_item_limit
        self.__state_item_limit = state_item_limit

        self.__iterations = []
        self.__remark = ''

    def add_iteration(self, transition_event, transition_target):
        selected_state = transition_target.new_state if transition_target else None
        iter_var = IterationTemplateVariables(
            index=len(self.__iterations),
            states=_create_state_vars(self.__states, selected_state, self.__state_item_limit),
            tapes=create_tape_vars(self.__tape, self.__tape_item_limit))

        self.__iterations.append(iter_var)

    def set_remark(self, remark):
        self.__remark = remark

    def empty(self):
        return not self.__iterations

    def document_variables(self):
        return DocumentTemplateVariables(iterations=self.__iterations, remark=self.__remark)
