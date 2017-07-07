import collections

TapeItemTemplateVariables = collections.namedtuple('TapeItemTemplateVariables', 'tape_index value type')

TapeTemplateVariables = collections.namedtuple('TapeTemplateVariables', 'index items current_item_index')

StateTemplateVariables = collections.namedtuple('StateTemplateVariables', 'name type')

IterationTemplateVariables = collections.namedtuple('IterationTemplateVariables', 'index states tapes')

DocumentTemplateVariables = collections.namedtuple('DocumentTemplateVariables', 'iterations remark')
