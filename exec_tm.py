import os

from core.tape_parser import parse_tape
from file_export.document_variable_factory import DocumentVariableFactory
from file_export.template_engine import TemplateEngine
from file_import.parser import parse_file

from utils.os_utils import os_open_command, open_with


class ExecuteTM:
    def __init__(self, turing_machine, observer):
        self.__turing_machine = turing_machine
        self.__observer = observer if observer else []

    def add_observer(self, observer):
        self.__observer.append(observer)

    def __init_observer(self, tape):
        states = self.__turing_machine.states
        for observer in self.__observer:
            observer.register_state(tape, states)

    def __notify_observer(self, transition_event, transition_target):
        for observer in self.__observer:
            observer.register_iteration(transition_event, transition_target)

    def execute_TM(self, input_string):

        tape = parse_tape(input_string)
        self.__turing_machine.assert_charset(tape)
        self.__init_observer(tape)

        for transition_event, transition_target in self.__turing_machine.as_iterator(tape):
            self.__notify_observer(transition_event, transition_target)

    @staticmethod
    def _parse_file(filename):
        turing_machine = parse_file(filename)
        return ExecuteTM(turing_machine)


class VisualizeTM:
    def __init__(self, output_dir, template_engine, viewer):
        self.__output_dir = output_dir
        self.__template_engine = template_engine
        self.__viewer = viewer

        self.__doc_factory = None
        self.__generated_file = None

    def create(self, output_dir, template_path, viewer=os_open_command()):
        os.makedirs(self.__output_dir, exist_ok=True)
        template_engine = TemplateEngine.load(template_path)
        return VisualizeTM(output_dir, template_engine, viewer)

    def register_state(self, tape, states):
        self.__doc_factory = DocumentVariableFactory(tape, states)

    def register_iteration(self, transition_event, transition_target):
        self.__doc_factory.add_iteration(transition_target)

    def set_viewer(self, viewername):
        self.__viewer = viewername

    def write_file(self):
        if not self.__doc_factory:
            raise RuntimeError('No state registered.')

        if self.__doc_factory.empty():
            raise RuntimeError('No iterations registered.')

        doc_vars = self.__doc_factory.document_variables()
        self.__generated_file = self.__template_engine.create_document(doc_vars, self.__output_dir)

    def visualize(self):
        if not self.__generated_file:
            self.write_file()

        open_with(self.__generated_file, self.__viewer)




class RunConfiguration:
    def __init__(self, output_dir):
        self.args['output_dir']

        self.output_dir = output_dir
        self.template_path = 'templates/latex'
        self.viewer = os_open_command()


# TODO:
'''
TODO
 - compile latex file 1.5 h
 - parse args and run program 2h
 - test n debug 2h
 ----------
 > DONE in 5h
'''
