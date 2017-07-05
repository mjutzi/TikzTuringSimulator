from unittest import TestCase

from file_export.template_engine import *


class TestLaTeXTemplate(TestCase):
    def test_generation_of_latex_file(self):
        item00 = TapeItemTemplateVariables(tape_index=0, value='0_0', specifier='')
        item01 = TapeItemTemplateVariables(tape_index=0, value='0_1', specifier='highlited')
        item02 = TapeItemTemplateVariables(tape_index=0, value='0_2', specifier='')

        item10 = TapeItemTemplateVariables(tape_index=1, value='1_0', specifier='')
        item11 = TapeItemTemplateVariables(tape_index=1, value='1_1', specifier='highlited')
        item12 = TapeItemTemplateVariables(tape_index=1, value='1_2', specifier='')

        tape0 = TapeTemplateVariables(index=0, items=[item00, item01, item02])
        tape1 = TapeTemplateVariables(index=1, items=[item10, item11, item12])

        state0 = StateTemplateVariables(name='q0', specifier='current_state')
        state1 = StateTemplateVariables(name='q1', specifier='state')
        turing_machine = TuringMachineTemplateVariables(states=[state0, state1], tapes=[tape0, tape1])

        iteration0 = IterationTemplateVariables(turing_machine=turing_machine, iteration_count=0)

        document = DocumentTemplateVariables(iterations=[iteration0], remark=None)

        path2template = '../../templates/latex'
        template_engine = load_template_engine(path2template)

        path2file = 'tex_file.tex'
        template_engine.create_document(document, path2file)
