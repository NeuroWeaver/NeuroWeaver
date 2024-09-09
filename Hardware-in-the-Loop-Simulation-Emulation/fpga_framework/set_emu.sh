#! /bin/bash

platform="xilinx_u280_xdma_201920_1"
emconfigutil --platform $platform


export XCL_EMULATION_MODE=hw_emu
echo $XCL_EMULATION_MODE
