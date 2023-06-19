
from lib.io import read_volts, output
from machine import Timer
import machine

# choose the firmware:
from firmware.stepper import Stepper as Firmware
firmware = Firmware()

machine.freq(250_000_000)  # overclock to 2x the default

Timer(
    mode=Timer.PERIODIC,
    freq=48_000,  # choose the sample rate
    callback=lambda _timer: firmware.process(read_volts(), output)
)
