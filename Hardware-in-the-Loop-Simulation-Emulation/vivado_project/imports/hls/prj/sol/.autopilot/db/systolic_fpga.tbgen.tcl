set moduleName systolic_fpga
set isTopModule 1
set isCombinational 0
set isDatapathOnly 0
set isPipelined 0
set pipeline_type none
set FunctionProtocol ap_ctrl_hs
set isOneStateSeq 0
set ProfileFlag 0
set StallSigGenFlag 0
set isEnableWaveformDebug 1
set C_modelName {systolic_fpga}
set C_modelType { void 0 }
set C_modelArgList {
	{ m00_imem_axi int 512 regular {axi_master 2}  }
	{ m01_parambuf_axi int 512 regular {axi_master 2}  }
	{ m02_ibuf_axi int 512 regular {axi_master 2}  }
	{ m03_obuf_axi int 512 regular {axi_master 2}  }
	{ slv_reg0_out int 32 unused {axi_slave 0}  }
	{ slv_reg1_out int 32 unused {axi_slave 0}  }
	{ slv_reg2_out int 32 unused {axi_slave 0}  }
	{ slv_reg3_out int 32 unused {axi_slave 0}  }
	{ slv_reg4_out int 32 unused {axi_slave 0}  }
	{ slv_reg5_out int 32 unused {axi_slave 0}  }
	{ slv_reg6_out int 32 unused {axi_slave 0}  }
	{ slv_reg7_out int 32 unused {axi_slave 0}  }
	{ slv_reg8_out int 32 unused {axi_slave 0}  }
	{ slv_reg9_out int 32 unused {axi_slave 0}  }
	{ slv_reg10_out int 32 unused {axi_slave 0}  }
	{ slv_reg11_out int 32 unused {axi_slave 0}  }
	{ slv_reg12_out int 32 unused {axi_slave 0}  }
	{ slv_reg13_out int 32 unused {axi_slave 0}  }
	{ slv_reg14_out int 32 unused {axi_slave 0}  }
	{ axi00_imem_ptr0 int 64 regular {axi_slave 0}  }
	{ axi01_parambuf_ptr0 int 64 regular {axi_slave 0}  }
	{ axi02_ibuf_ptr0 int 64 regular {axi_slave 0}  }
	{ axi03_obuf_ptr0 int 64 regular {axi_slave 0}  }
}
set C_modelArgMapList {[ 
	{ "Name" : "m00_imem_axi", "interface" : "axi_master", "bitwidth" : 512, "direction" : "READWRITE", "bitSlice":[{"low":0,"up":0,"cElement": [{"cName": "axi00_imem_ptr0","cData": "int512","bit_use": { "low": 0,"up": 0},"offset": { "type": "dynamic","port_name": "axi00_imem_ptr0","bundle": "control"},"direction": "READWRITE","cArray": [{"low" : 0,"up" : 0,"step" : 0}]}]}]} , 
 	{ "Name" : "m01_parambuf_axi", "interface" : "axi_master", "bitwidth" : 512, "direction" : "READWRITE", "bitSlice":[{"low":0,"up":0,"cElement": [{"cName": "axi01_parambuf_ptr0","cData": "int512","bit_use": { "low": 0,"up": 0},"offset": { "type": "dynamic","port_name": "axi01_parambuf_ptr0","bundle": "control"},"direction": "READWRITE","cArray": [{"low" : 0,"up" : 0,"step" : 0}]}]}]} , 
 	{ "Name" : "m02_ibuf_axi", "interface" : "axi_master", "bitwidth" : 512, "direction" : "READWRITE", "bitSlice":[{"low":0,"up":0,"cElement": [{"cName": "axi02_ibuf_ptr0","cData": "int512","bit_use": { "low": 0,"up": 0},"offset": { "type": "dynamic","port_name": "axi02_ibuf_ptr0","bundle": "control"},"direction": "READWRITE","cArray": [{"low" : 0,"up" : 0,"step" : 0}]}]}]} , 
 	{ "Name" : "m03_obuf_axi", "interface" : "axi_master", "bitwidth" : 512, "direction" : "READWRITE", "bitSlice":[{"low":0,"up":0,"cElement": [{"cName": "axi03_obuf_ptr0","cData": "int512","bit_use": { "low": 0,"up": 0},"offset": { "type": "dynamic","port_name": "axi03_obuf_ptr0","bundle": "control"},"direction": "READWRITE","cArray": [{"low" : 0,"up" : 0,"step" : 0}]}]}]} , 
 	{ "Name" : "slv_reg0_out", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "bitSlice":[{"low":0,"up":0,"cElement": [{"cName": "slv_reg0_out","cData": "int","bit_use": { "low": 0,"up": 0},"cArray": [{"low" : 0,"up" : 0,"step" : 0}]}]}], "offset" : {"in":16}, "offset_end" : {"in":23}} , 
 	{ "Name" : "slv_reg1_out", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "bitSlice":[{"low":0,"up":0,"cElement": [{"cName": "slv_reg1_out","cData": "int","bit_use": { "low": 0,"up": 0},"cArray": [{"low" : 0,"up" : 0,"step" : 0}]}]}], "offset" : {"in":24}, "offset_end" : {"in":31}} , 
 	{ "Name" : "slv_reg2_out", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "bitSlice":[{"low":0,"up":0,"cElement": [{"cName": "slv_reg2_out","cData": "int","bit_use": { "low": 0,"up": 0},"cArray": [{"low" : 0,"up" : 0,"step" : 0}]}]}], "offset" : {"in":32}, "offset_end" : {"in":39}} , 
 	{ "Name" : "slv_reg3_out", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "bitSlice":[{"low":0,"up":0,"cElement": [{"cName": "slv_reg3_out","cData": "int","bit_use": { "low": 0,"up": 0},"cArray": [{"low" : 0,"up" : 0,"step" : 0}]}]}], "offset" : {"in":40}, "offset_end" : {"in":47}} , 
 	{ "Name" : "slv_reg4_out", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "bitSlice":[{"low":0,"up":0,"cElement": [{"cName": "slv_reg4_out","cData": "int","bit_use": { "low": 0,"up": 0},"cArray": [{"low" : 0,"up" : 0,"step" : 0}]}]}], "offset" : {"in":48}, "offset_end" : {"in":55}} , 
 	{ "Name" : "slv_reg5_out", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "bitSlice":[{"low":0,"up":0,"cElement": [{"cName": "slv_reg5_out","cData": "int","bit_use": { "low": 0,"up": 0},"cArray": [{"low" : 0,"up" : 0,"step" : 0}]}]}], "offset" : {"in":56}, "offset_end" : {"in":63}} , 
 	{ "Name" : "slv_reg6_out", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "bitSlice":[{"low":0,"up":0,"cElement": [{"cName": "slv_reg6_out","cData": "int","bit_use": { "low": 0,"up": 0},"cArray": [{"low" : 0,"up" : 0,"step" : 0}]}]}], "offset" : {"in":64}, "offset_end" : {"in":71}} , 
 	{ "Name" : "slv_reg7_out", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "bitSlice":[{"low":0,"up":0,"cElement": [{"cName": "slv_reg7_out","cData": "int","bit_use": { "low": 0,"up": 0},"cArray": [{"low" : 0,"up" : 0,"step" : 0}]}]}], "offset" : {"in":72}, "offset_end" : {"in":79}} , 
 	{ "Name" : "slv_reg8_out", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "bitSlice":[{"low":0,"up":0,"cElement": [{"cName": "slv_reg8_out","cData": "int","bit_use": { "low": 0,"up": 0},"cArray": [{"low" : 0,"up" : 0,"step" : 0}]}]}], "offset" : {"in":80}, "offset_end" : {"in":87}} , 
 	{ "Name" : "slv_reg9_out", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "bitSlice":[{"low":0,"up":0,"cElement": [{"cName": "slv_reg9_out","cData": "int","bit_use": { "low": 0,"up": 0},"cArray": [{"low" : 0,"up" : 0,"step" : 0}]}]}], "offset" : {"in":88}, "offset_end" : {"in":95}} , 
 	{ "Name" : "slv_reg10_out", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "bitSlice":[{"low":0,"up":0,"cElement": [{"cName": "slv_reg10_out","cData": "int","bit_use": { "low": 0,"up": 0},"cArray": [{"low" : 0,"up" : 0,"step" : 0}]}]}], "offset" : {"in":96}, "offset_end" : {"in":103}} , 
 	{ "Name" : "slv_reg11_out", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "bitSlice":[{"low":0,"up":0,"cElement": [{"cName": "slv_reg11_out","cData": "int","bit_use": { "low": 0,"up": 0},"cArray": [{"low" : 0,"up" : 0,"step" : 0}]}]}], "offset" : {"in":104}, "offset_end" : {"in":111}} , 
 	{ "Name" : "slv_reg12_out", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "bitSlice":[{"low":0,"up":0,"cElement": [{"cName": "slv_reg12_out","cData": "int","bit_use": { "low": 0,"up": 0},"cArray": [{"low" : 0,"up" : 0,"step" : 0}]}]}], "offset" : {"in":112}, "offset_end" : {"in":119}} , 
 	{ "Name" : "slv_reg13_out", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "bitSlice":[{"low":0,"up":0,"cElement": [{"cName": "slv_reg13_out","cData": "int","bit_use": { "low": 0,"up": 0},"cArray": [{"low" : 0,"up" : 0,"step" : 0}]}]}], "offset" : {"in":120}, "offset_end" : {"in":127}} , 
 	{ "Name" : "slv_reg14_out", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "bitSlice":[{"low":0,"up":0,"cElement": [{"cName": "slv_reg14_out","cData": "int","bit_use": { "low": 0,"up": 0},"cArray": [{"low" : 0,"up" : 0,"step" : 0}]}]}], "offset" : {"in":128}, "offset_end" : {"in":135}} , 
 	{ "Name" : "axi00_imem_ptr0", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 64, "direction" : "READONLY", "offset" : {"in":136}, "offset_end" : {"in":147}} , 
 	{ "Name" : "axi01_parambuf_ptr0", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 64, "direction" : "READONLY", "offset" : {"in":148}, "offset_end" : {"in":159}} , 
 	{ "Name" : "axi02_ibuf_ptr0", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 64, "direction" : "READONLY", "offset" : {"in":160}, "offset_end" : {"in":171}} , 
 	{ "Name" : "axi03_obuf_ptr0", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 64, "direction" : "READONLY", "offset" : {"in":172}, "offset_end" : {"in":183}} ]}
# RTL Port declarations: 
set portNum 200
set portList { 
	{ ap_clk sc_in sc_logic 1 clock -1 } 
	{ ap_rst_n sc_in sc_logic 1 reset -1 active_low_sync } 
	{ m_axi_m00_imem_axi_AWVALID sc_out sc_logic 1 signal 0 } 
	{ m_axi_m00_imem_axi_AWREADY sc_in sc_logic 1 signal 0 } 
	{ m_axi_m00_imem_axi_AWADDR sc_out sc_lv 64 signal 0 } 
	{ m_axi_m00_imem_axi_AWID sc_out sc_lv 1 signal 0 } 
	{ m_axi_m00_imem_axi_AWLEN sc_out sc_lv 8 signal 0 } 
	{ m_axi_m00_imem_axi_AWSIZE sc_out sc_lv 3 signal 0 } 
	{ m_axi_m00_imem_axi_AWBURST sc_out sc_lv 2 signal 0 } 
	{ m_axi_m00_imem_axi_AWLOCK sc_out sc_lv 2 signal 0 } 
	{ m_axi_m00_imem_axi_AWCACHE sc_out sc_lv 4 signal 0 } 
	{ m_axi_m00_imem_axi_AWPROT sc_out sc_lv 3 signal 0 } 
	{ m_axi_m00_imem_axi_AWQOS sc_out sc_lv 4 signal 0 } 
	{ m_axi_m00_imem_axi_AWREGION sc_out sc_lv 4 signal 0 } 
	{ m_axi_m00_imem_axi_AWUSER sc_out sc_lv 1 signal 0 } 
	{ m_axi_m00_imem_axi_WVALID sc_out sc_logic 1 signal 0 } 
	{ m_axi_m00_imem_axi_WREADY sc_in sc_logic 1 signal 0 } 
	{ m_axi_m00_imem_axi_WDATA sc_out sc_lv 512 signal 0 } 
	{ m_axi_m00_imem_axi_WSTRB sc_out sc_lv 64 signal 0 } 
	{ m_axi_m00_imem_axi_WLAST sc_out sc_logic 1 signal 0 } 
	{ m_axi_m00_imem_axi_WID sc_out sc_lv 1 signal 0 } 
	{ m_axi_m00_imem_axi_WUSER sc_out sc_lv 1 signal 0 } 
	{ m_axi_m00_imem_axi_ARVALID sc_out sc_logic 1 signal 0 } 
	{ m_axi_m00_imem_axi_ARREADY sc_in sc_logic 1 signal 0 } 
	{ m_axi_m00_imem_axi_ARADDR sc_out sc_lv 64 signal 0 } 
	{ m_axi_m00_imem_axi_ARID sc_out sc_lv 1 signal 0 } 
	{ m_axi_m00_imem_axi_ARLEN sc_out sc_lv 8 signal 0 } 
	{ m_axi_m00_imem_axi_ARSIZE sc_out sc_lv 3 signal 0 } 
	{ m_axi_m00_imem_axi_ARBURST sc_out sc_lv 2 signal 0 } 
	{ m_axi_m00_imem_axi_ARLOCK sc_out sc_lv 2 signal 0 } 
	{ m_axi_m00_imem_axi_ARCACHE sc_out sc_lv 4 signal 0 } 
	{ m_axi_m00_imem_axi_ARPROT sc_out sc_lv 3 signal 0 } 
	{ m_axi_m00_imem_axi_ARQOS sc_out sc_lv 4 signal 0 } 
	{ m_axi_m00_imem_axi_ARREGION sc_out sc_lv 4 signal 0 } 
	{ m_axi_m00_imem_axi_ARUSER sc_out sc_lv 1 signal 0 } 
	{ m_axi_m00_imem_axi_RVALID sc_in sc_logic 1 signal 0 } 
	{ m_axi_m00_imem_axi_RREADY sc_out sc_logic 1 signal 0 } 
	{ m_axi_m00_imem_axi_RDATA sc_in sc_lv 512 signal 0 } 
	{ m_axi_m00_imem_axi_RLAST sc_in sc_logic 1 signal 0 } 
	{ m_axi_m00_imem_axi_RID sc_in sc_lv 1 signal 0 } 
	{ m_axi_m00_imem_axi_RUSER sc_in sc_lv 1 signal 0 } 
	{ m_axi_m00_imem_axi_RRESP sc_in sc_lv 2 signal 0 } 
	{ m_axi_m00_imem_axi_BVALID sc_in sc_logic 1 signal 0 } 
	{ m_axi_m00_imem_axi_BREADY sc_out sc_logic 1 signal 0 } 
	{ m_axi_m00_imem_axi_BRESP sc_in sc_lv 2 signal 0 } 
	{ m_axi_m00_imem_axi_BID sc_in sc_lv 1 signal 0 } 
	{ m_axi_m00_imem_axi_BUSER sc_in sc_lv 1 signal 0 } 
	{ m_axi_m01_parambuf_axi_AWVALID sc_out sc_logic 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_AWREADY sc_in sc_logic 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_AWADDR sc_out sc_lv 64 signal 1 } 
	{ m_axi_m01_parambuf_axi_AWID sc_out sc_lv 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_AWLEN sc_out sc_lv 8 signal 1 } 
	{ m_axi_m01_parambuf_axi_AWSIZE sc_out sc_lv 3 signal 1 } 
	{ m_axi_m01_parambuf_axi_AWBURST sc_out sc_lv 2 signal 1 } 
	{ m_axi_m01_parambuf_axi_AWLOCK sc_out sc_lv 2 signal 1 } 
	{ m_axi_m01_parambuf_axi_AWCACHE sc_out sc_lv 4 signal 1 } 
	{ m_axi_m01_parambuf_axi_AWPROT sc_out sc_lv 3 signal 1 } 
	{ m_axi_m01_parambuf_axi_AWQOS sc_out sc_lv 4 signal 1 } 
	{ m_axi_m01_parambuf_axi_AWREGION sc_out sc_lv 4 signal 1 } 
	{ m_axi_m01_parambuf_axi_AWUSER sc_out sc_lv 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_WVALID sc_out sc_logic 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_WREADY sc_in sc_logic 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_WDATA sc_out sc_lv 512 signal 1 } 
	{ m_axi_m01_parambuf_axi_WSTRB sc_out sc_lv 64 signal 1 } 
	{ m_axi_m01_parambuf_axi_WLAST sc_out sc_logic 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_WID sc_out sc_lv 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_WUSER sc_out sc_lv 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_ARVALID sc_out sc_logic 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_ARREADY sc_in sc_logic 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_ARADDR sc_out sc_lv 64 signal 1 } 
	{ m_axi_m01_parambuf_axi_ARID sc_out sc_lv 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_ARLEN sc_out sc_lv 8 signal 1 } 
	{ m_axi_m01_parambuf_axi_ARSIZE sc_out sc_lv 3 signal 1 } 
	{ m_axi_m01_parambuf_axi_ARBURST sc_out sc_lv 2 signal 1 } 
	{ m_axi_m01_parambuf_axi_ARLOCK sc_out sc_lv 2 signal 1 } 
	{ m_axi_m01_parambuf_axi_ARCACHE sc_out sc_lv 4 signal 1 } 
	{ m_axi_m01_parambuf_axi_ARPROT sc_out sc_lv 3 signal 1 } 
	{ m_axi_m01_parambuf_axi_ARQOS sc_out sc_lv 4 signal 1 } 
	{ m_axi_m01_parambuf_axi_ARREGION sc_out sc_lv 4 signal 1 } 
	{ m_axi_m01_parambuf_axi_ARUSER sc_out sc_lv 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_RVALID sc_in sc_logic 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_RREADY sc_out sc_logic 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_RDATA sc_in sc_lv 512 signal 1 } 
	{ m_axi_m01_parambuf_axi_RLAST sc_in sc_logic 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_RID sc_in sc_lv 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_RUSER sc_in sc_lv 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_RRESP sc_in sc_lv 2 signal 1 } 
	{ m_axi_m01_parambuf_axi_BVALID sc_in sc_logic 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_BREADY sc_out sc_logic 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_BRESP sc_in sc_lv 2 signal 1 } 
	{ m_axi_m01_parambuf_axi_BID sc_in sc_lv 1 signal 1 } 
	{ m_axi_m01_parambuf_axi_BUSER sc_in sc_lv 1 signal 1 } 
	{ m_axi_m02_ibuf_axi_AWVALID sc_out sc_logic 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_AWREADY sc_in sc_logic 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_AWADDR sc_out sc_lv 64 signal 2 } 
	{ m_axi_m02_ibuf_axi_AWID sc_out sc_lv 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_AWLEN sc_out sc_lv 8 signal 2 } 
	{ m_axi_m02_ibuf_axi_AWSIZE sc_out sc_lv 3 signal 2 } 
	{ m_axi_m02_ibuf_axi_AWBURST sc_out sc_lv 2 signal 2 } 
	{ m_axi_m02_ibuf_axi_AWLOCK sc_out sc_lv 2 signal 2 } 
	{ m_axi_m02_ibuf_axi_AWCACHE sc_out sc_lv 4 signal 2 } 
	{ m_axi_m02_ibuf_axi_AWPROT sc_out sc_lv 3 signal 2 } 
	{ m_axi_m02_ibuf_axi_AWQOS sc_out sc_lv 4 signal 2 } 
	{ m_axi_m02_ibuf_axi_AWREGION sc_out sc_lv 4 signal 2 } 
	{ m_axi_m02_ibuf_axi_AWUSER sc_out sc_lv 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_WVALID sc_out sc_logic 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_WREADY sc_in sc_logic 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_WDATA sc_out sc_lv 512 signal 2 } 
	{ m_axi_m02_ibuf_axi_WSTRB sc_out sc_lv 64 signal 2 } 
	{ m_axi_m02_ibuf_axi_WLAST sc_out sc_logic 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_WID sc_out sc_lv 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_WUSER sc_out sc_lv 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_ARVALID sc_out sc_logic 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_ARREADY sc_in sc_logic 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_ARADDR sc_out sc_lv 64 signal 2 } 
	{ m_axi_m02_ibuf_axi_ARID sc_out sc_lv 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_ARLEN sc_out sc_lv 8 signal 2 } 
	{ m_axi_m02_ibuf_axi_ARSIZE sc_out sc_lv 3 signal 2 } 
	{ m_axi_m02_ibuf_axi_ARBURST sc_out sc_lv 2 signal 2 } 
	{ m_axi_m02_ibuf_axi_ARLOCK sc_out sc_lv 2 signal 2 } 
	{ m_axi_m02_ibuf_axi_ARCACHE sc_out sc_lv 4 signal 2 } 
	{ m_axi_m02_ibuf_axi_ARPROT sc_out sc_lv 3 signal 2 } 
	{ m_axi_m02_ibuf_axi_ARQOS sc_out sc_lv 4 signal 2 } 
	{ m_axi_m02_ibuf_axi_ARREGION sc_out sc_lv 4 signal 2 } 
	{ m_axi_m02_ibuf_axi_ARUSER sc_out sc_lv 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_RVALID sc_in sc_logic 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_RREADY sc_out sc_logic 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_RDATA sc_in sc_lv 512 signal 2 } 
	{ m_axi_m02_ibuf_axi_RLAST sc_in sc_logic 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_RID sc_in sc_lv 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_RUSER sc_in sc_lv 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_RRESP sc_in sc_lv 2 signal 2 } 
	{ m_axi_m02_ibuf_axi_BVALID sc_in sc_logic 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_BREADY sc_out sc_logic 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_BRESP sc_in sc_lv 2 signal 2 } 
	{ m_axi_m02_ibuf_axi_BID sc_in sc_lv 1 signal 2 } 
	{ m_axi_m02_ibuf_axi_BUSER sc_in sc_lv 1 signal 2 } 
	{ m_axi_m03_obuf_axi_AWVALID sc_out sc_logic 1 signal 3 } 
	{ m_axi_m03_obuf_axi_AWREADY sc_in sc_logic 1 signal 3 } 
	{ m_axi_m03_obuf_axi_AWADDR sc_out sc_lv 64 signal 3 } 
	{ m_axi_m03_obuf_axi_AWID sc_out sc_lv 1 signal 3 } 
	{ m_axi_m03_obuf_axi_AWLEN sc_out sc_lv 8 signal 3 } 
	{ m_axi_m03_obuf_axi_AWSIZE sc_out sc_lv 3 signal 3 } 
	{ m_axi_m03_obuf_axi_AWBURST sc_out sc_lv 2 signal 3 } 
	{ m_axi_m03_obuf_axi_AWLOCK sc_out sc_lv 2 signal 3 } 
	{ m_axi_m03_obuf_axi_AWCACHE sc_out sc_lv 4 signal 3 } 
	{ m_axi_m03_obuf_axi_AWPROT sc_out sc_lv 3 signal 3 } 
	{ m_axi_m03_obuf_axi_AWQOS sc_out sc_lv 4 signal 3 } 
	{ m_axi_m03_obuf_axi_AWREGION sc_out sc_lv 4 signal 3 } 
	{ m_axi_m03_obuf_axi_AWUSER sc_out sc_lv 1 signal 3 } 
	{ m_axi_m03_obuf_axi_WVALID sc_out sc_logic 1 signal 3 } 
	{ m_axi_m03_obuf_axi_WREADY sc_in sc_logic 1 signal 3 } 
	{ m_axi_m03_obuf_axi_WDATA sc_out sc_lv 512 signal 3 } 
	{ m_axi_m03_obuf_axi_WSTRB sc_out sc_lv 64 signal 3 } 
	{ m_axi_m03_obuf_axi_WLAST sc_out sc_logic 1 signal 3 } 
	{ m_axi_m03_obuf_axi_WID sc_out sc_lv 1 signal 3 } 
	{ m_axi_m03_obuf_axi_WUSER sc_out sc_lv 1 signal 3 } 
	{ m_axi_m03_obuf_axi_ARVALID sc_out sc_logic 1 signal 3 } 
	{ m_axi_m03_obuf_axi_ARREADY sc_in sc_logic 1 signal 3 } 
	{ m_axi_m03_obuf_axi_ARADDR sc_out sc_lv 64 signal 3 } 
	{ m_axi_m03_obuf_axi_ARID sc_out sc_lv 1 signal 3 } 
	{ m_axi_m03_obuf_axi_ARLEN sc_out sc_lv 8 signal 3 } 
	{ m_axi_m03_obuf_axi_ARSIZE sc_out sc_lv 3 signal 3 } 
	{ m_axi_m03_obuf_axi_ARBURST sc_out sc_lv 2 signal 3 } 
	{ m_axi_m03_obuf_axi_ARLOCK sc_out sc_lv 2 signal 3 } 
	{ m_axi_m03_obuf_axi_ARCACHE sc_out sc_lv 4 signal 3 } 
	{ m_axi_m03_obuf_axi_ARPROT sc_out sc_lv 3 signal 3 } 
	{ m_axi_m03_obuf_axi_ARQOS sc_out sc_lv 4 signal 3 } 
	{ m_axi_m03_obuf_axi_ARREGION sc_out sc_lv 4 signal 3 } 
	{ m_axi_m03_obuf_axi_ARUSER sc_out sc_lv 1 signal 3 } 
	{ m_axi_m03_obuf_axi_RVALID sc_in sc_logic 1 signal 3 } 
	{ m_axi_m03_obuf_axi_RREADY sc_out sc_logic 1 signal 3 } 
	{ m_axi_m03_obuf_axi_RDATA sc_in sc_lv 512 signal 3 } 
	{ m_axi_m03_obuf_axi_RLAST sc_in sc_logic 1 signal 3 } 
	{ m_axi_m03_obuf_axi_RID sc_in sc_lv 1 signal 3 } 
	{ m_axi_m03_obuf_axi_RUSER sc_in sc_lv 1 signal 3 } 
	{ m_axi_m03_obuf_axi_RRESP sc_in sc_lv 2 signal 3 } 
	{ m_axi_m03_obuf_axi_BVALID sc_in sc_logic 1 signal 3 } 
	{ m_axi_m03_obuf_axi_BREADY sc_out sc_logic 1 signal 3 } 
	{ m_axi_m03_obuf_axi_BRESP sc_in sc_lv 2 signal 3 } 
	{ m_axi_m03_obuf_axi_BID sc_in sc_lv 1 signal 3 } 
	{ m_axi_m03_obuf_axi_BUSER sc_in sc_lv 1 signal 3 } 
	{ s_axi_control_AWVALID sc_in sc_logic 1 signal -1 } 
	{ s_axi_control_AWREADY sc_out sc_logic 1 signal -1 } 
	{ s_axi_control_AWADDR sc_in sc_lv 8 signal -1 } 
	{ s_axi_control_WVALID sc_in sc_logic 1 signal -1 } 
	{ s_axi_control_WREADY sc_out sc_logic 1 signal -1 } 
	{ s_axi_control_WDATA sc_in sc_lv 32 signal -1 } 
	{ s_axi_control_WSTRB sc_in sc_lv 4 signal -1 } 
	{ s_axi_control_ARVALID sc_in sc_logic 1 signal -1 } 
	{ s_axi_control_ARREADY sc_out sc_logic 1 signal -1 } 
	{ s_axi_control_ARADDR sc_in sc_lv 8 signal -1 } 
	{ s_axi_control_RVALID sc_out sc_logic 1 signal -1 } 
	{ s_axi_control_RREADY sc_in sc_logic 1 signal -1 } 
	{ s_axi_control_RDATA sc_out sc_lv 32 signal -1 } 
	{ s_axi_control_RRESP sc_out sc_lv 2 signal -1 } 
	{ s_axi_control_BVALID sc_out sc_logic 1 signal -1 } 
	{ s_axi_control_BREADY sc_in sc_logic 1 signal -1 } 
	{ s_axi_control_BRESP sc_out sc_lv 2 signal -1 } 
	{ interrupt sc_out sc_logic 1 signal -1 } 
}
set NewPortList {[ 
	{ "name": "s_axi_control_AWADDR", "direction": "in", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "control", "role": "AWADDR" },"address":[{"name":"systolic_fpga","role":"start","value":"0","valid_bit":"0"},{"name":"systolic_fpga","role":"continue","value":"0","valid_bit":"4"},{"name":"systolic_fpga","role":"auto_start","value":"0","valid_bit":"7"},{"name":"slv_reg0_out","role":"data","value":"16"},{"name":"slv_reg1_out","role":"data","value":"24"},{"name":"slv_reg2_out","role":"data","value":"32"},{"name":"slv_reg3_out","role":"data","value":"40"},{"name":"slv_reg4_out","role":"data","value":"48"},{"name":"slv_reg5_out","role":"data","value":"56"},{"name":"slv_reg6_out","role":"data","value":"64"},{"name":"slv_reg7_out","role":"data","value":"72"},{"name":"slv_reg8_out","role":"data","value":"80"},{"name":"slv_reg9_out","role":"data","value":"88"},{"name":"slv_reg10_out","role":"data","value":"96"},{"name":"slv_reg11_out","role":"data","value":"104"},{"name":"slv_reg12_out","role":"data","value":"112"},{"name":"slv_reg13_out","role":"data","value":"120"},{"name":"slv_reg14_out","role":"data","value":"128"},{"name":"axi00_imem_ptr0","role":"data","value":"136"},{"name":"axi01_parambuf_ptr0","role":"data","value":"148"},{"name":"axi02_ibuf_ptr0","role":"data","value":"160"},{"name":"axi03_obuf_ptr0","role":"data","value":"172"}] },
	{ "name": "s_axi_control_AWVALID", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "AWVALID" } },
	{ "name": "s_axi_control_AWREADY", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "AWREADY" } },
	{ "name": "s_axi_control_WVALID", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "WVALID" } },
	{ "name": "s_axi_control_WREADY", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "WREADY" } },
	{ "name": "s_axi_control_WDATA", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "control", "role": "WDATA" } },
	{ "name": "s_axi_control_WSTRB", "direction": "in", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "control", "role": "WSTRB" } },
	{ "name": "s_axi_control_ARADDR", "direction": "in", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "control", "role": "ARADDR" },"address":[{"name":"systolic_fpga","role":"start","value":"0","valid_bit":"0"},{"name":"systolic_fpga","role":"done","value":"0","valid_bit":"1"},{"name":"systolic_fpga","role":"idle","value":"0","valid_bit":"2"},{"name":"systolic_fpga","role":"ready","value":"0","valid_bit":"3"},{"name":"systolic_fpga","role":"auto_start","value":"0","valid_bit":"7"}] },
	{ "name": "s_axi_control_ARVALID", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "ARVALID" } },
	{ "name": "s_axi_control_ARREADY", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "ARREADY" } },
	{ "name": "s_axi_control_RVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "RVALID" } },
	{ "name": "s_axi_control_RREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "RREADY" } },
	{ "name": "s_axi_control_RDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "control", "role": "RDATA" } },
	{ "name": "s_axi_control_RRESP", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "control", "role": "RRESP" } },
	{ "name": "s_axi_control_BVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "BVALID" } },
	{ "name": "s_axi_control_BREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "BREADY" } },
	{ "name": "s_axi_control_BRESP", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "control", "role": "BRESP" } },
	{ "name": "interrupt", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "interrupt" } }, 
 	{ "name": "ap_clk", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "clock", "bundle":{"name": "ap_clk", "role": "default" }} , 
 	{ "name": "ap_rst_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "reset", "bundle":{"name": "ap_rst_n", "role": "default" }} , 
 	{ "name": "m_axi_m00_imem_axi_AWVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "AWVALID" }} , 
 	{ "name": "m_axi_m00_imem_axi_AWREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "AWREADY" }} , 
 	{ "name": "m_axi_m00_imem_axi_AWADDR", "direction": "out", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "AWADDR" }} , 
 	{ "name": "m_axi_m00_imem_axi_AWID", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "AWID" }} , 
 	{ "name": "m_axi_m00_imem_axi_AWLEN", "direction": "out", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "AWLEN" }} , 
 	{ "name": "m_axi_m00_imem_axi_AWSIZE", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "AWSIZE" }} , 
 	{ "name": "m_axi_m00_imem_axi_AWBURST", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "AWBURST" }} , 
 	{ "name": "m_axi_m00_imem_axi_AWLOCK", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "AWLOCK" }} , 
 	{ "name": "m_axi_m00_imem_axi_AWCACHE", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "AWCACHE" }} , 
 	{ "name": "m_axi_m00_imem_axi_AWPROT", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "AWPROT" }} , 
 	{ "name": "m_axi_m00_imem_axi_AWQOS", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "AWQOS" }} , 
 	{ "name": "m_axi_m00_imem_axi_AWREGION", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "AWREGION" }} , 
 	{ "name": "m_axi_m00_imem_axi_AWUSER", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "AWUSER" }} , 
 	{ "name": "m_axi_m00_imem_axi_WVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "WVALID" }} , 
 	{ "name": "m_axi_m00_imem_axi_WREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "WREADY" }} , 
 	{ "name": "m_axi_m00_imem_axi_WDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":512, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "WDATA" }} , 
 	{ "name": "m_axi_m00_imem_axi_WSTRB", "direction": "out", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "WSTRB" }} , 
 	{ "name": "m_axi_m00_imem_axi_WLAST", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "WLAST" }} , 
 	{ "name": "m_axi_m00_imem_axi_WID", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "WID" }} , 
 	{ "name": "m_axi_m00_imem_axi_WUSER", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "WUSER" }} , 
 	{ "name": "m_axi_m00_imem_axi_ARVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "ARVALID" }} , 
 	{ "name": "m_axi_m00_imem_axi_ARREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "ARREADY" }} , 
 	{ "name": "m_axi_m00_imem_axi_ARADDR", "direction": "out", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "ARADDR" }} , 
 	{ "name": "m_axi_m00_imem_axi_ARID", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "ARID" }} , 
 	{ "name": "m_axi_m00_imem_axi_ARLEN", "direction": "out", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "ARLEN" }} , 
 	{ "name": "m_axi_m00_imem_axi_ARSIZE", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "ARSIZE" }} , 
 	{ "name": "m_axi_m00_imem_axi_ARBURST", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "ARBURST" }} , 
 	{ "name": "m_axi_m00_imem_axi_ARLOCK", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "ARLOCK" }} , 
 	{ "name": "m_axi_m00_imem_axi_ARCACHE", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "ARCACHE" }} , 
 	{ "name": "m_axi_m00_imem_axi_ARPROT", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "ARPROT" }} , 
 	{ "name": "m_axi_m00_imem_axi_ARQOS", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "ARQOS" }} , 
 	{ "name": "m_axi_m00_imem_axi_ARREGION", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "ARREGION" }} , 
 	{ "name": "m_axi_m00_imem_axi_ARUSER", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "ARUSER" }} , 
 	{ "name": "m_axi_m00_imem_axi_RVALID", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "RVALID" }} , 
 	{ "name": "m_axi_m00_imem_axi_RREADY", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "RREADY" }} , 
 	{ "name": "m_axi_m00_imem_axi_RDATA", "direction": "in", "datatype": "sc_lv", "bitwidth":512, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "RDATA" }} , 
 	{ "name": "m_axi_m00_imem_axi_RLAST", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "RLAST" }} , 
 	{ "name": "m_axi_m00_imem_axi_RID", "direction": "in", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "RID" }} , 
 	{ "name": "m_axi_m00_imem_axi_RUSER", "direction": "in", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "RUSER" }} , 
 	{ "name": "m_axi_m00_imem_axi_RRESP", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "RRESP" }} , 
 	{ "name": "m_axi_m00_imem_axi_BVALID", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "BVALID" }} , 
 	{ "name": "m_axi_m00_imem_axi_BREADY", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "BREADY" }} , 
 	{ "name": "m_axi_m00_imem_axi_BRESP", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "BRESP" }} , 
 	{ "name": "m_axi_m00_imem_axi_BID", "direction": "in", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "BID" }} , 
 	{ "name": "m_axi_m00_imem_axi_BUSER", "direction": "in", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m00_imem_axi", "role": "BUSER" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_AWVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "AWVALID" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_AWREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "AWREADY" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_AWADDR", "direction": "out", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "AWADDR" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_AWID", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "AWID" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_AWLEN", "direction": "out", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "AWLEN" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_AWSIZE", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "AWSIZE" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_AWBURST", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "AWBURST" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_AWLOCK", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "AWLOCK" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_AWCACHE", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "AWCACHE" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_AWPROT", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "AWPROT" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_AWQOS", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "AWQOS" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_AWREGION", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "AWREGION" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_AWUSER", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "AWUSER" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_WVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "WVALID" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_WREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "WREADY" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_WDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":512, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "WDATA" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_WSTRB", "direction": "out", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "WSTRB" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_WLAST", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "WLAST" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_WID", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "WID" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_WUSER", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "WUSER" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_ARVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "ARVALID" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_ARREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "ARREADY" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_ARADDR", "direction": "out", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "ARADDR" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_ARID", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "ARID" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_ARLEN", "direction": "out", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "ARLEN" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_ARSIZE", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "ARSIZE" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_ARBURST", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "ARBURST" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_ARLOCK", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "ARLOCK" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_ARCACHE", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "ARCACHE" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_ARPROT", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "ARPROT" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_ARQOS", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "ARQOS" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_ARREGION", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "ARREGION" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_ARUSER", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "ARUSER" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_RVALID", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "RVALID" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_RREADY", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "RREADY" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_RDATA", "direction": "in", "datatype": "sc_lv", "bitwidth":512, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "RDATA" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_RLAST", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "RLAST" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_RID", "direction": "in", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "RID" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_RUSER", "direction": "in", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "RUSER" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_RRESP", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "RRESP" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_BVALID", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "BVALID" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_BREADY", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "BREADY" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_BRESP", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "BRESP" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_BID", "direction": "in", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "BID" }} , 
 	{ "name": "m_axi_m01_parambuf_axi_BUSER", "direction": "in", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m01_parambuf_axi", "role": "BUSER" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_AWVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "AWVALID" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_AWREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "AWREADY" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_AWADDR", "direction": "out", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "AWADDR" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_AWID", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "AWID" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_AWLEN", "direction": "out", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "AWLEN" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_AWSIZE", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "AWSIZE" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_AWBURST", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "AWBURST" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_AWLOCK", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "AWLOCK" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_AWCACHE", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "AWCACHE" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_AWPROT", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "AWPROT" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_AWQOS", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "AWQOS" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_AWREGION", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "AWREGION" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_AWUSER", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "AWUSER" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_WVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "WVALID" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_WREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "WREADY" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_WDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":512, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "WDATA" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_WSTRB", "direction": "out", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "WSTRB" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_WLAST", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "WLAST" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_WID", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "WID" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_WUSER", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "WUSER" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_ARVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "ARVALID" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_ARREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "ARREADY" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_ARADDR", "direction": "out", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "ARADDR" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_ARID", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "ARID" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_ARLEN", "direction": "out", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "ARLEN" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_ARSIZE", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "ARSIZE" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_ARBURST", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "ARBURST" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_ARLOCK", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "ARLOCK" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_ARCACHE", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "ARCACHE" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_ARPROT", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "ARPROT" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_ARQOS", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "ARQOS" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_ARREGION", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "ARREGION" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_ARUSER", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "ARUSER" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_RVALID", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "RVALID" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_RREADY", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "RREADY" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_RDATA", "direction": "in", "datatype": "sc_lv", "bitwidth":512, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "RDATA" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_RLAST", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "RLAST" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_RID", "direction": "in", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "RID" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_RUSER", "direction": "in", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "RUSER" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_RRESP", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "RRESP" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_BVALID", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "BVALID" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_BREADY", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "BREADY" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_BRESP", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "BRESP" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_BID", "direction": "in", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "BID" }} , 
 	{ "name": "m_axi_m02_ibuf_axi_BUSER", "direction": "in", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m02_ibuf_axi", "role": "BUSER" }} , 
 	{ "name": "m_axi_m03_obuf_axi_AWVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "AWVALID" }} , 
 	{ "name": "m_axi_m03_obuf_axi_AWREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "AWREADY" }} , 
 	{ "name": "m_axi_m03_obuf_axi_AWADDR", "direction": "out", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "AWADDR" }} , 
 	{ "name": "m_axi_m03_obuf_axi_AWID", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "AWID" }} , 
 	{ "name": "m_axi_m03_obuf_axi_AWLEN", "direction": "out", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "AWLEN" }} , 
 	{ "name": "m_axi_m03_obuf_axi_AWSIZE", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "AWSIZE" }} , 
 	{ "name": "m_axi_m03_obuf_axi_AWBURST", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "AWBURST" }} , 
 	{ "name": "m_axi_m03_obuf_axi_AWLOCK", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "AWLOCK" }} , 
 	{ "name": "m_axi_m03_obuf_axi_AWCACHE", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "AWCACHE" }} , 
 	{ "name": "m_axi_m03_obuf_axi_AWPROT", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "AWPROT" }} , 
 	{ "name": "m_axi_m03_obuf_axi_AWQOS", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "AWQOS" }} , 
 	{ "name": "m_axi_m03_obuf_axi_AWREGION", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "AWREGION" }} , 
 	{ "name": "m_axi_m03_obuf_axi_AWUSER", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "AWUSER" }} , 
 	{ "name": "m_axi_m03_obuf_axi_WVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "WVALID" }} , 
 	{ "name": "m_axi_m03_obuf_axi_WREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "WREADY" }} , 
 	{ "name": "m_axi_m03_obuf_axi_WDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":512, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "WDATA" }} , 
 	{ "name": "m_axi_m03_obuf_axi_WSTRB", "direction": "out", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "WSTRB" }} , 
 	{ "name": "m_axi_m03_obuf_axi_WLAST", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "WLAST" }} , 
 	{ "name": "m_axi_m03_obuf_axi_WID", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "WID" }} , 
 	{ "name": "m_axi_m03_obuf_axi_WUSER", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "WUSER" }} , 
 	{ "name": "m_axi_m03_obuf_axi_ARVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "ARVALID" }} , 
 	{ "name": "m_axi_m03_obuf_axi_ARREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "ARREADY" }} , 
 	{ "name": "m_axi_m03_obuf_axi_ARADDR", "direction": "out", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "ARADDR" }} , 
 	{ "name": "m_axi_m03_obuf_axi_ARID", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "ARID" }} , 
 	{ "name": "m_axi_m03_obuf_axi_ARLEN", "direction": "out", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "ARLEN" }} , 
 	{ "name": "m_axi_m03_obuf_axi_ARSIZE", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "ARSIZE" }} , 
 	{ "name": "m_axi_m03_obuf_axi_ARBURST", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "ARBURST" }} , 
 	{ "name": "m_axi_m03_obuf_axi_ARLOCK", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "ARLOCK" }} , 
 	{ "name": "m_axi_m03_obuf_axi_ARCACHE", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "ARCACHE" }} , 
 	{ "name": "m_axi_m03_obuf_axi_ARPROT", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "ARPROT" }} , 
 	{ "name": "m_axi_m03_obuf_axi_ARQOS", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "ARQOS" }} , 
 	{ "name": "m_axi_m03_obuf_axi_ARREGION", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "ARREGION" }} , 
 	{ "name": "m_axi_m03_obuf_axi_ARUSER", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "ARUSER" }} , 
 	{ "name": "m_axi_m03_obuf_axi_RVALID", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "RVALID" }} , 
 	{ "name": "m_axi_m03_obuf_axi_RREADY", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "RREADY" }} , 
 	{ "name": "m_axi_m03_obuf_axi_RDATA", "direction": "in", "datatype": "sc_lv", "bitwidth":512, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "RDATA" }} , 
 	{ "name": "m_axi_m03_obuf_axi_RLAST", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "RLAST" }} , 
 	{ "name": "m_axi_m03_obuf_axi_RID", "direction": "in", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "RID" }} , 
 	{ "name": "m_axi_m03_obuf_axi_RUSER", "direction": "in", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "RUSER" }} , 
 	{ "name": "m_axi_m03_obuf_axi_RRESP", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "RRESP" }} , 
 	{ "name": "m_axi_m03_obuf_axi_BVALID", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "BVALID" }} , 
 	{ "name": "m_axi_m03_obuf_axi_BREADY", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "BREADY" }} , 
 	{ "name": "m_axi_m03_obuf_axi_BRESP", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "BRESP" }} , 
 	{ "name": "m_axi_m03_obuf_axi_BID", "direction": "in", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "BID" }} , 
 	{ "name": "m_axi_m03_obuf_axi_BUSER", "direction": "in", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "m03_obuf_axi", "role": "BUSER" }}  ]}

set RtlHierarchyInfo {[
	{"ID" : "0", "Level" : "0", "Path" : "`AUTOTB_DUT_INST", "Parent" : "", "Child" : ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"],
		"CDFG" : "systolic_fpga",
		"Protocol" : "ap_ctrl_hs",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "0", "ap_idle" : "1", "real_start" : "0",
		"Pipeline" : "None", "UnalignedPipeline" : "0", "RewindPipeline" : "0", "ProcessNetwork" : "0",
		"II" : "0",
		"VariableLatency" : "1", "ExactLatency" : "-1", "EstimateLatencyMin" : "49528", "EstimateLatencyMax" : "49528",
		"Combinational" : "0",
		"Datapath" : "0",
		"ClockEnable" : "0",
		"HasSubDataflow" : "0",
		"InDataflowNetwork" : "0",
		"HasNonBlockingOperation" : "0",
		"Port" : [
			{"Name" : "m00_imem_axi", "Type" : "MAXI", "Direction" : "IO",
				"BlockSignal" : [
					{"Name" : "m00_imem_axi_blk_n_AR", "Type" : "RtlSignal"},
					{"Name" : "m00_imem_axi_blk_n_R", "Type" : "RtlSignal"},
					{"Name" : "m00_imem_axi_blk_n_AW", "Type" : "RtlSignal"},
					{"Name" : "m00_imem_axi_blk_n_W", "Type" : "RtlSignal"},
					{"Name" : "m00_imem_axi_blk_n_B", "Type" : "RtlSignal"}]},
			{"Name" : "m01_parambuf_axi", "Type" : "MAXI", "Direction" : "IO",
				"BlockSignal" : [
					{"Name" : "m01_parambuf_axi_blk_n_AR", "Type" : "RtlSignal"},
					{"Name" : "m01_parambuf_axi_blk_n_R", "Type" : "RtlSignal"},
					{"Name" : "m01_parambuf_axi_blk_n_AW", "Type" : "RtlSignal"},
					{"Name" : "m01_parambuf_axi_blk_n_W", "Type" : "RtlSignal"},
					{"Name" : "m01_parambuf_axi_blk_n_B", "Type" : "RtlSignal"}]},
			{"Name" : "m02_ibuf_axi", "Type" : "MAXI", "Direction" : "IO",
				"BlockSignal" : [
					{"Name" : "m02_ibuf_axi_blk_n_AR", "Type" : "RtlSignal"},
					{"Name" : "m02_ibuf_axi_blk_n_R", "Type" : "RtlSignal"},
					{"Name" : "m02_ibuf_axi_blk_n_AW", "Type" : "RtlSignal"},
					{"Name" : "m02_ibuf_axi_blk_n_W", "Type" : "RtlSignal"},
					{"Name" : "m02_ibuf_axi_blk_n_B", "Type" : "RtlSignal"}]},
			{"Name" : "m03_obuf_axi", "Type" : "MAXI", "Direction" : "IO",
				"BlockSignal" : [
					{"Name" : "m03_obuf_axi_blk_n_AR", "Type" : "RtlSignal"},
					{"Name" : "m03_obuf_axi_blk_n_R", "Type" : "RtlSignal"},
					{"Name" : "m03_obuf_axi_blk_n_AW", "Type" : "RtlSignal"},
					{"Name" : "m03_obuf_axi_blk_n_W", "Type" : "RtlSignal"},
					{"Name" : "m03_obuf_axi_blk_n_B", "Type" : "RtlSignal"}]},
			{"Name" : "slv_reg0_out", "Type" : "None", "Direction" : "I"},
			{"Name" : "slv_reg1_out", "Type" : "None", "Direction" : "I"},
			{"Name" : "slv_reg2_out", "Type" : "None", "Direction" : "I"},
			{"Name" : "slv_reg3_out", "Type" : "None", "Direction" : "I"},
			{"Name" : "slv_reg4_out", "Type" : "None", "Direction" : "I"},
			{"Name" : "slv_reg5_out", "Type" : "None", "Direction" : "I"},
			{"Name" : "slv_reg6_out", "Type" : "None", "Direction" : "I"},
			{"Name" : "slv_reg7_out", "Type" : "None", "Direction" : "I"},
			{"Name" : "slv_reg8_out", "Type" : "None", "Direction" : "I"},
			{"Name" : "slv_reg9_out", "Type" : "None", "Direction" : "I"},
			{"Name" : "slv_reg10_out", "Type" : "None", "Direction" : "I"},
			{"Name" : "slv_reg11_out", "Type" : "None", "Direction" : "I"},
			{"Name" : "slv_reg12_out", "Type" : "None", "Direction" : "I"},
			{"Name" : "slv_reg13_out", "Type" : "None", "Direction" : "I"},
			{"Name" : "slv_reg14_out", "Type" : "None", "Direction" : "I"},
			{"Name" : "axi00_imem_ptr0", "Type" : "None", "Direction" : "I"},
			{"Name" : "axi01_parambuf_ptr0", "Type" : "None", "Direction" : "I"},
			{"Name" : "axi02_ibuf_ptr0", "Type" : "None", "Direction" : "I"},
			{"Name" : "axi03_obuf_ptr0", "Type" : "None", "Direction" : "I"}]},
	{"ID" : "1", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.control_s_axi_U", "Parent" : "0"},
	{"ID" : "2", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.m00_imem_axi_m_axi_U", "Parent" : "0"},
	{"ID" : "3", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.m01_parambuf_axi_m_axi_U", "Parent" : "0"},
	{"ID" : "4", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.m02_ibuf_axi_m_axi_U", "Parent" : "0"},
	{"ID" : "5", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.m03_obuf_axi_m_axi_U", "Parent" : "0"},
	{"ID" : "6", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.m00_imem_axi_input_buffer_U", "Parent" : "0"},
	{"ID" : "7", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.m00_imem_axi_output_buffer_U", "Parent" : "0"},
	{"ID" : "8", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.m01_parambuf_axi_input_buffer_U", "Parent" : "0"},
	{"ID" : "9", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.m01_parambuf_axi_output_buffer_U", "Parent" : "0"},
	{"ID" : "10", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.m02_ibuf_axi_input_buffer_U", "Parent" : "0"},
	{"ID" : "11", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.m02_ibuf_axi_output_buffer_U", "Parent" : "0"},
	{"ID" : "12", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.m03_obuf_axi_input_buffer_U", "Parent" : "0"},
	{"ID" : "13", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.m03_obuf_axi_output_buffer_U", "Parent" : "0"}]}


set ArgLastReadFirstWriteLatency {
	systolic_fpga {
		m00_imem_axi {Type IO LastRead 76 FirstWrite 77}
		m01_parambuf_axi {Type IO LastRead 151 FirstWrite 152}
		m02_ibuf_axi {Type IO LastRead 226 FirstWrite 227}
		m03_obuf_axi {Type IO LastRead 301 FirstWrite 302}
		slv_reg0_out {Type I LastRead -1 FirstWrite -1}
		slv_reg1_out {Type I LastRead -1 FirstWrite -1}
		slv_reg2_out {Type I LastRead -1 FirstWrite -1}
		slv_reg3_out {Type I LastRead -1 FirstWrite -1}
		slv_reg4_out {Type I LastRead -1 FirstWrite -1}
		slv_reg5_out {Type I LastRead -1 FirstWrite -1}
		slv_reg6_out {Type I LastRead -1 FirstWrite -1}
		slv_reg7_out {Type I LastRead -1 FirstWrite -1}
		slv_reg8_out {Type I LastRead -1 FirstWrite -1}
		slv_reg9_out {Type I LastRead -1 FirstWrite -1}
		slv_reg10_out {Type I LastRead -1 FirstWrite -1}
		slv_reg11_out {Type I LastRead -1 FirstWrite -1}
		slv_reg12_out {Type I LastRead -1 FirstWrite -1}
		slv_reg13_out {Type I LastRead -1 FirstWrite -1}
		slv_reg14_out {Type I LastRead -1 FirstWrite -1}
		axi00_imem_ptr0 {Type I LastRead 0 FirstWrite -1}
		axi01_parambuf_ptr0 {Type I LastRead 0 FirstWrite -1}
		axi02_ibuf_ptr0 {Type I LastRead 0 FirstWrite -1}
		axi03_obuf_ptr0 {Type I LastRead 0 FirstWrite -1}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "49528", "Max" : "49528"}
	, {"Name" : "Interval", "Min" : "49529", "Max" : "49529"}
]}

set PipelineEnableSignalInfo {[
	{"Pipeline" : "0", "EnableSignal" : "ap_enable_pp0"}
	{"Pipeline" : "1", "EnableSignal" : "ap_enable_pp1"}
	{"Pipeline" : "2", "EnableSignal" : "ap_enable_pp2"}
	{"Pipeline" : "3", "EnableSignal" : "ap_enable_pp3"}
	{"Pipeline" : "4", "EnableSignal" : "ap_enable_pp4"}
	{"Pipeline" : "5", "EnableSignal" : "ap_enable_pp5"}
	{"Pipeline" : "6", "EnableSignal" : "ap_enable_pp6"}
	{"Pipeline" : "7", "EnableSignal" : "ap_enable_pp7"}
	{"Pipeline" : "8", "EnableSignal" : "ap_enable_pp8"}
	{"Pipeline" : "9", "EnableSignal" : "ap_enable_pp9"}
	{"Pipeline" : "10", "EnableSignal" : "ap_enable_pp10"}
	{"Pipeline" : "11", "EnableSignal" : "ap_enable_pp11"}
]}

set Spec2ImplPortList { 
	m00_imem_axi { m_axi {  { m_axi_m00_imem_axi_AWVALID VALID 1 1 }  { m_axi_m00_imem_axi_AWREADY READY 0 1 }  { m_axi_m00_imem_axi_AWADDR ADDR 1 64 }  { m_axi_m00_imem_axi_AWID ID 1 1 }  { m_axi_m00_imem_axi_AWLEN LEN 1 8 }  { m_axi_m00_imem_axi_AWSIZE SIZE 1 3 }  { m_axi_m00_imem_axi_AWBURST BURST 1 2 }  { m_axi_m00_imem_axi_AWLOCK LOCK 1 2 }  { m_axi_m00_imem_axi_AWCACHE CACHE 1 4 }  { m_axi_m00_imem_axi_AWPROT PROT 1 3 }  { m_axi_m00_imem_axi_AWQOS QOS 1 4 }  { m_axi_m00_imem_axi_AWREGION REGION 1 4 }  { m_axi_m00_imem_axi_AWUSER USER 1 1 }  { m_axi_m00_imem_axi_WVALID VALID 1 1 }  { m_axi_m00_imem_axi_WREADY READY 0 1 }  { m_axi_m00_imem_axi_WDATA DATA 1 512 }  { m_axi_m00_imem_axi_WSTRB STRB 1 64 }  { m_axi_m00_imem_axi_WLAST LAST 1 1 }  { m_axi_m00_imem_axi_WID ID 1 1 }  { m_axi_m00_imem_axi_WUSER USER 1 1 }  { m_axi_m00_imem_axi_ARVALID VALID 1 1 }  { m_axi_m00_imem_axi_ARREADY READY 0 1 }  { m_axi_m00_imem_axi_ARADDR ADDR 1 64 }  { m_axi_m00_imem_axi_ARID ID 1 1 }  { m_axi_m00_imem_axi_ARLEN LEN 1 8 }  { m_axi_m00_imem_axi_ARSIZE SIZE 1 3 }  { m_axi_m00_imem_axi_ARBURST BURST 1 2 }  { m_axi_m00_imem_axi_ARLOCK LOCK 1 2 }  { m_axi_m00_imem_axi_ARCACHE CACHE 1 4 }  { m_axi_m00_imem_axi_ARPROT PROT 1 3 }  { m_axi_m00_imem_axi_ARQOS QOS 1 4 }  { m_axi_m00_imem_axi_ARREGION REGION 1 4 }  { m_axi_m00_imem_axi_ARUSER USER 1 1 }  { m_axi_m00_imem_axi_RVALID VALID 0 1 }  { m_axi_m00_imem_axi_RREADY READY 1 1 }  { m_axi_m00_imem_axi_RDATA DATA 0 512 }  { m_axi_m00_imem_axi_RLAST LAST 0 1 }  { m_axi_m00_imem_axi_RID ID 0 1 }  { m_axi_m00_imem_axi_RUSER USER 0 1 }  { m_axi_m00_imem_axi_RRESP RESP 0 2 }  { m_axi_m00_imem_axi_BVALID VALID 0 1 }  { m_axi_m00_imem_axi_BREADY READY 1 1 }  { m_axi_m00_imem_axi_BRESP RESP 0 2 }  { m_axi_m00_imem_axi_BID ID 0 1 }  { m_axi_m00_imem_axi_BUSER USER 0 1 } } }
	m01_parambuf_axi { m_axi {  { m_axi_m01_parambuf_axi_AWVALID VALID 1 1 }  { m_axi_m01_parambuf_axi_AWREADY READY 0 1 }  { m_axi_m01_parambuf_axi_AWADDR ADDR 1 64 }  { m_axi_m01_parambuf_axi_AWID ID 1 1 }  { m_axi_m01_parambuf_axi_AWLEN LEN 1 8 }  { m_axi_m01_parambuf_axi_AWSIZE SIZE 1 3 }  { m_axi_m01_parambuf_axi_AWBURST BURST 1 2 }  { m_axi_m01_parambuf_axi_AWLOCK LOCK 1 2 }  { m_axi_m01_parambuf_axi_AWCACHE CACHE 1 4 }  { m_axi_m01_parambuf_axi_AWPROT PROT 1 3 }  { m_axi_m01_parambuf_axi_AWQOS QOS 1 4 }  { m_axi_m01_parambuf_axi_AWREGION REGION 1 4 }  { m_axi_m01_parambuf_axi_AWUSER USER 1 1 }  { m_axi_m01_parambuf_axi_WVALID VALID 1 1 }  { m_axi_m01_parambuf_axi_WREADY READY 0 1 }  { m_axi_m01_parambuf_axi_WDATA DATA 1 512 }  { m_axi_m01_parambuf_axi_WSTRB STRB 1 64 }  { m_axi_m01_parambuf_axi_WLAST LAST 1 1 }  { m_axi_m01_parambuf_axi_WID ID 1 1 }  { m_axi_m01_parambuf_axi_WUSER USER 1 1 }  { m_axi_m01_parambuf_axi_ARVALID VALID 1 1 }  { m_axi_m01_parambuf_axi_ARREADY READY 0 1 }  { m_axi_m01_parambuf_axi_ARADDR ADDR 1 64 }  { m_axi_m01_parambuf_axi_ARID ID 1 1 }  { m_axi_m01_parambuf_axi_ARLEN LEN 1 8 }  { m_axi_m01_parambuf_axi_ARSIZE SIZE 1 3 }  { m_axi_m01_parambuf_axi_ARBURST BURST 1 2 }  { m_axi_m01_parambuf_axi_ARLOCK LOCK 1 2 }  { m_axi_m01_parambuf_axi_ARCACHE CACHE 1 4 }  { m_axi_m01_parambuf_axi_ARPROT PROT 1 3 }  { m_axi_m01_parambuf_axi_ARQOS QOS 1 4 }  { m_axi_m01_parambuf_axi_ARREGION REGION 1 4 }  { m_axi_m01_parambuf_axi_ARUSER USER 1 1 }  { m_axi_m01_parambuf_axi_RVALID VALID 0 1 }  { m_axi_m01_parambuf_axi_RREADY READY 1 1 }  { m_axi_m01_parambuf_axi_RDATA DATA 0 512 }  { m_axi_m01_parambuf_axi_RLAST LAST 0 1 }  { m_axi_m01_parambuf_axi_RID ID 0 1 }  { m_axi_m01_parambuf_axi_RUSER USER 0 1 }  { m_axi_m01_parambuf_axi_RRESP RESP 0 2 }  { m_axi_m01_parambuf_axi_BVALID VALID 0 1 }  { m_axi_m01_parambuf_axi_BREADY READY 1 1 }  { m_axi_m01_parambuf_axi_BRESP RESP 0 2 }  { m_axi_m01_parambuf_axi_BID ID 0 1 }  { m_axi_m01_parambuf_axi_BUSER USER 0 1 } } }
	m02_ibuf_axi { m_axi {  { m_axi_m02_ibuf_axi_AWVALID VALID 1 1 }  { m_axi_m02_ibuf_axi_AWREADY READY 0 1 }  { m_axi_m02_ibuf_axi_AWADDR ADDR 1 64 }  { m_axi_m02_ibuf_axi_AWID ID 1 1 }  { m_axi_m02_ibuf_axi_AWLEN LEN 1 8 }  { m_axi_m02_ibuf_axi_AWSIZE SIZE 1 3 }  { m_axi_m02_ibuf_axi_AWBURST BURST 1 2 }  { m_axi_m02_ibuf_axi_AWLOCK LOCK 1 2 }  { m_axi_m02_ibuf_axi_AWCACHE CACHE 1 4 }  { m_axi_m02_ibuf_axi_AWPROT PROT 1 3 }  { m_axi_m02_ibuf_axi_AWQOS QOS 1 4 }  { m_axi_m02_ibuf_axi_AWREGION REGION 1 4 }  { m_axi_m02_ibuf_axi_AWUSER USER 1 1 }  { m_axi_m02_ibuf_axi_WVALID VALID 1 1 }  { m_axi_m02_ibuf_axi_WREADY READY 0 1 }  { m_axi_m02_ibuf_axi_WDATA DATA 1 512 }  { m_axi_m02_ibuf_axi_WSTRB STRB 1 64 }  { m_axi_m02_ibuf_axi_WLAST LAST 1 1 }  { m_axi_m02_ibuf_axi_WID ID 1 1 }  { m_axi_m02_ibuf_axi_WUSER USER 1 1 }  { m_axi_m02_ibuf_axi_ARVALID VALID 1 1 }  { m_axi_m02_ibuf_axi_ARREADY READY 0 1 }  { m_axi_m02_ibuf_axi_ARADDR ADDR 1 64 }  { m_axi_m02_ibuf_axi_ARID ID 1 1 }  { m_axi_m02_ibuf_axi_ARLEN LEN 1 8 }  { m_axi_m02_ibuf_axi_ARSIZE SIZE 1 3 }  { m_axi_m02_ibuf_axi_ARBURST BURST 1 2 }  { m_axi_m02_ibuf_axi_ARLOCK LOCK 1 2 }  { m_axi_m02_ibuf_axi_ARCACHE CACHE 1 4 }  { m_axi_m02_ibuf_axi_ARPROT PROT 1 3 }  { m_axi_m02_ibuf_axi_ARQOS QOS 1 4 }  { m_axi_m02_ibuf_axi_ARREGION REGION 1 4 }  { m_axi_m02_ibuf_axi_ARUSER USER 1 1 }  { m_axi_m02_ibuf_axi_RVALID VALID 0 1 }  { m_axi_m02_ibuf_axi_RREADY READY 1 1 }  { m_axi_m02_ibuf_axi_RDATA DATA 0 512 }  { m_axi_m02_ibuf_axi_RLAST LAST 0 1 }  { m_axi_m02_ibuf_axi_RID ID 0 1 }  { m_axi_m02_ibuf_axi_RUSER USER 0 1 }  { m_axi_m02_ibuf_axi_RRESP RESP 0 2 }  { m_axi_m02_ibuf_axi_BVALID VALID 0 1 }  { m_axi_m02_ibuf_axi_BREADY READY 1 1 }  { m_axi_m02_ibuf_axi_BRESP RESP 0 2 }  { m_axi_m02_ibuf_axi_BID ID 0 1 }  { m_axi_m02_ibuf_axi_BUSER USER 0 1 } } }
	m03_obuf_axi { m_axi {  { m_axi_m03_obuf_axi_AWVALID VALID 1 1 }  { m_axi_m03_obuf_axi_AWREADY READY 0 1 }  { m_axi_m03_obuf_axi_AWADDR ADDR 1 64 }  { m_axi_m03_obuf_axi_AWID ID 1 1 }  { m_axi_m03_obuf_axi_AWLEN LEN 1 8 }  { m_axi_m03_obuf_axi_AWSIZE SIZE 1 3 }  { m_axi_m03_obuf_axi_AWBURST BURST 1 2 }  { m_axi_m03_obuf_axi_AWLOCK LOCK 1 2 }  { m_axi_m03_obuf_axi_AWCACHE CACHE 1 4 }  { m_axi_m03_obuf_axi_AWPROT PROT 1 3 }  { m_axi_m03_obuf_axi_AWQOS QOS 1 4 }  { m_axi_m03_obuf_axi_AWREGION REGION 1 4 }  { m_axi_m03_obuf_axi_AWUSER USER 1 1 }  { m_axi_m03_obuf_axi_WVALID VALID 1 1 }  { m_axi_m03_obuf_axi_WREADY READY 0 1 }  { m_axi_m03_obuf_axi_WDATA DATA 1 512 }  { m_axi_m03_obuf_axi_WSTRB STRB 1 64 }  { m_axi_m03_obuf_axi_WLAST LAST 1 1 }  { m_axi_m03_obuf_axi_WID ID 1 1 }  { m_axi_m03_obuf_axi_WUSER USER 1 1 }  { m_axi_m03_obuf_axi_ARVALID VALID 1 1 }  { m_axi_m03_obuf_axi_ARREADY READY 0 1 }  { m_axi_m03_obuf_axi_ARADDR ADDR 1 64 }  { m_axi_m03_obuf_axi_ARID ID 1 1 }  { m_axi_m03_obuf_axi_ARLEN LEN 1 8 }  { m_axi_m03_obuf_axi_ARSIZE SIZE 1 3 }  { m_axi_m03_obuf_axi_ARBURST BURST 1 2 }  { m_axi_m03_obuf_axi_ARLOCK LOCK 1 2 }  { m_axi_m03_obuf_axi_ARCACHE CACHE 1 4 }  { m_axi_m03_obuf_axi_ARPROT PROT 1 3 }  { m_axi_m03_obuf_axi_ARQOS QOS 1 4 }  { m_axi_m03_obuf_axi_ARREGION REGION 1 4 }  { m_axi_m03_obuf_axi_ARUSER USER 1 1 }  { m_axi_m03_obuf_axi_RVALID VALID 0 1 }  { m_axi_m03_obuf_axi_RREADY READY 1 1 }  { m_axi_m03_obuf_axi_RDATA DATA 0 512 }  { m_axi_m03_obuf_axi_RLAST LAST 0 1 }  { m_axi_m03_obuf_axi_RID ID 0 1 }  { m_axi_m03_obuf_axi_RUSER USER 0 1 }  { m_axi_m03_obuf_axi_RRESP RESP 0 2 }  { m_axi_m03_obuf_axi_BVALID VALID 0 1 }  { m_axi_m03_obuf_axi_BREADY READY 1 1 }  { m_axi_m03_obuf_axi_BRESP RESP 0 2 }  { m_axi_m03_obuf_axi_BID ID 0 1 }  { m_axi_m03_obuf_axi_BUSER USER 0 1 } } }
}

set busDeadlockParameterList { 
	{ m00_imem_axi { NUM_READ_OUTSTANDING 16 NUM_WRITE_OUTSTANDING 16 MAX_READ_BURST_LENGTH 16 MAX_WRITE_BURST_LENGTH 16 } } \
	{ m01_parambuf_axi { NUM_READ_OUTSTANDING 16 NUM_WRITE_OUTSTANDING 16 MAX_READ_BURST_LENGTH 16 MAX_WRITE_BURST_LENGTH 16 } } \
	{ m02_ibuf_axi { NUM_READ_OUTSTANDING 16 NUM_WRITE_OUTSTANDING 16 MAX_READ_BURST_LENGTH 16 MAX_WRITE_BURST_LENGTH 16 } } \
	{ m03_obuf_axi { NUM_READ_OUTSTANDING 16 NUM_WRITE_OUTSTANDING 16 MAX_READ_BURST_LENGTH 16 MAX_WRITE_BURST_LENGTH 16 } } \
}

# RTL port scheduling information:
set fifoSchedulingInfoList { 
}

# RTL bus port read request latency information:
set busReadReqLatencyList { 
	{ m00_imem_axi 64 }
	{ m01_parambuf_axi 64 }
	{ m02_ibuf_axi 64 }
	{ m03_obuf_axi 64 }
}

# RTL bus port write response latency information:
set busWriteResLatencyList { 
	{ m00_imem_axi 64 }
	{ m01_parambuf_axi 64 }
	{ m02_ibuf_axi 64 }
	{ m03_obuf_axi 64 }
}

# RTL array port load latency information:
set memoryLoadLatencyList { 
}
