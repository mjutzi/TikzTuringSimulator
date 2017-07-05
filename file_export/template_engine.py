import collections
import os
import re

from file_export.caching import memorize

TapeItemTemplateVariables = collections.namedtuple('TapeItemTemplateVariables', 'tape_index value specifier')

TapeTemplateVariables = collections.namedtuple('TapeTemplateVariables', 'index items')

StateTemplateVariables = collections.namedtuple('StateTemplateVariables', 'states current_state')

TuringMachineTemplateVariables = collections.namedtuple('TuringMachineTemplateVariables', 'states tapes')

IterationTemplateVariables = collections.namedtuple('IterationTemplateVariables', 'turing_machine iteration_count')

DocumentTemplateVariables = collections.namedtuple('IterationTemplateVariables', 'turing_machine iteration_count')

class TemplateItemFormatter:
    def __init__(self, template_path, name):
        self.template_path = template_path
        self.name = name

    def __get_template_path(self):
        return os.path.join(self.template_path, '{}_template'.format(self.name))

    def __load_template(self):
        with open(self.__get_template_path(), 'r') as file:
            return file.read().replace('\n', '')

    def __escape_braces(self, str):
        return str.replace('{', '{{').replace('}', '}}')

    @memorize
    def __get_variable_pattern(self):
        return re.compile('<{}\.(?P<var_name>\w+)>'.format(self.name))

    def __get_template_variables(self, str):
        pattern = self.__get_variable_pattern()
        return {match.group('var_name') for match in pattern.finditer(str)}

    def __adapt_template_variables(self, str):
        pattern = self.__get_variable_pattern()
        return pattern.sub(r'{\g<var_name>}', str)

    @memorize
    def __get_fromat_string(self):
        template = self.__load_template()
        format_str = self.__escape_braces(template)

        variables = self.__get_template_variables(format_str)
        format_str = self.__adapt_template_variables(format_str)

        return format_str, variables

    def is_empty(self):
        return not os.path.exists(self.__get_template_path())

    def format_map(self, map):
        format_str, variables = self.__get_fromat_string()

        def_vars = {var: map[var] for var in map if var in variables}
        all_vars = {var: '' for var in variables}
        all_vars.update(def_vars)

        return format_str.format_map(all_vars)

    def format(self, **args):
        return self.format_map(args)

    def inject_values(self, obj):
        obj_attributes = {attr: getattr(obj, attr) for attr in dir(obj)}
        return self.format_map(obj_attributes)

class TemplateEngine:

    def __init__(self, tape_item_format, tape_format, turing_machine_format):
        pass

def load_template(path):
    pass

