from ..lib.dsp import BipolarTrigger


class Stepper:

    def __init__(self):
        self.trigger = BipolarTrigger(rising_thresh=1, lpf_weight=0)
        self.active_gate = 0

    def process(self, volts, output, num_outs):
        if self.trigger.detect(volts) != 0:
            offset = min(max(int(volts), -4), 4)
            if offset != 0:
                output(self.active_gate, 0)
                self.active_gate = (self.active_gate + offset) % num_outs
                output(self.active_gate, 1)
