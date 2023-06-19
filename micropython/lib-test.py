from machine import Timer
from lib.io import read_volts, output
from lib.dsp import MovingAverage, Counter

SAMPLERATE = 48000

averager = MovingAverage(samplecount=1000)
counter = Counter(max=4800)

while(True):
    volts = read_volts()
    avg = averager.process(volts)
    if counter.process():
        print("volts=%.2f" % volts)


#Timer(
#    mode=Timer.PERIODIC,
#    freq=SAMPLERATE,
#    callback=mainloop
#)
