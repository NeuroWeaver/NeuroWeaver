onbreak {quit -f}
onerror {quit -f}

vsim -lib xil_defaultlib slv_m03_obuf_axi_vip_opt

do {wave.do}

view wave
view structure
view signals

do {slv_m03_obuf_axi_vip.udo}

run -all

quit -force
