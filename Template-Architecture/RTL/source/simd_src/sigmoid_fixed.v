`timescale 1ns / 1ps

module sigmoid_fixed #(
    parameter BIT_WIDTH      		=	32,
    parameter DECIMAL_WIDTH         =   16
)(  
    input   clk,
    input   reset,
    input   wire [BIT_WIDTH-1:0] in,
    output  reg [BIT_WIDTH-1:0] out
);
    
    wire [BIT_WIDTH-1:0] p003125, p025, p05, p4, p1;
    assign p003125 = 2048;
    assign p025 = 16384;
    assign p05 = 32768;
    assign p4 = 262144;
    assign p1 = 65536;
    
    reg [BIT_WIDTH-1:0] in_abs, out_temp, square_out, p025_mul;
    wire [BIT_WIDTH-1:0] square_out_cropped, sig_out, n03125_mul;
    reg [2*BIT_WIDTH-1:0] square_out_temp, p025_mul_temp, n03125_mul_temp;
    wire larger_than_4;
    reg positive, positive_d, positive_d2, positive_d3, larger_than_4_d, larger_than_4_d2;
    
    assign larger_than_4 = in_abs >= p4;
    
    always @(posedge clk) begin
        if (in[BIT_WIDTH-1] == 1'b0) begin
            in_abs <= in;
            positive <= 1'b1;
        end else begin
            in_abs <= (~in) + 1;
            positive <= 1'b0;
        end
        
        positive_d <= positive;
        positive_d2 <= positive_d;
        positive_d3 <= positive_d2;
      
        larger_than_4_d <= larger_than_4;
        larger_than_4_d2 <= larger_than_4_d;
    end
    
    always @(posedge clk) begin
        square_out_temp <= in_abs * in_abs;
        n03125_mul_temp <= square_out * p003125;
        
        p025_mul_temp <= p025 * in_abs;
        p025_mul <= p025_mul_temp[DECIMAL_WIDTH +: BIT_WIDTH];
    end
    
    assign sig_out = n03125_mul + p025_mul + p05;
    assign square_out_cropped = square_out_temp[DECIMAL_WIDTH +: BIT_WIDTH];
    //assign p025_mul = p025_mul_temp[DECIMAL_WIDTH +: BIT_WIDTH];
    assign n03125_mul = ~(n03125_mul_temp[DECIMAL_WIDTH +: BIT_WIDTH])+1;
    
    // Cover all the integer bits possibility here since the cropped length varies
    reg zeros_square,ones_square;
    wire [3:0] checks_square;
    reg overflow_square;
    reg underflow_square;
    reg overflow_reg_square;
    reg underflow_reg_square;
    
    always @(posedge clk) begin
        if (reset) begin
            overflow_reg_square <= 1'b0;
        end else if (!overflow_reg_square && overflow_square) begin
            overflow_reg_square <= 1'b1;
        end else begin
            overflow_reg_square <= overflow_reg_square;
        end
    end

    always @(posedge clk) begin
        if (reset) begin
            underflow_reg_square <= 1'b0;
        end else if (!underflow_reg_square && underflow_square) begin
            underflow_reg_square <= 1'b1;
        end else begin
            underflow_reg_square <= underflow_reg_square;
        end
    end
        
    always @(*) begin
        zeros_square = |square_out_cropped[BIT_WIDTH*2-1:DECIMAL_WIDTH+BIT_WIDTH];
        ones_square = &square_out_cropped[BIT_WIDTH*2-1:DECIMAL_WIDTH+BIT_WIDTH]; 
    end
    
    always @(*) begin
        case(checks_square)
            4'b00x0, 4'b11x0: begin
                overflow_square = 1'b1;
                square_out = {1'b0,{BIT_WIDTH-1{1'b1}}}; 
            end
            4'b01x1, 4'b10x1: begin
                underflow_square = 1'b1;
                square_out = {1'b1,{BIT_WIDTH-1{1'b0}}};
            end
            default: begin
                overflow_square = 1'b0;
                underflow_square = 1'b0;
                if (overflow_reg_square) begin
                    square_out = {1'b0,{BIT_WIDTH-1{1'b1}}}; 
                end else if (underflow_reg_square) begin
                    square_out = {1'b1,{BIT_WIDTH-1{1'b0}}};
                end else begin
                    square_out = square_out_cropped[BIT_WIDTH-1:0];
                end
            end
        endcase
    end
    
    always @(posedge clk) begin 
        if (larger_than_4_d2) begin
            out_temp <= p1;
        end else begin
            out_temp <= sig_out;
        end
    end
    
    always @(*) begin
        if (positive_d3) begin
            out = out_temp;
        end else begin
            out = p1 - out_temp;
        end
    end
endmodule


module sigmoid_tb();
    wire done;    
    reg [31 : 0]  data_in;
    wire [31 : 0]  data_out;
    reg clk,reset;
    integer i, fd_w;
    always #1 clk = ~clk;
    
    initial begin
        fd_w = $fopen("C:/Users/hax032/Desktop/SIMD_dev_hanyang/sigmoid_test_out.txt", "w");
    
        clk <= 1; reset <= 1'b1; @(posedge clk); @(posedge clk); 
        reset <= 1'b0;
        // 6553 = 0.1
        data_in <= -393216; @(posedge clk);
        for (i = 0; i < 120; i=i+1) begin
            if (i > 3) begin
                $fdisplay(fd_w, "%0d", data_out); 
            end
            data_in <= data_in + 6553; @(posedge clk);
        end
        
        repeat(4) begin
            $fdisplay(fd_w, "%0d", data_out); @(posedge clk); 
        end
        
        $fclose(fd_w);
        $stop();
    end

    sigmoid_fixed dut (
        .clk(clk),
        .reset(reset),
        .in(data_in),
        .out(data_out)
    );
endmodule