from unittest import TestCase

from core.tape import Tape, MultiTape, Direction
from core.turing_states import State, TransitionTarget
from file_export.template_engine import *
from file_export.document_variable_factory import DocumentVariableFactory


class TestLaTeXTemplate(TestCase):
    def test_generation_of_multitape_file(self):
        tape0 = Tape(['01', '02', '03', '04', '05', '06', '07', '08', '09'])
        tape1 = Tape(['11', '12', '13', '14', '15', '16', '17', '18', '19'])

        tape = MultiTape([tape0, tape1])
        states = [State(index=0, name='q0'), State(index=1, name='q1'), State(index=2, name='q2'),
                  State(index=3, name='q3')]

        docfactory = DocumentVariableFactory(tape, states)

        directions = [[Direction.LEFT, Direction.RIGHT],
                      [Direction.LEFT, Direction.RIGHT],
                      [Direction.NONE, Direction.RIGHT],
                      [Direction.RIGHT, Direction.RIGHT],
                      [Direction.RIGHT, Direction.RIGHT],
                      [Direction.RIGHT, Direction.RIGHT],
                      [Direction.RIGHT, Direction.RIGHT],
                      [Direction.RIGHT, Direction.RIGHT],
                      [Direction.RIGHT, Direction.RIGHT],
                      [Direction.RIGHT, Direction.RIGHT]]

        for iteration, direction in enumerate(directions):
            target = TransitionTarget(new_state=states[iteration % len(states)],
                                      new_chars=['x', 'y'],
                                      move_directions=direction)

            tape.move(target.move_directions)
            tape.write(target.new_chars)

            docfactory.add_iteration(target)

        document = docfactory.document_variables()

        path2template = '../../templates/latex'
        template_engine = load_template_engine(path2template)

        path2file = 'tex_file.tex'
        template_engine.create_document(document, path2file)
