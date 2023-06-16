######################
# lib.py

import machine
from machine import ADC, Pin, Timer
from collections import deque
from enum import Enum

cv_in = ADC(Pin(26))

outs = [Pin(number, Pin.OUT) for number in [27, 28, 29, 0, 3, 4, 2, 1]]

num_outs = len(outs)


# Read from the CV input.
# Returns a number in the clamped range (-1, 1) over approx. -5V to +5V of input voltage.
def read_cv():
    # different modules may need different calibration here
    normalized = (cv_in.read_u16() - 3470) / 65500
    clamped = min(max(normalized, 0), 1)
    return 2 * clamped - 1


def write_out(index, value):
    try:
        outs[index].value(value)
    except IndexError:
        print("Invalid index %s" % index)


######################
# More lib

class SimpleLPF:
    def __init__(self, weight=0.5):
        self.weight = weight
        self.prev = 0

    def filter(self, sample):
        self.prev = self.weight * self.prev + (1 - self.weight) * sample
        return self.prev


class BipolarTrigger:
    State = Enum('BipolarTriggerState', ['OFF', 'RISING', 'ON', 'FALLING'])

    def __init__(self, rising_thresh=0.2, falling_thresh=0.1, rising_window=100, falling_window=100):
        self.rising_thresh = rising_thresh
        self.falling_thresh = falling_thresh
        self.rising_window = rising_window
        self.falling_window = falling_window
        self.state = BipolarTrigger.State.OFF
        self.countdown = 0
        self.lpf = SimpleLPF(0.1)

    def detect(self, sample):
        filtered = self.lpf.filter(sample)
        absval = abs(filtered)

        if self.state == BipolarTrigger.State.OFF:
            if absval > self.rising_thresh:
                self.state = BipolarTrigger.State.RISING
                self.countdown = self.rising_window

        elif self.state == BipolarTrigger.State.RISING:
            if absval > self.rising_thresh:
                self.countdown -= 1
                if self.countdown < 0:
                    self.state = BipolarTrigger.State.ON
                    # the only time this returns anything other than zero is the moment we transition to the ON state:
                    return filtered

            else:
                self.state = BipolarTrigger.State.OFF

        elif self.state == BipolarTrigger.State.ON:
            if absval < self.falling_thresh:
                self.state = BipolarTrigger.State.FALLING
                self.countdown = self.falling_window

        elif self.state == BipolarTrigger.State.FALLING:
            if absval < self.falling_thresh:
                self.countdown -= 1
                if self.countdown < 0:
                    self.state = BipolarTrigger.State.OFF
            else:
                self.state = BipolarTrigger.State.ON

        # if we didn't transition to ON, we always return 0
        return 0


######################
# Stepper firmeware

machine.freq(250000000)  # 2x default
trigger = BipolarTrigger(rising_thresh=0.25)
active_gate = 0

while True:
    offset = int(trigger.detect(read_cv())/0.25)
    if offset > 0:
        active_gate = (active_gate + offset) % num_outs
        for index in range(num_outs):
            write_out(index, index == active_gate)
