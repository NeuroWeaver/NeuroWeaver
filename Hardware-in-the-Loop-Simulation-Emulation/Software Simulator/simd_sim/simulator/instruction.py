

class InstructionRegister:
    def __init__(self, instruction=None,
                 opcode=0,
                 function=15,
                 dst_ns_id=None,
                 dst_index_id=None,
                 src1_ns_id=None,
                 src1_index_id=None,
                 src2_ns_id=None,
                 src2_index_id=None,
                 immediate=None,
                 dest_bank=None,
                 first_permute=False,
                 op_spec=None,
                 addr_src1=None,
                 addr_src2=None,
                 addr_dst=None,
                 alu_src1=None,
                 alu_src2=None,
                 alu_dst=None,
                 pc_idx=None,
                 remain_cycle=None,
                 parse_instr=True
                 ):
        self.instruction = instruction
        self.opcode = opcode
        self.function = function
        self.dst_ns_id = dst_ns_id
        self.dst_index_id = dst_index_id
        self.src1_ns_id = src1_ns_id
        self.src1_index_id = src1_index_id
        self.src2_ns_id = src2_ns_id
        self.src2_index_id = src2_index_id
        self.immediate = immediate
        self.dest_bank = dest_bank
        self.first_permute = first_permute

        self.op_spec = op_spec

        self.addr_src1 = addr_src1
        self.addr_src2 = addr_src2
        self.addr_dst = addr_dst

        self.alu_src1 = alu_src1
        self.alu_src2 = alu_src2
        self.alu_dst = alu_dst

        # for single base loop profiling
        self.pc_idx = pc_idx

        # for multi-cycle in ALU
        self.remain_cycle = remain_cycle

        if instruction is not None and parse_instr:
            self.__parse(instruction)

    def is_nop(self):
        if self.opcode == 0 and self.function == 15:
            return True

        return False

    def __parse(self, instruction):
        self.opcode = int(instruction[0:4], 2)            # 4  bits
        self.function = int(instruction[4:8], 2)          # 4  bits
        self.dst_ns_id = int(instruction[8:11], 2)        # 3  bits
        self.dst_index_id = int(instruction[11:16], 2)    # 5  bits
        self.src1_ns_id = int(instruction[16:19], 2)      # 3  bits
        self.src1_index_id = int(instruction[19:24], 2)   # 5  bits
        self.src2_ns_id = int(instruction[24:27], 2)      # 3  bits
        self.src2_index_id = int(instruction[27:32], 2)   # 5  bits
        self.immediate = int(instruction[16:32], 2)       # 16 bits
        self.op_spec = int(instruction[4:10], 2)          # 6  bits

    def copy_instr(self):

        return InstructionRegister(
            instruction=self.instruction,
            opcode=self.opcode,
            function=self.function,
            dst_ns_id=self.dst_ns_id,
            dst_index_id=self.dst_index_id,
            src1_ns_id=self.src1_ns_id,
            src1_index_id=self.src1_index_id,
            src2_ns_id=self.src2_ns_id,
            src2_index_id=self.src2_index_id,
            immediate=self.immediate,
            dest_bank=self.dest_bank,
            first_permute=self.first_permute,
            op_spec=self.op_spec,
            addr_src1=self.addr_src1,
            addr_src2=self.addr_src2,
            addr_dst=self.addr_dst,
            alu_src1=self.alu_src1,
            alu_src2=self.alu_src2,
            alu_dst=self.alu_dst,
            pc_idx=self.pc_idx,
            remain_cycle=self.remain_cycle,
            parse_instr=False
        )


if __name__ == "__main__":
    ir = InstructionRegister(instruction=274743296)
    print(ir.opcode)
    print(ir.function)
    print(ir.dst_ns_id)
