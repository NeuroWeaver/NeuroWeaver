// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2020.2 (64-bit)
// Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
// ==============================================================
/***************************** Include Files *********************************/
#include "xsystolic_fpga.h"

/************************** Function Implementation *************************/
#ifndef __linux__
int XSystolic_fpga_CfgInitialize(XSystolic_fpga *InstancePtr, XSystolic_fpga_Config *ConfigPtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(ConfigPtr != NULL);

    InstancePtr->Control_BaseAddress = ConfigPtr->Control_BaseAddress;
    InstancePtr->IsReady = XIL_COMPONENT_IS_READY;

    return XST_SUCCESS;
}
#endif

void XSystolic_fpga_Start(XSystolic_fpga *InstancePtr) {
    u32 Data;

    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AP_CTRL) & 0x80;
    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AP_CTRL, Data | 0x01);
}

u32 XSystolic_fpga_IsDone(XSystolic_fpga *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AP_CTRL);
    return (Data >> 1) & 0x1;
}

u32 XSystolic_fpga_IsIdle(XSystolic_fpga *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AP_CTRL);
    return (Data >> 2) & 0x1;
}

u32 XSystolic_fpga_IsReady(XSystolic_fpga *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AP_CTRL);
    // check ap_start to see if the pcore is ready for next input
    return !(Data & 0x1);
}

void XSystolic_fpga_EnableAutoRestart(XSystolic_fpga *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AP_CTRL, 0x80);
}

void XSystolic_fpga_DisableAutoRestart(XSystolic_fpga *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AP_CTRL, 0);
}

void XSystolic_fpga_Set_slv_reg0_out(XSystolic_fpga *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG0_OUT_DATA, Data);
}

u32 XSystolic_fpga_Get_slv_reg0_out(XSystolic_fpga *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG0_OUT_DATA);
    return Data;
}

void XSystolic_fpga_Set_slv_reg1_out(XSystolic_fpga *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG1_OUT_DATA, Data);
}

u32 XSystolic_fpga_Get_slv_reg1_out(XSystolic_fpga *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG1_OUT_DATA);
    return Data;
}

void XSystolic_fpga_Set_slv_reg2_out(XSystolic_fpga *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG2_OUT_DATA, Data);
}

u32 XSystolic_fpga_Get_slv_reg2_out(XSystolic_fpga *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG2_OUT_DATA);
    return Data;
}

void XSystolic_fpga_Set_slv_reg3_out(XSystolic_fpga *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG3_OUT_DATA, Data);
}

u32 XSystolic_fpga_Get_slv_reg3_out(XSystolic_fpga *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG3_OUT_DATA);
    return Data;
}

void XSystolic_fpga_Set_slv_reg4_out(XSystolic_fpga *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG4_OUT_DATA, Data);
}

u32 XSystolic_fpga_Get_slv_reg4_out(XSystolic_fpga *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG4_OUT_DATA);
    return Data;
}

void XSystolic_fpga_Set_slv_reg5_out(XSystolic_fpga *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG5_OUT_DATA, Data);
}

u32 XSystolic_fpga_Get_slv_reg5_out(XSystolic_fpga *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG5_OUT_DATA);
    return Data;
}

void XSystolic_fpga_Set_slv_reg6_out(XSystolic_fpga *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG6_OUT_DATA, Data);
}

u32 XSystolic_fpga_Get_slv_reg6_out(XSystolic_fpga *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG6_OUT_DATA);
    return Data;
}

void XSystolic_fpga_Set_slv_reg7_out(XSystolic_fpga *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG7_OUT_DATA, Data);
}

u32 XSystolic_fpga_Get_slv_reg7_out(XSystolic_fpga *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG7_OUT_DATA);
    return Data;
}

void XSystolic_fpga_Set_slv_reg8_out(XSystolic_fpga *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG8_OUT_DATA, Data);
}

u32 XSystolic_fpga_Get_slv_reg8_out(XSystolic_fpga *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG8_OUT_DATA);
    return Data;
}

void XSystolic_fpga_Set_slv_reg9_out(XSystolic_fpga *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG9_OUT_DATA, Data);
}

u32 XSystolic_fpga_Get_slv_reg9_out(XSystolic_fpga *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG9_OUT_DATA);
    return Data;
}

void XSystolic_fpga_Set_slv_reg10_out(XSystolic_fpga *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG10_OUT_DATA, Data);
}

u32 XSystolic_fpga_Get_slv_reg10_out(XSystolic_fpga *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG10_OUT_DATA);
    return Data;
}

void XSystolic_fpga_Set_slv_reg11_out(XSystolic_fpga *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG11_OUT_DATA, Data);
}

u32 XSystolic_fpga_Get_slv_reg11_out(XSystolic_fpga *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG11_OUT_DATA);
    return Data;
}

void XSystolic_fpga_Set_slv_reg12_out(XSystolic_fpga *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG12_OUT_DATA, Data);
}

u32 XSystolic_fpga_Get_slv_reg12_out(XSystolic_fpga *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG12_OUT_DATA);
    return Data;
}

void XSystolic_fpga_Set_slv_reg13_out(XSystolic_fpga *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG13_OUT_DATA, Data);
}

u32 XSystolic_fpga_Get_slv_reg13_out(XSystolic_fpga *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG13_OUT_DATA);
    return Data;
}

void XSystolic_fpga_Set_slv_reg14_out(XSystolic_fpga *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG14_OUT_DATA, Data);
}

u32 XSystolic_fpga_Get_slv_reg14_out(XSystolic_fpga *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_SLV_REG14_OUT_DATA);
    return Data;
}

void XSystolic_fpga_Set_axi00_imem_ptr0(XSystolic_fpga *InstancePtr, u64 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AXI00_IMEM_PTR0_DATA, (u32)(Data));
    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AXI00_IMEM_PTR0_DATA + 4, (u32)(Data >> 32));
}

u64 XSystolic_fpga_Get_axi00_imem_ptr0(XSystolic_fpga *InstancePtr) {
    u64 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AXI00_IMEM_PTR0_DATA);
    Data += (u64)XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AXI00_IMEM_PTR0_DATA + 4) << 32;
    return Data;
}

void XSystolic_fpga_Set_axi01_parambuf_ptr0(XSystolic_fpga *InstancePtr, u64 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AXI01_PARAMBUF_PTR0_DATA, (u32)(Data));
    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AXI01_PARAMBUF_PTR0_DATA + 4, (u32)(Data >> 32));
}

u64 XSystolic_fpga_Get_axi01_parambuf_ptr0(XSystolic_fpga *InstancePtr) {
    u64 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AXI01_PARAMBUF_PTR0_DATA);
    Data += (u64)XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AXI01_PARAMBUF_PTR0_DATA + 4) << 32;
    return Data;
}

void XSystolic_fpga_Set_axi02_ibuf_ptr0(XSystolic_fpga *InstancePtr, u64 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AXI02_IBUF_PTR0_DATA, (u32)(Data));
    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AXI02_IBUF_PTR0_DATA + 4, (u32)(Data >> 32));
}

u64 XSystolic_fpga_Get_axi02_ibuf_ptr0(XSystolic_fpga *InstancePtr) {
    u64 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AXI02_IBUF_PTR0_DATA);
    Data += (u64)XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AXI02_IBUF_PTR0_DATA + 4) << 32;
    return Data;
}

void XSystolic_fpga_Set_axi03_obuf_ptr0(XSystolic_fpga *InstancePtr, u64 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AXI03_OBUF_PTR0_DATA, (u32)(Data));
    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AXI03_OBUF_PTR0_DATA + 4, (u32)(Data >> 32));
}

u64 XSystolic_fpga_Get_axi03_obuf_ptr0(XSystolic_fpga *InstancePtr) {
    u64 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AXI03_OBUF_PTR0_DATA);
    Data += (u64)XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_AXI03_OBUF_PTR0_DATA + 4) << 32;
    return Data;
}

void XSystolic_fpga_InterruptGlobalEnable(XSystolic_fpga *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_GIE, 1);
}

void XSystolic_fpga_InterruptGlobalDisable(XSystolic_fpga *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_GIE, 0);
}

void XSystolic_fpga_InterruptEnable(XSystolic_fpga *InstancePtr, u32 Mask) {
    u32 Register;

    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Register =  XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_IER);
    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_IER, Register | Mask);
}

void XSystolic_fpga_InterruptDisable(XSystolic_fpga *InstancePtr, u32 Mask) {
    u32 Register;

    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Register =  XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_IER);
    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_IER, Register & (~Mask));
}

void XSystolic_fpga_InterruptClear(XSystolic_fpga *InstancePtr, u32 Mask) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSystolic_fpga_WriteReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_ISR, Mask);
}

u32 XSystolic_fpga_InterruptGetEnabled(XSystolic_fpga *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_IER);
}

u32 XSystolic_fpga_InterruptGetStatus(XSystolic_fpga *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XSystolic_fpga_ReadReg(InstancePtr->Control_BaseAddress, XSYSTOLIC_FPGA_CONTROL_ADDR_ISR);
}

