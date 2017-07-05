from unittest import TestCase
from core.tape_expansion import left_of_expandable, right_of_expandable


class TestBandExpansion(TestCase):
    def test_left_of_expandable_reducesIndexByOne_ifIndexIsGreaterZero(self):
        some_non_empty_list = [0, 1, 2, 3]
        some_positive_index = 1

        actual_index = left_of_expandable(some_positive_index, some_non_empty_list)
        expected_index = 0

        self.assertEqual(expected_index, actual_index)

    def test_left_of_expandable_expandsListByOne_ifIndexIsZero(self):
        some_non_empty_list = [0, 1, 2, 3]
        zero_index = 0

        _ = left_of_expandable(zero_index, some_non_empty_list)

        expected_list = [None, 0, 1, 2, 3]
        self.assertEqual(expected_list, some_non_empty_list)

    def test_left_of_expandable_expandsListByN_ifIndexIsNegative(self):
        some_non_empty_list = [0, 1, 2, 3]
        some_negative_index = -1

        _ = left_of_expandable(some_negative_index, some_non_empty_list)

        expected_list = [None, None, 0, 1, 2, 3]
        self.assertEqual(expected_list, some_non_empty_list)

    def test_left_of_expandable_setsIndexToZero_ifLeftIndexIsNegative(self):
        some_non_empty_list = [0, 1, 2, 3]
        some_negative_index = -1

        actual_index = left_of_expandable(some_negative_index, some_non_empty_list)
        expected_index = 0

        self.assertEqual(expected_index, actual_index)

    def test_right_of_expandable_increasesIndexByOne_ifIndexIsLowerThanSizeMinusOne(self):
        some_non_empty_list = [0, 1, 2, 3]
        far_lower_that_size = 2

        actual_index = right_of_expandable(far_lower_that_size, some_non_empty_list)
        expected_index = 3

        self.assertEqual(expected_index, actual_index)

    def test_right_of_expandable_expandsListByOne_ifIndexIsSizeMinusOne(self):
        some_non_empty_list = [0, 1, 2, 3]
        last_index = 3

        _ = right_of_expandable(last_index, some_non_empty_list)

        expected_list = [0, 1, 2, 3, None]
        self.assertEqual(expected_list, some_non_empty_list)
