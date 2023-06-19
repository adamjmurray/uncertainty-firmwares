import random
from ..lib.dsp import BipolarTrigger
from ..lib.constants import NUM_OUTS


class Selector:

    def __init__(self):
        self.trigger = BipolarTrigger(rising_thresh=1, lpf_weight=0)
        self.active_gate = 0
        self.gate_indexes = list(range(NUM_OUTS))

    def process(self, volts, output, num_outs):
        if self.trigger.detect(volts) != 0:
            num_gates = min(max(int(volts), -4), 4) % num_outs
            active_gates = random.sample(self.gate_indexes, num_gates)
            for index in range(num_outs):
                output(index, index in active_gates)
