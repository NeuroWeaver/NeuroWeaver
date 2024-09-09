`timescale 1ns / 1ps

module calculus_unit#(
    parameter FUNCTION_BITS 		=	4,
    parameter BIT_WIDTH      		=	32
)(
    input       clk,
    input       reset,
    
    input [FUNCTION_BITS-1 : 0] fn,
    
    input signed [BIT_WIDTH-1 : 0] data_in0,
    input signed [BIT_WIDTH-1 : 0] data_in1,
    
    input [7:0] dest_integer_bits,
    input [7:0] src1_integer_bits,
    input [7:0] src2_integer_bits,
    
    output reg signed [BIT_WIDTH-1 : 0] data_out
);
    wire [BIT_WIDTH-1 : 0]  sqrt_out;
    wire gtz, etz;
    
    assign gtz = ~data_in0[BIT_WIDTH-1];
    assign etz = data_in0 == 'b0;

    // reg [BIT_WIDTH-1 : 0]   sigmoid_in, tanh_in;
    // wire [BIT_WIDTH-1 : 0]  sigmoid_out;
    // wire [BIT_WIDTH-1 : 0]  tanh_out;
    
    // tanh_fixed #( .BIT_WIDTH(BIT_WIDTH)
    // ) tanh_unit (
    //  .clk            (   clk             ),
    //  .reset          (   reset           ),
    //  .in        (   data_in0        ),
    //  .out       (   tanh_out        )
    // );
    
    // sqrt_fix sqrt_unit (
    //     .ap_clk(clk),
    //     .ap_rst(reset),
    //     .ap_start(),
    //     .ap_done(),
    //     .ap_idle(),
    //     .ap_ready(),
    //     .in_r(data_in0),
    //     .ap_return(sqrt_out)
    // );
    
    always @(*) begin
        case(fn)
            4'b0000:    data_out = gtz ? data_in0 : 'd0;        // ReLU
            4'b0010:    data_out = gtz ? data_in0 : -(data_in0);
            4'b0011:    data_out = gtz ? 1 : etz ? 0 : -1;
            // 4'b1000:    data_out = sqrt_out; // oneOverSqrt
            // 4'b0101:    data_out = tanh_out;  // Tanh     ----- Add operator depending on bitwidth ------
            default:    data_out = 'd0;
        endcase
    end
endmodule