import numpy as np
import pyopencl as cl
import json

# REG_INIT_VALUE = np.int32(0)
# NUM_INSTRUCTION = np.int32(880) #bytes
# INT_SIZE = 4
# ADDR_OFFSET_INSTRUCTION = 0
# ADDR_OFFSET_INPUT = 4259840
# ADDR_OFFSET_WEIGHT = 24576
# ADDR_OFFSET_BIAS = 4096
# INPUT_ADDR_PTR = ADDR_OFFSET_INPUT // INT_SIZE
# WEIGHTS_ADDR_PTR = ADDR_OFFSET_WEIGHT // INT_SIZE
# BIAS_ADDR_PTR =  ADDR_OFFSET_BIAS // INT_SIZE
# TOTAL_DATA_SIZE_INT = 17902240//INT_SIZE
# NUM_OUTPUT = 1605632
# base_path = '/home/rohanmahapatra/testcases_real/all_32x32_tests//mobilenetv2_custom_conv_32x32_t12_6/'
# instruction_file = base_path + 'mobilenetv2_custom_conv_decimal.txt'
# bias_file = base_path + 'bias.txt'
# weight_file = base_path + 'weight_shuffled.txt'
# input_file = base_path + 'data_shuffled.txt'
# genesys_binary = '/home/rohanmahapatra/genesys-final/genesys-fpga/fpga_framework/systolic_fpga.hw.xclbin'

class GenesysDriver:

    def __init__(self, reg_init_value = 0,
                    int_size = 4,
                    addr_offset_instruction = 0,
                    addr_offset_input = 134217728,      # systolic
                    addr_offset_weight = 24576,         # systolic
                    addr_offset_bias = 4096,            # systolic
                    addr_offset_vmem1 = 0,              #SIMD
                    addr_offset_vmem2 = 23068672,       #SIMD
                    addr_offset_vmem1_rd = 46137344,    #SIMD
                    addr_offset_vmem2_rd = 69206016,    #SIMD
                    input_buffer_size_byte = 44457984, #17902240 * 15,
                    output_buffer_size_byte = 5767168 * 5,
                    compiled_test_path = '/home/rohanmahapatra/testcases_real/all_32x32_tests//mobilenetv2_custom_conv_32x32_t12_6/',
                    # test_path = '/home/lavanya/genesys-16x16/tests/resnet50_benchmark16x16_endtoend_quant0/',
                    test_path = '/home/lavanya/genesys-neuroweaver/ppo_model_0benchmark4x4_0/',
                    # data_info_file = '/home/lavanya/micro_tutorial/genesys-fpga/fpga_framework/host_py/resnet50_operand_storage_info.json',
                    data_info_file ='/home/lavanya/genesys-neuroweaver/ppo_model_0benchmark4x4_0/program/ppo_model_operand_storage_info.json',
                    # base_path = '/home/lavanya/genesys-16x16/tests/',
                    base_path ='/home/lavanya/genesys-neuroweaver/',
                    instruction_file = 'mobilenetv2_custom_conv_decimal.txt',
                    genesys_binary = '/home/lavanya/micro_tutorial/genesys-fpga/fpga_framework/systolic_fpga.hw.xclbin',
                    input_dir=None,
                    weight_dir=None,
                    bias_dir=None,
                    vmem1_dir=None,
                    vmem2_dir=None,
                    golden_output_dir='./',
                    output_systolic = False,
                    output_vmem1 = False,
                    output_vmem2 = False):

        self.genesys_binary = genesys_binary
        self.device = None
        self.ctx = None
        self.program = None
        self.systolic_fpga_krnl = None
        self.base_address = None
        self.simd_address = None
        self.systolic_outputs = None
        self.host_input_buffer = None
        self.host_simd_buffer = None
        self.host_systolic_output_buffer = None
        self.host_simd_output_buffer = None
        self.vmem1_file = None
        self.vmem2_file = None
        self.weight_file = None
        self.bias_file = None
        self.input_file = None

        # Instruction 
        self.int_size = int_size
        self.reg_init_value = np.int32(reg_init_value)
        self.output_buffer_size_byte = output_buffer_size_byte
        self.addr_offset_instruction = addr_offset_instruction
        self.input_buffer_size = input_buffer_size_byte 
        self.output_buffer_size = output_buffer_size_byte
        self.num_instruction = 2048

        # Systolic Buffer
        self.input_addr_ptr = addr_offset_input // self.int_size
        self.weights_addr_ptr = addr_offset_weight // self.int_size
        self.bias_addr_ptr = addr_offset_bias // self.int_size
 
        # SIMD buffer
        self.addr_offset_vmem1 = addr_offset_vmem1
        self.addr_offset_vmem2 = addr_offset_vmem2
        self.addr_offset_vmem1_rd = addr_offset_vmem1_rd
        self.addr_offset_vmem2_rd = addr_offset_vmem2_rd
        self.vmem1_addr_ptr = self.addr_offset_vmem1 // self.int_size
        self.vmem2_addr_ptr = self.addr_offset_vmem2 // self.int_size
        self.vmem1_addr_rd_ptr = self.addr_offset_vmem1_rd // self.int_size
        self.vmem2_addr_rd_ptr = self.addr_offset_vmem2_rd // self.int_size
        
        # Outputs
        self.output_systolic = output_systolic
        self.output_vmem1 = output_vmem1
        self.output_vmem2 = output_vmem2
        self.compiled_test = compiled_test_path
        self.test_path     = test_path
        self.data_info_file = data_info_file
        self.base_path  = base_path
        
        # Data Paths
        self.instruction_file = self.compiled_test + instruction_file
        if input_dir != None:
            self.weight_file = self.compiled_test + 'data/' + weight_dir
            self.bias_file = self.compiled_test + 'data/' + bias_dir
            self.input_file = self.compiled_test + 'data/' + input_dir
        if vmem1_dir != None:  
            self.vmem1_file = self.compiled_test + 'data/' + vmem1_dir
        if vmem2_dir != None:
            self.vmem2_file = self.compiled_test + 'data/' + vmem2_dir
        self.golden_output_dir = self.compiled_test + 'data/' + golden_output_dir

    def get_devices(self):
        platforms = cl.get_platforms()
        platform_id = None
        for i, platform in enumerate(platforms):
            if platform.name == 'Xilinx':
                platform_id = i
        if platform_id is None:
            raise RuntimeError('No Xilinx platform found!')
        devices = platforms[platform_id].get_devices()
        print(f'Detected {devices} devices for Xilinx platform')
        return devices

    def set_device(self, device):
        self.device = device

    def get_device(self):
        return self.device

    def set_context(self, ctx):
        self.ctx = ctx

    def get_context(self):
        return self.ctx

    def init_context(self, devices):
        context = cl.Context(devices=devices)
        if not context:
            raise RuntimeError(f'Unable to create context for devices {devices}')
        self.ctx = context

    def build_program(self):
        # run required checks
        if self.ctx is None:
            raise RuntimeError("No valid context set, use init_context() to create context or set using set_context()")
        if self.device is None:
            raise RuntimeError("No valid device set. Use get_devices() to get list of devices on system and set using set_device()")
        binary = None
        with open(self.genesys_binary, "rb") as f:
            binary = f.read()
        bld = cl.Program(self.ctx, [self.device], [binary]).build()
        self.program = bld
        self.systolic_fpga_krnl = cl.Kernel(bld, "systolic_fpga")

    def load(self, filename, buf, offset):
        lines = []
        with open(filename, "r") as f:
            lines = f.readlines()
        file_size = np.int32(len(lines))
        for i, l in enumerate(lines):
            buf[i + offset] = int(l)

        return file_size 

    def initialize(self): 
        devices = self.get_devices()
        if len(devices) == 0:
            raise RuntimeError("No xilinx devices found!")
        self.set_device(devices[0])
        self.init_context([driver.get_device()])
        self.build_program()
        self.init_buffers_b2b()
        self.program_registers()

    def init_buffers(self):
        print("Initializing buffers...")
        # run required checks
        if self.ctx is None:
            raise RuntimeError("No valid context set, use init_context() to create context and set using set_context()")
        
        # Load Systolic Inputs
        systolic_buffer = np.zeros((self.input_buffer_size,), dtype=np.int32)
        self.num_instruction = self.load(self.instruction_file, systolic_buffer, 0)
        if self.input_file != None:
            self.load(self.bias_file, systolic_buffer, self.bias_addr_ptr)
            self.load(self.weight_file, systolic_buffer, self.weights_addr_ptr)
            self.load(self.input_file, systolic_buffer, self.input_addr_ptr)

        self.host_input_buffer = systolic_buffer
        self.base_address = cl.Buffer(self.ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=self.host_input_buffer)
        print("Systolic Buffer loaded:")

        # Load SIMD Inputs
        simd_buffer = np.zeros((self.output_buffer_size,), dtype=np.int32)
        if self.vmem1_file != None or self.vmem2_file != None:
            if self.vmem1_file != None:
                self.load(self.vmem1_file, simd_buffer, self.vmem1_addr_ptr)

            if self.vmem2_file != None:
                self.load(self.vmem2_file, simd_buffer, self.vmem2_addr_ptr)
        self.host_simd_buffer = simd_buffer
        self.simd_address = cl.Buffer(self.ctx, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=self.host_simd_buffer)
        print("SIMD Buffer loaded:")

        # Load Systolic Outputs
        res_systolic = np.ones(self.output_buffer_size, dtype=np.int32)
        self.host_systolic_output_buffer = res_systolic
        self.systolic_outputs = cl.Buffer(self.ctx, cl.mem_flags.READ_WRITE, res_systolic.nbytes)

        # Load SIMD Outputs
        res_simd = np.empty((self.output_buffer_size,), dtype=np.int32)
        self.host_simd_output_buffer = res_simd

    def init_buffers_b2b(self):
        print("Initializing buffers...")
        # run required checks
        if self.ctx is None:
            raise RuntimeError("No valid context set, use init_context() to create context and set using set_context()")
        
        # Load all Inputs
        systolic_buffer = np.zeros((self.input_buffer_size,), dtype=np.int32)

        num_blocks = 0 
        inst_offsets = []
        inst_paths = []
        data_info_f = open(self.data_info_file)
        data_info = json.load(data_info_f)
        for (layer,value) in data_info.items():
            layer_inputs = data_info[layer]["inputs"]
            for layer_input in layer_inputs.items():
                file_path = self.base_path + str(layer_input[1].get("path"))[71:]
                offset = int(layer_input[1].get("offset"))/4
                self.load(file_path, systolic_buffer, int(offset))
                print(file_path,int(offset))
            
            layer_inst = data_info[layer]["instructions"]
            inst_offset = int(layer_inst["offset"])/4
            inst_offsets.append(inst_offset)
            path = layer_inst["path"]
            inst_path = self.test_path + path[97:len(path)-16] + "decimal.txt"
            inst_paths.append(inst_path)
            num_blocks+=1

        data_info_f.close()

        #Load all instructions
        for i in range (num_blocks):
            self.load(inst_paths[i],systolic_buffer,int(inst_offsets[i]))
            print(inst_paths[i],int(inst_offsets[i]))

        
        self.host_input_buffer = systolic_buffer
        self.base_address = cl.Buffer(self.ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=self.host_input_buffer)
        

    def program_registers(self):
        # run required checks
        if self.systolic_fpga_krnl is None:
            raise RuntimeError("No valid kernel found! Use build_program() to compile bitstream and set the kernel")
        if self.base_address is None or self.host_input_buffer is None:
            raise RuntimeError("Buffers not initialized! Run init_buffers() before programming registers")
        # if self.simd_address is None or self.host_simd_buffer is None:
        #     raise RuntimeError("Buffers not initialized! Run init_buffers() before programming registers")

        print('Setting register values...')
        for i in range(15):
            if i != 2:
                self.systolic_fpga_krnl.set_arg(i, self.reg_init_value)
    
        self.systolic_fpga_krnl.set_arg(2, np.int32(2048))
        self.systolic_fpga_krnl.set_arg(15, self.base_address)
        self.systolic_fpga_krnl.set_arg(16, self.base_address)
        self.systolic_fpga_krnl.set_arg(17, self.base_address)
        self.systolic_fpga_krnl.set_arg(18, self.base_address)
        self.systolic_fpga_krnl.set_arg(19, self.base_address)

    def check_output(self):
        
        golden_output = np.zeros((self.output_buffer_size_byte,), dtype=np.int32)
        data_info_f = open(self.data_info_file)
        data_info = json.load(data_info_f)
        for (layer,value) in data_info.items():
            layer_outputs = data_info[layer]["outputs"]
            for layer_output in layer_outputs.items():
                file_path = self.base_path + str(layer_output[1].get("path"))[71:]
                offset = int(layer_output[1].get("offset"))/4
                self.num_output = self.load(file_path, golden_output, 0)
                print(file_path,int(offset))
                for i in range(self.num_output):
                    # print(self.host_input_buffer[int(offset)+i])
                    if ( ((golden_output[i] - self.host_input_buffer[int(offset)+i]) > 1) or ((golden_output[i] - self.host_input_buffer[int(offset)+i]) < -1)):
                        print("comparison fail, i="+str(i)+", expected=" + str(golden_output[i]) + ", actual="+ str(self.host_input_buffer[int(offset)+i]))
                      


    def run(self):
        if self.ctx is None:
            raise RuntimeError("No valid context set, use init_context() to create context and set using set_context()")
        if self.base_address is None or self.host_input_buffer is None:
            raise RuntimeError("Systolic input buffers aren't allocated! Run init_buffer() before you call run")
        if self.systolic_fpga_krnl is None:
            raise RuntimeError("No valid kernel found! Use build_program() to compile bitstream and set the kernel")
        
        print('Copying buffers...')
        queue = cl.CommandQueue(self.ctx)
        cl.enqueue_copy(queue, self.base_address, self.host_input_buffer).wait()
        # cl.enqueue_copy(queue, self.simd_address, self.host_simd_buffer).wait()
        print('Launching kernel...')
        ev = cl.enqueue_nd_range_kernel(queue, self.systolic_fpga_krnl,(1,), (1,))
        # cl.enqueue_task(queue, self.systolic_fpga_krnl)
        ev.wait()
        print("Copy Output back...")
        cl.enqueue_copy(queue, self.host_input_buffer, self.base_address).wait()
        # cl.enqueue_copy(queue, self.host_simd_output_buffer, self.simd_address).wait()




driver =  GenesysDriver()
devices = driver.get_devices()
if len(devices) == 0:
            raise RuntimeError("No xilinx devices found!")
driver.set_device(devices[0])
driver.init_context([driver.get_device()])
driver.build_program()
driver.init_buffers_b2b()
driver.program_registers()
# driver.initialize()
driver.run()
driver.check_output()
# driver.get_performance_data()


