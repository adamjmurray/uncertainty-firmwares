import time
import random
from machine import Pin, ADC
from machine import Timer
from math import sin, pi

# print(machine.freq()) # 125000000, 125MHz, plenty for running a high sample rate, and we can probably clock faster
SAMPLERATE = 96000

CALIB_NEG5 = 3470
CALIB_POS5 = 65500
CALIB_RANGE = CALIB_POS5 - CALIB_NEG5


# convert to range (-1, 1) over approximately -5V to +5V of input
def normalize(read_u16_val): 
    normalized = (read_u16_val - CALIB_NEG5)/CALIB_RANGE
    clamped = min(max(normalized, 0), 1)
    return 2 * clamped - 1

def voltage(read_u16_val):
    return 5 * normalize(read_u16_val);


class LPF: # butchered version of oopsy.ctrl.smooth2.gendsp from the Oopsy Max package
    def __init__(self, mix):
        self.mix = mix
        self.hist1 = 0
        self.hist2 = 0

    def filter(self, sample):
        self.hist1 = self.mix * self.hist1 + (1 - self.mix) * sample
        self.hist2 = self.mix * self.hist2 + (1 - self.mix) * self.hist1
        return self.hist2


cv_in = ADC(Pin(26))
outs = [Pin(27, Pin.OUT),
        Pin(28, Pin.OUT),
        Pin(29, Pin.OUT),
        Pin(0, Pin.OUT),
        Pin(3, Pin.OUT),
        Pin(4, Pin.OUT),
        Pin(2, Pin.OUT),
        Pin(1, Pin.OUT)]

num_outs = len(outs)

lpf = LPF(0.05)


def mainloop(_timer):
    raw = cv_in.read_u16()
    normalized = raw / 65535
    # -6.1V => 0
    # -6V => 0.001
    # -5V => 0.053
    # -4V => 0.145
    # -3V => 0.241
    # -2V => 0.337
    # -1V => 0.430
    # +0V => 0.527
    # +1V => 0.623
    # +2V => 0.716
    # +3V => 0.812
    # +4V => 0.906
    # +5V => 0.983
    # +6V => 0.997
    # +6.5V => 1 (normalized)
    
    # Attempt at calibration
    # u16 at -5V: 3470
    # u16 at +5V: 64440 (and then I fudged it because 0-4V was all a bit high)
    
    volts = voltage(raw)
    cv = lpf.filter(normalize(raw))
     
    active_gate = min(abs(int(cv * num_outs)), num_outs-1)
    
    # Only print() at low samplerates, like SAMPLERATE=1
    # print("raw=%i, voltage=%.2f, normalized=%.2f, active_gate=%i" % (raw, volts, cv, active_gate))
         
    for num in range (8):
        if num != active_gate:
            outs[num].value(0)

    outs[active_gate].value(1)


Timer(freq=SAMPLERATE, mode=Timer.PERIODIC, callback=mainloop)
