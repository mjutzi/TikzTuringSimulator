import collections
import os

from file_export.formatting import TemplateItemFormatter

TapeItemTemplateVariables = collections.namedtuple('TapeItemTemplateVariables', 'tape_index value specifier')

TapeTemplateVariables = collections.namedtuple('TapeTemplateVariables', 'index items')

StateTemplateVariables = collections.namedtuple('StateTemplateVariables', 'name specifier')

TuringMachineTemplateVariables = collections.namedtuple('TuringMachineTemplateVariables', 'states tapes')

IterationTemplateVariables = collections.namedtuple('IterationTemplateVariables', 'turing_machine iteration_count')

DocumentTemplateVariables = collections.namedtuple('DocumentTemplateVariables', 'iterations remark')


class __TemplateEngine:
    DELIMITER = '\n'

    def __init__(self,
                 tape_item_format,
                 tape_format,
                 state_format,
                 turing_machine_format,
                 iteration_format,
                 document_format):
        self.tape_item_format = tape_item_format
        self.tape_format = tape_format
        self.state_format = state_format
        self.turing_machine_format = turing_machine_format
        self.iteration_format = iteration_format
        self.document_format = document_format

    def __format_each(self, elements, format_fn):
        return self.DELIMITER.join(format_fn(element) for element in elements)

    def __compile_item(self, variables):
        return self.tape_item_format.inject_values(variables)

    def __compile_tape(self, variables):
        items_string = self.__format_each(variables.items, self.__compile_item)
        return self.tape_format.format(index=variables.index, items=items_string)

    def __compile_state(self, variables):
        return self.state_format.inject_values(variables)

    def __compile_turing_machine(self, variables):
        states_str = self.__format_each(variables.states, self.__compile_state)
        tapes_str = self.__format_each(variables.tapes, self.__compile_tape)
        return self.turing_machine_format.format(states=states_str, tapes=tapes_str)

    def __compile_iteration(self, variables):
        turing_machine_string = self.__compile_turing_machine(variables.turing_machine)
        return self.iteration_format.format(iteration_count=variables.iteration_count,
                                            turing_machine=turing_machine_string)

    def compile_document(self, variables):
        iterations_string = self.__format_each(variables.iterations, self.__compile_iteration)
        return self.document_format.format(remark=variables.remark, iterations=iterations_string)

    def create_document(self, variables, output_file):
        with open(output_file, 'w') as file:
            file.write(self.compile_document(variables))


def load_template_engine(path):
    template_item_names = ['tape_item', 'tape', 'turing_state', 'turing_machine', 'iteration', 'document']
    template_items = {item_name: TemplateItemFormatter(path, item_name) for item_name in template_item_names}

    return __TemplateEngine(
        template_items['tape_item'],
        template_items['tape'],
        template_items['turing_state'],
        template_items['turing_machine'],
        template_items['iteration'],
        template_items['document']
    )
