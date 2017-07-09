import argparse
import os

from core.tape_parser import parse_tape, load_tape
from file_export.document_variable_factory import DocumentVariableFactory
from file_export.template_engine import TemplateEngine
from file_import.parser import parse_file
from utils.os_utils import os_open_command, open_with


class ExecuteTM:
    def __init__(self, turing_machine, observer=None):
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

        tape = load_tape(input_string) if os.path.isfile(input_string) else parse_tape(input_string)
        self.__turing_machine.assert_charset(tape)
        self.__init_observer(tape)

        for transition_event, transition_target in self.__turing_machine.as_iterator(tape):
            self.__notify_observer(transition_event, transition_target)

    @staticmethod
    def _parse_file(filename):
        turing_machine = parse_file(filename)
        return ExecuteTM(turing_machine)


class VisualizeTM:
    def __init__(self, template_engine, viewer):
        self.__template_engine = template_engine
        self.__viewer = viewer

        self.__tape_item_limit = 12
        self.__doc_factory = None
        self.__generated_file = None

    @staticmethod
    def create(template_path, viewer=os_open_command()):
        template_engine = TemplateEngine.load(template_path)
        return VisualizeTM(template_engine, viewer)

    def register_state(self, tape, states):
        self.__doc_factory = DocumentVariableFactory(tape, states, self.__tape_item_limit)

    def register_iteration(self, transition_event, transition_target):
        self.__doc_factory.add_iteration(transition_target)

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

    def visualize(self):
        if not self.__generated_file:
            self.write_file()

        open_with(self.__generated_file, self.__viewer)


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
        if transition_target:
            event_str = self._format_event(transition_event)
            target_str = self._format_target(transition_target)
            print(event_str, ' > ', target_str)
        else:
            print('Input string is invalid.')


'''
TODO parse commands
'''
parser = argparse.ArgumentParser(description='Visualizes Turing Machines')
parser.add_argument('--turing_program', help='the path to the turing program')
parser.add_argument('--tape', help='the path to the tape to run')
parser.add_argument('--out_dir', help='the path to the tape to run')

parser.add_argument('--interactive', help='the path to the turing program')
parser.add_argument('--template', help='the path to the turing program')
parser.add_argument('--tape_item_limit', help='the path to the turing program')
parser.add_argument('--verbose', help='the path to the turing program')

file_to_tm = '/home/martin_jutzi/Temp/teilfolge.txt'
tm_executor = ExecuteTM._parse_file(file_to_tm)

template_path = '/home/martin_jutzi/PycharmProjects/TikzTuringSimulator/templates/latex'
tape_item_limit = 12
viewer = ''

visual_executor = VisualizeTM.create(template_path)
visual_executor.set_tape_item_limit(tape_item_limit)
# visual_executor.set_viewer(viewer)

tm_executor.add_observer(PrintTM())
tm_executor.add_observer(visual_executor)

# 0', '0', '1', '1', '1
tape_str = '1,1,0,1,-,0,0,1,1,1,1,0,1;B'
tm_executor.execute_TM(tape_str)

output_dir = '/home/martin_jutzi/Temp'
visual_executor.write_file(output_dir)
