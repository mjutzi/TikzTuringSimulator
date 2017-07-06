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
    if item_index == current_item_index:
        specifier = 'selected_item_{}'.format(tape_index)
        return TapeItemTemplateVariables(tape_index=tape_index, value=value, type='selected_item', specifier=specifier)
    else:
        return TapeItemTemplateVariables(tape_index=tape_index, value=value, type='regular_item', specifier='')


def _create_tape_var(entries, current_item_index, tape_index, offset=0):
    def item_var(value, item_index):
        return _create_tape_item_var(value, item_index, current_item_index, tape_index)

    items = [item_var(value, index + offset) for index, value in enumerate(entries)]
    return TapeTemplateVariables(index=tape_index, items=items, current_item_index=current_item_index)


def _clamp(entries, left, right):
    l = max(0, left)
    r = min(len(entries), right)
    return entries[l:r], left, right


def _create_tape_var_d1(d1_tape, tape_index, limit_items_to):
    current_item_index = d1_tape.position()
    entries = d1_tape.entries()
    offset = 0

    if tape_index <= limit_items_to:
        entries, offset, _ = _clamp(entries, 0, limit_items_to)
    else:
        entries, offset, _ = _clamp(entries, tape_index - limit_items_to // 2, tape_index + limit_items_to // 2)

    return _create_tape_var(entries, current_item_index, tape_index, offset)


def create_tabe_vars(tape, limit_items_to):
    return [_create_tape_var_d1(d1_tape, tape_index, limit_items_to)
            for tape_index, d1_tape in enumerate(tape.inner_tapes())]


def create_iteration_variable(iteration_count, transition_event, tape, states, limit_items_to=15):
    pass
