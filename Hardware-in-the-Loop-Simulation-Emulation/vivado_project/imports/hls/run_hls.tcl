# This is a generated file. Use and modify at your own risk.
################################################################################

open_project prj
open_solution sol -flow_target vitis
set_part xcu280-fsvh2892-2L-e
add_files ../systolic_fpga_cmodel.cpp
set_top systolic_fpga
csynth_design
exit

