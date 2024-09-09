// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2020.2 (64-bit)
// Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
// ==============================================================
#ifndef __linux__

#include "xstatus.h"
#include "xparameters.h"
#include "xsystolic_fpga.h"

extern XSystolic_fpga_Config XSystolic_fpga_ConfigTable[];

XSystolic_fpga_Config *XSystolic_fpga_LookupConfig(u16 DeviceId) {
	XSystolic_fpga_Config *ConfigPtr = NULL;

	int Index;

	for (Index = 0; Index < XPAR_XSYSTOLIC_FPGA_NUM_INSTANCES; Index++) {
		if (XSystolic_fpga_ConfigTable[Index].DeviceId == DeviceId) {
			ConfigPtr = &XSystolic_fpga_ConfigTable[Index];
			break;
		}
	}

	return ConfigPtr;
}

int XSystolic_fpga_Initialize(XSystolic_fpga *InstancePtr, u16 DeviceId) {
	XSystolic_fpga_Config *ConfigPtr;

	Xil_AssertNonvoid(InstancePtr != NULL);

	ConfigPtr = XSystolic_fpga_LookupConfig(DeviceId);
	if (ConfigPtr == NULL) {
		InstancePtr->IsReady = 0;
		return (XST_DEVICE_NOT_FOUND);
	}

	return XSystolic_fpga_CfgInitialize(InstancePtr, ConfigPtr);
}

#endif

