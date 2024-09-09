
class AccTable(object):
    def __init__(self, fd, accelerator_name, input_dtype, output_dtype, state_dtype, param_dtype):
        self.fd = fd
        self.accelerator_name = accelerator_name
        self.input_dtype = input_dtype
        self.output_dtype = output_dtype
        self.state_dtype = state_dtype
        self.param_dtype = param_dtype

    def get_accelerator_entry(self):
        pass
