import numpy as np

import ohai.analytics as analytics


with Component() as main:
    with Component(outputs=[input_np, weight_np]) as Data_gen:
        wf = open("./data/axi_out_all.txt", "r")
        inp_f = open("./data/axi_out_data.txt", "r")
        weight_a = []
        input_a = []
        for val in wf:
            weight_a.append(val.rstrip('\n'))
        for val in inp_f:
            input_a.append(val.rstrip('\n'))
        weight_np = np.asarray(weight_a, dtype = np.uint16)
        input_np = np.asarray(input_a, dtype = np.uint16)
    input_np, weight_np = Data_gen()
    analytics.linear_regression(weight_np, input_np)
    with Component(inputs=[data]) as Placeholder:
        print(data)
    Placeholder(data)

main()
