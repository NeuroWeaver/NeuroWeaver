# SIMD Simulator
- - -
## Requirements
- python3
- numpy
- tqdm
- fxpmath
- - -
## How to run
### 1. Data preprocessing
Running FXP in simulator would take too long time. For a quick simulation, convert data in benchmarks from FXP to FP32
(Example script: `convert-fxp-to-fp.py`).
### 2. Configuration
Configure simulator in `sim_config.json`
```json
# sim_config.json
{
  "layer-example-path": "path/to/testcase",        # a path of testcase
  "fast-run": false,                               # fast run iterate only one base loop
  "should-validate-dram-output": true,             # if true, validate output elements in dram
  "num-input-to-load-from-ddr": 1,                 # number of inputs (e.g., relu: 1, add: 2)
  "num-output-to-store-to-ddr": 1,                 # number of outputs, always 1

  # cycle delays which are calculated statically
  "ld-init-delay-cycles": 0,
  "ld-scale-of-delay": 0,
  "st-init-delay-cycles": 0,
  "st-scale-of-delay": 0
}
```
### 3. Execution Command
Run `pipeline.py`
```commandline
$ python pipeline.py
```
- - - 
