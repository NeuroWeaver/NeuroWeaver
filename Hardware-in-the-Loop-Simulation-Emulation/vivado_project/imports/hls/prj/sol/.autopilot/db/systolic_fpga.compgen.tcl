# This script segment is generated automatically by AutoPilot

# Memory (RAM/ROM)  definition:
set ID 1
set hasByteEnable 0
set MemName systolic_fpga_m00_imem_axi_input_buffer
set CoreName ap_simcore_mem
set PortList { 2 3 }
set DataWd 32
set AddrRange 8192
set AddrWd 13
set impl_style auto
set TrueReset 0
set HasInitializer 0
set IsROM 0
set ROMData {}
set NumOfStage 2
set MaxLatency -1
set DelayBudget 1.248
set ClkPeriod 10
set RegisteredInput 0
if {${::AESL::PGuard_simmodel_gen}} {
if {[info proc ap_gen_simcore_mem] == "ap_gen_simcore_mem"} {
    eval "ap_gen_simcore_mem { \
    id ${ID} \
    name ${MemName} \
    corename ${CoreName}  \
    op mem \
    hasByteEnable ${hasByteEnable} \
    reset_level 1 \
    sync_rst true \
    stage_num ${NumOfStage}  \
    registered_input ${RegisteredInput} \
    port_num 2 \
    port_list \{${PortList}\} \
    data_wd ${DataWd} \
    addr_wd ${AddrWd} \
    addr_range ${AddrRange} \
    style ${impl_style} \
    true_reset ${TrueReset} \
    delay_budget ${DelayBudget} \
    clk_period ${ClkPeriod} \
    HasInitializer ${HasInitializer} \
    rom_data \{${ROMData}\} \
 } "
} else {
    puts "@W \[IMPL-102\] Cannot find ap_gen_simcore_mem, check your platform lib"
}
}


if {${::AESL::PGuard_rtl_comp_handler}} {
  ::AP::rtl_comp_handler $MemName
}


set CoreName RAM
if {${::AESL::PGuard_autocg_gen} && ${::AESL::PGuard_autocg_ipmgen}} {
if {[info proc ::AESL_LIB_VIRTEX::xil_gen_RAM] == "::AESL_LIB_VIRTEX::xil_gen_RAM"} {
    eval "::AESL_LIB_VIRTEX::xil_gen_RAM { \
    id ${ID} \
    name ${MemName} \
    corename ${CoreName}  \
    op mem \
    hasByteEnable ${hasByteEnable} \
    reset_level 1 \
    sync_rst true \
    stage_num ${NumOfStage}  \
    registered_input ${RegisteredInput} \
    port_num 2 \
    port_list \{${PortList}\} \
    data_wd ${DataWd} \
    addr_wd ${AddrWd} \
    addr_range ${AddrRange} \
    style ${impl_style} \
    true_reset ${TrueReset} \
    delay_budget ${DelayBudget} \
    clk_period ${ClkPeriod} \
    HasInitializer ${HasInitializer} \
    rom_data \{${ROMData}\} \
 } "
  } else {
    puts "@W \[IMPL-104\] Cannot find ::AESL_LIB_VIRTEX::xil_gen_RAM, check your platform lib"
  }
}


# clear list
if {${::AESL::PGuard_autoexp_gen}} {
    cg_default_interface_gen_dc_begin
    cg_default_interface_gen_bundle_begin
    AESL_LIB_XILADAPTER::native_axis_begin
}

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


# Native S_AXILite:
if {${::AESL::PGuard_simmodel_gen}} {
	if {[info proc ::AESL_LIB_XILADAPTER::s_axilite_gen] == "::AESL_LIB_XILADAPTER::s_axilite_gen"} {
		eval "::AESL_LIB_XILADAPTER::s_axilite_gen { \
			id 2 \
			corename systolic_fpga_control_axilite \
			name systolic_fpga_control_s_axi \
			ports {$port_control} \
			op interface \
			is_flushable 0 \ 
			is_datawidth64 0 \ 
		} "
	} else {
		puts "@W \[IMPL-110\] Cannot find AXI Lite interface model in the library. Ignored generation of AXI Lite  interface for 'control'"
	}
}

if {${::AESL::PGuard_rtl_comp_handler}} {
	::AP::rtl_comp_handler systolic_fpga_control_s_axi
}

# Native M_AXI:
if {${::AESL::PGuard_simmodel_gen}} {
if {[info proc ::AESL_LIB_XILADAPTER::m_axi_gen] == "::AESL_LIB_XILADAPTER::m_axi_gen"} {
eval "::AESL_LIB_XILADAPTER::m_axi_gen { \
    id 3 \
    corename {m_axi} \
    op interface \
    max_latency -1 \ 
    delay_budget 7.3 \ 
    is_flushable 0 \ 
    name {systolic_fpga_m00_imem_axi_m_axi} \
} "
} else {
puts "@W \[IMPL-110\] Cannot find AXI interface model in the library. Ignored generation of AXI interface for 'm00_imem_axi'"
}
}

if {${::AESL::PGuard_rtl_comp_handler}} {
	::AP::rtl_comp_handler systolic_fpga_m00_imem_axi_m_axi
}

# Native M_AXI:
if {${::AESL::PGuard_simmodel_gen}} {
if {[info proc ::AESL_LIB_XILADAPTER::m_axi_gen] == "::AESL_LIB_XILADAPTER::m_axi_gen"} {
eval "::AESL_LIB_XILADAPTER::m_axi_gen { \
    id 4 \
    corename {m_axi} \
    op interface \
    max_latency -1 \ 
    delay_budget 7.3 \ 
    is_flushable 0 \ 
    name {systolic_fpga_m01_parambuf_axi_m_axi} \
} "
} else {
puts "@W \[IMPL-110\] Cannot find AXI interface model in the library. Ignored generation of AXI interface for 'm01_parambuf_axi'"
}
}

if {${::AESL::PGuard_rtl_comp_handler}} {
	::AP::rtl_comp_handler systolic_fpga_m01_parambuf_axi_m_axi
}

# Native M_AXI:
if {${::AESL::PGuard_simmodel_gen}} {
if {[info proc ::AESL_LIB_XILADAPTER::m_axi_gen] == "::AESL_LIB_XILADAPTER::m_axi_gen"} {
eval "::AESL_LIB_XILADAPTER::m_axi_gen { \
    id 5 \
    corename {m_axi} \
    op interface \
    max_latency -1 \ 
    delay_budget 7.3 \ 
    is_flushable 0 \ 
    name {systolic_fpga_m02_ibuf_axi_m_axi} \
} "
} else {
puts "@W \[IMPL-110\] Cannot find AXI interface model in the library. Ignored generation of AXI interface for 'm02_ibuf_axi'"
}
}

if {${::AESL::PGuard_rtl_comp_handler}} {
	::AP::rtl_comp_handler systolic_fpga_m02_ibuf_axi_m_axi
}

# Native M_AXI:
if {${::AESL::PGuard_simmodel_gen}} {
if {[info proc ::AESL_LIB_XILADAPTER::m_axi_gen] == "::AESL_LIB_XILADAPTER::m_axi_gen"} {
eval "::AESL_LIB_XILADAPTER::m_axi_gen { \
    id 6 \
    corename {m_axi} \
    op interface \
    max_latency -1 \ 
    delay_budget 7.3 \ 
    is_flushable 0 \ 
    name {systolic_fpga_m03_obuf_axi_m_axi} \
} "
} else {
puts "@W \[IMPL-110\] Cannot find AXI interface model in the library. Ignored generation of AXI interface for 'm03_obuf_axi'"
}
}

if {${::AESL::PGuard_rtl_comp_handler}} {
	::AP::rtl_comp_handler systolic_fpga_m03_obuf_axi_m_axi
}


# Adapter definition:
set PortName ap_clk
set DataWd 1 
if {${::AESL::PGuard_autoexp_gen}} {
if {[info proc cg_default_interface_gen_clock] == "cg_default_interface_gen_clock"} {
eval "cg_default_interface_gen_clock { \
    id -1 \
    name ${PortName} \
    reset_level 0 \
    sync_rst true \
    corename apif_ap_clk \
    data_wd ${DataWd} \
    op interface \
}"
} else {
puts "@W \[IMPL-113\] Cannot find bus interface model in the library. Ignored generation of bus interface for '${PortName}'"
}
}


# Adapter definition:
set PortName ap_rst_n
set DataWd 1 
if {${::AESL::PGuard_autoexp_gen}} {
if {[info proc cg_default_interface_gen_reset] == "cg_default_interface_gen_reset"} {
eval "cg_default_interface_gen_reset { \
    id -2 \
    name ${PortName} \
    reset_level 0 \
    sync_rst true \
    corename apif_ap_rst_n \
    data_wd ${DataWd} \
    op interface \
}"
} else {
puts "@W \[IMPL-114\] Cannot find bus interface model in the library. Ignored generation of bus interface for '${PortName}'"
}
}



# merge
if {${::AESL::PGuard_autoexp_gen}} {
    cg_default_interface_gen_dc_end
    cg_default_interface_gen_bundle_end
    AESL_LIB_XILADAPTER::native_axis_end
}


