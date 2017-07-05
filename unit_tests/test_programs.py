from unittest import TestCase

from file_import.parser import parse_lines


class TestSolutions(TestCase):

    def test_collatz(self):
        lines = [
            '1|7|0,1|0,1,B|B|6;',
            'q0,0>q0,0,R',
            'q0,1>q0,1,R',
            'q0,B>q1,B,L',
            'q1,0>q1,B,L',
            'q1,1>q2,1,L',
            'q2,0>q4,0,R',
            'q2,1>q4,1,R',
            'q2,B>q6,B,R',
            'q3,0>q3,0,L',
            'q3,1>q4,1,L',
            'q3,B>q0,B,R',
            'q4,0>q3,1,L',
            'q4,1>q5,0,L',
            'q4,B>q0,1,R',
            'q5,0>q4,0,L',
            'q5,1>q5,1,L',
            'q5,B>q4,0,L'
        ]

        turing_machine = parse_lines(lines)
        # todo

    def test_div_by_3(self):
        lines = [
            '1 | 6 | 0, 1 | 0, 1, B | B | 5;',
            'q0, 0 > q0, B, R',
            'q0, 1 > q1, 1, R',
            'q0, B > q5, B, R',
            'q1, 0 > q3, 0, R',
            'q1, 1 > q2, 0, L',
            'q2, 0 > q2, 0, L',
            'q2, 1 > q2, 0, L',
            'q2, B > q0, B, R',
            'q3, 0 > q2, 1, L',
            'q3, 1 > q4, 0, L',
            'q4, 0 > q2, 1, L'
        ]

        turing_machine = parse_lines(lines)
        # todo

    def test_div_by_7(self):
        lines = [
            '1|17|0,1|0,1,B|B|16;',
            'q0,0>q0,B,R',
            'q0,1>q1,1,R',
            'q0,B>q16,B,R',
            'q1,0>q2,0,R',
            'q1,1>q3,1,R',
            'q2,0>q4,0,R',
            'q2,1>q5,1,R',
            'q3,0>q6,0,R',
            'q3,1>q7,0,L',
            'q4,0>q7,1,L',
            'q4,1>q8,0,L',
            'q5,0>q9,1,L',
            'q5,1>q10,0,L',
            'q6,0>q12,1,L',
            'q6,1>q14,0,L',
            'q7,0>q7,0,L',
            'q7,1>q7,0,L',
            'q7,B>q0,B,R',
            'q8,0>q7,1,L',
            'q9,1>q7,1,L',
            'q10,1>q11,0,L',
            'q11,0>q7,1,L',
            'q12,0>q13,0,L',
            'q13,1>q7,1,L',
            'q14,0>q15,1,L',
            'q15,1>q7,1,L'
        ]

        turing_machine = parse_lines(lines)
        # todo
