# Output chaotic patterns using the Logistic Map equation (https://en.wikipedia.org/wiki/Logistic_map)
# Negative triggers < -2V will reseed the equation.
# Values close to 4 are used for r because this exhibits chaotic patterns that span nearly
# 0-1, so it's easy to convert to a gate index.
from lib.core import NUM_OUTS, BipolarTrigger
from random import random


class Chaos:

    def __init__(self, output, gated=False):
        self.trigger = BipolarTrigger(rising_thresh=2, window=10)
        self.gated = gated
        self.gate_index = None
        for index in range(NUM_OUTS):
            output(index, False)
        self.reseed()

    def reseed(self):
        self.r = 3.97 + 0.03 * random()
        self.x = 0.01 + 0.99 * random()
        # print("\n(seeded) X=%f, r=%f" % (self.x, self.r))

    def process(self, volts, output):
        state_change = self.trigger.detect(volts)
        if state_change is True:  # trigger transitioned to ON
            if volts < 0:
                self.reseed()

            self.x = self.r * self.x * (1 - self.x)
            # print("X=%f" % self.x)

            gate_index = min(max(int(NUM_OUTS * self.x), 0), NUM_OUTS-1)

            if gate_index != self.gate_index:
                if self.gate_index is not None:
                    output(self.gate_index, False)
                output(gate_index, True)
                self.gate_index = gate_index

        elif state_change is False and self.gated and self.gate_index is not None:
            # trigger transitioned to OFF, so turn the gate off if the other conditions are met
            output(self.gate_index, False)
            self.gate_index = None
