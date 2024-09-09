#!/bin/bash

#xvlog -f ./genesys_systolic_fpga_sim.f      \
#      -L xilinx_vip                 \
#      --sv # -d DUMP_WAVEFORM
#
xvlog --incr --relax -L uvm -L axi_vip_v1_1_8 -L xilinx_vip -f ./genesys_systolic_fpga_sim.f --sv 2>&1 | tee compile.log


#xelab systolic_fpga_tb glbl      \
#      -debug typical        \
#      -L unisims_ver        \
#      -L xpm                \
#      -L xilinx_vip

xelab -wto 2d9f831c8e5841b5be568eea32746cd3 --incr --debug typical \
      --relax --mt 8 -L xil_defaultlib -L axi_infrastructure_v1_1_0 \
      -L axi_vip_v1_1_8 -L uvm -L xilinx_vip -L unisims_ver -L unimacro_ver \
      -L secureip -L xpm --snapshot systolic_fpga_tb_behav systolic_fpga_tb \
      glbl -log elaborate.log



#xsim -t xsim.tcl --wdb work.systolic_fpga_tb.wdb work.systolic_fpga_tb#work.glbl

xsim systolic_fpga_tb_behav -key {Behavioral:sim_1:Functional:systolic_fpga_tb} -tclbatch systolic_fpga_tb.tcl -log simulate.log


