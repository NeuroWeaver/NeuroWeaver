`define PPO4x4_gemm
    bit [31:0] instruction_base_addr    = 32'd67108864;

`ifdef PPO4x4_tanh
    bit [31:0] num_instruction_bytes               = 32'd880; // num_instr * 4
    bit [63:0] axi00_imem_addr                     = 67108864; // does not matter as Innstructions as written using config reg
    bit [63:0] axi03_obuf_addr                     = 542003200;
                                                     
    bit [63:0] axi01_parambuf_addr                 = 67133440;
    bit [63:0] axi02_ibuf_addr                     = 71368704;
    bit [63:0] axi04_bias_addr                     = 67112960;
    bit [63:0] axi04_simd_addr                     = 0;

    integer config_stride                          = 1048576; // high stride = 0 & Low stride = 4096
    integer config_input_num_tiles                 = 1;
    integer config_bias_num_tiles                  = 4;
    integer config_weight_num_tiles                = 4;
    integer config_output_num_tiles                = 4;  
    integer config_input_tile_size_32B_cnt         = 128;
    integer config_bias_tile_size_32B_cnt          = 256;
    integer config_weight_tile_size_32B_cnt        = 32768;
    integer config_output_tile_size_32B_cnt        = 256;
    
    bit last_layer_obuf                            = 0;
    
    integer instr_filep   = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer1_elem_tanh2d2/elem_tanh2d2_decimal.txt","r");
    integer instr_filep1  = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer1_elem_tanh2d2/elem_tanh2d2_decimal.txt","r"); 

    integer output_filep  = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer1_elem_tanh2d2/data/onnx_Gemm_14_Y.txt","r");
    integer output_filep1 = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer1_elem_tanh2d2/data/onnx_Gemm_14_Y.txt","r");
    integer output_filep2 = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer1_elem_tanh2d2/data/onnx_Gemm_14_Y.txt","r");

    integer input_filep   = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer0_gemm1/data/onnx_Gemm_0_A.txt","r");
    integer input_filep1  = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer0_gemm1/data/onnx_Gemm_0_A.txt","r");

    integer params_filep  = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer0_gemm1/data/extractor.policy_net.0.weight.txt","r"); 
    integer params_filep1 = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer0_gemm1/data/extractor.policy_net.0.weight.txt","r"); 

    integer bias_filep    = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer0_gemm1/data/extractor.policy_net.0.bias.txt","r"); 
    integer bias_filep1   = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer0_gemm1/data/extractor.policy_net.0.bias.txt","r"); 
    
    integer simd_file1    = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer1_elem_tanh2d2/data/onnx_Tanh_13_Y.txt","r");
    integer simd_file2    = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer1_elem_tanh2d2/data/onnx_Tanh_13_Y.txt","r");

`elsif PPO4x4_gemm
    bit [31:0] num_instruction_bytes               = 32'd880; // num_instr * 4
    bit [63:0] axi00_imem_addr                     = 67108864; // does not matter as Innstructions as written using config reg
    bit [63:0] axi03_obuf_addr                     = 542003200;
                                                     
    bit [63:0] axi01_parambuf_addr                 = 67133440;
    bit [63:0] axi02_ibuf_addr                     = 201326592;
    bit [63:0] axi04_bias_addr                     = 67112960;
    bit [63:0] axi04_simd_addr                     = 0;

    integer config_stride                          = 1048576; // high stride = 0 & Low stride = 4096
    integer config_input_num_tiles                 = 1;
    integer config_bias_num_tiles                  = 4;
    integer config_weight_num_tiles                = 4;
    integer config_output_num_tiles                = 4;  
    integer config_input_tile_size_32B_cnt         = 128;
    integer config_bias_tile_size_32B_cnt          = 256;
    integer config_weight_tile_size_32B_cnt        = 32768;
    integer config_output_tile_size_32B_cnt        = 256;
    
    bit last_layer_obuf                            = 0;

// With bias
    integer instr_filep   = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer0_gemm1/gemm1_decimal.txt","r");
    integer instr_filep1  = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer0_gemm1/gemm1_decimal.txt","r"); 

//    integer output_filep  = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer0_gemm1/data/onnx_Tanh_13_Y.txt","r");
//    integer output_filep1 = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer0_gemm1/data/onnx_Tanh_13_Y.txt","r");
//    integer output_filep2 = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer0_gemm1/data/onnx_Tanh_13_Y.txt","r");

//    integer input_filep   = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer0_gemm1/data/onnx_Gemm_0_A/onnx_Gemm_0_A_shuffled.txt","r");
//    integer input_filep1  = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer0_gemm1/data/onnx_Gemm_0_A/onnx_Gemm_0_A_shuffled.txt","r");

//    integer params_filep  = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer0_gemm1/data/extractor.policy_net.0.weight/extractor.policy_net.0.weight_shuffled.txt","r"); 
//    integer params_filep1 = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer0_gemm1/data/extractor.policy_net.0.weight/extractor.policy_net.0.weight_shuffled.txt","r"); 

//    integer bias_filep    = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer0_gemm1/data/extractor.policy_net.0.bias.txt","r"); 
//    integer bias_filep1   = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer0_gemm1/data/extractor.policy_net.0.bias.txt","r"); 
    
//    integer simd_file1    = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer1_elem_tanh2d2/data/onnx_Tanh_13_Y.txt","r");
//    integer simd_file2    = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_6/layer1_elem_tanh2d2/data/onnx_Tanh_13_Y.txt","r");

    integer output_filep  = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_7/layer0_gemm1/data/onnx_Tanh_13_Y.txt","r");
    integer output_filep1 = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_7/layer0_gemm1/data/onnx_Tanh_13_Y.txt","r");
    integer output_filep2 = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_7/layer0_gemm1/data/onnx_Tanh_13_Y.txt","r");

    integer input_filep   = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_7/layer0_gemm1/data/onnx_Gemm_0_A/onnx_Gemm_0_A_shuffled.txt","r");
    integer input_filep1  = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_7/layer0_gemm1/data/onnx_Gemm_0_A/onnx_Gemm_0_A_shuffled.txt","r");

    integer params_filep  = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_7/layer0_gemm1/data/extractor.policy_net.0.weight/extractor.policy_net.0.weight_shuffled.txt","r"); 
    integer params_filep1 = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_7/layer0_gemm1/data/extractor.policy_net.0.weight/extractor.policy_net.0.weight_shuffled.txt","r"); 

    integer bias_filep    = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_7/layer0_gemm1/data/extractor.policy_net.0.bias.txt","r"); 
    integer bias_filep1   = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_7/layer0_gemm1/data/extractor.policy_net.0.bias.txt","r"); 
    
    integer simd_file1    = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_7/layer1_elem_tanh2d2/data/onnx_Tanh_13_Y.txt","r");
    integer simd_file2    = $fopen("C:/Users/hax032/Desktop/ppo_model_benchmark4x4_7/layer1_elem_tanh2d2/data/onnx_Tanh_13_Y.txt","r");

`elsif FFT_LAYER5_SQRT
    bit [31:0] num_instruction_bytes               = 32'd880; // num_instr * 4
    bit [63:0] axi00_imem_addr                     = 67108864; // does not matter as Innstructions as written using config reg
    bit [63:0] axi03_obuf_addr                     = 542003200;
                                                     
    bit [63:0] axi01_parambuf_addr                 = 67133440;
    bit [63:0] axi02_ibuf_addr                     = 71368704;
    bit [63:0] axi04_bias_addr                     = 67112960;
    bit [63:0] axi04_simd_addr                     = 0;

    integer config_stride                          = 1048576; // high stride = 0 & Low stride = 4096
    integer config_input_num_tiles                 = 1;
    integer config_bias_num_tiles                  = 4;
    integer config_weight_num_tiles                = 4;
    integer config_output_num_tiles                = 4;  
    integer config_input_tile_size_32B_cnt         = 128;
    integer config_bias_tile_size_32B_cnt          = 256;
    integer config_weight_tile_size_32B_cnt        = 32768;
    integer config_output_tile_size_32B_cnt        = 256;
    
    bit last_layer_obuf                            = 0;
      
    
    integer instr_filep   = $fopen("/home/lavanya/testcases/custom_fft_benchmark16x16_4/layer5_elem_sqrt2d6/elem_sqrt2d6_decimal.txt","r"); 
    integer instr_filep1  = $fopen("/home/lavanya/testcases/custom_fft_benchmark16x16_4/layer5_elem_sqrt2d6/elem_sqrt2d6_decimal.txt","r"); 

    integer output_filep  = $fopen("/home/lavanya/testcases/custom_fft_benchmark16x16_4/layer5_elem_sqrt2d6/data/output.txt","r");
    integer output_filep1 = $fopen("/home/lavanya/testcases/custom_fft_benchmark16x16_4/layer5_elem_sqrt2d6/data/output.txt","r");
    integer output_filep2 = $fopen("/home/lavanya/testcases/custom_fft_benchmark16x16_4/layer5_elem_sqrt2d6/data/output.txt","r");

    integer input_filep   = $fopen("/home/lavanya/testcases/custom_fft_benchmark16x16_4/layer5_elem_sqrt2d6/data/output.txt","r");
    integer input_filep1  = $fopen("/home/lavanya/testcases/custom_fft_benchmark16x16_4/layer5_elem_sqrt2d6/data/output.txt","r");

    integer params_filep  = $fopen("/home/lavanya/testcases/custom_fft_benchmark16x16_4/layer5_elem_sqrt2d6/data/output.txt","r"); 
    integer params_filep1 = $fopen("/home/lavanya/testcases/custom_fft_benchmark16x16_4/layer5_elem_sqrt2d6/data/output.txt","r"); 

    integer bias_filep    = $fopen("/home/lavanya/testcases/custom_fft_benchmark16x16_4/layer5_elem_sqrt2d6/data/output.txt","r"); 
    integer bias_filep1   = $fopen("/home/lavanya/testcases/custom_fft_benchmark16x16_4/layer5_elem_sqrt2d6/data/output.txt","r"); 
    
    integer simd_file1    = $fopen("/home/lavanya/testcases/custom_fft_benchmark16x16_4/layer5_elem_sqrt2d6/data/add_6_11Y.txt","r");
    integer simd_file2    = $fopen("/home/lavanya/testcases/custom_fft_benchmark16x16_4/layer5_elem_sqrt2d6/data/add_6_11Y.txt","r");
`endif
