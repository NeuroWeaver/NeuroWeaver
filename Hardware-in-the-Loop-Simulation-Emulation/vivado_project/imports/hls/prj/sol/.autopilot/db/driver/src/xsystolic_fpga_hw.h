// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2020.2 (64-bit)
// Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
// ==============================================================
// control
// 0x00 : Control signals
//        bit 0  - ap_start (Read/Write/COH)
//        bit 1  - ap_done (Read/COR)
//        bit 2  - ap_idle (Read)
//        bit 3  - ap_ready (Read)
//        bit 7  - auto_restart (Read/Write)
//        others - reserved
// 0x04 : Global Interrupt Enable Register
//        bit 0  - Global Interrupt Enable (Read/Write)
//        others - reserved
// 0x08 : IP Interrupt Enable Register (Read/Write)
//        bit 0  - enable ap_done interrupt (Read/Write)
//        bit 1  - enable ap_ready interrupt (Read/Write)
//        others - reserved
// 0x0c : IP Interrupt Status Register (Read/TOW)
//        bit 0  - ap_done (COR/TOW)
//        bit 1  - ap_ready (COR/TOW)
//        others - reserved
// 0x10 : Data signal of slv_reg0_out
//        bit 31~0 - slv_reg0_out[31:0] (Read/Write)
// 0x14 : reserved
// 0x18 : Data signal of slv_reg1_out
//        bit 31~0 - slv_reg1_out[31:0] (Read/Write)
// 0x1c : reserved
// 0x20 : Data signal of slv_reg2_out
//        bit 31~0 - slv_reg2_out[31:0] (Read/Write)
// 0x24 : reserved
// 0x28 : Data signal of slv_reg3_out
//        bit 31~0 - slv_reg3_out[31:0] (Read/Write)
// 0x2c : reserved
// 0x30 : Data signal of slv_reg4_out
//        bit 31~0 - slv_reg4_out[31:0] (Read/Write)
// 0x34 : reserved
// 0x38 : Data signal of slv_reg5_out
//        bit 31~0 - slv_reg5_out[31:0] (Read/Write)
// 0x3c : reserved
// 0x40 : Data signal of slv_reg6_out
//        bit 31~0 - slv_reg6_out[31:0] (Read/Write)
// 0x44 : reserved
// 0x48 : Data signal of slv_reg7_out
//        bit 31~0 - slv_reg7_out[31:0] (Read/Write)
// 0x4c : reserved
// 0x50 : Data signal of slv_reg8_out
//        bit 31~0 - slv_reg8_out[31:0] (Read/Write)
// 0x54 : reserved
// 0x58 : Data signal of slv_reg9_out
//        bit 31~0 - slv_reg9_out[31:0] (Read/Write)
// 0x5c : reserved
// 0x60 : Data signal of slv_reg10_out
//        bit 31~0 - slv_reg10_out[31:0] (Read/Write)
// 0x64 : reserved
// 0x68 : Data signal of slv_reg11_out
//        bit 31~0 - slv_reg11_out[31:0] (Read/Write)
// 0x6c : reserved
// 0x70 : Data signal of slv_reg12_out
//        bit 31~0 - slv_reg12_out[31:0] (Read/Write)
// 0x74 : reserved
// 0x78 : Data signal of slv_reg13_out
//        bit 31~0 - slv_reg13_out[31:0] (Read/Write)
// 0x7c : reserved
// 0x80 : Data signal of slv_reg14_out
//        bit 31~0 - slv_reg14_out[31:0] (Read/Write)
// 0x84 : reserved
// 0x88 : Data signal of axi00_imem_ptr0
//        bit 31~0 - axi00_imem_ptr0[31:0] (Read/Write)
// 0x8c : Data signal of axi00_imem_ptr0
//        bit 31~0 - axi00_imem_ptr0[63:32] (Read/Write)
// 0x90 : reserved
// 0x94 : Data signal of axi01_parambuf_ptr0
//        bit 31~0 - axi01_parambuf_ptr0[31:0] (Read/Write)
// 0x98 : Data signal of axi01_parambuf_ptr0
//        bit 31~0 - axi01_parambuf_ptr0[63:32] (Read/Write)
// 0x9c : reserved
// 0xa0 : Data signal of axi02_ibuf_ptr0
//        bit 31~0 - axi02_ibuf_ptr0[31:0] (Read/Write)
// 0xa4 : Data signal of axi02_ibuf_ptr0
//        bit 31~0 - axi02_ibuf_ptr0[63:32] (Read/Write)
// 0xa8 : reserved
// 0xac : Data signal of axi03_obuf_ptr0
//        bit 31~0 - axi03_obuf_ptr0[31:0] (Read/Write)
// 0xb0 : Data signal of axi03_obuf_ptr0
//        bit 31~0 - axi03_obuf_ptr0[63:32] (Read/Write)
// 0xb4 : reserved
// (SC = Self Clear, COR = Clear on Read, TOW = Toggle on Write, COH = Clear on Handshake)

#define XSYSTOLIC_FPGA_CONTROL_ADDR_AP_CTRL                  0x00
#define XSYSTOLIC_FPGA_CONTROL_ADDR_GIE                      0x04
#define XSYSTOLIC_FPGA_CONTROL_ADDR_IER                      0x08
#define XSYSTOLIC_FPGA_CONTROL_ADDR_ISR                      0x0c
#define XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG0_OUT_DATA        0x10
#define XSYSTOLIC_FPGA_CONTROL_BITS_SLV_REG0_OUT_DATA        32
#define XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG1_OUT_DATA        0x18
#define XSYSTOLIC_FPGA_CONTROL_BITS_SLV_REG1_OUT_DATA        32
#define XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG2_OUT_DATA        0x20
#define XSYSTOLIC_FPGA_CONTROL_BITS_SLV_REG2_OUT_DATA        32
#define XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG3_OUT_DATA        0x28
#define XSYSTOLIC_FPGA_CONTROL_BITS_SLV_REG3_OUT_DATA        32
#define XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG4_OUT_DATA        0x30
#define XSYSTOLIC_FPGA_CONTROL_BITS_SLV_REG4_OUT_DATA        32
#define XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG5_OUT_DATA        0x38
#define XSYSTOLIC_FPGA_CONTROL_BITS_SLV_REG5_OUT_DATA        32
#define XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG6_OUT_DATA        0x40
#define XSYSTOLIC_FPGA_CONTROL_BITS_SLV_REG6_OUT_DATA        32
#define XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG7_OUT_DATA        0x48
#define XSYSTOLIC_FPGA_CONTROL_BITS_SLV_REG7_OUT_DATA        32
#define XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG8_OUT_DATA        0x50
#define XSYSTOLIC_FPGA_CONTROL_BITS_SLV_REG8_OUT_DATA        32
#define XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG9_OUT_DATA        0x58
#define XSYSTOLIC_FPGA_CONTROL_BITS_SLV_REG9_OUT_DATA        32
#define XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG10_OUT_DATA       0x60
#define XSYSTOLIC_FPGA_CONTROL_BITS_SLV_REG10_OUT_DATA       32
#define XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG11_OUT_DATA       0x68
#define XSYSTOLIC_FPGA_CONTROL_BITS_SLV_REG11_OUT_DATA       32
#define XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG12_OUT_DATA       0x70
#define XSYSTOLIC_FPGA_CONTROL_BITS_SLV_REG12_OUT_DATA       32
#define XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG13_OUT_DATA       0x78
#define XSYSTOLIC_FPGA_CONTROL_BITS_SLV_REG13_OUT_DATA       32
#define XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG14_OUT_DATA       0x80
#define XSYSTOLIC_FPGA_CONTROL_BITS_SLV_REG14_OUT_DATA       32
#define XSYSTOLIC_FPGA_CONTROL_ADDR_AXI00_IMEM_PTR0_DATA     0x88
#define XSYSTOLIC_FPGA_CONTROL_BITS_AXI00_IMEM_PTR0_DATA     64
#define XSYSTOLIC_FPGA_CONTROL_ADDR_AXI01_PARAMBUF_PTR0_DATA 0x94
#define XSYSTOLIC_FPGA_CONTROL_BITS_AXI01_PARAMBUF_PTR0_DATA 64
#define XSYSTOLIC_FPGA_CONTROL_ADDR_AXI02_IBUF_PTR0_DATA     0xa0
#define XSYSTOLIC_FPGA_CONTROL_BITS_AXI02_IBUF_PTR0_DATA     64
#define XSYSTOLIC_FPGA_CONTROL_ADDR_AXI03_OBUF_PTR0_DATA     0xac
#define XSYSTOLIC_FPGA_CONTROL_BITS_AXI03_OBUF_PTR0_DATA     64

