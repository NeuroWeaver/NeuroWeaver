from pathlib import Path

from tablav2.compiler import compile


def main():
    DFG_ROOT = f"{Path(f'{__file__}').parent}"
    dfg_name = f"fft_tabla.json"
    optimizations = {'reorder_instr': False, 'unused_ni_opt': False, 'apply_reuse': False}

    compile(Path(f"{DFG_ROOT}/../{dfg_name}").resolve(),
            'config.json',
            'input_data.txt',
            'input_weights.txt',
            'meta.txt',
            sort_alg="custom",
            gen_sched_file=False,
            gen_mem_instr=True,
            save_data=True,
            debug=False,
            optimizations=optimizations,
            show_ns_utilization=["NI", "NW", "ND"])


if __name__ == '__main__':
    main()
