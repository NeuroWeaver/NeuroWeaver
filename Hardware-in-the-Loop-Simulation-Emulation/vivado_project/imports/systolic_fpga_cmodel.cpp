// This is a generated file. Use and modify at your own risk.
////////////////////////////////////////////////////////////////////////////////

//-----------------------------------------------------------------------------
// kernel: systolic_fpga
//
// Purpose: This is a C-model of the RTL kernel intended to be used for cpu
//          emulation.  It is designed to only be functionally equivalent to
//          the RTL Kernel.
//-----------------------------------------------------------------------------
#define WORD_SIZE 32
#define SHORT_WORD_SIZE 16
#define CHAR_WORD_SIZE 8
// Transfer size and buffer size are in words.
#define TRANSFER_SIZE_BITS WORD_SIZE*4096*8
#define BUFFER_WORD_SIZE 8192
#include <string.h>
#include <stdbool.h>
#include "hls_half.h"
#include "ap_axi_sdata.h"
#include "hls_stream.h"


// Function declaration/Interface pragmas to match RTL Kernel
extern "C" void systolic_fpga (
    unsigned int slv_reg0_out,
    unsigned int slv_reg1_out,
    unsigned int slv_reg2_out,
    unsigned int slv_reg3_out,
    unsigned int slv_reg4_out,
    unsigned int slv_reg5_out,
    unsigned int slv_reg6_out,
    unsigned int slv_reg7_out,
    unsigned int slv_reg8_out,
    unsigned int slv_reg9_out,
    unsigned int slv_reg10_out,
    unsigned int slv_reg11_out,
    unsigned int slv_reg12_out,
    unsigned int slv_reg13_out,
    unsigned int slv_reg14_out,
    int* axi00_imem_ptr0,
    int* axi01_parambuf_ptr0,
    int* axi02_ibuf_ptr0,
    int* axi03_obuf_ptr0
) {

    #pragma HLS INTERFACE m_axi port=axi00_imem_ptr0 offset=slave bundle=m00_imem_axi
    #pragma HLS INTERFACE m_axi port=axi01_parambuf_ptr0 offset=slave bundle=m01_parambuf_axi
    #pragma HLS INTERFACE m_axi port=axi02_ibuf_ptr0 offset=slave bundle=m02_ibuf_axi
    #pragma HLS INTERFACE m_axi port=axi03_obuf_ptr0 offset=slave bundle=m03_obuf_axi
    #pragma HLS INTERFACE s_axilite port=slv_reg0_out bundle=control
    #pragma HLS INTERFACE s_axilite port=slv_reg1_out bundle=control
    #pragma HLS INTERFACE s_axilite port=slv_reg2_out bundle=control
    #pragma HLS INTERFACE s_axilite port=slv_reg3_out bundle=control
    #pragma HLS INTERFACE s_axilite port=slv_reg4_out bundle=control
    #pragma HLS INTERFACE s_axilite port=slv_reg5_out bundle=control
    #pragma HLS INTERFACE s_axilite port=slv_reg6_out bundle=control
    #pragma HLS INTERFACE s_axilite port=slv_reg7_out bundle=control
    #pragma HLS INTERFACE s_axilite port=slv_reg8_out bundle=control
    #pragma HLS INTERFACE s_axilite port=slv_reg9_out bundle=control
    #pragma HLS INTERFACE s_axilite port=slv_reg10_out bundle=control
    #pragma HLS INTERFACE s_axilite port=slv_reg11_out bundle=control
    #pragma HLS INTERFACE s_axilite port=slv_reg12_out bundle=control
    #pragma HLS INTERFACE s_axilite port=slv_reg13_out bundle=control
    #pragma HLS INTERFACE s_axilite port=slv_reg14_out bundle=control
    #pragma HLS INTERFACE s_axilite port=axi00_imem_ptr0 bundle=control
    #pragma HLS INTERFACE s_axilite port=axi01_parambuf_ptr0 bundle=control
    #pragma HLS INTERFACE s_axilite port=axi02_ibuf_ptr0 bundle=control
    #pragma HLS INTERFACE s_axilite port=axi03_obuf_ptr0 bundle=control
    #pragma HLS INTERFACE s_axilite port=return bundle=control
    #pragma HLS INTERFACE ap_ctrl_hs port=return

// Modify contents below to match the function of the RTL Kernel
    unsigned int data;

    // Create input and output buffers for interface m00_imem_axi
    int m00_imem_axi_input_buffer[BUFFER_WORD_SIZE];
    int m00_imem_axi_output_buffer[BUFFER_WORD_SIZE];


    // length is specified in number of words.
    unsigned int m00_imem_axi_length = 4096;


    // Assign input to a buffer
    memcpy(m00_imem_axi_input_buffer, (int*) axi00_imem_ptr0, m00_imem_axi_length*sizeof(int));

    // Add 1 to input buffer and assign to output buffer.
    for (unsigned int i = 0; i < m00_imem_axi_length; i++) {
      m00_imem_axi_output_buffer[i] = m00_imem_axi_input_buffer[i]  + 1;
    }

    // assign output buffer out to memory
    memcpy((int*) axi00_imem_ptr0, m00_imem_axi_output_buffer, m00_imem_axi_length*sizeof(int));


    // Create input and output buffers for interface m01_parambuf_axi
    int m01_parambuf_axi_input_buffer[BUFFER_WORD_SIZE];
    int m01_parambuf_axi_output_buffer[BUFFER_WORD_SIZE];


    // length is specified in number of words.
    unsigned int m01_parambuf_axi_length = 4096;


    // Assign input to a buffer
    memcpy(m01_parambuf_axi_input_buffer, (int*) axi01_parambuf_ptr0, m01_parambuf_axi_length*sizeof(int));

    // Add 1 to input buffer and assign to output buffer.
    for (unsigned int i = 0; i < m01_parambuf_axi_length; i++) {
      m01_parambuf_axi_output_buffer[i] = m01_parambuf_axi_input_buffer[i]  + 1;
    }

    // assign output buffer out to memory
    memcpy((int*) axi01_parambuf_ptr0, m01_parambuf_axi_output_buffer, m01_parambuf_axi_length*sizeof(int));


    // Create input and output buffers for interface m02_ibuf_axi
    int m02_ibuf_axi_input_buffer[BUFFER_WORD_SIZE];
    int m02_ibuf_axi_output_buffer[BUFFER_WORD_SIZE];


    // length is specified in number of words.
    unsigned int m02_ibuf_axi_length = 4096;


    // Assign input to a buffer
    memcpy(m02_ibuf_axi_input_buffer, (int*) axi02_ibuf_ptr0, m02_ibuf_axi_length*sizeof(int));

    // Add 1 to input buffer and assign to output buffer.
    for (unsigned int i = 0; i < m02_ibuf_axi_length; i++) {
      m02_ibuf_axi_output_buffer[i] = m02_ibuf_axi_input_buffer[i]  + 1;
    }

    // assign output buffer out to memory
    memcpy((int*) axi02_ibuf_ptr0, m02_ibuf_axi_output_buffer, m02_ibuf_axi_length*sizeof(int));


    // Create input and output buffers for interface m03_obuf_axi
    int m03_obuf_axi_input_buffer[BUFFER_WORD_SIZE];
    int m03_obuf_axi_output_buffer[BUFFER_WORD_SIZE];


    // length is specified in number of words.
    unsigned int m03_obuf_axi_length = 4096;


    // Assign input to a buffer
    memcpy(m03_obuf_axi_input_buffer, (int*) axi03_obuf_ptr0, m03_obuf_axi_length*sizeof(int));

    // Add 1 to input buffer and assign to output buffer.
    for (unsigned int i = 0; i < m03_obuf_axi_length; i++) {
      m03_obuf_axi_output_buffer[i] = m03_obuf_axi_input_buffer[i]  + 1;
    }

    // assign output buffer out to memory
    memcpy((int*) axi03_obuf_ptr0, m03_obuf_axi_output_buffer, m03_obuf_axi_length*sizeof(int));


}

