class InvalidCharacterException(Exception):
    def __init__(self, chars):
        super(InvalidCharacterException, self).__init__('\'{}\' are not in alphabet.'.format(chars))


class TuringMachine:
    def __init__(self, initial_state, final_states, transition_graph, alphabet=None):
        self.initial_state = initial_state
        self.final_states = final_states
        self.transition_graph = transition_graph
        self.alphabet = alphabet

    def assert_charset(self, tape):
        '''
        Prüft ob das Band nur character aus dem gesetzten Alphabet hat und setzt das Bandalphabet, des Tape Objektes.
        '''
        tape.set_alphabet(self.alphabet)
        non_alphabet_chars = tape.non_alphabet_chars()

        if len(non_alphabet_chars) > 0:
            raise InvalidCharacterException(non_alphabet_chars)

    def as_iterator(self, tape):
        '''
        Führt das Program mit dem aktuellen Band als input aus. In jeder Iteration wird dabei eine Instanz von
        TransitionEvent und TransitionTarget zurück gegeben. Das Event Beschreibt ein Tupel aus dem aktuelllen Zustand
        und den gelesenen Buchstaben. TransitionTarget, beschreibt ein Tupel aus dem Zielzustand, den zu schreibenden
        Buchstaben und der Kopfbewegung(en) aud den Band bzw. Bändern.
        Ist der Input valide, so Terminiert das Program in einem der finalen Zustände. Anderen Falls ist in einer Iteration
        Traget None und die Iteration wird abgebrochen.
        :param tape: eine Instanz von Tape oder MultiTape
        :return: einen Generator, der die Zustandswechsel zurück gibt.
        '''
        current_state = self.initial_state

        while current_state and not current_state in self.final_states:

            event, target = self.transition_graph.get_transition(current_state, tape.read())

            if target:
                tape.write(target.new_chars)
                tape.move(target.move_directions)
                current_state = target.new_state
            else:
                current_state = None

            yield event, target

    @property
    def states(self):
        return self.transition_graph.states
