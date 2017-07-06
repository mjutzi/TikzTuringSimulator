from file_export.template_variables import *

'''
TapeItemTemplateVariables = collections.namedtuple('TapeItemTemplateVariables', 'tape_index value type specifier')

TapeTemplateVariables = collections.namedtuple('TapeTemplateVariables', 'index items')

StateTemplateVariables = collections.namedtuple('StateTemplateVariables', 'name specifier')

TuringMachineTemplateVariables = collections.namedtuple('TuringMachineTemplateVariables', 'states tapes')

IterationTemplateVariables = collections.namedtuple('IterationTemplateVariables', 'turing_machine iteration_count')

DocumentTemplateVariables = collections.namedtuple('DocumentTemplateVariables', 'iterations remark')
'''


def _create_tape_item_var(value, item_index, current_item_index, tape_index):
    item_type = 'selected_item' if item_index == current_item_index else 'regular_item'
    return TapeItemTemplateVariables(tape_index=tape_index, value=value, type=item_type)


def _create_tape_var(entries, current_item_index, tape_index, offset=0):
    def item_var(value, item_index):
        return _create_tape_item_var(value, item_index, current_item_index, tape_index)

    items = [item_var(value, index + offset) for index, value in enumerate(entries)]
    return TapeTemplateVariables(index=tape_index, items=items)


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


def _create_tape_vars(tape, limit_items_to):
    return [_create_tape_var_d1(d1_tape, tape_index, limit_items_to)
            for tape_index, d1_tape in enumerate(tape.inner_tapes)]


def create_iteration_variable(iteration_count, transition_event, tape, states, limit_items_to=15):
    pass
