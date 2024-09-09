#include <systemc>
#include <iostream>
#include <cstdlib>
#include <cstddef>
#include <stdint.h>
#include "SysCFileHandler.h"
#include "ap_int.h"
#include "ap_fixed.h"
#include <complex>
#include <stdbool.h>
#include "autopilot_cbe.h"
#include "hls_stream.h"
#include "hls_half.h"
#include "hls_signal_handler.h"

using namespace std;
using namespace sc_core;
using namespace sc_dt;

// wrapc file define:
#define AUTOTB_TVIN_m00_imem_axi "../tv/cdatafile/c.systolic_fpga.autotvin_m00_imem_axi.dat"
#define AUTOTB_TVOUT_m00_imem_axi "../tv/cdatafile/c.systolic_fpga.autotvout_m00_imem_axi.dat"
// wrapc file define:
#define AUTOTB_TVIN_m01_parambuf_axi "../tv/cdatafile/c.systolic_fpga.autotvin_m01_parambuf_axi.dat"
#define AUTOTB_TVOUT_m01_parambuf_axi "../tv/cdatafile/c.systolic_fpga.autotvout_m01_parambuf_axi.dat"
// wrapc file define:
#define AUTOTB_TVIN_m02_ibuf_axi "../tv/cdatafile/c.systolic_fpga.autotvin_m02_ibuf_axi.dat"
#define AUTOTB_TVOUT_m02_ibuf_axi "../tv/cdatafile/c.systolic_fpga.autotvout_m02_ibuf_axi.dat"
// wrapc file define:
#define AUTOTB_TVIN_m03_obuf_axi "../tv/cdatafile/c.systolic_fpga.autotvin_m03_obuf_axi.dat"
#define AUTOTB_TVOUT_m03_obuf_axi "../tv/cdatafile/c.systolic_fpga.autotvout_m03_obuf_axi.dat"
// wrapc file define:
#define AUTOTB_TVIN_slv_reg0_out "../tv/cdatafile/c.systolic_fpga.autotvin_slv_reg0_out.dat"
#define AUTOTB_TVOUT_slv_reg0_out "../tv/cdatafile/c.systolic_fpga.autotvout_slv_reg0_out.dat"
// wrapc file define:
#define AUTOTB_TVIN_slv_reg1_out "../tv/cdatafile/c.systolic_fpga.autotvin_slv_reg1_out.dat"
#define AUTOTB_TVOUT_slv_reg1_out "../tv/cdatafile/c.systolic_fpga.autotvout_slv_reg1_out.dat"
// wrapc file define:
#define AUTOTB_TVIN_slv_reg2_out "../tv/cdatafile/c.systolic_fpga.autotvin_slv_reg2_out.dat"
#define AUTOTB_TVOUT_slv_reg2_out "../tv/cdatafile/c.systolic_fpga.autotvout_slv_reg2_out.dat"
// wrapc file define:
#define AUTOTB_TVIN_slv_reg3_out "../tv/cdatafile/c.systolic_fpga.autotvin_slv_reg3_out.dat"
#define AUTOTB_TVOUT_slv_reg3_out "../tv/cdatafile/c.systolic_fpga.autotvout_slv_reg3_out.dat"
// wrapc file define:
#define AUTOTB_TVIN_slv_reg4_out "../tv/cdatafile/c.systolic_fpga.autotvin_slv_reg4_out.dat"
#define AUTOTB_TVOUT_slv_reg4_out "../tv/cdatafile/c.systolic_fpga.autotvout_slv_reg4_out.dat"
// wrapc file define:
#define AUTOTB_TVIN_slv_reg5_out "../tv/cdatafile/c.systolic_fpga.autotvin_slv_reg5_out.dat"
#define AUTOTB_TVOUT_slv_reg5_out "../tv/cdatafile/c.systolic_fpga.autotvout_slv_reg5_out.dat"
// wrapc file define:
#define AUTOTB_TVIN_slv_reg6_out "../tv/cdatafile/c.systolic_fpga.autotvin_slv_reg6_out.dat"
#define AUTOTB_TVOUT_slv_reg6_out "../tv/cdatafile/c.systolic_fpga.autotvout_slv_reg6_out.dat"
// wrapc file define:
#define AUTOTB_TVIN_slv_reg7_out "../tv/cdatafile/c.systolic_fpga.autotvin_slv_reg7_out.dat"
#define AUTOTB_TVOUT_slv_reg7_out "../tv/cdatafile/c.systolic_fpga.autotvout_slv_reg7_out.dat"
// wrapc file define:
#define AUTOTB_TVIN_slv_reg8_out "../tv/cdatafile/c.systolic_fpga.autotvin_slv_reg8_out.dat"
#define AUTOTB_TVOUT_slv_reg8_out "../tv/cdatafile/c.systolic_fpga.autotvout_slv_reg8_out.dat"
// wrapc file define:
#define AUTOTB_TVIN_slv_reg9_out "../tv/cdatafile/c.systolic_fpga.autotvin_slv_reg9_out.dat"
#define AUTOTB_TVOUT_slv_reg9_out "../tv/cdatafile/c.systolic_fpga.autotvout_slv_reg9_out.dat"
// wrapc file define:
#define AUTOTB_TVIN_slv_reg10_out "../tv/cdatafile/c.systolic_fpga.autotvin_slv_reg10_out.dat"
#define AUTOTB_TVOUT_slv_reg10_out "../tv/cdatafile/c.systolic_fpga.autotvout_slv_reg10_out.dat"
// wrapc file define:
#define AUTOTB_TVIN_slv_reg11_out "../tv/cdatafile/c.systolic_fpga.autotvin_slv_reg11_out.dat"
#define AUTOTB_TVOUT_slv_reg11_out "../tv/cdatafile/c.systolic_fpga.autotvout_slv_reg11_out.dat"
// wrapc file define:
#define AUTOTB_TVIN_slv_reg12_out "../tv/cdatafile/c.systolic_fpga.autotvin_slv_reg12_out.dat"
#define AUTOTB_TVOUT_slv_reg12_out "../tv/cdatafile/c.systolic_fpga.autotvout_slv_reg12_out.dat"
// wrapc file define:
#define AUTOTB_TVIN_slv_reg13_out "../tv/cdatafile/c.systolic_fpga.autotvin_slv_reg13_out.dat"
#define AUTOTB_TVOUT_slv_reg13_out "../tv/cdatafile/c.systolic_fpga.autotvout_slv_reg13_out.dat"
// wrapc file define:
#define AUTOTB_TVIN_slv_reg14_out "../tv/cdatafile/c.systolic_fpga.autotvin_slv_reg14_out.dat"
#define AUTOTB_TVOUT_slv_reg14_out "../tv/cdatafile/c.systolic_fpga.autotvout_slv_reg14_out.dat"
// wrapc file define:
#define AUTOTB_TVIN_axi00_imem_ptr0 "../tv/cdatafile/c.systolic_fpga.autotvin_axi00_imem_ptr0.dat"
#define AUTOTB_TVOUT_axi00_imem_ptr0 "../tv/cdatafile/c.systolic_fpga.autotvout_axi00_imem_ptr0.dat"
// wrapc file define:
#define AUTOTB_TVIN_axi01_parambuf_ptr0 "../tv/cdatafile/c.systolic_fpga.autotvin_axi01_parambuf_ptr0.dat"
#define AUTOTB_TVOUT_axi01_parambuf_ptr0 "../tv/cdatafile/c.systolic_fpga.autotvout_axi01_parambuf_ptr0.dat"
// wrapc file define:
#define AUTOTB_TVIN_axi02_ibuf_ptr0 "../tv/cdatafile/c.systolic_fpga.autotvin_axi02_ibuf_ptr0.dat"
#define AUTOTB_TVOUT_axi02_ibuf_ptr0 "../tv/cdatafile/c.systolic_fpga.autotvout_axi02_ibuf_ptr0.dat"
// wrapc file define:
#define AUTOTB_TVIN_axi03_obuf_ptr0 "../tv/cdatafile/c.systolic_fpga.autotvin_axi03_obuf_ptr0.dat"
#define AUTOTB_TVOUT_axi03_obuf_ptr0 "../tv/cdatafile/c.systolic_fpga.autotvout_axi03_obuf_ptr0.dat"

#define INTER_TCL "../tv/cdatafile/ref.tcl"

// tvout file define:
#define AUTOTB_TVOUT_PC_m00_imem_axi "../tv/rtldatafile/rtl.systolic_fpga.autotvout_m00_imem_axi.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_m01_parambuf_axi "../tv/rtldatafile/rtl.systolic_fpga.autotvout_m01_parambuf_axi.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_m02_ibuf_axi "../tv/rtldatafile/rtl.systolic_fpga.autotvout_m02_ibuf_axi.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_m03_obuf_axi "../tv/rtldatafile/rtl.systolic_fpga.autotvout_m03_obuf_axi.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_slv_reg0_out "../tv/rtldatafile/rtl.systolic_fpga.autotvout_slv_reg0_out.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_slv_reg1_out "../tv/rtldatafile/rtl.systolic_fpga.autotvout_slv_reg1_out.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_slv_reg2_out "../tv/rtldatafile/rtl.systolic_fpga.autotvout_slv_reg2_out.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_slv_reg3_out "../tv/rtldatafile/rtl.systolic_fpga.autotvout_slv_reg3_out.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_slv_reg4_out "../tv/rtldatafile/rtl.systolic_fpga.autotvout_slv_reg4_out.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_slv_reg5_out "../tv/rtldatafile/rtl.systolic_fpga.autotvout_slv_reg5_out.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_slv_reg6_out "../tv/rtldatafile/rtl.systolic_fpga.autotvout_slv_reg6_out.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_slv_reg7_out "../tv/rtldatafile/rtl.systolic_fpga.autotvout_slv_reg7_out.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_slv_reg8_out "../tv/rtldatafile/rtl.systolic_fpga.autotvout_slv_reg8_out.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_slv_reg9_out "../tv/rtldatafile/rtl.systolic_fpga.autotvout_slv_reg9_out.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_slv_reg10_out "../tv/rtldatafile/rtl.systolic_fpga.autotvout_slv_reg10_out.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_slv_reg11_out "../tv/rtldatafile/rtl.systolic_fpga.autotvout_slv_reg11_out.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_slv_reg12_out "../tv/rtldatafile/rtl.systolic_fpga.autotvout_slv_reg12_out.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_slv_reg13_out "../tv/rtldatafile/rtl.systolic_fpga.autotvout_slv_reg13_out.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_slv_reg14_out "../tv/rtldatafile/rtl.systolic_fpga.autotvout_slv_reg14_out.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_axi00_imem_ptr0 "../tv/rtldatafile/rtl.systolic_fpga.autotvout_axi00_imem_ptr0.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_axi01_parambuf_ptr0 "../tv/rtldatafile/rtl.systolic_fpga.autotvout_axi01_parambuf_ptr0.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_axi02_ibuf_ptr0 "../tv/rtldatafile/rtl.systolic_fpga.autotvout_axi02_ibuf_ptr0.dat"
// tvout file define:
#define AUTOTB_TVOUT_PC_axi03_obuf_ptr0 "../tv/rtldatafile/rtl.systolic_fpga.autotvout_axi03_obuf_ptr0.dat"

class INTER_TCL_FILE {
  public:
INTER_TCL_FILE(const char* name) {
  mName = name; 
  m00_imem_axi_depth = 0;
  m01_parambuf_axi_depth = 0;
  m02_ibuf_axi_depth = 0;
  m03_obuf_axi_depth = 0;
  slv_reg0_out_depth = 0;
  slv_reg1_out_depth = 0;
  slv_reg2_out_depth = 0;
  slv_reg3_out_depth = 0;
  slv_reg4_out_depth = 0;
  slv_reg5_out_depth = 0;
  slv_reg6_out_depth = 0;
  slv_reg7_out_depth = 0;
  slv_reg8_out_depth = 0;
  slv_reg9_out_depth = 0;
  slv_reg10_out_depth = 0;
  slv_reg11_out_depth = 0;
  slv_reg12_out_depth = 0;
  slv_reg13_out_depth = 0;
  slv_reg14_out_depth = 0;
  axi00_imem_ptr0_depth = 0;
  axi01_parambuf_ptr0_depth = 0;
  axi02_ibuf_ptr0_depth = 0;
  axi03_obuf_ptr0_depth = 0;
  trans_num =0;
}
~INTER_TCL_FILE() {
  mFile.open(mName);
  if (!mFile.good()) {
    cout << "Failed to open file ref.tcl" << endl;
    exit (1); 
  }
  string total_list = get_depth_list();
  mFile << "set depth_list {\n";
  mFile << total_list;
  mFile << "}\n";
  mFile << "set trans_num "<<trans_num<<endl;
  mFile.close();
}
string get_depth_list () {
  stringstream total_list;
  total_list << "{m00_imem_axi " << m00_imem_axi_depth << "}\n";
  total_list << "{m01_parambuf_axi " << m01_parambuf_axi_depth << "}\n";
  total_list << "{m02_ibuf_axi " << m02_ibuf_axi_depth << "}\n";
  total_list << "{m03_obuf_axi " << m03_obuf_axi_depth << "}\n";
  total_list << "{slv_reg0_out " << slv_reg0_out_depth << "}\n";
  total_list << "{slv_reg1_out " << slv_reg1_out_depth << "}\n";
  total_list << "{slv_reg2_out " << slv_reg2_out_depth << "}\n";
  total_list << "{slv_reg3_out " << slv_reg3_out_depth << "}\n";
  total_list << "{slv_reg4_out " << slv_reg4_out_depth << "}\n";
  total_list << "{slv_reg5_out " << slv_reg5_out_depth << "}\n";
  total_list << "{slv_reg6_out " << slv_reg6_out_depth << "}\n";
  total_list << "{slv_reg7_out " << slv_reg7_out_depth << "}\n";
  total_list << "{slv_reg8_out " << slv_reg8_out_depth << "}\n";
  total_list << "{slv_reg9_out " << slv_reg9_out_depth << "}\n";
  total_list << "{slv_reg10_out " << slv_reg10_out_depth << "}\n";
  total_list << "{slv_reg11_out " << slv_reg11_out_depth << "}\n";
  total_list << "{slv_reg12_out " << slv_reg12_out_depth << "}\n";
  total_list << "{slv_reg13_out " << slv_reg13_out_depth << "}\n";
  total_list << "{slv_reg14_out " << slv_reg14_out_depth << "}\n";
  total_list << "{axi00_imem_ptr0 " << axi00_imem_ptr0_depth << "}\n";
  total_list << "{axi01_parambuf_ptr0 " << axi01_parambuf_ptr0_depth << "}\n";
  total_list << "{axi02_ibuf_ptr0 " << axi02_ibuf_ptr0_depth << "}\n";
  total_list << "{axi03_obuf_ptr0 " << axi03_obuf_ptr0_depth << "}\n";
  return total_list.str();
}
void set_num (int num , int* class_num) {
  (*class_num) = (*class_num) > num ? (*class_num) : num;
}
void set_string(std::string list, std::string* class_list) {
  (*class_list) = list;
}
  public:
    int m00_imem_axi_depth;
    int m01_parambuf_axi_depth;
    int m02_ibuf_axi_depth;
    int m03_obuf_axi_depth;
    int slv_reg0_out_depth;
    int slv_reg1_out_depth;
    int slv_reg2_out_depth;
    int slv_reg3_out_depth;
    int slv_reg4_out_depth;
    int slv_reg5_out_depth;
    int slv_reg6_out_depth;
    int slv_reg7_out_depth;
    int slv_reg8_out_depth;
    int slv_reg9_out_depth;
    int slv_reg10_out_depth;
    int slv_reg11_out_depth;
    int slv_reg12_out_depth;
    int slv_reg13_out_depth;
    int slv_reg14_out_depth;
    int axi00_imem_ptr0_depth;
    int axi01_parambuf_ptr0_depth;
    int axi02_ibuf_ptr0_depth;
    int axi03_obuf_ptr0_depth;
    int trans_num;
  private:
    ofstream mFile;
    const char* mName;
};

static void RTLOutputCheckAndReplacement(std::string &AESL_token, std::string PortName) {
  bool no_x = false;
  bool err = false;

  no_x = false;
  // search and replace 'X' with '0' from the 3rd char of token
  while (!no_x) {
    size_t x_found = AESL_token.find('X', 0);
    if (x_found != string::npos) {
      if (!err) { 
        cerr << "WARNING: [SIM 212-201] RTL produces unknown value 'X' on port" 
             << PortName << ", possible cause: There are uninitialized variables in the C design."
             << endl; 
        err = true;
      }
      AESL_token.replace(x_found, 1, "0");
    } else
      no_x = true;
  }
  no_x = false;
  // search and replace 'x' with '0' from the 3rd char of token
  while (!no_x) {
    size_t x_found = AESL_token.find('x', 2);
    if (x_found != string::npos) {
      if (!err) { 
        cerr << "WARNING: [SIM 212-201] RTL produces unknown value 'x' on port" 
             << PortName << ", possible cause: There are uninitialized variables in the C design."
             << endl; 
        err = true;
      }
      AESL_token.replace(x_found, 1, "0");
    } else
      no_x = true;
  }
}
struct __cosim_s40__ { char data[64]; };
extern "C" void systolic_fpga_hw_stub_wrapper(int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, volatile void *, volatile void *, volatile void *, volatile void *);

extern "C" void apatb_systolic_fpga_hw(int __xlx_apatb_param_slv_reg0_out, int __xlx_apatb_param_slv_reg1_out, int __xlx_apatb_param_slv_reg2_out, int __xlx_apatb_param_slv_reg3_out, int __xlx_apatb_param_slv_reg4_out, int __xlx_apatb_param_slv_reg5_out, int __xlx_apatb_param_slv_reg6_out, int __xlx_apatb_param_slv_reg7_out, int __xlx_apatb_param_slv_reg8_out, int __xlx_apatb_param_slv_reg9_out, int __xlx_apatb_param_slv_reg10_out, int __xlx_apatb_param_slv_reg11_out, int __xlx_apatb_param_slv_reg12_out, int __xlx_apatb_param_slv_reg13_out, int __xlx_apatb_param_slv_reg14_out, volatile void * __xlx_apatb_param_axi00_imem_ptr0, volatile void * __xlx_apatb_param_axi01_parambuf_ptr0, volatile void * __xlx_apatb_param_axi02_ibuf_ptr0, volatile void * __xlx_apatb_param_axi03_obuf_ptr0) {
  refine_signal_handler();
  fstream wrapc_switch_file_token;
  wrapc_switch_file_token.open(".hls_cosim_wrapc_switch.log");
  int AESL_i;
  if (wrapc_switch_file_token.good())
  {

    CodeState = ENTER_WRAPC_PC;
    static unsigned AESL_transaction_pc = 0;
    string AESL_token;
    string AESL_num;{
      static ifstream rtl_tv_out_file;
      if (!rtl_tv_out_file.is_open()) {
        rtl_tv_out_file.open(AUTOTB_TVOUT_PC_m00_imem_axi);
        if (rtl_tv_out_file.good()) {
          rtl_tv_out_file >> AESL_token;
          if (AESL_token != "[[[runtime]]]")
            exit(1);
        }
      }
  
      if (rtl_tv_out_file.good()) {
        rtl_tv_out_file >> AESL_token; 
        rtl_tv_out_file >> AESL_num;  // transaction number
        if (AESL_token != "[[transaction]]") {
          cerr << "Unexpected token: " << AESL_token << endl;
          exit(1);
        }
        if (atoi(AESL_num.c_str()) == AESL_transaction_pc) {
          std::vector<sc_bv<512> > m00_imem_axi_pc_buffer(1);
          int i = 0;

          rtl_tv_out_file >> AESL_token; //data
          while (AESL_token != "[[/transaction]]"){

            RTLOutputCheckAndReplacement(AESL_token, "m00_imem_axi");
  
            // push token into output port buffer
            if (AESL_token != "") {
              m00_imem_axi_pc_buffer[i] = AESL_token.c_str();;
              i++;
            }
  
            rtl_tv_out_file >> AESL_token; //data or [[/transaction]]
            if (AESL_token == "[[[/runtime]]]" || rtl_tv_out_file.eof())
              exit(1);
          }
          if (i > 0) {{
            int i = 0;
            for (int j = 0, e = 1; j < e; j += 1, ++i) {((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+0] = m00_imem_axi_pc_buffer[i].range(63,0).to_int64();
((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+1] = m00_imem_axi_pc_buffer[i].range(127,64).to_int64();
((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+2] = m00_imem_axi_pc_buffer[i].range(191,128).to_int64();
((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+3] = m00_imem_axi_pc_buffer[i].range(255,192).to_int64();
((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+4] = m00_imem_axi_pc_buffer[i].range(319,256).to_int64();
((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+5] = m00_imem_axi_pc_buffer[i].range(383,320).to_int64();
((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+6] = m00_imem_axi_pc_buffer[i].range(447,384).to_int64();
((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+7] = m00_imem_axi_pc_buffer[i].range(511,448).to_int64();
}}}
        } // end transaction
      } // end file is good
    } // end post check logic bolck
  {
      static ifstream rtl_tv_out_file;
      if (!rtl_tv_out_file.is_open()) {
        rtl_tv_out_file.open(AUTOTB_TVOUT_PC_m01_parambuf_axi);
        if (rtl_tv_out_file.good()) {
          rtl_tv_out_file >> AESL_token;
          if (AESL_token != "[[[runtime]]]")
            exit(1);
        }
      }
  
      if (rtl_tv_out_file.good()) {
        rtl_tv_out_file >> AESL_token; 
        rtl_tv_out_file >> AESL_num;  // transaction number
        if (AESL_token != "[[transaction]]") {
          cerr << "Unexpected token: " << AESL_token << endl;
          exit(1);
        }
        if (atoi(AESL_num.c_str()) == AESL_transaction_pc) {
          std::vector<sc_bv<512> > m01_parambuf_axi_pc_buffer(1);
          int i = 0;

          rtl_tv_out_file >> AESL_token; //data
          while (AESL_token != "[[/transaction]]"){

            RTLOutputCheckAndReplacement(AESL_token, "m01_parambuf_axi");
  
            // push token into output port buffer
            if (AESL_token != "") {
              m01_parambuf_axi_pc_buffer[i] = AESL_token.c_str();;
              i++;
            }
  
            rtl_tv_out_file >> AESL_token; //data or [[/transaction]]
            if (AESL_token == "[[[/runtime]]]" || rtl_tv_out_file.eof())
              exit(1);
          }
          if (i > 0) {{
            int i = 0;
            for (int j = 0, e = 1; j < e; j += 1, ++i) {((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+0] = m01_parambuf_axi_pc_buffer[i].range(63,0).to_int64();
((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+1] = m01_parambuf_axi_pc_buffer[i].range(127,64).to_int64();
((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+2] = m01_parambuf_axi_pc_buffer[i].range(191,128).to_int64();
((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+3] = m01_parambuf_axi_pc_buffer[i].range(255,192).to_int64();
((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+4] = m01_parambuf_axi_pc_buffer[i].range(319,256).to_int64();
((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+5] = m01_parambuf_axi_pc_buffer[i].range(383,320).to_int64();
((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+6] = m01_parambuf_axi_pc_buffer[i].range(447,384).to_int64();
((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+7] = m01_parambuf_axi_pc_buffer[i].range(511,448).to_int64();
}}}
        } // end transaction
      } // end file is good
    } // end post check logic bolck
  {
      static ifstream rtl_tv_out_file;
      if (!rtl_tv_out_file.is_open()) {
        rtl_tv_out_file.open(AUTOTB_TVOUT_PC_m02_ibuf_axi);
        if (rtl_tv_out_file.good()) {
          rtl_tv_out_file >> AESL_token;
          if (AESL_token != "[[[runtime]]]")
            exit(1);
        }
      }
  
      if (rtl_tv_out_file.good()) {
        rtl_tv_out_file >> AESL_token; 
        rtl_tv_out_file >> AESL_num;  // transaction number
        if (AESL_token != "[[transaction]]") {
          cerr << "Unexpected token: " << AESL_token << endl;
          exit(1);
        }
        if (atoi(AESL_num.c_str()) == AESL_transaction_pc) {
          std::vector<sc_bv<512> > m02_ibuf_axi_pc_buffer(1);
          int i = 0;

          rtl_tv_out_file >> AESL_token; //data
          while (AESL_token != "[[/transaction]]"){

            RTLOutputCheckAndReplacement(AESL_token, "m02_ibuf_axi");
  
            // push token into output port buffer
            if (AESL_token != "") {
              m02_ibuf_axi_pc_buffer[i] = AESL_token.c_str();;
              i++;
            }
  
            rtl_tv_out_file >> AESL_token; //data or [[/transaction]]
            if (AESL_token == "[[[/runtime]]]" || rtl_tv_out_file.eof())
              exit(1);
          }
          if (i > 0) {{
            int i = 0;
            for (int j = 0, e = 1; j < e; j += 1, ++i) {((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+0] = m02_ibuf_axi_pc_buffer[i].range(63,0).to_int64();
((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+1] = m02_ibuf_axi_pc_buffer[i].range(127,64).to_int64();
((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+2] = m02_ibuf_axi_pc_buffer[i].range(191,128).to_int64();
((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+3] = m02_ibuf_axi_pc_buffer[i].range(255,192).to_int64();
((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+4] = m02_ibuf_axi_pc_buffer[i].range(319,256).to_int64();
((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+5] = m02_ibuf_axi_pc_buffer[i].range(383,320).to_int64();
((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+6] = m02_ibuf_axi_pc_buffer[i].range(447,384).to_int64();
((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+7] = m02_ibuf_axi_pc_buffer[i].range(511,448).to_int64();
}}}
        } // end transaction
      } // end file is good
    } // end post check logic bolck
  {
      static ifstream rtl_tv_out_file;
      if (!rtl_tv_out_file.is_open()) {
        rtl_tv_out_file.open(AUTOTB_TVOUT_PC_m03_obuf_axi);
        if (rtl_tv_out_file.good()) {
          rtl_tv_out_file >> AESL_token;
          if (AESL_token != "[[[runtime]]]")
            exit(1);
        }
      }
  
      if (rtl_tv_out_file.good()) {
        rtl_tv_out_file >> AESL_token; 
        rtl_tv_out_file >> AESL_num;  // transaction number
        if (AESL_token != "[[transaction]]") {
          cerr << "Unexpected token: " << AESL_token << endl;
          exit(1);
        }
        if (atoi(AESL_num.c_str()) == AESL_transaction_pc) {
          std::vector<sc_bv<512> > m03_obuf_axi_pc_buffer(1);
          int i = 0;

          rtl_tv_out_file >> AESL_token; //data
          while (AESL_token != "[[/transaction]]"){

            RTLOutputCheckAndReplacement(AESL_token, "m03_obuf_axi");
  
            // push token into output port buffer
            if (AESL_token != "") {
              m03_obuf_axi_pc_buffer[i] = AESL_token.c_str();;
              i++;
            }
  
            rtl_tv_out_file >> AESL_token; //data or [[/transaction]]
            if (AESL_token == "[[[/runtime]]]" || rtl_tv_out_file.eof())
              exit(1);
          }
          if (i > 0) {{
            int i = 0;
            for (int j = 0, e = 1; j < e; j += 1, ++i) {((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+0] = m03_obuf_axi_pc_buffer[i].range(63,0).to_int64();
((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+1] = m03_obuf_axi_pc_buffer[i].range(127,64).to_int64();
((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+2] = m03_obuf_axi_pc_buffer[i].range(191,128).to_int64();
((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+3] = m03_obuf_axi_pc_buffer[i].range(255,192).to_int64();
((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+4] = m03_obuf_axi_pc_buffer[i].range(319,256).to_int64();
((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+5] = m03_obuf_axi_pc_buffer[i].range(383,320).to_int64();
((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+6] = m03_obuf_axi_pc_buffer[i].range(447,384).to_int64();
((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+7] = m03_obuf_axi_pc_buffer[i].range(511,448).to_int64();
}}}
        } // end transaction
      } // end file is good
    } // end post check logic bolck
  
    AESL_transaction_pc++;
    return ;
  }
static unsigned AESL_transaction;
static AESL_FILE_HANDLER aesl_fh;
static INTER_TCL_FILE tcl_file(INTER_TCL);
std::vector<char> __xlx_sprintf_buffer(1024);
CodeState = ENTER_WRAPC;
//m00_imem_axi
aesl_fh.touch(AUTOTB_TVIN_m00_imem_axi);
aesl_fh.touch(AUTOTB_TVOUT_m00_imem_axi);
//m01_parambuf_axi
aesl_fh.touch(AUTOTB_TVIN_m01_parambuf_axi);
aesl_fh.touch(AUTOTB_TVOUT_m01_parambuf_axi);
//m02_ibuf_axi
aesl_fh.touch(AUTOTB_TVIN_m02_ibuf_axi);
aesl_fh.touch(AUTOTB_TVOUT_m02_ibuf_axi);
//m03_obuf_axi
aesl_fh.touch(AUTOTB_TVIN_m03_obuf_axi);
aesl_fh.touch(AUTOTB_TVOUT_m03_obuf_axi);
//slv_reg0_out
aesl_fh.touch(AUTOTB_TVIN_slv_reg0_out);
aesl_fh.touch(AUTOTB_TVOUT_slv_reg0_out);
//slv_reg1_out
aesl_fh.touch(AUTOTB_TVIN_slv_reg1_out);
aesl_fh.touch(AUTOTB_TVOUT_slv_reg1_out);
//slv_reg2_out
aesl_fh.touch(AUTOTB_TVIN_slv_reg2_out);
aesl_fh.touch(AUTOTB_TVOUT_slv_reg2_out);
//slv_reg3_out
aesl_fh.touch(AUTOTB_TVIN_slv_reg3_out);
aesl_fh.touch(AUTOTB_TVOUT_slv_reg3_out);
//slv_reg4_out
aesl_fh.touch(AUTOTB_TVIN_slv_reg4_out);
aesl_fh.touch(AUTOTB_TVOUT_slv_reg4_out);
//slv_reg5_out
aesl_fh.touch(AUTOTB_TVIN_slv_reg5_out);
aesl_fh.touch(AUTOTB_TVOUT_slv_reg5_out);
//slv_reg6_out
aesl_fh.touch(AUTOTB_TVIN_slv_reg6_out);
aesl_fh.touch(AUTOTB_TVOUT_slv_reg6_out);
//slv_reg7_out
aesl_fh.touch(AUTOTB_TVIN_slv_reg7_out);
aesl_fh.touch(AUTOTB_TVOUT_slv_reg7_out);
//slv_reg8_out
aesl_fh.touch(AUTOTB_TVIN_slv_reg8_out);
aesl_fh.touch(AUTOTB_TVOUT_slv_reg8_out);
//slv_reg9_out
aesl_fh.touch(AUTOTB_TVIN_slv_reg9_out);
aesl_fh.touch(AUTOTB_TVOUT_slv_reg9_out);
//slv_reg10_out
aesl_fh.touch(AUTOTB_TVIN_slv_reg10_out);
aesl_fh.touch(AUTOTB_TVOUT_slv_reg10_out);
//slv_reg11_out
aesl_fh.touch(AUTOTB_TVIN_slv_reg11_out);
aesl_fh.touch(AUTOTB_TVOUT_slv_reg11_out);
//slv_reg12_out
aesl_fh.touch(AUTOTB_TVIN_slv_reg12_out);
aesl_fh.touch(AUTOTB_TVOUT_slv_reg12_out);
//slv_reg13_out
aesl_fh.touch(AUTOTB_TVIN_slv_reg13_out);
aesl_fh.touch(AUTOTB_TVOUT_slv_reg13_out);
//slv_reg14_out
aesl_fh.touch(AUTOTB_TVIN_slv_reg14_out);
aesl_fh.touch(AUTOTB_TVOUT_slv_reg14_out);
//axi00_imem_ptr0
aesl_fh.touch(AUTOTB_TVIN_axi00_imem_ptr0);
aesl_fh.touch(AUTOTB_TVOUT_axi00_imem_ptr0);
//axi01_parambuf_ptr0
aesl_fh.touch(AUTOTB_TVIN_axi01_parambuf_ptr0);
aesl_fh.touch(AUTOTB_TVOUT_axi01_parambuf_ptr0);
//axi02_ibuf_ptr0
aesl_fh.touch(AUTOTB_TVIN_axi02_ibuf_ptr0);
aesl_fh.touch(AUTOTB_TVOUT_axi02_ibuf_ptr0);
//axi03_obuf_ptr0
aesl_fh.touch(AUTOTB_TVIN_axi03_obuf_ptr0);
aesl_fh.touch(AUTOTB_TVOUT_axi03_obuf_ptr0);
CodeState = DUMP_INPUTS;
unsigned __xlx_offset_byte_param_axi00_imem_ptr0 = 0;
// print m00_imem_axi Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_m00_imem_axi, __xlx_sprintf_buffer.data());
  {  __xlx_offset_byte_param_axi00_imem_ptr0 = 0*64;
  if (__xlx_apatb_param_axi00_imem_ptr0) {
    for (int j = 0  - 0, e = 1 - 0; j != e; ++j) {
sc_bv<512> __xlx_tmp_lv;
__xlx_tmp_lv.range(63,0) = ((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+0];
__xlx_tmp_lv.range(127,64) = ((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+1];
__xlx_tmp_lv.range(191,128) = ((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+2];
__xlx_tmp_lv.range(255,192) = ((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+3];
__xlx_tmp_lv.range(319,256) = ((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+4];
__xlx_tmp_lv.range(383,320) = ((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+5];
__xlx_tmp_lv.range(447,384) = ((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+6];
__xlx_tmp_lv.range(511,448) = ((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+7];

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_m00_imem_axi, __xlx_sprintf_buffer.data()); 
      }
  }
}
  tcl_file.set_num(1, &tcl_file.m00_imem_axi_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_m00_imem_axi, __xlx_sprintf_buffer.data());
}
unsigned __xlx_offset_byte_param_axi01_parambuf_ptr0 = 0;
// print m01_parambuf_axi Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_m01_parambuf_axi, __xlx_sprintf_buffer.data());
  {  __xlx_offset_byte_param_axi01_parambuf_ptr0 = 0*64;
  if (__xlx_apatb_param_axi01_parambuf_ptr0) {
    for (int j = 0  - 0, e = 1 - 0; j != e; ++j) {
sc_bv<512> __xlx_tmp_lv;
__xlx_tmp_lv.range(63,0) = ((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+0];
__xlx_tmp_lv.range(127,64) = ((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+1];
__xlx_tmp_lv.range(191,128) = ((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+2];
__xlx_tmp_lv.range(255,192) = ((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+3];
__xlx_tmp_lv.range(319,256) = ((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+4];
__xlx_tmp_lv.range(383,320) = ((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+5];
__xlx_tmp_lv.range(447,384) = ((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+6];
__xlx_tmp_lv.range(511,448) = ((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+7];

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_m01_parambuf_axi, __xlx_sprintf_buffer.data()); 
      }
  }
}
  tcl_file.set_num(1, &tcl_file.m01_parambuf_axi_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_m01_parambuf_axi, __xlx_sprintf_buffer.data());
}
unsigned __xlx_offset_byte_param_axi02_ibuf_ptr0 = 0;
// print m02_ibuf_axi Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_m02_ibuf_axi, __xlx_sprintf_buffer.data());
  {  __xlx_offset_byte_param_axi02_ibuf_ptr0 = 0*64;
  if (__xlx_apatb_param_axi02_ibuf_ptr0) {
    for (int j = 0  - 0, e = 1 - 0; j != e; ++j) {
sc_bv<512> __xlx_tmp_lv;
__xlx_tmp_lv.range(63,0) = ((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+0];
__xlx_tmp_lv.range(127,64) = ((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+1];
__xlx_tmp_lv.range(191,128) = ((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+2];
__xlx_tmp_lv.range(255,192) = ((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+3];
__xlx_tmp_lv.range(319,256) = ((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+4];
__xlx_tmp_lv.range(383,320) = ((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+5];
__xlx_tmp_lv.range(447,384) = ((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+6];
__xlx_tmp_lv.range(511,448) = ((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+7];

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_m02_ibuf_axi, __xlx_sprintf_buffer.data()); 
      }
  }
}
  tcl_file.set_num(1, &tcl_file.m02_ibuf_axi_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_m02_ibuf_axi, __xlx_sprintf_buffer.data());
}
unsigned __xlx_offset_byte_param_axi03_obuf_ptr0 = 0;
// print m03_obuf_axi Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_m03_obuf_axi, __xlx_sprintf_buffer.data());
  {  __xlx_offset_byte_param_axi03_obuf_ptr0 = 0*64;
  if (__xlx_apatb_param_axi03_obuf_ptr0) {
    for (int j = 0  - 0, e = 1 - 0; j != e; ++j) {
sc_bv<512> __xlx_tmp_lv;
__xlx_tmp_lv.range(63,0) = ((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+0];
__xlx_tmp_lv.range(127,64) = ((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+1];
__xlx_tmp_lv.range(191,128) = ((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+2];
__xlx_tmp_lv.range(255,192) = ((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+3];
__xlx_tmp_lv.range(319,256) = ((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+4];
__xlx_tmp_lv.range(383,320) = ((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+5];
__xlx_tmp_lv.range(447,384) = ((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+6];
__xlx_tmp_lv.range(511,448) = ((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+7];

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_m03_obuf_axi, __xlx_sprintf_buffer.data()); 
      }
  }
}
  tcl_file.set_num(1, &tcl_file.m03_obuf_axi_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_m03_obuf_axi, __xlx_sprintf_buffer.data());
}
// print slv_reg0_out Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_slv_reg0_out, __xlx_sprintf_buffer.data());
  {
    sc_bv<32> __xlx_tmp_lv = *((int*)&__xlx_apatb_param_slv_reg0_out);

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_slv_reg0_out, __xlx_sprintf_buffer.data()); 
  }
  tcl_file.set_num(1, &tcl_file.slv_reg0_out_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_slv_reg0_out, __xlx_sprintf_buffer.data());
}
// print slv_reg1_out Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_slv_reg1_out, __xlx_sprintf_buffer.data());
  {
    sc_bv<32> __xlx_tmp_lv = *((int*)&__xlx_apatb_param_slv_reg1_out);

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_slv_reg1_out, __xlx_sprintf_buffer.data()); 
  }
  tcl_file.set_num(1, &tcl_file.slv_reg1_out_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_slv_reg1_out, __xlx_sprintf_buffer.data());
}
// print slv_reg2_out Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_slv_reg2_out, __xlx_sprintf_buffer.data());
  {
    sc_bv<32> __xlx_tmp_lv = *((int*)&__xlx_apatb_param_slv_reg2_out);

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_slv_reg2_out, __xlx_sprintf_buffer.data()); 
  }
  tcl_file.set_num(1, &tcl_file.slv_reg2_out_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_slv_reg2_out, __xlx_sprintf_buffer.data());
}
// print slv_reg3_out Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_slv_reg3_out, __xlx_sprintf_buffer.data());
  {
    sc_bv<32> __xlx_tmp_lv = *((int*)&__xlx_apatb_param_slv_reg3_out);

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_slv_reg3_out, __xlx_sprintf_buffer.data()); 
  }
  tcl_file.set_num(1, &tcl_file.slv_reg3_out_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_slv_reg3_out, __xlx_sprintf_buffer.data());
}
// print slv_reg4_out Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_slv_reg4_out, __xlx_sprintf_buffer.data());
  {
    sc_bv<32> __xlx_tmp_lv = *((int*)&__xlx_apatb_param_slv_reg4_out);

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_slv_reg4_out, __xlx_sprintf_buffer.data()); 
  }
  tcl_file.set_num(1, &tcl_file.slv_reg4_out_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_slv_reg4_out, __xlx_sprintf_buffer.data());
}
// print slv_reg5_out Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_slv_reg5_out, __xlx_sprintf_buffer.data());
  {
    sc_bv<32> __xlx_tmp_lv = *((int*)&__xlx_apatb_param_slv_reg5_out);

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_slv_reg5_out, __xlx_sprintf_buffer.data()); 
  }
  tcl_file.set_num(1, &tcl_file.slv_reg5_out_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_slv_reg5_out, __xlx_sprintf_buffer.data());
}
// print slv_reg6_out Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_slv_reg6_out, __xlx_sprintf_buffer.data());
  {
    sc_bv<32> __xlx_tmp_lv = *((int*)&__xlx_apatb_param_slv_reg6_out);

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_slv_reg6_out, __xlx_sprintf_buffer.data()); 
  }
  tcl_file.set_num(1, &tcl_file.slv_reg6_out_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_slv_reg6_out, __xlx_sprintf_buffer.data());
}
// print slv_reg7_out Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_slv_reg7_out, __xlx_sprintf_buffer.data());
  {
    sc_bv<32> __xlx_tmp_lv = *((int*)&__xlx_apatb_param_slv_reg7_out);

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_slv_reg7_out, __xlx_sprintf_buffer.data()); 
  }
  tcl_file.set_num(1, &tcl_file.slv_reg7_out_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_slv_reg7_out, __xlx_sprintf_buffer.data());
}
// print slv_reg8_out Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_slv_reg8_out, __xlx_sprintf_buffer.data());
  {
    sc_bv<32> __xlx_tmp_lv = *((int*)&__xlx_apatb_param_slv_reg8_out);

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_slv_reg8_out, __xlx_sprintf_buffer.data()); 
  }
  tcl_file.set_num(1, &tcl_file.slv_reg8_out_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_slv_reg8_out, __xlx_sprintf_buffer.data());
}
// print slv_reg9_out Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_slv_reg9_out, __xlx_sprintf_buffer.data());
  {
    sc_bv<32> __xlx_tmp_lv = *((int*)&__xlx_apatb_param_slv_reg9_out);

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_slv_reg9_out, __xlx_sprintf_buffer.data()); 
  }
  tcl_file.set_num(1, &tcl_file.slv_reg9_out_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_slv_reg9_out, __xlx_sprintf_buffer.data());
}
// print slv_reg10_out Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_slv_reg10_out, __xlx_sprintf_buffer.data());
  {
    sc_bv<32> __xlx_tmp_lv = *((int*)&__xlx_apatb_param_slv_reg10_out);

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_slv_reg10_out, __xlx_sprintf_buffer.data()); 
  }
  tcl_file.set_num(1, &tcl_file.slv_reg10_out_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_slv_reg10_out, __xlx_sprintf_buffer.data());
}
// print slv_reg11_out Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_slv_reg11_out, __xlx_sprintf_buffer.data());
  {
    sc_bv<32> __xlx_tmp_lv = *((int*)&__xlx_apatb_param_slv_reg11_out);

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_slv_reg11_out, __xlx_sprintf_buffer.data()); 
  }
  tcl_file.set_num(1, &tcl_file.slv_reg11_out_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_slv_reg11_out, __xlx_sprintf_buffer.data());
}
// print slv_reg12_out Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_slv_reg12_out, __xlx_sprintf_buffer.data());
  {
    sc_bv<32> __xlx_tmp_lv = *((int*)&__xlx_apatb_param_slv_reg12_out);

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_slv_reg12_out, __xlx_sprintf_buffer.data()); 
  }
  tcl_file.set_num(1, &tcl_file.slv_reg12_out_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_slv_reg12_out, __xlx_sprintf_buffer.data());
}
// print slv_reg13_out Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_slv_reg13_out, __xlx_sprintf_buffer.data());
  {
    sc_bv<32> __xlx_tmp_lv = *((int*)&__xlx_apatb_param_slv_reg13_out);

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_slv_reg13_out, __xlx_sprintf_buffer.data()); 
  }
  tcl_file.set_num(1, &tcl_file.slv_reg13_out_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_slv_reg13_out, __xlx_sprintf_buffer.data());
}
// print slv_reg14_out Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_slv_reg14_out, __xlx_sprintf_buffer.data());
  {
    sc_bv<32> __xlx_tmp_lv = *((int*)&__xlx_apatb_param_slv_reg14_out);

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_slv_reg14_out, __xlx_sprintf_buffer.data()); 
  }
  tcl_file.set_num(1, &tcl_file.slv_reg14_out_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_slv_reg14_out, __xlx_sprintf_buffer.data());
}
// print axi00_imem_ptr0 Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_axi00_imem_ptr0, __xlx_sprintf_buffer.data());
  {
    sc_bv<64> __xlx_tmp_lv = __xlx_offset_byte_param_axi00_imem_ptr0;

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_axi00_imem_ptr0, __xlx_sprintf_buffer.data()); 
  }
  tcl_file.set_num(1, &tcl_file.axi00_imem_ptr0_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_axi00_imem_ptr0, __xlx_sprintf_buffer.data());
}
// print axi01_parambuf_ptr0 Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_axi01_parambuf_ptr0, __xlx_sprintf_buffer.data());
  {
    sc_bv<64> __xlx_tmp_lv = __xlx_offset_byte_param_axi01_parambuf_ptr0;

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_axi01_parambuf_ptr0, __xlx_sprintf_buffer.data()); 
  }
  tcl_file.set_num(1, &tcl_file.axi01_parambuf_ptr0_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_axi01_parambuf_ptr0, __xlx_sprintf_buffer.data());
}
// print axi02_ibuf_ptr0 Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_axi02_ibuf_ptr0, __xlx_sprintf_buffer.data());
  {
    sc_bv<64> __xlx_tmp_lv = __xlx_offset_byte_param_axi02_ibuf_ptr0;

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_axi02_ibuf_ptr0, __xlx_sprintf_buffer.data()); 
  }
  tcl_file.set_num(1, &tcl_file.axi02_ibuf_ptr0_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_axi02_ibuf_ptr0, __xlx_sprintf_buffer.data());
}
// print axi03_obuf_ptr0 Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVIN_axi03_obuf_ptr0, __xlx_sprintf_buffer.data());
  {
    sc_bv<64> __xlx_tmp_lv = __xlx_offset_byte_param_axi03_obuf_ptr0;

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVIN_axi03_obuf_ptr0, __xlx_sprintf_buffer.data()); 
  }
  tcl_file.set_num(1, &tcl_file.axi03_obuf_ptr0_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVIN_axi03_obuf_ptr0, __xlx_sprintf_buffer.data());
}
CodeState = CALL_C_DUT;
systolic_fpga_hw_stub_wrapper(__xlx_apatb_param_slv_reg0_out, __xlx_apatb_param_slv_reg1_out, __xlx_apatb_param_slv_reg2_out, __xlx_apatb_param_slv_reg3_out, __xlx_apatb_param_slv_reg4_out, __xlx_apatb_param_slv_reg5_out, __xlx_apatb_param_slv_reg6_out, __xlx_apatb_param_slv_reg7_out, __xlx_apatb_param_slv_reg8_out, __xlx_apatb_param_slv_reg9_out, __xlx_apatb_param_slv_reg10_out, __xlx_apatb_param_slv_reg11_out, __xlx_apatb_param_slv_reg12_out, __xlx_apatb_param_slv_reg13_out, __xlx_apatb_param_slv_reg14_out, __xlx_apatb_param_axi00_imem_ptr0, __xlx_apatb_param_axi01_parambuf_ptr0, __xlx_apatb_param_axi02_ibuf_ptr0, __xlx_apatb_param_axi03_obuf_ptr0);
CodeState = DUMP_OUTPUTS;
// print m00_imem_axi Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVOUT_m00_imem_axi, __xlx_sprintf_buffer.data());
  {  __xlx_offset_byte_param_axi00_imem_ptr0 = 0*64;
  if (__xlx_apatb_param_axi00_imem_ptr0) {
    for (int j = 0  - 0, e = 1 - 0; j != e; ++j) {
sc_bv<512> __xlx_tmp_lv;
__xlx_tmp_lv.range(63,0) = ((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+0];
__xlx_tmp_lv.range(127,64) = ((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+1];
__xlx_tmp_lv.range(191,128) = ((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+2];
__xlx_tmp_lv.range(255,192) = ((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+3];
__xlx_tmp_lv.range(319,256) = ((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+4];
__xlx_tmp_lv.range(383,320) = ((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+5];
__xlx_tmp_lv.range(447,384) = ((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+6];
__xlx_tmp_lv.range(511,448) = ((long long*)__xlx_apatb_param_axi00_imem_ptr0)[j*8+7];

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVOUT_m00_imem_axi, __xlx_sprintf_buffer.data()); 
      }
  }
}
  tcl_file.set_num(1, &tcl_file.m00_imem_axi_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVOUT_m00_imem_axi, __xlx_sprintf_buffer.data());
}
// print m01_parambuf_axi Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVOUT_m01_parambuf_axi, __xlx_sprintf_buffer.data());
  {  __xlx_offset_byte_param_axi01_parambuf_ptr0 = 0*64;
  if (__xlx_apatb_param_axi01_parambuf_ptr0) {
    for (int j = 0  - 0, e = 1 - 0; j != e; ++j) {
sc_bv<512> __xlx_tmp_lv;
__xlx_tmp_lv.range(63,0) = ((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+0];
__xlx_tmp_lv.range(127,64) = ((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+1];
__xlx_tmp_lv.range(191,128) = ((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+2];
__xlx_tmp_lv.range(255,192) = ((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+3];
__xlx_tmp_lv.range(319,256) = ((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+4];
__xlx_tmp_lv.range(383,320) = ((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+5];
__xlx_tmp_lv.range(447,384) = ((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+6];
__xlx_tmp_lv.range(511,448) = ((long long*)__xlx_apatb_param_axi01_parambuf_ptr0)[j*8+7];

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVOUT_m01_parambuf_axi, __xlx_sprintf_buffer.data()); 
      }
  }
}
  tcl_file.set_num(1, &tcl_file.m01_parambuf_axi_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVOUT_m01_parambuf_axi, __xlx_sprintf_buffer.data());
}
// print m02_ibuf_axi Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVOUT_m02_ibuf_axi, __xlx_sprintf_buffer.data());
  {  __xlx_offset_byte_param_axi02_ibuf_ptr0 = 0*64;
  if (__xlx_apatb_param_axi02_ibuf_ptr0) {
    for (int j = 0  - 0, e = 1 - 0; j != e; ++j) {
sc_bv<512> __xlx_tmp_lv;
__xlx_tmp_lv.range(63,0) = ((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+0];
__xlx_tmp_lv.range(127,64) = ((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+1];
__xlx_tmp_lv.range(191,128) = ((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+2];
__xlx_tmp_lv.range(255,192) = ((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+3];
__xlx_tmp_lv.range(319,256) = ((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+4];
__xlx_tmp_lv.range(383,320) = ((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+5];
__xlx_tmp_lv.range(447,384) = ((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+6];
__xlx_tmp_lv.range(511,448) = ((long long*)__xlx_apatb_param_axi02_ibuf_ptr0)[j*8+7];

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVOUT_m02_ibuf_axi, __xlx_sprintf_buffer.data()); 
      }
  }
}
  tcl_file.set_num(1, &tcl_file.m02_ibuf_axi_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVOUT_m02_ibuf_axi, __xlx_sprintf_buffer.data());
}
// print m03_obuf_axi Transactions
{
  sprintf(__xlx_sprintf_buffer.data(), "[[transaction]] %d\n", AESL_transaction);
  aesl_fh.write(AUTOTB_TVOUT_m03_obuf_axi, __xlx_sprintf_buffer.data());
  {  __xlx_offset_byte_param_axi03_obuf_ptr0 = 0*64;
  if (__xlx_apatb_param_axi03_obuf_ptr0) {
    for (int j = 0  - 0, e = 1 - 0; j != e; ++j) {
sc_bv<512> __xlx_tmp_lv;
__xlx_tmp_lv.range(63,0) = ((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+0];
__xlx_tmp_lv.range(127,64) = ((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+1];
__xlx_tmp_lv.range(191,128) = ((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+2];
__xlx_tmp_lv.range(255,192) = ((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+3];
__xlx_tmp_lv.range(319,256) = ((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+4];
__xlx_tmp_lv.range(383,320) = ((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+5];
__xlx_tmp_lv.range(447,384) = ((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+6];
__xlx_tmp_lv.range(511,448) = ((long long*)__xlx_apatb_param_axi03_obuf_ptr0)[j*8+7];

    sprintf(__xlx_sprintf_buffer.data(), "%s\n", __xlx_tmp_lv.to_string(SC_HEX).c_str());
    aesl_fh.write(AUTOTB_TVOUT_m03_obuf_axi, __xlx_sprintf_buffer.data()); 
      }
  }
}
  tcl_file.set_num(1, &tcl_file.m03_obuf_axi_depth);
  sprintf(__xlx_sprintf_buffer.data(), "[[/transaction]] \n");
  aesl_fh.write(AUTOTB_TVOUT_m03_obuf_axi, __xlx_sprintf_buffer.data());
}
CodeState = DELETE_CHAR_BUFFERS;
AESL_transaction++;
tcl_file.set_num(AESL_transaction , &tcl_file.trans_num);
}
