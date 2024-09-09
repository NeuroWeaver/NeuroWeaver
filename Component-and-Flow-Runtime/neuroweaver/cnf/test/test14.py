import numpy as np

import ohai.digital_signal_processing as dsp


with Component(outputs=[s]) as comp_A:
    t = np.linspace(0, 0.5, 500)
    s = np.sin(40 * 2 * np.pi * t) + 0.5 * np.sin(90 * 2 * np.pi * t)

with Component(inputs=[a]) as comp_B:
    for i in range(2):
        print("Value at index {}:\t{}".format(i, a[i + 1]), 
              "\nValue at index {}:\t{}".format(a.size -1 - i, a[-1 - i]))


s = comp_A()
out = dsp.fft(s)
comp_B(out)
