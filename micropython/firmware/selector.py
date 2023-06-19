from lib.core import NUM_OUTS, BipolarTrigger, random_subset


class Selector:

    def __init__(self, gated=False):
        self.trigger = BipolarTrigger(rising_thresh=1)
        self.active_gate = 0
        self.gate_indexes = list(range(NUM_OUTS))
        self.gated = gated
        self.prev_active_gates = None

    def process(self, volts, output):
        state_change = self.trigger.detect(volts)
        if state_change is True:
            num_gates = min(max(int(volts), -4), 4) % NUM_OUTS

            active_gates = random_subset(self.gate_indexes, num_gates)
            while active_gates == self.prev_active_gates:
                active_gates = random_subset(self.gate_indexes, num_gates)
            self.prev_active_gates = active_gates

            for index in range(NUM_OUTS):
                output(index, index in active_gates)

        elif self.gated and state_change is False:
            for index in range(NUM_OUTS):
                output(index, 0)
