import random
from ..lib.constants import NUM_OUTS
from ..lib.dsp import BipolarTrigger


class CellularAutomata:

    interesting_rules = (22, 30, 45, 73, 75, 86, 89, 110)

    def __init__(self, rule_number):
        self.rule = rule_number
        self.randomize()
        self.trigger = BipolarTrigger(rising_thresh=1)

    @property
    def rule(self):
        return self._rule

    @rule.setter
    def rule(self, number):
        self._rule = number
        # Convert a rule number (such as Rule 30: https://mathworld.wolfram.com/Rule30.html) to
        # a list of 8 booleans indicating the 8 possible state transitions for elemenentary cellular automata.
        binary_representation = format(number, '0' + str(NUM_OUTS) + 'b')
        self._transitions = [x == '1' for x in list(binary_representation)]

    def randomize(self):
        # use '0' and '1' to represent state because we can use it to form binary numbers and
        # easily lookup the transition to use.
        self.state = random.choices([True, False], k=NUM_OUTS)
        self._next_state = self.state.copy()

    def step(self):
        state = self.state
        for i in range(NUM_OUTS):
            transition_index = 0
            if state[(i - 1) % NUM_OUTS]:
                transition_index += 4
            if state[i]:
                transition_index += 2
            if state[(i + 1) % NUM_OUTS]:
                transition_index += 1
            self._next_state[i] = self._transitions[transition_index]
        self.state = self._next_state
        self._next_state = state

    def process(self, volts, output):
        if self.trigger.detect(volts):
            if volts > 0:
                self.step()
            else:
                rules = CellularAutomata.interesting_rules
                self.rule = rules[abs(int(2 * volts)) % len(rules)]
                self.randomize()

            for i in range(NUM_OUTS):
                output(i, self.state[i])
