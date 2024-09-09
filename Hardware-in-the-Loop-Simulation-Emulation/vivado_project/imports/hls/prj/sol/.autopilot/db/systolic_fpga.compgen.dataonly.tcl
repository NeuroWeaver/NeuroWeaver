# This script segment is generated automatically by AutoPilot

set axilite_register_dict [dict create]
set port_control {
slv_reg0_out { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 16
	offset_end 23
}
slv_reg1_out { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 24
	offset_end 31
}
slv_reg2_out { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 32
	offset_end 39
}
slv_reg3_out { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 40
	offset_end 47
}
slv_reg4_out { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 48
	offset_end 55
}
slv_reg5_out { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 56
	offset_end 63
}
slv_reg6_out { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 64
	offset_end 71
}
slv_reg7_out { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 72
	offset_end 79
}
slv_reg8_out { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 80
	offset_end 87
}
slv_reg9_out { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 88
	offset_end 95
}
slv_reg10_out { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 96
	offset_end 103
}
slv_reg11_out { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 104
	offset_end 111
}
slv_reg12_out { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 112
	offset_end 119
}
slv_reg13_out { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 120
	offset_end 127
}
slv_reg14_out { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 128
	offset_end 135
}
axi00_imem_ptr0 { 
	dir I
	width 64
	depth 1
	mode ap_none
	offset 136
	offset_end 147
}
axi01_parambuf_ptr0 { 
	dir I
	width 64
	depth 1
	mode ap_none
	offset 148
	offset_end 159
}
axi02_ibuf_ptr0 { 
	dir I
	width 64
	depth 1
	mode ap_none
	offset 160
	offset_end 171
}
axi03_obuf_ptr0 { 
	dir I
	width 64
	depth 1
	mode ap_none
	offset 172
	offset_end 183
}
ap_start { }
ap_done { }
ap_ready { }
ap_idle { }
}
dict set axilite_register_dict control $port_control


