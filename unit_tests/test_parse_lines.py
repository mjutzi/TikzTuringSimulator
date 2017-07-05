from unittest import TestCase

from file_import.parser import parse_lines


class TestParseLines(TestCase):
    def test_parse_lines_returns_single_band_turing_machine(self):
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

        result = parse_lines(lines)


