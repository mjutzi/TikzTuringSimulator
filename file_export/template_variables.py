import collections

TapeItemTemplateVariables = collections.namedtuple('TapeItemTemplateVariables', 'tape_index value type specifier')

TapeTemplateVariables = collections.namedtuple('TapeTemplateVariables', 'index items')

StateTemplateVariables = collections.namedtuple('StateTemplateVariables', 'name specifier')

TuringMachineTemplateVariables = collections.namedtuple('TuringMachineTemplateVariables', 'current_sate states tapes')

IterationTemplateVariables = collections.namedtuple('IterationTemplateVariables', 'turing_machine iteration_count')

DocumentTemplateVariables = collections.namedtuple('DocumentTemplateVariables', 'iterations remark')
