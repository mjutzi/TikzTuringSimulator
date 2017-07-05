from unittest import TestCase

from core.tape import Tape
from core.turing_states import State
from file_import.parser import parse_lines


class TestSolutions(TestCase):

    def setUp(self):
        lines = [
            '1 | 6 | 0, 1 | 0, 1, B | B | 5;',
            'q0, 0 > q0, B, R',
            'q0, 1 > q1, 1, R',
            'q0, B > q5, B, N',
            'q1, 0 > q3, 0, R',
            'q1, 1 > q2, 0, L',
            'q2, 0 > q2, 0, L',
            'q2, 1 > q2, 0, L',
            'q2, B > q0, B, R',
            'q3, 0 > q2, 1, L',
            'q3, 1 > q4, 0, L',
            'q4, 0 > q2, 1, L'
        ]

        self.turing_machine, self.band_alphabet = parse_lines(lines)


    def test_tm_terminates_immediatly_if_type_ist_empty(self):

        empty_tape = Tape([], alphabet=self.band_alphabet)
        iterations = list(self.turing_machine.as_iterator(empty_tape))
        self.assertEqual(1, len(iterations))

    def test_0_is_valid_input(self):

        tape = Tape(['0'], alphabet=self.band_alphabet)
        iterations = list(self.turing_machine.as_iterator(tape))

    def test_1_is_invalid_input(self):

        tape = Tape(['1'], alphabet=self.band_alphabet)
        iterations = list(self.turing_machine.as_iterator(tape))
        print(iterations)

