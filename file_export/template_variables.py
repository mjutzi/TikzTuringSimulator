import collections

TapeItemTemplateVariables = collections.namedtuple('TapeItemTemplateVariables', 'tape_index value type')

TapeTemplateVariables = collections.namedtuple('TapeTemplateVariables', 'index items current_item_index')

StateTemplateVariables = collections.namedtuple('StateTemplateVariables', 'name type')

TuringMachineTemplateVariables = collections.namedtuple('TuringMachineTemplateVariables', 'states tapes')

IterationTemplateVariables = collections.namedtuple('IterationTemplateVariables',
                                                    'turing_machine iteration_count remarks new_chars move_directions')

DocumentTemplateVariables = collections.namedtuple('DocumentTemplateVariables', 'iterations remark')
