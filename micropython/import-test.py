from lib.io import read_cv, num_outs, write_out

while(True):
    cv = read_cv()    
    active_gate = abs(round(cv * (num_outs-1)))
    for index in range (num_outs):
        write_out(index, index == active_gate)        