# A template for running firmwares found in the firmware subfolder.
# If you save this file as main.py on the Uncertainty, it will run automatically
# when the module powers on.

from lib.io import read_volts, output
from machine import Timer
import machine

# 1. Choose the firmware:
from firmware.selector import Selector as Firmware
firmware = Firmware()

machine.freq(250_000_000)  # 2. Choose processor speed. (250_000_000 is overclocked to 2x the default)

Timer(
    mode=Timer.PERIODIC,
    freq=48_000,  # 3. Choose the sample rate (TODO: it doesn't seem like Micropython can run this fast. Investigate...)
    callback=lambda _: firmware.process(read_volts(), output)
)
