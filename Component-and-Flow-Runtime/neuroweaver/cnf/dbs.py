import numpy as np
from random import randint

import ohai.digital_signal_processing as dsp


with Component(outputs=[n_rows, n_cols, param]) as init:
    n_rows =1
    n_cols = 100
    param = np.float64(randint(0, 100))

with Component(inputs=[n_rows, n_cols, param], outputs=[data_param]) as data_generator:
    data = np.random.uniform(0, 1, (n_rows, n_cols))
    data_param = (data,param)

with Component(inputs=[data_in], outputs=[obj_param]) as signal_processing:
    with Component(inputs=[data_in], outputs=[signal, param]) as parse:
        signal = data_in[0]
        param = data_in[1]
    signal, param = parse(data_in)
    fft_out = dsp.fft(signal)
    with Component(inputs=[fft_out], outputs=[obj_param]) as produce:
        objective = np.sum(abs(fft_out),axis=1)
        obj_param = (objective, param)
    obj_param = produce(fft_out)


n_rows, n_cols, param = init()
data_in = data_generator(n_rows, n_cols, param)
#data_out_signal = signal_processing(data_in)
