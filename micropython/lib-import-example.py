from lib.io import read_cv, num_outs, output

while (True):
    cv = read_cv()
    active_gate = abs(round(cv * (num_outs-1)))
    for index in range(num_outs):
        output(index, index == active_gate)
