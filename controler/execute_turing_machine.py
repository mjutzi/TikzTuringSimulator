import os

from core.tape_parser import parse_tape, load_tape
from file_import.parser import parse_file


class ExecuteTM:
    '''
    Hilfklasse zum ausführen von Turing maschinen.
    '''

    def __init__(self, turing_machine, observer=None):
        self.__turing_machine = turing_machine
        self.__observer = observer if observer else []

    def add_observer(self, observer):
        self.__observer.append(observer)

    def __init_observer(self, tape):
        states = self.__turing_machine.states
        for observer in self.__observer:
            observer.register_state(tape, states)

    def __notify_observer(self, transition_event=None, transition_target=None):
        for observer in self.__observer:
            observer.register_iteration(transition_event, transition_target)

    def _get_tape(self, input_string, num_of_tapes):
        if os.path.isfile(input_string):
            return load_tape(input_string, num_of_tapes)
        else:
            return parse_tape(input_string, num_of_tapes)

    def execute_TM(self, input_string):

        num_of_tapes = self.__turing_machine.num_of_tapes
        tape = self._get_tape(input_string, num_of_tapes)
        self.__turing_machine.assert_charset(tape)
        self.__init_observer(tape)

        for transition_event, transition_target in self.__turing_machine.as_iterator(tape):
            self.__notify_observer(transition_event, transition_target)

    @staticmethod
    def _parse_file(filename):
        turing_machine = parse_file(filename)
        return ExecuteTM(turing_machine)
