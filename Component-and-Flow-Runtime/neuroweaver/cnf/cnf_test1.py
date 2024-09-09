import logging
import time

import numpy as np

#import ohai.analytics as analytics
import ohai.digital_signal_processing as dsp


with Component(outputs=[data, weight_np]) as thread_1:
    sleep_interval = 0.5  # seconds
    n_rows = 1
    n_cols = 1
    while True:
        data = np.random.uniform(0, 1, (n_rows, n_cols))
        logging.debug(f'Thread 1: generated random data: \n{data}')
        wf = open(f"./data/axi_out_all.txt", "r")
        weight_a = []
        for val in wf:
            weight_a.append(val.rstrip('\n'))
        weight_np = np.asarray(weight_a, dtype = np.uint16)
        time.sleep(sleep_interval)
        with open('thread_1', 'a') as f:
            f.write(str(data) + '\n')


with Component(inputs=[buffer_2]) as thread_3:
        sleep_interval2 = 0.5
        inter_interval = 0.5
        while True:
            logging.debug(f'Thread 3: buffer_2: \n{buffer_2}')
            time.sleep(sleep_interval2)
            time.sleep(inter_interval)
            with open('thread_3', 'a') as f:
                f.write(str(buffer_2) + '\n')


buffer_1 = thread_1()
buffer_2 = dsp.fft(buffer_1)
thread_3(buffer_2)
