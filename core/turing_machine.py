class InvalidCharacterException(Exception):
    def __init__(self, chars):
        super(InvalidCharacterException, self).__init__('\'{}\' are not in alphabet.'.format(chars))


class InvalidStateException(Exception):
    def __init__(self, event):
        super(InvalidStateException, self).__init__('event={} is not registered.'.format(event))


class TuringMachine:
    def __init__(self, initial_state, final_states, transition_graph, alphabet=None):
        self.initial_state = initial_state
        self.final_states = final_states
        self.transition_graph = transition_graph
        self.alphabet = alphabet

    def assert_has_only_alphabet_chars(self, tape):
        '''
        Prüft ob das Band nur character aus dem gesetzten Alphabet hat.
        '''
        tape.set_alphabet(self.alphabet)
        non_alphabet_chars = tape.non_alphabet_chars()

        if len(non_alphabet_chars) > 0:
            raise InvalidCharacterException(non_alphabet_chars)

    def as_iterator(self, tape):

        current_state = self.initial_state

        while not current_state in self.final_states:

            event, target = self.transition_graph.get_transition(current_state, tape.read())

            if not target:
                raise InvalidStateException(event)

            tape.write(target.new_chars)
            tape.move(target.move_directions)

            current_state = target.new_state

            yield event, target
