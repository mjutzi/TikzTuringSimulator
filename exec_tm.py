from core.tape_parser import parse_tape
from file_import.parser import parse_file


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
    def __init__(self, document_var_factory, template_engine, template_path):
        pass

    def register_state(self, tape, states):
        pass

    def register_iteration(self, transition_event, transition_target):
        pass

    def write_file(self, path):
        pass

    def set_viewer(self, viewername):
        pass

    def visualize(self):
        pass


# TODO:
'''
TODO
 - compile latex file 1.5 h
 - parse tape 0.5h
 - call viewer 0.5h
 - parse args and run program 2h
 - test n debug 2h
 ----------
 > DONE in 5h
'''
