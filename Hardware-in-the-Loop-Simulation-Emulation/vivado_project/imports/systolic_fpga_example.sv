// This is a generated file. Use and modify at your own risk.
//////////////////////////////////////////////////////////////////////////////// 
// default_nettype of none prevents implicit wire declaration.
`default_nettype none
module systolic_fpga_example #(
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
  // Control Signals
  input  wire                                       ap_start                ,
  output wire                                       ap_idle                 ,
  output wire                                       ap_done                 ,
  output wire                                       ap_ready                ,
  input  wire [32-1:0]                              slv_reg0_out            ,
  input  wire [32-1:0]                              slv_reg1_out            ,
  input  wire [32-1:0]                              slv_reg2_out            ,
  input  wire [32-1:0]                              slv_reg3_out            ,
  input  wire [32-1:0]                              slv_reg4_out            ,
  input  wire [32-1:0]                              slv_reg5_out            ,
  input  wire [32-1:0]                              slv_reg6_out            ,
  input  wire [32-1:0]                              slv_reg7_out            ,
  input  wire [32-1:0]                              slv_reg8_out            ,
  input  wire [32-1:0]                              slv_reg9_out            ,
  input  wire [32-1:0]                              slv_reg10_out           ,
  input  wire [32-1:0]                              slv_reg11_out           ,
  input  wire [32-1:0]                              slv_reg12_out           ,
  input  wire [32-1:0]                              slv_reg13_out           ,
  input  wire [32-1:0]                              slv_reg14_out           ,
  input  wire [64-1:0]                              axi00_imem_ptr0         ,
  input  wire [64-1:0]                              axi01_parambuf_ptr0     ,
  input  wire [64-1:0]                              axi02_ibuf_ptr0         ,
  input  wire [64-1:0]                              axi03_obuf_ptr0         
);


timeunit 1ps;
timeprecision 1ps;

///////////////////////////////////////////////////////////////////////////////
// Local Parameters
///////////////////////////////////////////////////////////////////////////////
// Large enough for interesting traffic.
localparam integer  LP_DEFAULT_LENGTH_IN_BYTES = 16384;
localparam integer  LP_NUM_EXAMPLES    = 4;

///////////////////////////////////////////////////////////////////////////////
// Wires and Variables
///////////////////////////////////////////////////////////////////////////////
(* KEEP = "yes" *)
logic                                areset                         = 1'b0;
logic                                ap_start_r                     = 1'b0;
logic                                ap_idle_r                      = 1'b1;
logic                                ap_start_pulse                ;
logic [LP_NUM_EXAMPLES-1:0]          ap_done_i                     ;
logic [LP_NUM_EXAMPLES-1:0]          ap_done_r                      = {LP_NUM_EXAMPLES{1'b0}};
logic [32-1:0]                       ctrl_xfer_size_in_bytes        = LP_DEFAULT_LENGTH_IN_BYTES;
logic [32-1:0]                       ctrl_constant                  = 32'd1;

///////////////////////////////////////////////////////////////////////////////
// Begin RTL
///////////////////////////////////////////////////////////////////////////////

// Register and invert reset signal.
always @(posedge ap_clk) begin
  areset <= ~ap_rst_n;
end

// create pulse when ap_start transitions to 1
always @(posedge ap_clk) begin
  begin
    ap_start_r <= ap_start;
  end
end

assign ap_start_pulse = ap_start & ~ap_start_r;

// ap_idle is asserted when done is asserted, it is de-asserted when ap_start_pulse
// is asserted
always @(posedge ap_clk) begin
  if (areset) begin
    ap_idle_r <= 1'b1;
  end
  else begin
    ap_idle_r <= ap_done ? 1'b1 :
      ap_start_pulse ? 1'b0 : ap_idle;
  end
end

assign ap_idle = ap_idle_r;

// Done logic
always @(posedge ap_clk) begin
  if (areset) begin
    ap_done_r <= '0;
  end
  else begin
    ap_done_r <= (ap_done) ? '0 : ap_done_r | ap_done_i;
  end
end

assign ap_done = &ap_done_r;

// Ready Logic (non-pipelined case)
assign ap_ready = ap_done;

// Vadd example
systolic_fpga_example_vadd #(
  .C_M_AXI_ADDR_WIDTH ( C_M00_IMEM_AXI_ADDR_WIDTH ),
  .C_M_AXI_DATA_WIDTH ( C_M00_IMEM_AXI_DATA_WIDTH ),
  .C_ADDER_BIT_WIDTH  ( 32                        ),
  .C_XFER_SIZE_WIDTH  ( 32                        )
)
inst_example_vadd_m00_imem_axi (
  .aclk                    ( ap_clk                  ),
  .areset                  ( areset                  ),
  .kernel_clk              ( ap_clk                  ),
  .kernel_rst              ( areset                  ),
  .ctrl_addr_offset        ( axi00_imem_ptr0         ),
  .ctrl_xfer_size_in_bytes ( ctrl_xfer_size_in_bytes ),
  .ctrl_constant           ( ctrl_constant           ),
  .ap_start                ( ap_start_pulse          ),
  .ap_done                 ( ap_done_i[0]            ),
  .m_axi_awvalid           ( m00_imem_axi_awvalid    ),
  .m_axi_awready           ( m00_imem_axi_awready    ),
  .m_axi_awaddr            ( m00_imem_axi_awaddr     ),
  .m_axi_awlen             ( m00_imem_axi_awlen      ),
  .m_axi_wvalid            ( m00_imem_axi_wvalid     ),
  .m_axi_wready            ( m00_imem_axi_wready     ),
  .m_axi_wdata             ( m00_imem_axi_wdata      ),
  .m_axi_wstrb             ( m00_imem_axi_wstrb      ),
  .m_axi_wlast             ( m00_imem_axi_wlast      ),
  .m_axi_bvalid            ( m00_imem_axi_bvalid     ),
  .m_axi_bready            ( m00_imem_axi_bready     ),
  .m_axi_arvalid           ( m00_imem_axi_arvalid    ),
  .m_axi_arready           ( m00_imem_axi_arready    ),
  .m_axi_araddr            ( m00_imem_axi_araddr     ),
  .m_axi_arlen             ( m00_imem_axi_arlen      ),
  .m_axi_rvalid            ( m00_imem_axi_rvalid     ),
  .m_axi_rready            ( m00_imem_axi_rready     ),
  .m_axi_rdata             ( m00_imem_axi_rdata      ),
  .m_axi_rlast             ( m00_imem_axi_rlast      )
);


// Vadd example
systolic_fpga_example_vadd #(
  .C_M_AXI_ADDR_WIDTH ( C_M01_PARAMBUF_AXI_ADDR_WIDTH ),
  .C_M_AXI_DATA_WIDTH ( C_M01_PARAMBUF_AXI_DATA_WIDTH ),
  .C_ADDER_BIT_WIDTH  ( 32                            ),
  .C_XFER_SIZE_WIDTH  ( 32                            )
)
inst_example_vadd_m01_parambuf_axi (
  .aclk                    ( ap_clk                   ),
  .areset                  ( areset                   ),
  .kernel_clk              ( ap_clk                   ),
  .kernel_rst              ( areset                   ),
  .ctrl_addr_offset        ( axi01_parambuf_ptr0      ),
  .ctrl_xfer_size_in_bytes ( ctrl_xfer_size_in_bytes  ),
  .ctrl_constant           ( ctrl_constant            ),
  .ap_start                ( ap_start_pulse           ),
  .ap_done                 ( ap_done_i[1]             ),
  .m_axi_awvalid           ( m01_parambuf_axi_awvalid ),
  .m_axi_awready           ( m01_parambuf_axi_awready ),
  .m_axi_awaddr            ( m01_parambuf_axi_awaddr  ),
  .m_axi_awlen             ( m01_parambuf_axi_awlen   ),
  .m_axi_wvalid            ( m01_parambuf_axi_wvalid  ),
  .m_axi_wready            ( m01_parambuf_axi_wready  ),
  .m_axi_wdata             ( m01_parambuf_axi_wdata   ),
  .m_axi_wstrb             ( m01_parambuf_axi_wstrb   ),
  .m_axi_wlast             ( m01_parambuf_axi_wlast   ),
  .m_axi_bvalid            ( m01_parambuf_axi_bvalid  ),
  .m_axi_bready            ( m01_parambuf_axi_bready  ),
  .m_axi_arvalid           ( m01_parambuf_axi_arvalid ),
  .m_axi_arready           ( m01_parambuf_axi_arready ),
  .m_axi_araddr            ( m01_parambuf_axi_araddr  ),
  .m_axi_arlen             ( m01_parambuf_axi_arlen   ),
  .m_axi_rvalid            ( m01_parambuf_axi_rvalid  ),
  .m_axi_rready            ( m01_parambuf_axi_rready  ),
  .m_axi_rdata             ( m01_parambuf_axi_rdata   ),
  .m_axi_rlast             ( m01_parambuf_axi_rlast   )
);


// Vadd example
systolic_fpga_example_vadd #(
  .C_M_AXI_ADDR_WIDTH ( C_M02_IBUF_AXI_ADDR_WIDTH ),
  .C_M_AXI_DATA_WIDTH ( C_M02_IBUF_AXI_DATA_WIDTH ),
  .C_ADDER_BIT_WIDTH  ( 32                        ),
  .C_XFER_SIZE_WIDTH  ( 32                        )
)
inst_example_vadd_m02_ibuf_axi (
  .aclk                    ( ap_clk                  ),
  .areset                  ( areset                  ),
  .kernel_clk              ( ap_clk                  ),
  .kernel_rst              ( areset                  ),
  .ctrl_addr_offset        ( axi02_ibuf_ptr0         ),
  .ctrl_xfer_size_in_bytes ( ctrl_xfer_size_in_bytes ),
  .ctrl_constant           ( ctrl_constant           ),
  .ap_start                ( ap_start_pulse          ),
  .ap_done                 ( ap_done_i[2]            ),
  .m_axi_awvalid           ( m02_ibuf_axi_awvalid    ),
  .m_axi_awready           ( m02_ibuf_axi_awready    ),
  .m_axi_awaddr            ( m02_ibuf_axi_awaddr     ),
  .m_axi_awlen             ( m02_ibuf_axi_awlen      ),
  .m_axi_wvalid            ( m02_ibuf_axi_wvalid     ),
  .m_axi_wready            ( m02_ibuf_axi_wready     ),
  .m_axi_wdata             ( m02_ibuf_axi_wdata      ),
  .m_axi_wstrb             ( m02_ibuf_axi_wstrb      ),
  .m_axi_wlast             ( m02_ibuf_axi_wlast      ),
  .m_axi_bvalid            ( m02_ibuf_axi_bvalid     ),
  .m_axi_bready            ( m02_ibuf_axi_bready     ),
  .m_axi_arvalid           ( m02_ibuf_axi_arvalid    ),
  .m_axi_arready           ( m02_ibuf_axi_arready    ),
  .m_axi_araddr            ( m02_ibuf_axi_araddr     ),
  .m_axi_arlen             ( m02_ibuf_axi_arlen      ),
  .m_axi_rvalid            ( m02_ibuf_axi_rvalid     ),
  .m_axi_rready            ( m02_ibuf_axi_rready     ),
  .m_axi_rdata             ( m02_ibuf_axi_rdata      ),
  .m_axi_rlast             ( m02_ibuf_axi_rlast      )
);


// Vadd example
systolic_fpga_example_vadd #(
  .C_M_AXI_ADDR_WIDTH ( C_M03_OBUF_AXI_ADDR_WIDTH ),
  .C_M_AXI_DATA_WIDTH ( C_M03_OBUF_AXI_DATA_WIDTH ),
  .C_ADDER_BIT_WIDTH  ( 32                        ),
  .C_XFER_SIZE_WIDTH  ( 32                        )
)
inst_example_vadd_m03_obuf_axi (
  .aclk                    ( ap_clk                  ),
  .areset                  ( areset                  ),
  .kernel_clk              ( ap_clk                  ),
  .kernel_rst              ( areset                  ),
  .ctrl_addr_offset        ( axi03_obuf_ptr0         ),
  .ctrl_xfer_size_in_bytes ( ctrl_xfer_size_in_bytes ),
  .ctrl_constant           ( ctrl_constant           ),
  .ap_start                ( ap_start_pulse          ),
  .ap_done                 ( ap_done_i[3]            ),
  .m_axi_awvalid           ( m03_obuf_axi_awvalid    ),
  .m_axi_awready           ( m03_obuf_axi_awready    ),
  .m_axi_awaddr            ( m03_obuf_axi_awaddr     ),
  .m_axi_awlen             ( m03_obuf_axi_awlen      ),
  .m_axi_wvalid            ( m03_obuf_axi_wvalid     ),
  .m_axi_wready            ( m03_obuf_axi_wready     ),
  .m_axi_wdata             ( m03_obuf_axi_wdata      ),
  .m_axi_wstrb             ( m03_obuf_axi_wstrb      ),
  .m_axi_wlast             ( m03_obuf_axi_wlast      ),
  .m_axi_bvalid            ( m03_obuf_axi_bvalid     ),
  .m_axi_bready            ( m03_obuf_axi_bready     ),
  .m_axi_arvalid           ( m03_obuf_axi_arvalid    ),
  .m_axi_arready           ( m03_obuf_axi_arready    ),
  .m_axi_araddr            ( m03_obuf_axi_araddr     ),
  .m_axi_arlen             ( m03_obuf_axi_arlen      ),
  .m_axi_rvalid            ( m03_obuf_axi_rvalid     ),
  .m_axi_rready            ( m03_obuf_axi_rready     ),
  .m_axi_rdata             ( m03_obuf_axi_rdata      ),
  .m_axi_rlast             ( m03_obuf_axi_rlast      )
);


endmodule : systolic_fpga_example
`default_nettype wire
