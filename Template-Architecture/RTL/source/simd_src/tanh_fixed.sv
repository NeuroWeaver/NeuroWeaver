`timescale 1ns / 1ps

module tanh_fixed #(
    parameter BIT_WIDTH      		=	32,
    parameter DECIMAL_WIDTH         =   16
)(  
    input   clk,
    input   reset,
    input   wire [BIT_WIDTH-1:0] in,
    output  reg [BIT_WIDTH-1:0] out
);  
    reg [BIT_WIDTH-1:0] in_abs, sig_out;
    wire [BIT_WIDTH:0] in_shifted, sig_out_shifted;
    reg positive, positive_d4;
    
    wire [BIT_WIDTH-1:0] p1;
    assign p1 = 65536;
    
    assign in_shifted = in_abs << 1;
    assign sig_out_shifted = sig_out << 1;
    
    pipeline #( 
        .NUM_BITS	( 1 ), 
        .NUM_STAGES	( 4	), 
        .EN_RESET   ( 0 )
    ) reg_4 (
        .clk		(	clk		    ), 
        .rst		(	reset		), 
        .data_in	(	positive	), 
        .data_out	(	positive_d4 ) 
    );

    always @(posedge clk) begin
        if (in[BIT_WIDTH-1] == 1'b0) begin
            in_abs <= in;
            positive <= 1'b1;
        end else begin
            in_abs <= (~in) + 1;
            positive <= 1'b0;
        end
    end
    
    sigmoid_fixed #(
        .BIT_WIDTH     (BIT_WIDTH),
        .DECIMAL_WIDTH (DECIMAL_WIDTH)
    ) sigmoid (
        .clk(clk),
        .reset(reset),
        .in(in_shifted),
        .out(sig_out)
    );
     
    always @(*) begin
        if (positive_d4) begin
            out = sig_out_shifted - p1;
        end else begin
            out = p1 - sig_out_shifted;
        end
    end
    
endmodule

module tanh_tb();
    wire done;    
    reg [31 : 0]  data_in;
    logic signed [31 : 0]  data_out;
    reg clk,reset;
    integer i, fd_w;
    always #1 clk = ~clk;
    
    initial begin
        fd_w = $fopen("C:/Users/hax032/Desktop/SIMD_dev_hanyang/tanh_test_out.txt", "w");
    
        clk <= 1; reset <= 1'b1; @(posedge clk); @(posedge clk); 
        reset <= 1'b0;
        // 6553 = 0.1
        data_in <= -393216; @(posedge clk);
        for (i = 0; i < 120; i=i+1) begin
            if (i > 5) begin
                $fdisplay(fd_w, "%0d", data_out); 
            end
            data_in <= data_in + 6553; @(posedge clk);
        end
        
        repeat(6) begin
            $fdisplay(fd_w, "%0d", data_out); @(posedge clk); 
        end
        
        $fclose(fd_w);
        $stop();
    end

    tanh_fixed dut (
        .clk(clk),
        .reset(reset),
        .in(data_in),
        .out(data_out)
    );
endmodule