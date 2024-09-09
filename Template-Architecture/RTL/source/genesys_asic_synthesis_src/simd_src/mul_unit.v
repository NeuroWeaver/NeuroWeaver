module mul_unit #(
    parameter OPCODE_BITS 			=	4,
    parameter FUNCTION_BITS 		=	4,
    parameter BIT_WIDTH      		=	32
)(
    input       clk,
    input       reset,
    
    input [OPCODE_BITS-1 : 0] opcode,
    input [FUNCTION_BITS-1 : 0] fn,
    
    input signed [BIT_WIDTH-1 : 0] data_in0,
    input signed [BIT_WIDTH-1 : 0] data_in1,
    input signed [BIT_WIDTH-1 : 0] data_acc,
    
    input [7:0] dest_integer_bits,
    input [7:0] src1_integer_bits,
    input [7:0] src2_integer_bits,
    
    output reg signed [BIT_WIDTH-1 : 0] data_out
);
    wire gtz;
    wire [BIT_WIDTH:0] decimal_start;
    wire signed [2*BIT_WIDTH-1:0]   mult_out_temp;
    wire signed [BIT_WIDTH-1:0]     mult_out_cropped;
    reg signed [BIT_WIDTH-1:0]      mult_out, acc_final;
    wire signed [BIT_WIDTH:0]       acc_out;
    wire [7:0] src_bit_width;
    
    assign src_bit_width = (src1_integer_bits > src2_integer_bits) ? src1_integer_bits : src2_integer_bits;
    assign gtz = ~data_in0[BIT_WIDTH-1];
    assign decimal_start = 2*BIT_WIDTH-src_bit_width-BIT_WIDTH;
    assign mult_out_temp = data_in0 * data_in1;
    assign mult_out_cropped = mult_out_temp[decimal_start +: BIT_WIDTH];
    
    wire zeros,ones;
    assign zeros = |mult_out_temp[2*BIT_WIDTH-2:BIT_WIDTH-1];
    assign ones = &mult_out_temp[2*BIT_WIDTH-2:BIT_WIDTH-1];
    
    always @(*) begin
        case({mult_out_temp[2*BIT_WIDTH-1],ones,zeros} )
            3'b001,3'b011 : mult_out = {1'b0,{BIT_WIDTH-1{1'b1}}};
            3'b100,3'b101 : mult_out = {1'b1,{BIT_WIDTH-1{1'b0}}};
            default : mult_out = mult_out_cropped[BIT_WIDTH-1:0];
        endcase
    end

    assign acc_out = mult_out + data_acc;
    always @(*) begin
        case( acc_out[BIT_WIDTH:BIT_WIDTH-1])
            2'b01 : acc_final = {1'b0,{BIT_WIDTH-1{1'b1}}};
            2'b10 : acc_final = {1'b1,{BIT_WIDTH-1{1'b0}}};
            default : acc_final = acc_out[BIT_WIDTH-1 : 0];
        endcase
    end

    always @(*) begin
        case (opcode)
            4'b0000: begin
                case (fn)
                    4'b0010: data_out = mult_out;
                    4'b0011: data_out = acc_final;
                    default: data_out = data_in0;
                endcase
            end

            4'b0001: begin
                case (fn)
                    4'b0001: data_out = gtz ? data_in0 : mult_out;
                    default: data_out = data_in0;
                endcase
            end
            
            default:    data_out = data_in0;
        endcase        
    end
endmodule