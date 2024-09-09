import numpy as np
from simulator.stage import InstructionFetch, Decode
from simulator.instruction import InstructionRegister

ns_dict = {
    0: "obuf",
    1: "ibuf",
    2: "vmem1",
    3: "vmem2",
    4: "imm"
}

function_dict = {
    0: "BASE_SIGNEXT",
    1: "BASE_LOW",
    2: "BASE_HIGH",
    3: "BASE_ZEROFILL",
    4: "STRIDE_SIGNEXT",
    5: "STRIDE_LOW",
    6: "STRIDE_HIGH",
    7: "STRIDE_ZEROFILL",
    8: "IMMEDIATE_LOW",
    9: "IMMEDIATE_HIGH",
    10: "IMMEDIATE_SIGN_EXTEND",
}


class DecodeTest(Decode):
    def __init__(self):
        super(DecodeTest, self).__init__(1)
        self.instruction_fetch = InstructionFetch(simd_lane_cnt=1)

    def test(self, config):
        inst_list = self.__gen_inst_list(config)

        for i in range(len(inst_list)):
            print(f"[test {i}]")
            self.__test(inst_list[i])

    def __test(self, inst):
        self.input_inst_reg = InstructionRegister(inst)
        dst_ns = self.input_inst_reg.dst_ns_id
        dst_index = self.input_inst_reg.dst_index_id
        immediate = self.input_inst_reg.immediate
        function = self.input_inst_reg.function

        self._handle()

        print(f"inst   | {inst}")
        print(f"inputs | function: {function_dict[function]}, dst_ns: {ns_dict[dst_ns]}({dst_ns}), dst_index: {dst_index}, imm: {np.int16(immediate)}")

        if function < 4:
            output = self.index_tables[ns_dict[dst_ns]][dst_index]["base"]
        elif 4 <= function < 8:
            output = self.index_tables[ns_dict[dst_ns]][dst_index]["stride"]
        else:
            output = self.index_tables[ns_dict[dst_ns]][dst_index]
        print(f"output | imm: {output} ({np.uint32(output):032b})")

    def __gen_inst_list(self, config):
        return [self.__gen_inst(c[0], c[1], c[2], c[3]) for c in config]

    def __gen_inst(self, function, dst_ns_id, dst_index_id, immediate):
        return f"{(6 << 28) + (function << 24) + (dst_ns_id << 21) + (dst_index_id << 16) + np.uint16(immediate):032b}"


if __name__ == "__main__":
    decode = DecodeTest()
    ns = 1
    index_id = 16

    # test base or stride
    is_base = False
    decode.test([
        [0 if is_base else 4, ns, index_id, np.int16(0b1111_1111_1111_1111)],
        [1 if is_base else 5, ns, index_id, np.int16(0b1111_0000_1010_1010)],
        [2 if is_base else 6, ns, index_id, np.int16(0b1100_1111_0110_1100)],
        [3 if is_base else 7, ns, index_id, np.int16(-2)],
    ])

    # test imm
    ns = 4
    index_id = 16
    decode.test([
        [10, ns, index_id, np.int16(0b1111_0000_1111_0000)],
        [8, ns, index_id, np.int16(0b0000_1111_0000_1111)],
        [9, ns, index_id, np.int16(0b1010_1100_0011_0101)],
    ])
