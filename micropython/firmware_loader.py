# A template for running firmwares found in the firmware subfolder. If you save
# this file as main.py on the Uncertainty, it will run automatically when the
# module powers on.

from lib.io import read_volts, output
from machine import Timer
import machine

# 1. Choose the firmware:
from firmware.stepper import Stepper as Firmware
firmware = Firmware(output)

# Overclock to 2x the default because Python isn't as fast as C.
# WARNING: do not go much higher. Somewhere above 260_000_000 the device will
# stop working. If you overclock too high in the main.py file, the device may
# become unresponsive immediately after powering on. Then you probably have to
# completely reinstall the firmware to reset the filesystem on the device.
machine.freq(250_000_000)

Timer(
    mode=Timer.PERIODIC,
    freq=48_000,  # 3. Choose the sample rate (TODO: it doesn't seem like Micropython can run this fast. Investigate...)
    callback=lambda _: firmware.process(read_volts(), output)
)
