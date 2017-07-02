from unittest import TestCase

from core.band import BandDirection, Band, MultiBand
from core.turing_machine import TuringMachine
from core.turing_states import State, TransitionGraph, TransitionEvent, TransitionTarget


class TestTuringMachine(TestCase):
    def setUp(self):
        self.state_1 = State(index=1, name='state 1')
        self.state_2 = State(index=2, name='state 2')
        self.state_3 = State(index=3, name='state 3')

        self.transition_graph = TransitionGraph()
        self.transition_graph.register_transition(self.state_1, ['1', '2'],
                                                  TransitionTarget(
                                                      new_state=self.state_2,
                                                      new_chars=['2', '1'],
                                                      move_directions=[BandDirection.RIGHT, BandDirection.RIGHT]))

        self.transition_graph.register_transition(self.state_2, ['2', '3'],
                                                  TransitionTarget(
                                                      new_state=self.state_2,
                                                      new_chars=['0', '1'],
                                                      move_directions=[BandDirection.RIGHT, BandDirection.LEFT]))

        self.transition_graph.register_transition(self.state_2, ['2', '1'],
                                                  TransitionTarget(
                                                      new_state=self.state_3,
                                                      new_chars=['-', '-'],
                                                      move_directions=[BandDirection.NONE, BandDirection.NONE]))

        self.under_test = TuringMachine(self.state_1, {self.state_3}, self.transition_graph, None)

    def test_turing_machine_writes_accurately(self):
        band1_chars = ['1', '2', '2']
        band2_chars = ['2', '3', '1']
        multi_band = MultiBand([Band(band1_chars), Band(band2_chars)])

        for _, _ in self.under_test.as_iterator(multi_band):
            pass

        expected_band1 = ['2', '0', '-']
        expected_band2 = ['-', '1', '1']

        self.assertEqual(band1_chars, expected_band1, 'check final chars of first band')
        self.assertEqual(band2_chars, expected_band2, 'check final chars of second band')
