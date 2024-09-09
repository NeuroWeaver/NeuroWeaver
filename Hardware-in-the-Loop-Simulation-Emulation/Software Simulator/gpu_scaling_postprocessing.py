import glob
import subprocess
import time
import csv

net = "gpt/unfused"
output_name = "gpt_unfused_best.csv"
test_dir = f"/home/hanyang/genesys.sim/test/simd_gpu_profiling_csv_results/{net}/*"
path_len = len(f"/home/hanyang/genesys.sim/test/simd_gpu_profiling_csv_results/{net}/")
test_list = glob.glob(test_dir)
first_test = True
first_row = True
best_results = {}
categories = {}

for test in test_list:
    #print(test)
    with open(test, mode='r') as csv_file:
        csvreader_object=csv.reader(csv_file)
        # Skip the first row
        next(csvreader_object)
        
        # Skip the categories row for the other test files
        if not first_row:
            next(csvreader_object)
        
        for row in csvreader_object:
            # Grab the catergorys for the tests
            if first_row:
                categories = row
                first_row = False
            else:
                layer_name = row[0]
                stats = {}
                # construct best_result if it is the first test
                if first_test:
                    for idx, x in enumerate(row):
                        if idx != 0:
                            stats[categories[idx]] = x                
                    stats["config"] = test[path_len:]
                    best_results[layer_name] = stats

                # Else check and update the best result
                else:
                    current_best = best_results[layer_name]["totCycles"]
                    # row[21] is totCycles
                    if row[21] < current_best:
                        for idx, x in enumerate(row):
                            if idx != 0:
                                stats[categories[idx]] = x                
                        stats["config"] = test[path_len:]
                        best_results[layer_name] = stats
    csv_file.close()
    first_test = False

# print(best_results.keys())
# print(best_results["layer21_conv_bias22"]["config"])

output_file = f"/home/hanyang/genesys.sim/test/simd_gpu_profiling_csv_results/{output_name}"
with open(output_file, 'w') as csvfile:
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(categories) 
    for layer in best_results:
        row = []
        row.append(layer)
        elements = best_results[layer]
        for element in elements:
            row.append(elements[element])
        csvwriter.writerow(row)
        # print(categories)
        # print(row)