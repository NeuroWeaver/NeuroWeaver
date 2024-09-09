import numpy as np
import pyopencl as cl
import json

class GenesysDriver:

    def __init__(self, reg_init_value = 0,
                    input_buffer_size_byte = 44457984, #17902240 * 15,
                    output_buffer_size_byte = 5767168 * 5,
                    # test_path = '/home/lavanya/genesys-16x16/tests/resnet50_benchmark16x16_endtoend_quant0/',
                    test_path = '/home/lavanya/genesys-neuroweaver/ppo_model_0benchmark4x4_0/',
                    # data_info_file = '/home/lavanya/micro_tutorial/genesys-fpga/fpga_framework/host_py/resnet50_operand_storage_info.json',
                    data_info_file ='/home/lavanya/genesys-neuroweaver/ppo_model_0benchmark4x4_0/program/ppo_model_operand_storage_info.json',
                    # base_path = '/home/lavanya/genesys-16x16/tests/',
                    base_path ='/home/lavanya/genesys-neuroweaver/',
                    genesys_binary = '/home/lavanya/micro_tutorial/genesys-fpga/fpga_framework/systolic_fpga.hw.xclbin'
                    ):

        self.genesys_binary = genesys_binary
        self.device = None
        self.ctx = None
        self.program = None
        self.systolic_fpga_krnl = None
        self.base_address = None
        self.simd_address = None
        self.output_address = None
        self.host_systolic_input_buffer = None
        self.host_simd_buffer = None
        self.host_systolic_output_buffer = None
        
        self.reg_init_value = np.int32(reg_init_value)
        self.output_buffer_size_byte = output_buffer_size_byte
        self.input_buffer_size = input_buffer_size_byte 
        self.output_buffer_size = output_buffer_size_byte
        self.num_instruction = 2048      
        self.test_path     = test_path
        self.data_info_file = data_info_file
        self.base_path  = base_path        
      
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

    def init_buffers_b2b(self):
        print("Initializing buffers...")
        # run required checks
        if self.ctx is None:
            raise RuntimeError("No valid context set, use init_context() to create context and set using set_context()")
        
        # Load all Inputs
        systolic_input_buffer = np.zeros((self.input_buffer_size,), dtype=np.int32)
        simd_buffer = np.zeros((self.input_buffer_size,), dtype=np.int32)
        systolic_output_buffer = np.zeros((self.input_buffer_size,), dtype=np.int32)

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
                if ((layer_input[1].get("buffer") == "VMEM1") or (layer_input[1].get("buffer") == "VMEM2")):
                    self.load(file_path, simd_buffer, int(offset))
                else:
                    self.load(file_path, systolic_input_buffer, int(offset))
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
            self.load(inst_paths[i],systolic_input_buffer,int(inst_offsets[i]))
            print(inst_paths[i],int(inst_offsets[i]))

        
        self.host_systolic_input_buffer = systolic_input_buffer
        self.host_simd_buffer = simd_buffer
        self.host_systolic_output_buffer = systolic_output_buffer

        self.base_address = cl.Buffer(self.ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=self.host_systolic_input_buffer)
        self.output_address = cl.Buffer(self.ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=self.host_systolic_output_buffer)
        self.simd_address = cl.Buffer(self.ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=self.host_simd_buffer)

    def program_registers(self):
        # run required checks
        if self.systolic_fpga_krnl is None:
            raise RuntimeError("No valid kernel found! Use build_program() to compile bitstream and set the kernel")
        if self.base_address is None or self.host_systolic_input_buffer is None:
            raise RuntimeError("Buffers not initialized! Run init_buffers() before programming registers")
        if self.simd_address is None or self.host_simd_buffer is None:
            raise RuntimeError("Buffers not initialized! Run init_buffers() before programming registers")

        print('Setting register values...')
        for i in range(15):
            if i != 2:
                self.systolic_fpga_krnl.set_arg(i, self.reg_init_value)
    
        self.systolic_fpga_krnl.set_arg(2, np.int32(self.num_instruction))
        self.systolic_fpga_krnl.set_arg(15, self.base_address)
        self.systolic_fpga_krnl.set_arg(16, self.base_address)
        self.systolic_fpga_krnl.set_arg(17, self.base_address)
        self.systolic_fpga_krnl.set_arg(18, self.output_address)
        self.systolic_fpga_krnl.set_arg(19, self.simd_address)

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
                    if ((layer_output[1].get("buffer") == "VMEM1") or  (layer_output[1].get("buffer") == "VMEM2")):
                        if ( ((golden_output[i] - self.host_simd_buffer[int(offset)+i]) > 1) or ((golden_output[i] - self.host_simd_buffer[int(offset)+i]) < -1)):
                            print("comparison fail, i="+str(i)+", expected=" + str(golden_output[i]) + ", actual="+ str(self.host_simd_buffer[int(offset)+i]))
                    else:
                        if ( ((golden_output[i] - self.host_systolic_output_buffer[int(offset)+i]) > 1) or ((golden_output[i] - self.host_systolic_output_buffer[int(offset)+i]) < -1)):
                            print("comparison fail, i="+str(i)+", expected=" + str(golden_output[i]) + ", actual="+ str(self.host_systolic_output_buffer[int(offset)+i])) 


    def run(self):
        if self.ctx is None:
            raise RuntimeError("No valid context set, use init_context() to create context and set using set_context()")
        if self.base_address is None or self.host_systolic_input_buffer is None:
            raise RuntimeError("Systolic input buffers aren't allocated! Run init_buffer() before you call run")
        if self.systolic_fpga_krnl is None:
            raise RuntimeError("No valid kernel found! Use build_program() to compile bitstream and set the kernel")
        
        print('Copying buffers...')
        queue = cl.CommandQueue(self.ctx)
        cl.enqueue_copy(queue, self.base_address, self.host_systolic_input_buffer).wait()
        cl.enqueue_copy(queue, self.simd_address, self.host_simd_buffer).wait()
        print('Launching kernel...')
        ev = cl.enqueue_nd_range_kernel(queue, self.systolic_fpga_krnl,(1,), (1,))
        ev.wait()
        print("Copy Output back...")
        cl.enqueue_copy(queue, self.host_systolic_output_buffer, self.output_address).wait()
        cl.enqueue_copy(queue, self.host_systolic_input_buffer, self.base_address).wait()
        cl.enqueue_copy(queue, self.host_simd_buffer, self.simd_address).wait()

    def get_performance_data(self):
        count = 0
        i = 0
        while (i<24):
        
            local_i = i
            value = 0
            if (count ==0):
                value = self.host_systolic_input_buffer[local_i]
                print("pc_num_tiles: "+str(value))
                local_i+=1
                value = self.host_systolic_input_buffer[local_i]
                print("pc_simd_tot_compute: "+str(value))
                local_i+=1
                value = self.host_systolic_input_buffer[local_i]
                print("pc_sys_tot_compute: "+str(value))
                local_i+=1
                value = self.host_systolic_input_buffer[local_i]
                print("pc_end2end: "+str(value))
            
            elif (count ==1):
                value = self.host_systolic_input_buffer[local_i]
                print("pc_ibuf_size_per_requests: "+str(value))
                local_i+=1
                value = self.host_systolic_input_buffer[local_i]
                print("pc_ibuf_tot_requests: "+str(value))
                local_i+=1
                value = self.host_systolic_input_buffer[local_i]
                print("pc_ibuf_tot_cycles: "+str(value))
                local_i+=1
                value = self.host_systolic_input_buffer[local_i]
                print("pc_ibuf_num_tiles: "+str(value))
            

            elif (count ==2):
                value = self.host_systolic_input_buffer[local_i]
                print("pc_obuf_st_tot_cycles: "+str(value))
                local_i+=1
                value = self.host_systolic_input_buffer[local_i]
                print("pc_obuf_st_num_tiles: "+str(value))
                local_i+=1
                value = self.host_systolic_input_buffer[local_i]
                print("pc_obuf_ld_tot_cycles: "+str(value))
                local_i+=1
                value = self.host_systolic_input_buffer[local_i]
                print("pc_obuf_ld_num_tiles: "+str(value))
            
            elif (count ==3):
                value = self.host_systolic_input_buffer[local_i]
                print("pc_bbuf_tot_cycles: "+str(value))
                local_i+=1
                value = self.host_systolic_input_buffer[local_i]
                print("pc_bbuf_num_tiles: "+str(value))
                local_i+=1
                value = self.host_systolic_input_buffer[local_i]
                print("pc_wbuf_tot_cycles: "+str(value))
                local_i+=1
                value = self.host_systolic_input_buffer[local_i]
                print("pc_wbuf_num_tiles: "+str(value))
            
            elif (count ==4):
                value = self.host_systolic_input_buffer[local_i]
                print("pc_vmem1_st_tot_cycles: "+str(value))
                local_i+=1
                value = self.host_systolic_input_buffer[local_i]
                print("pc_vmem1_st_num_tiles: "+str(value))
                local_i+=1
                value = self.host_systolic_input_buffer[local_i]
                print("pc_vmem1_ld_tot_cycles: "+str(value))
                local_i+=1
                value = self.host_systolic_input_buffer[local_i]
                print("pc_vmem1_ld_num_tiles: "+str(value))
            
            elif (count ==5):
                print("pc_vmem2_st_tot_cycles: "+str(value))
                local_i+=1
                value = self.host_systolic_input_buffer[local_i]
                print("pc_vmem2_st_num_tiles: "+str(value))
                local_i+=1
                value = self.host_systolic_input_buffer[local_i]
                print("pc_vmem2_ld_tot_cycles: "+str(value))
                local_i+=1
                value = self.host_systolic_input_buffer[local_i]
                print("pc_vmem2_ld_num_tiles: "+str(value))
            

            count+=1
            i+=4
        
        


driver = GenesysDriver()
driver.initialize()
driver.run()
driver.check_output()
driver.get_performance_data()


