# "Scanner" Firmware
# ------------------
# This firmware always has one active gate.
# The firmware scans across the 8 gates over the input range 0-3.5V.
# It advances to the next gate every 0.5V.
# Above 3.5V it stays on the last gate.
# Negative voltages -0.5V to -4V also work and go in the reverse direction.

from lib.core import NUM_OUTS, OnePoleLowpassFilter


class Scanner:

    def __init__(self, output, filter=OnePoleLowpassFilter(a=0.1)):
        self.filter = None if filter is None else filter.filter  # store the actual filter function, not the filter
        self.active_gate = 0
        for index in range(NUM_OUTS):
            output(index, index == self.active_gate)

    def process(self, volts, output):
        filtered = volts if self.filter is None else self.filter(volts)
        clamped = min(max(filtered, -4), 3.5)
        active_gate = int(2 * clamped) % NUM_OUTS
        if active_gate != self.active_gate:
            output(self.active_gate, False)
            output(active_gate, True)
            self.active_gate = active_gate
