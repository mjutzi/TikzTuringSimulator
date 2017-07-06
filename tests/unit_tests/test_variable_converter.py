from unittest import TestCase

from core.tape import Tape, Direction
from file_export.varible_converter import create_tape_variables, TapeTemplateVariables, TapeItemTemplateVariables


class TestVariableConverter(TestCase):
    def test__create_tape_vars_contains_current_item_if_index_greater_limit(self):
        tape = Tape(['0', '1', '2', '3', '4'])

        tape.move(Direction.RIGHT)
        tape.move(Direction.RIGHT)
        tape.move(Direction.RIGHT)
        tape.move(Direction.RIGHT)

        limit_lower_index = 2
        tape_vars = create_tape_variables(tape, limit_lower_index)

        expected_items = [TapeItemTemplateVariables(tape_index=0, value='3', type='regular_item'),
                          TapeItemTemplateVariables(tape_index=0, value='4', type='selected_item')]
        self.assertEqual(expected_items, tape_vars[0].items)

    def test__create_tape_vars_contains_current_item_if_index_smaler_limit(self):
        tape = Tape(['0', '1', '2', '3', '4'])

        tape.move(Direction.RIGHT)

        limit_lower_index = 2
        tape_vars = create_tape_variables(tape, limit_lower_index)

        expected_items = [TapeItemTemplateVariables(tape_index=0, value='0', type='regular_item'),
                          TapeItemTemplateVariables(tape_index=0, value='1', type='selected_item')]
        self.assertEqual(expected_items, tape_vars[0].items)
