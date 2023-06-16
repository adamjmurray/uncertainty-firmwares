import machine
import lib.io as io
import lib.dsp as dsp

machine.freq(250000000)  # 2x default

while (True):
    cv = io.read_cv()
    active_gate = abs(round(cv * (io.num_outs-1)))
    for index in range(io.num_outs):
        io.output(index, index == active_gate)
