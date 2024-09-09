#ifdef FPGA_sac_fused1
std::string instruction_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer0_gemm_relu1/gemm_relu1_decimal.txt";
std::string output_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer0_gemm_relu1/data/_Relu_output_0_Y.txt";
std::string bias_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer0_gemm_relu1/data/linear1.bias.txt";
std::string weight_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer0_gemm_relu1/data/linear1.weight/linear1.weight_shuffled.txt";
std::string input_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer0_gemm_relu1/data/onnx_Gemm_0_A/onnx_Gemm_0_A_shuffled.txt";
std::string simd_input_file1 = "";
std::string simd_input_file2 = "";

#define ADDR_OFFSET_INPUT 180224
#define ADDR_OFFSET_WEIGHT 16384
#define ADDR_OFFSET_BIAS 81920
#define ADDR_OFFSET_OUTPUT 0
#define MAX_OFFSET_SYSTOLIC 180224

#define ADDR_OFFSET_VMEM1 176128
#define ADDR_OFFSET_VMEM2 0
#define ADDR_OFFSET_VMEM1_LD 0
#define ADDR_OFFSET_VMEM2_LD 0
#define MAX_OFFSET_SIMD 176128

#define NUM_INSTRUCTION 764 // this has to be in bytes as it is used by hardware. Or change hardware
#define NUM_INPUT 512
#define NUM_WEIGHT 65536
#define NUM_BIAS 256
#define NUM_OUTPUT 512

#elif FPGA_sac_fused2
std::string instruction_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer1_gemm_relu2/gemm_relu2_decimal.txt";
std::string output_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer1_gemm_relu2/data/_Relu_1_output_0_Y.txt";
std::string bias_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer1_gemm_relu2/data/linear2.bias.txt";
std::string weight_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer1_gemm_relu2/data/linear2.weight/linear2.weight_shuffled.txt";
std::string input_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer1_gemm_relu2/data/_Relu_output_0_Y/_Relu_output_0_Y_shuffled.txt";
std::string simd_input_file1 = "";
std::string simd_input_file2 = "";

#define ADDR_OFFSET_INPUT 176128
#define ADDR_OFFSET_WEIGHT 98304
#define ADDR_OFFSET_BIAS 86016
#define ADDR_OFFSET_OUTPUT 0
#define MAX_OFFSET_SYSTOLIC 176128

#define ADDR_OFFSET_VMEM1 172032
#define ADDR_OFFSET_VMEM2 0
#define ADDR_OFFSET_VMEM1_LD 0
#define ADDR_OFFSET_VMEM2_LD 0
#define MAX_OFFSET_SIMD 172032

#define NUM_INSTRUCTION 764 // this has to be in bytes as it is used by hardware. Or change hardware
#define NUM_INPUT 512
#define NUM_WEIGHT 65536
#define NUM_BIAS 256
#define NUM_OUTPUT 512

#elif FPGA_sac_gemm3
std::string instruction_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer2_gemm3/gemm3_decimal.txt";
std::string output_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer2_gemm3/data/_nu_gemm_13Y.txt";
std::string bias_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer2_gemm3/data/nu.bias.txt";
std::string weight_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer2_gemm3/data/nu.weight/nu.weight_shuffled.txt";
std::string input_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer2_gemm3/data/_Relu_1_output_0_Y/_Relu_1_output_0_Y_shuffled.txt";
std::string simd_input_file1 = "";
std::string simd_input_file2 = "";

#define ADDR_OFFSET_INPUT 172032
#define ADDR_OFFSET_WEIGHT 163840
#define ADDR_OFFSET_BIAS 167936
#define ADDR_OFFSET_OUTPUT 0
#define MAX_OFFSET_SYSTOLIC 172032

#define ADDR_OFFSET_VMEM1 176128
#define ADDR_OFFSET_VMEM2 0
#define ADDR_OFFSET_VMEM1_LD 0
#define ADDR_OFFSET_VMEM2_LD 0
#define MAX_OFFSET_SIMD 176128

#define NUM_INSTRUCTION 692 // this has to be in bytes as it is used by hardware. Or change hardware
#define NUM_INPUT 512
#define NUM_WEIGHT 4096
#define NUM_BIAS 16
#define NUM_OUTPUT 32

#elif FPGA_sac_gemm4
std::string instruction_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer3_gemm4/gemm4_decimal.txt";
std::string output_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer3_gemm4/data/_prob_gemm_14Y.txt";
std::string bias_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer3_gemm4/data/prob.bias.txt";
std::string weight_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer3_gemm4/data/prob.weight/prob.weight_shuffled.txt";
std::string input_file  = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/layer3_gemm4/data/_Relu_1_output_0_Y/_Relu_1_output_0_Y_shuffled.txt";
std::string simd_input_file1 = "";
std::string simd_input_file2 = "";

#define ADDR_OFFSET_INPUT 172032
#define ADDR_OFFSET_WEIGHT 90112
#define ADDR_OFFSET_BIAS 94208
#define ADDR_OFFSET_OUTPUT 0
#define MAX_OFFSET_SYSTOLIC 172032

#define ADDR_OFFSET_VMEM1 176128
#define ADDR_OFFSET_VMEM2 0
#define ADDR_OFFSET_VMEM1_LD 0
#define ADDR_OFFSET_VMEM2_LD 0
#define MAX_OFFSET_SIMD 176128

#define NUM_INSTRUCTION 692 // this has to be in bytes as it is used by hardware. Or change hardware
#define NUM_INPUT 512
#define NUM_WEIGHT 4096
#define NUM_BIAS 16
#define NUM_OUTPUT 32

#elif FPGA_sac_b2b
#define NUM_LAYER 4
std::string data_info_file = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/program/sac_batch_size_2_operand_storage_info.json";
std::string test_path = REPO_PATH+"sac_batch_size_2_withgemmrequantbenchmark4x4_withgemmrequant_off_by_one_fix/";
std::string base_path = REPO_PATH;

#else
std::string instruction_file  = "/home/rohan/genesys-merged-repo/testcases/resnet50_1_conv_case106/resnet50_1_conv_decimal.txt";
std::string input_file        = "/home/rohan/genesys-merged-repo/testcases/resnet50_1_conv_case106/input_shuffled.txt";
std::string bias_file         = "/home/rohan/genesys-merged-repo/testcases/resnet50_1_conv_case106/bias.txt";
std::string weight_file       = "/home/rohan/genesys-merged-repo/testcases/resnet50_1_conv_case106/weights_shuffled.txt";
std::string output_file       = "/home/rohan/genesys-merged-repo/testcases/resnet50_1_conv_case106/output.txt";
#endif
