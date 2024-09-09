// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2020.2 (64-bit)
// Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
// ==============================================================
#ifndef XSYSTOLIC_FPGA_H
#define XSYSTOLIC_FPGA_H

#ifdef __cplusplus
extern "C" {
#endif

/***************************** Include Files *********************************/
#ifndef __linux__
#include "xil_types.h"
#include "xil_assert.h"
#include "xstatus.h"
#include "xil_io.h"
#else
#include <stdint.h>
#include <assert.h>
#include <dirent.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stddef.h>
#endif
#include "xsystolic_fpga_hw.h"

/**************************** Type Definitions ******************************/
#ifdef __linux__
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef uint64_t u64;
#else
typedef struct {
    u16 DeviceId;
    u32 Control_BaseAddress;
} XSystolic_fpga_Config;
#endif

typedef struct {
    u64 Control_BaseAddress;
    u32 IsReady;
} XSystolic_fpga;

typedef u32 word_type;

/***************** Macros (Inline Functions) Definitions *********************/
#ifndef __linux__
#define XSystolic_fpga_WriteReg(BaseAddress, RegOffset, Data) \
    Xil_Out32((BaseAddress) + (RegOffset), (u32)(Data))
#define XSystolic_fpga_ReadReg(BaseAddress, RegOffset) \
    Xil_In32((BaseAddress) + (RegOffset))
#else
#define XSystolic_fpga_WriteReg(BaseAddress, RegOffset, Data) \
    *(volatile u32*)((BaseAddress) + (RegOffset)) = (u32)(Data)
#define XSystolic_fpga_ReadReg(BaseAddress, RegOffset) \
    *(volatile u32*)((BaseAddress) + (RegOffset))

#define Xil_AssertVoid(expr)    assert(expr)
#define Xil_AssertNonvoid(expr) assert(expr)

#define XST_SUCCESS             0
#define XST_DEVICE_NOT_FOUND    2
#define XST_OPEN_DEVICE_FAILED  3
#define XIL_COMPONENT_IS_READY  1
#endif

/************************** Function Prototypes *****************************/
#ifndef __linux__
int XSystolic_fpga_Initialize(XSystolic_fpga *InstancePtr, u16 DeviceId);
XSystolic_fpga_Config* XSystolic_fpga_LookupConfig(u16 DeviceId);
int XSystolic_fpga_CfgInitialize(XSystolic_fpga *InstancePtr, XSystolic_fpga_Config *ConfigPtr);
#else
int XSystolic_fpga_Initialize(XSystolic_fpga *InstancePtr, const char* InstanceName);
int XSystolic_fpga_Release(XSystolic_fpga *InstancePtr);
#endif

void XSystolic_fpga_Start(XSystolic_fpga *InstancePtr);
u32 XSystolic_fpga_IsDone(XSystolic_fpga *InstancePtr);
u32 XSystolic_fpga_IsIdle(XSystolic_fpga *InstancePtr);
u32 XSystolic_fpga_IsReady(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_EnableAutoRestart(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_DisableAutoRestart(XSystolic_fpga *InstancePtr);

void XSystolic_fpga_Set_slv_reg0_out(XSystolic_fpga *InstancePtr, u32 Data);
u32 XSystolic_fpga_Get_slv_reg0_out(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_Set_slv_reg1_out(XSystolic_fpga *InstancePtr, u32 Data);
u32 XSystolic_fpga_Get_slv_reg1_out(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_Set_slv_reg2_out(XSystolic_fpga *InstancePtr, u32 Data);
u32 XSystolic_fpga_Get_slv_reg2_out(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_Set_slv_reg3_out(XSystolic_fpga *InstancePtr, u32 Data);
u32 XSystolic_fpga_Get_slv_reg3_out(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_Set_slv_reg4_out(XSystolic_fpga *InstancePtr, u32 Data);
u32 XSystolic_fpga_Get_slv_reg4_out(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_Set_slv_reg5_out(XSystolic_fpga *InstancePtr, u32 Data);
u32 XSystolic_fpga_Get_slv_reg5_out(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_Set_slv_reg6_out(XSystolic_fpga *InstancePtr, u32 Data);
u32 XSystolic_fpga_Get_slv_reg6_out(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_Set_slv_reg7_out(XSystolic_fpga *InstancePtr, u32 Data);
u32 XSystolic_fpga_Get_slv_reg7_out(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_Set_slv_reg8_out(XSystolic_fpga *InstancePtr, u32 Data);
u32 XSystolic_fpga_Get_slv_reg8_out(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_Set_slv_reg9_out(XSystolic_fpga *InstancePtr, u32 Data);
u32 XSystolic_fpga_Get_slv_reg9_out(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_Set_slv_reg10_out(XSystolic_fpga *InstancePtr, u32 Data);
u32 XSystolic_fpga_Get_slv_reg10_out(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_Set_slv_reg11_out(XSystolic_fpga *InstancePtr, u32 Data);
u32 XSystolic_fpga_Get_slv_reg11_out(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_Set_slv_reg12_out(XSystolic_fpga *InstancePtr, u32 Data);
u32 XSystolic_fpga_Get_slv_reg12_out(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_Set_slv_reg13_out(XSystolic_fpga *InstancePtr, u32 Data);
u32 XSystolic_fpga_Get_slv_reg13_out(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_Set_slv_reg14_out(XSystolic_fpga *InstancePtr, u32 Data);
u32 XSystolic_fpga_Get_slv_reg14_out(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_Set_axi00_imem_ptr0(XSystolic_fpga *InstancePtr, u64 Data);
u64 XSystolic_fpga_Get_axi00_imem_ptr0(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_Set_axi01_parambuf_ptr0(XSystolic_fpga *InstancePtr, u64 Data);
u64 XSystolic_fpga_Get_axi01_parambuf_ptr0(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_Set_axi02_ibuf_ptr0(XSystolic_fpga *InstancePtr, u64 Data);
u64 XSystolic_fpga_Get_axi02_ibuf_ptr0(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_Set_axi03_obuf_ptr0(XSystolic_fpga *InstancePtr, u64 Data);
u64 XSystolic_fpga_Get_axi03_obuf_ptr0(XSystolic_fpga *InstancePtr);

void XSystolic_fpga_InterruptGlobalEnable(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_InterruptGlobalDisable(XSystolic_fpga *InstancePtr);
void XSystolic_fpga_InterruptEnable(XSystolic_fpga *InstancePtr, u32 Mask);
void XSystolic_fpga_InterruptDisable(XSystolic_fpga *InstancePtr, u32 Mask);
void XSystolic_fpga_InterruptClear(XSystolic_fpga *InstancePtr, u32 Mask);
u32 XSystolic_fpga_InterruptGetEnabled(XSystolic_fpga *InstancePtr);
u32 XSystolic_fpga_InterruptGetStatus(XSystolic_fpga *InstancePtr);

#ifdef __cplusplus
}
#endif

#endif
