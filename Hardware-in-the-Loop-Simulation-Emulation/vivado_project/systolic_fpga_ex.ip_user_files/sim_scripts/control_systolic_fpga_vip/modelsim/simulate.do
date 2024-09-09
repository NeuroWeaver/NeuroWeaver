onbreak {quit -f}
onerror {quit -f}

vsim -voptargs="+acc" -L xilinx_vip -L xpm -L axi_infrastructure_v1_1_0 -L xil_defaultlib -L axi_vip_v1_1_8 -L xilinx_vip -L unisims_ver -L unimacro_ver -L secureip -lib xil_defaultlib xil_defaultlib.control_systolic_fpga_vip xil_defaultlib.glbl

do {wave.do}

view wave
view structure
view signals

do {control_systolic_fpga_vip.udo}

run -all

quit -force
