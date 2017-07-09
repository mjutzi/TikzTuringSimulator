import os

from file_export.formatting import TemplateItemFormatter
from utils.os_utils import runcmd
from utils.settings_utils import load_settings


class TemplateEngine:
    def __init__(self, settings, formats, delimiter):
        self.__settings = settings
        self.__formats = formats
        self.delimiter = delimiter

    @staticmethod
    def load(path, delimter='\n'):
        template_item_names = ['tape_item', 'tape', 'state', 'states', 'iteration', 'document']
        template_items = {item_name: TemplateItemFormatter(path, item_name) for item_name in template_item_names}

        default_settings = {'doc_name': 'document', 'gen_name': 'document', 'compile_cmd': None}
        settings_file = os.path.join(path, 'settings')
        settings_dict = load_settings(settings_file, default_settings)

        return TemplateEngine(settings_dict, template_items, delimter)

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

    def _run_compile_cmd(self, out_dir):
        compile_cmd = self.__settings['compile_cmd']
        if compile_cmd:
            timeout_10_min = 10 * 60
            runcmd(compile_cmd, cwd=out_dir, timeout=timeout_10_min)

    def create_document(self, variables, out_dir):
        doc_file = os.path.join(out_dir, self.__settings['doc_name'])
        gen_file = os.path.join(out_dir, self.__settings['gen_name'])

        with open(doc_file, 'w') as file:
            file.write(self.compile_document(variables))

        self._run_compile_cmd(out_dir)

        return gen_file
