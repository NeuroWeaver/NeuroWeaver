from esa.engines.engine import Engine
import polymath as pm
import os
from examples.genesys import compile_genesys_layer, compile_genesys, get_arch
from tools.compile_layer import store_compilation_output, store_values, BENCH_BASE_ADDR
import numpy as np
import json

class GenesysEngine(Engine):

    def __init__(self):
        super(GenesysEngine, self).__init__('genesys')
        self.compiled_instructions = None
        self.data = None

    def compile_model(self, onnx):
        # Setup directory structure like codelets compiler expects
        os.makedirs('genesys/models/srdfg', exist_ok=True)
        os.makedirs('genesys/compiler_outputs', exist_ok=True)
        os.makedirs('genesys/tiling_info', exist_ok=True)

        graph = pm.from_onnx(onnx, verbose=True)
        pm.pb_store(graph, "genesys/models/srdfg/")
        model_name = onnx.split('.')[0]
        program = compile_genesys(model_name,
                                  train=False,
                                  update_cfg_dtypes=False,
                                  tiling_path=None,
                                  batch_size=1,
                                  store_tiling=False,
                                  store_json_output=False,
                                  json_output_filename=None,
                                  verbose=True,
                                  benchmark_path='genesys',
                                  factor_fn='default',
                                  print_config=False
                                  )
        program.compile(verbose=False, finalize_instructions=True)
        arch_cfg = get_arch(None, None, False)
        base_path = store_compilation_output(program, "arch_cfg", extension="json", arch_cfg=arch_cfg, dir_ext=None)
        store_compilation_output(program, "operations_idx", extension="txt", dir_ext=None)
        store_compilation_output(program, "json", extension="json", dir_ext=None)
        store_compilation_output(program, "string_final", extension="txt", dir_ext=None)
        store_compilation_output(program, "decimal", extension="txt", dir_ext=None)
        store_compilation_output(program, "binary", extension="txt", dir_ext=None)
        store_values(program, model_name, base_path, use_random=True, load_path=None,
                     actual_data=False,
                     store_partials=False)
        self.compiled_instructions = program

    def read(self):
        pass

    def write(self, *args):
        self.data = list(args)
        print(self.data)

    def compute(self, capability, metadata):
        assert self.data is not None
        if capability == 'compile_model':
            self.compile_model(self.data[0][0])
        else:
            raise RuntimeError(f"GenesysEngine got an unimplemented capability {capability}")