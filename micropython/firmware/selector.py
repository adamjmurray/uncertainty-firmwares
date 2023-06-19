import random
from ..lib.dsp import BipolarTrigger
from ..lib.constants import NUM_OUTS


class Selector:

    def __init__(self, gated=False):
        self.trigger = BipolarTrigger(rising_thresh=1, falling_thresh=0.5)
        self.active_gate = 0
        self.gate_indexes = list(range(NUM_OUTS))
        self.gated = gated

    def process(self, volts, output, num_outs):
        state_change = self.trigger.detect(volts)
        if state_change is True:
            num_gates = min(max(int(volts), -4), 4) % num_outs
            active_gates = random.sample(self.gate_indexes, num_gates)
            for index in range(num_outs):
                output(index, index in active_gates)

        elif self.gated and state_change is False:
            for index in range(num_outs):
                output(index, 0)
