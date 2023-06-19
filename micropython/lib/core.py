# The core lib file that is designed to work on both the Uncertainty hardware and on
# a standard computer/Python interpreter, so that unit tests can be written.
# Anything that depends on the micropython `machine` module needs to go in another
# file like lib/io.py and passed into functions in this file as needed.
from collections import deque

NUM_OUTS = 8


class OnePoleLowpassFilter:
    def __init__(self, a=0.5):
        self.a = a
        self.prev = 0

    def filter(self, sample):
        self.prev = self.a * self.prev + (1 - self.a) * sample
        return self.prev


class MovingAverage:
    def __init__(self, samplecount=100):
        self.samplecount = samplecount
        self.queue = deque((), samplecount)
        self.running_sum = 0

    def process(self, sample):
        num_samples = len(self.queue)
        if num_samples == self.samplecount:
            self.running_sum -= self.queue.popleft()

        self.queue.append(sample)
        self.running_sum += sample

        return self.running_sum / num_samples if num_samples > 0 else 0


class Counter:
    def __init__(self, max=100):
        self.max = max
        self.count = 0

    def process(self, _sample=0):
        self.count = (self.count + 1) % self.max
        return self.count == 0


class BipolarTrigger:
    STATE_OFF = "OFF"
    STATE_RISING = "RISING"
    STATE_ON = "ON"
    STATE_FALLING = "FALLING"

    def __init__(self, rising_thresh=0.5, falling_thresh=None, window=100, rising_window=None, falling_window=None):
        self.rising_thresh = rising_thresh
        self.falling_thresh = rising_thresh / 2 if falling_thresh is None else falling_thresh
        self.rising_window = window if rising_window is None else rising_window
        self.falling_window = window if falling_window is None else falling_window
        self.state = BipolarTrigger.STATE_OFF
        self.countdown = 0

    def detect(self, sample):
        absval = abs(sample)

        if self.state == BipolarTrigger.STATE_OFF:
            if absval >= self.rising_thresh:
                self.state = BipolarTrigger.STATE_RISING
                self.countdown = self.rising_window

        elif self.state == BipolarTrigger.STATE_RISING:
            if absval >= self.rising_thresh:
                self.countdown -= 1
                if self.countdown <= 0:
                    self.state = BipolarTrigger.STATE_ON
                    return True  # True indicates the moment we transitioned to ON
            else:
                self.state = BipolarTrigger.STATE_OFF

        elif self.state == BipolarTrigger.STATE_ON:
            if absval <= self.falling_thresh:
                self.state = BipolarTrigger.STATE_FALLING
                self.countdown = self.falling_window

        elif self.state == BipolarTrigger.STATE_FALLING:
            if absval <= self.falling_thresh:
                self.countdown -= 1
                if self.countdown <= 0:
                    self.state = BipolarTrigger.STATE_OFF
                    return False  # False indicates the momen we transitioned to OFF
            else:
                self.state = BipolarTrigger.STATE_ON

        # if we didn't transition to ON or OFF, we always return None
        return None
