// This is a generated file. Use and modify at your own risk.
//////////////////////////////////////////////////////////////////////////////// 
// default_nettype of none prevents implicit wire declaration.
`default_nettype none
`timescale 1 ns / 1 ps
// Top level of the kernel. Do not modify module name, parameters or ports.
module systolic_fpga #(
  parameter integer C_S_AXI_CONTROL_ADDR_WIDTH    = 12 ,
  parameter integer C_S_AXI_CONTROL_DATA_WIDTH    = 32 ,
  parameter integer C_M00_IMEM_AXI_ADDR_WIDTH     = 64 ,
  parameter integer C_M00_IMEM_AXI_DATA_WIDTH     = 512,
  parameter integer C_M01_PARAMBUF_AXI_ADDR_WIDTH = 64 ,
  parameter integer C_M01_PARAMBUF_AXI_DATA_WIDTH = 512,
  parameter integer C_M02_IBUF_AXI_ADDR_WIDTH     = 64 ,
  parameter integer C_M02_IBUF_AXI_DATA_WIDTH     = 512,
  parameter integer C_M03_OBUF_AXI_ADDR_WIDTH     = 64 ,
  parameter integer C_M03_OBUF_AXI_DATA_WIDTH     = 512
)
(
  // System Signals
  input  wire                                       ap_clk                  ,
  input  wire                                       ap_rst_n                ,
  //  Note: A minimum subset of AXI4 memory mapped signals are declared.  AXI
  // signals omitted from these interfaces are automatically inferred with the
  // optimal values for Xilinx accleration platforms.  This allows Xilinx AXI4 Interconnects
  // within the system to be optimized by removing logic for AXI4 protocol
  // features that are not necessary. When adapting AXI4 masters within the RTL
  // kernel that have signals not declared below, it is suitable to add the
  // signals to the declarations below to connect them to the AXI4 Master.
  // 
  // List of ommited signals - effect
  // -------------------------------
  // ID - Transaction ID are used for multithreading and out of order
  // transactions.  This increases complexity. This saves logic and increases Fmax
  // in the system when ommited.
  // SIZE - Default value is log2(data width in bytes). Needed for subsize bursts.
  // This saves logic and increases Fmax in the system when ommited.
  // BURST - Default value (0b01) is incremental.  Wrap and fixed bursts are not
  // recommended. This saves logic and increases Fmax in the system when ommited.
  // LOCK - Not supported in AXI4
  // CACHE - Default value (0b0011) allows modifiable transactions. No benefit to
  // changing this.
  // PROT - Has no effect in current acceleration platforms.
  // QOS - Has no effect in current acceleration platforms.
  // REGION - Has no effect in current acceleration platforms.
  // USER - Has no effect in current acceleration platforms.
  // RESP - Not useful in most acceleration platforms.
  // 
  // AXI4 master interface m00_imem_axi
  output wire                                       m00_imem_axi_awvalid    ,
  input  wire                                       m00_imem_axi_awready    ,
  output wire [C_M00_IMEM_AXI_ADDR_WIDTH-1:0]       m00_imem_axi_awaddr     ,
  output wire [8-1:0]                               m00_imem_axi_awlen      ,
  output wire                                       m00_imem_axi_wvalid     ,
  input  wire                                       m00_imem_axi_wready     ,
  output wire [C_M00_IMEM_AXI_DATA_WIDTH-1:0]       m00_imem_axi_wdata      ,
  output wire [C_M00_IMEM_AXI_DATA_WIDTH/8-1:0]     m00_imem_axi_wstrb      ,
  output wire                                       m00_imem_axi_wlast      ,
  input  wire                                       m00_imem_axi_bvalid     ,
  output wire                                       m00_imem_axi_bready     ,
  output wire                                       m00_imem_axi_arvalid    ,
  input  wire                                       m00_imem_axi_arready    ,
  output wire [C_M00_IMEM_AXI_ADDR_WIDTH-1:0]       m00_imem_axi_araddr     ,
  output wire [8-1:0]                               m00_imem_axi_arlen      ,
  input  wire                                       m00_imem_axi_rvalid     ,
  output wire                                       m00_imem_axi_rready     ,
  input  wire [C_M00_IMEM_AXI_DATA_WIDTH-1:0]       m00_imem_axi_rdata      ,
  input  wire                                       m00_imem_axi_rlast      ,
  // AXI4 master interface m01_parambuf_axi
  output wire                                       m01_parambuf_axi_awvalid,
  input  wire                                       m01_parambuf_axi_awready,
  output wire [C_M01_PARAMBUF_AXI_ADDR_WIDTH-1:0]   m01_parambuf_axi_awaddr ,
  output wire [8-1:0]                               m01_parambuf_axi_awlen  ,
  output wire                                       m01_parambuf_axi_wvalid ,
  input  wire                                       m01_parambuf_axi_wready ,
  output wire [C_M01_PARAMBUF_AXI_DATA_WIDTH-1:0]   m01_parambuf_axi_wdata  ,
  output wire [C_M01_PARAMBUF_AXI_DATA_WIDTH/8-1:0] m01_parambuf_axi_wstrb  ,
  output wire                                       m01_parambuf_axi_wlast  ,
  input  wire                                       m01_parambuf_axi_bvalid ,
  output wire                                       m01_parambuf_axi_bready ,
  output wire                                       m01_parambuf_axi_arvalid,
  input  wire                                       m01_parambuf_axi_arready,
  output wire [C_M01_PARAMBUF_AXI_ADDR_WIDTH-1:0]   m01_parambuf_axi_araddr ,
  output wire [8-1:0]                               m01_parambuf_axi_arlen  ,
  input  wire                                       m01_parambuf_axi_rvalid ,
  output wire                                       m01_parambuf_axi_rready ,
  input  wire [C_M01_PARAMBUF_AXI_DATA_WIDTH-1:0]   m01_parambuf_axi_rdata  ,
  input  wire                                       m01_parambuf_axi_rlast  ,
  // AXI4 master interface m02_ibuf_axi
  output wire                                       m02_ibuf_axi_awvalid    ,
  input  wire                                       m02_ibuf_axi_awready    ,
  output wire [C_M02_IBUF_AXI_ADDR_WIDTH-1:0]       m02_ibuf_axi_awaddr     ,
  output wire [8-1:0]                               m02_ibuf_axi_awlen      ,
  output wire                                       m02_ibuf_axi_wvalid     ,
  input  wire                                       m02_ibuf_axi_wready     ,
  output wire [C_M02_IBUF_AXI_DATA_WIDTH-1:0]       m02_ibuf_axi_wdata      ,
  output wire [C_M02_IBUF_AXI_DATA_WIDTH/8-1:0]     m02_ibuf_axi_wstrb      ,
  output wire                                       m02_ibuf_axi_wlast      ,
  input  wire                                       m02_ibuf_axi_bvalid     ,
  output wire                                       m02_ibuf_axi_bready     ,
  output wire                                       m02_ibuf_axi_arvalid    ,
  input  wire                                       m02_ibuf_axi_arready    ,
  output wire [C_M02_IBUF_AXI_ADDR_WIDTH-1:0]       m02_ibuf_axi_araddr     ,
  output wire [8-1:0]                               m02_ibuf_axi_arlen      ,
  input  wire                                       m02_ibuf_axi_rvalid     ,
  output wire                                       m02_ibuf_axi_rready     ,
  input  wire [C_M02_IBUF_AXI_DATA_WIDTH-1:0]       m02_ibuf_axi_rdata      ,
  input  wire                                       m02_ibuf_axi_rlast      ,
  // AXI4 master interface m03_obuf_axi
  output wire                                       m03_obuf_axi_awvalid    ,
  input  wire                                       m03_obuf_axi_awready    ,
  output wire [C_M03_OBUF_AXI_ADDR_WIDTH-1:0]       m03_obuf_axi_awaddr     ,
  output wire [8-1:0]                               m03_obuf_axi_awlen      ,
  output wire                                       m03_obuf_axi_wvalid     ,
  input  wire                                       m03_obuf_axi_wready     ,
  output wire [C_M03_OBUF_AXI_DATA_WIDTH-1:0]       m03_obuf_axi_wdata      ,
  output wire [C_M03_OBUF_AXI_DATA_WIDTH/8-1:0]     m03_obuf_axi_wstrb      ,
  output wire                                       m03_obuf_axi_wlast      ,
  input  wire                                       m03_obuf_axi_bvalid     ,
  output wire                                       m03_obuf_axi_bready     ,
  output wire                                       m03_obuf_axi_arvalid    ,
  input  wire                                       m03_obuf_axi_arready    ,
  output wire [C_M03_OBUF_AXI_ADDR_WIDTH-1:0]       m03_obuf_axi_araddr     ,
  output wire [8-1:0]                               m03_obuf_axi_arlen      ,
  input  wire                                       m03_obuf_axi_rvalid     ,
  output wire                                       m03_obuf_axi_rready     ,
  input  wire [C_M03_OBUF_AXI_DATA_WIDTH-1:0]       m03_obuf_axi_rdata      ,
  input  wire                                       m03_obuf_axi_rlast      ,
  // AXI4-Lite slave interface
  input  wire                                       s_axi_control_awvalid   ,
  output wire                                       s_axi_control_awready   ,
  input  wire [C_S_AXI_CONTROL_ADDR_WIDTH-1:0]      s_axi_control_awaddr    ,
  input  wire                                       s_axi_control_wvalid    ,
  output wire                                       s_axi_control_wready    ,
  input  wire [C_S_AXI_CONTROL_DATA_WIDTH-1:0]      s_axi_control_wdata     ,
  input  wire [C_S_AXI_CONTROL_DATA_WIDTH/8-1:0]    s_axi_control_wstrb     ,
  input  wire                                       s_axi_control_arvalid   ,
  output wire                                       s_axi_control_arready   ,
  input  wire [C_S_AXI_CONTROL_ADDR_WIDTH-1:0]      s_axi_control_araddr    ,
  output wire                                       s_axi_control_rvalid    ,
  input  wire                                       s_axi_control_rready    ,
  output wire [C_S_AXI_CONTROL_DATA_WIDTH-1:0]      s_axi_control_rdata     ,
  output wire [2-1:0]                               s_axi_control_rresp     ,
  output wire                                       s_axi_control_bvalid    ,
  input  wire                                       s_axi_control_bready    ,
  output wire [2-1:0]                               s_axi_control_bresp     ,
  output wire                                       interrupt               
);

///////////////////////////////////////////////////////////////////////////////
// Local Parameters
///////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////
// Wires and Variables
///////////////////////////////////////////////////////////////////////////////
(* DONT_TOUCH = "yes" *)
reg                                 areset                         = 1'b0;
wire                                ap_start                      ;
wire                                ap_idle                       ;
wire                                ap_done                       ;
wire                                ap_ready                      ;
wire [32-1:0]                       slv_reg0_out                  ;
wire [32-1:0]                       slv_reg1_out                  ;
wire [32-1:0]                       slv_reg2_out                  ;
wire [32-1:0]                       slv_reg3_out                  ;
wire [32-1:0]                       slv_reg4_out                  ;
wire [32-1:0]                       slv_reg5_out                  ;
wire [32-1:0]                       slv_reg6_out                  ;
wire [32-1:0]                       slv_reg7_out                  ;
wire [32-1:0]                       slv_reg8_out                  ;
wire [32-1:0]                       slv_reg9_out                  ;
wire [32-1:0]                       slv_reg10_out                 ;
wire [32-1:0]                       slv_reg11_out                 ;
wire [32-1:0]                       slv_reg12_out                 ;
wire [32-1:0]                       slv_reg13_out                 ;
wire [32-1:0]                       slv_reg14_out                 ;
wire [64-1:0]                       axi00_imem_ptr0               ;
wire [64-1:0]                       axi01_parambuf_ptr0           ;
wire [64-1:0]                       axi02_ibuf_ptr0               ;
wire [64-1:0]                       axi03_obuf_ptr0               ;

// Register and invert reset signal.
always @(posedge ap_clk) begin
  areset <= ~ap_rst_n;
end

///////////////////////////////////////////////////////////////////////////////
// Begin control interface RTL.  Modifying not recommended.
///////////////////////////////////////////////////////////////////////////////


// AXI4-Lite slave interface
systolic_fpga_control_s_axi #(
  .C_S_AXI_ADDR_WIDTH ( C_S_AXI_CONTROL_ADDR_WIDTH ),
  .C_S_AXI_DATA_WIDTH ( C_S_AXI_CONTROL_DATA_WIDTH )
)
inst_control_s_axi (
  .ACLK                ( ap_clk                ),
  .ARESET              ( areset                ),
  .ACLK_EN             ( 1'b1                  ),
  .AWVALID             ( s_axi_control_awvalid ),
  .AWREADY             ( s_axi_control_awready ),
  .AWADDR              ( s_axi_control_awaddr  ),
  .WVALID              ( s_axi_control_wvalid  ),
  .WREADY              ( s_axi_control_wready  ),
  .WDATA               ( s_axi_control_wdata   ),
  .WSTRB               ( s_axi_control_wstrb   ),
  .ARVALID             ( s_axi_control_arvalid ),
  .ARREADY             ( s_axi_control_arready ),
  .ARADDR              ( s_axi_control_araddr  ),
  .RVALID              ( s_axi_control_rvalid  ),
  .RREADY              ( s_axi_control_rready  ),
  .RDATA               ( s_axi_control_rdata   ),
  .RRESP               ( s_axi_control_rresp   ),
  .BVALID              ( s_axi_control_bvalid  ),
  .BREADY              ( s_axi_control_bready  ),
  .BRESP               ( s_axi_control_bresp   ),
  .interrupt           ( interrupt             ),
  .ap_start            ( ap_start              ),
  .ap_done             ( ap_done               ),
  .ap_ready            ( ap_ready              ),
  .ap_idle             ( ap_idle               ),
  .slv_reg0_out        ( slv_reg0_out          ),
  .slv_reg1_out        ( slv_reg1_out          ),
  .slv_reg2_out        ( slv_reg2_out          ),
  .slv_reg3_out        ( slv_reg3_out          ),
  .slv_reg4_out        ( slv_reg4_out          ),
  .slv_reg5_out        ( slv_reg5_out          ),
  .slv_reg6_out        ( slv_reg6_out          ),
  .slv_reg7_out        ( slv_reg7_out          ),
  .slv_reg8_out        ( slv_reg8_out          ),
  .slv_reg9_out        ( slv_reg9_out          ),
  .slv_reg10_out       ( slv_reg10_out         ),
  .slv_reg11_out       ( slv_reg11_out         ),
  .slv_reg12_out       ( slv_reg12_out         ),
  .slv_reg13_out       ( slv_reg13_out         ),
  .slv_reg14_out       ( slv_reg14_out         ),
  .axi00_imem_ptr0     ( axi00_imem_ptr0       ),
  .axi01_parambuf_ptr0 ( axi01_parambuf_ptr0   ),
  .axi02_ibuf_ptr0     ( axi02_ibuf_ptr0       ),
  .axi03_obuf_ptr0     ( axi03_obuf_ptr0       )
);

///////////////////////////////////////////////////////////////////////////////
// Add kernel logic here.  Modify/remove example code as necessary.
///////////////////////////////////////////////////////////////////////////////

// Example RTL block.  Remove to insert custom logic.
systolic_fpga_example #(
  .C_M00_IMEM_AXI_ADDR_WIDTH     ( C_M00_IMEM_AXI_ADDR_WIDTH     ),
  .C_M00_IMEM_AXI_DATA_WIDTH     ( C_M00_IMEM_AXI_DATA_WIDTH     ),
  .C_M01_PARAMBUF_AXI_ADDR_WIDTH ( C_M01_PARAMBUF_AXI_ADDR_WIDTH ),
  .C_M01_PARAMBUF_AXI_DATA_WIDTH ( C_M01_PARAMBUF_AXI_DATA_WIDTH ),
  .C_M02_IBUF_AXI_ADDR_WIDTH     ( C_M02_IBUF_AXI_ADDR_WIDTH     ),
  .C_M02_IBUF_AXI_DATA_WIDTH     ( C_M02_IBUF_AXI_DATA_WIDTH     ),
  .C_M03_OBUF_AXI_ADDR_WIDTH     ( C_M03_OBUF_AXI_ADDR_WIDTH     ),
  .C_M03_OBUF_AXI_DATA_WIDTH     ( C_M03_OBUF_AXI_DATA_WIDTH     )
)
inst_example (
  .ap_clk                   ( ap_clk                   ),
  .ap_rst_n                 ( ap_rst_n                 ),
  .m00_imem_axi_awvalid     ( m00_imem_axi_awvalid     ),
  .m00_imem_axi_awready     ( m00_imem_axi_awready     ),
  .m00_imem_axi_awaddr      ( m00_imem_axi_awaddr      ),
  .m00_imem_axi_awlen       ( m00_imem_axi_awlen       ),
  .m00_imem_axi_wvalid      ( m00_imem_axi_wvalid      ),
  .m00_imem_axi_wready      ( m00_imem_axi_wready      ),
  .m00_imem_axi_wdata       ( m00_imem_axi_wdata       ),
  .m00_imem_axi_wstrb       ( m00_imem_axi_wstrb       ),
  .m00_imem_axi_wlast       ( m00_imem_axi_wlast       ),
  .m00_imem_axi_bvalid      ( m00_imem_axi_bvalid      ),
  .m00_imem_axi_bready      ( m00_imem_axi_bready      ),
  .m00_imem_axi_arvalid     ( m00_imem_axi_arvalid     ),
  .m00_imem_axi_arready     ( m00_imem_axi_arready     ),
  .m00_imem_axi_araddr      ( m00_imem_axi_araddr      ),
  .m00_imem_axi_arlen       ( m00_imem_axi_arlen       ),
  .m00_imem_axi_rvalid      ( m00_imem_axi_rvalid      ),
  .m00_imem_axi_rready      ( m00_imem_axi_rready      ),
  .m00_imem_axi_rdata       ( m00_imem_axi_rdata       ),
  .m00_imem_axi_rlast       ( m00_imem_axi_rlast       ),
  .m01_parambuf_axi_awvalid ( m01_parambuf_axi_awvalid ),
  .m01_parambuf_axi_awready ( m01_parambuf_axi_awready ),
  .m01_parambuf_axi_awaddr  ( m01_parambuf_axi_awaddr  ),
  .m01_parambuf_axi_awlen   ( m01_parambuf_axi_awlen   ),
  .m01_parambuf_axi_wvalid  ( m01_parambuf_axi_wvalid  ),
  .m01_parambuf_axi_wready  ( m01_parambuf_axi_wready  ),
  .m01_parambuf_axi_wdata   ( m01_parambuf_axi_wdata   ),
  .m01_parambuf_axi_wstrb   ( m01_parambuf_axi_wstrb   ),
  .m01_parambuf_axi_wlast   ( m01_parambuf_axi_wlast   ),
  .m01_parambuf_axi_bvalid  ( m01_parambuf_axi_bvalid  ),
  .m01_parambuf_axi_bready  ( m01_parambuf_axi_bready  ),
  .m01_parambuf_axi_arvalid ( m01_parambuf_axi_arvalid ),
  .m01_parambuf_axi_arready ( m01_parambuf_axi_arready ),
  .m01_parambuf_axi_araddr  ( m01_parambuf_axi_araddr  ),
  .m01_parambuf_axi_arlen   ( m01_parambuf_axi_arlen   ),
  .m01_parambuf_axi_rvalid  ( m01_parambuf_axi_rvalid  ),
  .m01_parambuf_axi_rready  ( m01_parambuf_axi_rready  ),
  .m01_parambuf_axi_rdata   ( m01_parambuf_axi_rdata   ),
  .m01_parambuf_axi_rlast   ( m01_parambuf_axi_rlast   ),
  .m02_ibuf_axi_awvalid     ( m02_ibuf_axi_awvalid     ),
  .m02_ibuf_axi_awready     ( m02_ibuf_axi_awready     ),
  .m02_ibuf_axi_awaddr      ( m02_ibuf_axi_awaddr      ),
  .m02_ibuf_axi_awlen       ( m02_ibuf_axi_awlen       ),
  .m02_ibuf_axi_wvalid      ( m02_ibuf_axi_wvalid      ),
  .m02_ibuf_axi_wready      ( m02_ibuf_axi_wready      ),
  .m02_ibuf_axi_wdata       ( m02_ibuf_axi_wdata       ),
  .m02_ibuf_axi_wstrb       ( m02_ibuf_axi_wstrb       ),
  .m02_ibuf_axi_wlast       ( m02_ibuf_axi_wlast       ),
  .m02_ibuf_axi_bvalid      ( m02_ibuf_axi_bvalid      ),
  .m02_ibuf_axi_bready      ( m02_ibuf_axi_bready      ),
  .m02_ibuf_axi_arvalid     ( m02_ibuf_axi_arvalid     ),
  .m02_ibuf_axi_arready     ( m02_ibuf_axi_arready     ),
  .m02_ibuf_axi_araddr      ( m02_ibuf_axi_araddr      ),
  .m02_ibuf_axi_arlen       ( m02_ibuf_axi_arlen       ),
  .m02_ibuf_axi_rvalid      ( m02_ibuf_axi_rvalid      ),
  .m02_ibuf_axi_rready      ( m02_ibuf_axi_rready      ),
  .m02_ibuf_axi_rdata       ( m02_ibuf_axi_rdata       ),
  .m02_ibuf_axi_rlast       ( m02_ibuf_axi_rlast       ),
  .m03_obuf_axi_awvalid     ( m03_obuf_axi_awvalid     ),
  .m03_obuf_axi_awready     ( m03_obuf_axi_awready     ),
  .m03_obuf_axi_awaddr      ( m03_obuf_axi_awaddr      ),
  .m03_obuf_axi_awlen       ( m03_obuf_axi_awlen       ),
  .m03_obuf_axi_wvalid      ( m03_obuf_axi_wvalid      ),
  .m03_obuf_axi_wready      ( m03_obuf_axi_wready      ),
  .m03_obuf_axi_wdata       ( m03_obuf_axi_wdata       ),
  .m03_obuf_axi_wstrb       ( m03_obuf_axi_wstrb       ),
  .m03_obuf_axi_wlast       ( m03_obuf_axi_wlast       ),
  .m03_obuf_axi_bvalid      ( m03_obuf_axi_bvalid      ),
  .m03_obuf_axi_bready      ( m03_obuf_axi_bready      ),
  .m03_obuf_axi_arvalid     ( m03_obuf_axi_arvalid     ),
  .m03_obuf_axi_arready     ( m03_obuf_axi_arready     ),
  .m03_obuf_axi_araddr      ( m03_obuf_axi_araddr      ),
  .m03_obuf_axi_arlen       ( m03_obuf_axi_arlen       ),
  .m03_obuf_axi_rvalid      ( m03_obuf_axi_rvalid      ),
  .m03_obuf_axi_rready      ( m03_obuf_axi_rready      ),
  .m03_obuf_axi_rdata       ( m03_obuf_axi_rdata       ),
  .m03_obuf_axi_rlast       ( m03_obuf_axi_rlast       ),
  .ap_start                 ( ap_start                 ),
  .ap_done                  ( ap_done                  ),
  .ap_idle                  ( ap_idle                  ),
  .ap_ready                 ( ap_ready                 ),
  .slv_reg0_out             ( slv_reg0_out             ),
  .slv_reg1_out             ( slv_reg1_out             ),
  .slv_reg2_out             ( slv_reg2_out             ),
  .slv_reg3_out             ( slv_reg3_out             ),
  .slv_reg4_out             ( slv_reg4_out             ),
  .slv_reg5_out             ( slv_reg5_out             ),
  .slv_reg6_out             ( slv_reg6_out             ),
  .slv_reg7_out             ( slv_reg7_out             ),
  .slv_reg8_out             ( slv_reg8_out             ),
  .slv_reg9_out             ( slv_reg9_out             ),
  .slv_reg10_out            ( slv_reg10_out            ),
  .slv_reg11_out            ( slv_reg11_out            ),
  .slv_reg12_out            ( slv_reg12_out            ),
  .slv_reg13_out            ( slv_reg13_out            ),
  .slv_reg14_out            ( slv_reg14_out            ),
  .axi00_imem_ptr0          ( axi00_imem_ptr0          ),
  .axi01_parambuf_ptr0      ( axi01_parambuf_ptr0      ),
  .axi02_ibuf_ptr0          ( axi02_ibuf_ptr0          ),
  .axi03_obuf_ptr0          ( axi03_obuf_ptr0          )
);

endmodule
`default_nettype wire
