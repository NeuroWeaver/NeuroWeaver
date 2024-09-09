import glob
import subprocess
import time
#nets = ['gpt', 'mobile', 'vgg', 'resnet', 'yolo', 'bert']
# nets = ['mobile', 'efficientnet' , 'vgg', 'resnet50', 'resnet18', 'yolo', 'gpt', 'bert']
nets=['gpt']
test = "tpu_comparison_output" # baseline_output, baseline_no_tile_constr_output, ld_st_overhead_output, obuf_move_overhead_output, loop_overhead_output, tpu_comparison_output, simd_gpu_profiling

start_time = time.time()
for net in nets:
    test_list = glob.glob(f"/home/hanyang/genesys.sim/test/{test}/{net}*_fused*")
    for test in test_list:
        subprocess.run(["python3", "genesys_sim/genesys.py", "configs/", test , "--mode", "energy"])

end_time = time.time()
elapsed_time = end_time - start_time

print(elapsed_time)