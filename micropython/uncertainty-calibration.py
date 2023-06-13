from machine import ADC, Pin, Timer

# print(machine.freq()) # 125000000, 125MHz, plenty for running a high sample rate, and we can overclock
SAMPLERATE = 96000

# different modules may need different calibration
CALIB_NEG5 = 3470
CALIB_POS5 = 65500 # I measured this at 64440, but fudged it because 0-4V were all a bit high
CALIB_RANGE = CALIB_POS5 - CALIB_NEG5


# convert to range (-1, 1) over approximately -5V to +5V of input
def normalize(read_u16_val): 
    normalized = (read_u16_val - CALIB_NEG5)/CALIB_RANGE
    clamped = min(max(normalized, 0), 1)
    return 2 * clamped - 1

def voltage(read_u16_val):
    return 5 * normalize(read_u16_val)


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
outs = [Pin(number, Pin.OUT) for number in [27,28,29,0,3,4,2,1]]

num_outs = len(outs)
lpf = LPF(0.05)


def mainloop(_timer):
    raw = cv_in.read_u16()
    cv = lpf.filter(normalize(raw)) # (-1, 1) range for -5V to +5V input
     
    active_gate = min(abs(int(cv * num_outs)), num_outs-1)
    
    # Slow down the sample rate (e.g. SAMPLERATE=1) to print:
    # print("raw=%i, voltage=%.2f, normalized=%.2f, active_gate=%i" % (raw, voltage(raw), cv, active_gate))
         
    for num in range (8):
        if num != active_gate:
            outs[num].value(0)

    outs[active_gate].value(1)


Timer(freq=SAMPLERATE, mode=Timer.PERIODIC, callback=mainloop)
