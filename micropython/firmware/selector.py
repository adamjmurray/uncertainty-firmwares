import random
from ..lib.dsp import BipolarTrigger
from ..lib.constants import NUM_OUTS


class Selector:

    def __init__(self, gated=False):
        self.trigger = BipolarTrigger(rising_thresh=1)
        self.active_gate = 0
        self.gate_indexes = list(range(NUM_OUTS))
        self.gated = gated

    def process(self, volts, output):
        state_change = self.trigger.detect(volts)
        if state_change is True:
            num_gates = min(max(int(volts), -4), 4) % NUM_OUTS
            active_gates = random.sample(self.gate_indexes, num_gates)
            for index in range(NUM_OUTS):
                output(index, index in active_gates)

        elif self.gated and state_change is False:
            for index in range(NUM_OUTS):
                output(index, 0)
