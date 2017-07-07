from file_export.formatting import TemplateItemFormatter


class TemplateEngine:
    def __init__(self, formats, delimiter):
        self.__formats = formats
        self.delimiter = delimiter

    @staticmethod
    def load(path, delimter='\n'):
        template_item_names = ['tape_item', 'tape', 'state', 'states', 'iteration', 'document']
        template_items = {item_name: TemplateItemFormatter(path, item_name) for item_name in template_item_names}
        return TemplateEngine(template_items, delimter)

    def __getitem__(self, key):
        return self.__formats[key]

    def __format_each(self, elements, format_fn):
        return self.delimiter.join(format_fn(element) for element in elements)

    def __compile_item(self, variables):
        return self['tape_item'].inject_values(variables)

    def __compile_tape(self, variables):
        return self['tape'].format(index=variables.index,
                                   items=self.__format_each(variables.items, self.__compile_item),
                                   current_item_index=variables.current_item_index)

    def __compile_state(self, variables):
        return self['state'].inject_values(variables)

    def __compile_states(self, states):
        return self['states'].format(items=self.__format_each(states, self.__compile_state))

    def __compile_iteration(self, variables):
        return self['iteration'].format(index=variables.index,
                                        states=self.__compile_states(variables.states),
                                        tapes=self.__format_each(variables.tapes, self.__compile_tape))

    def compile_document(self, variables):
        return self['document'].format(remark=variables.remark,
                                       iterations=self.__format_each(variables.iterations, self.__compile_iteration))

    def create_document(self, variables, output_file):
        with open(output_file, 'w') as file:
            file.write(self.compile_document(variables))

    def execute_postconstruct_script(self, output_file):
        pass  # todo
