import os

from file_export.document_variable_factory import DocumentVariableFactory
from file_export.template_engine import TemplateEngine
from utils.os_utils import open_with, try_open


def _resolve_template_path(path_or_name):
    template = path_or_name if path_or_name else 'latex'
    if os.path.exists(template):
        return template
    else:
        controler_dir = os.path.dirname(os.path.realpath(__file__))
        template_dir = os.path.join(controler_dir, '../templates')
        return os.path.join(template_dir, template)


def is_template(path_or_name):
    path = _resolve_template_path(path_or_name)
    return os.path.isdir(path)


class VisualizeTM:
    def __init__(self, template_engine, viewer):
        self.__template_engine = template_engine
        self.__viewer = viewer

        self.__tape_item_limit = 12
        self.__doc_factory = None
        self.__generated_file = None

    @staticmethod
    def create(template, viewer=None):
        template_path = _resolve_template_path(template)
        template_engine = TemplateEngine.load(template_path)
        return VisualizeTM(template_engine, viewer)

    def register_state(self, tape, states):
        self.__doc_factory = DocumentVariableFactory(tape, states, self.__tape_item_limit)
        self.__doc_factory.add_iteration(None, None)

    def register_iteration(self, transition_event, transition_target):
        if transition_target:
            self.__doc_factory.add_iteration(transition_event, transition_target)
            self.__doc_factory.set_remark('Input is valid.')
        else:
            self.__doc_factory.set_remark('Input is invalid.')

    def set_viewer(self, viewername):
        self.__viewer = viewername

    def set_tape_item_limit(self, tape_item_limit):
        self.__tape_item_limit = tape_item_limit

    def write_file(self, output_dir='./target/'):
        if not self.__doc_factory:
            raise RuntimeError('No state registered.')

        if self.__doc_factory.empty():
            raise RuntimeError('No iterations registered.')

        os.makedirs(output_dir, exist_ok=True)
        doc_vars = self.__doc_factory.document_variables()
        self.__generated_file = self.__template_engine.create_document(doc_vars, output_dir)

        return self.__generated_file

    def visualize(self):
        if not self.__generated_file:
            self.write_file()

        if self.__viewer:
            open_with(self.__generated_file, self.__viewer)
        else:
            try_open(self.__generated_file)


class PrintTM:
    def register_state(self, tape, states):
        print('setting state of turing machine:\n tape=', tape, '\n states=', states, '\n')

    def _format_event(self, transition_event):
        return '{} read: {}'.format(transition_event.current_state.name, transition_event.read_chars)

    def _format_target(self, transition_target):
        return '{} write: {} move: {}'.format(transition_target.new_state.name,
                                              transition_target.new_chars,
                                              transition_target.move_directions)

    def register_iteration(self, transition_event, transition_target):
        if transition_event and transition_target:
            event_str = self._format_event(transition_event)
            target_str = self._format_target(transition_target)
            print(event_str, ' > ', target_str)
        else:
            print('Input string is invalid.')
