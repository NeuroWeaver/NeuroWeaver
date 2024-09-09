import argparse
import shutil
import os
import time
from pathlib import Path
from compiler.parser import parse_program
from compiler.engine_selector import select_engine
from compiler.python_target_pass import compile_target
from runtime.xlvm import run_project
from esa.esa_compiler import compile_esa
CWD = Path(f"{__file__}").parent
CNF_DIR = f"{CWD}/../cnf"
from definitions import COMPILER_DIR
build_dir = COMPILER_DIR + '/build'
deps = {
    'cnf/pilco_v2.py' : ['_oscillator_cpp.so']
}

def resolve_dependencies(args):
    if args.cnf_source in deps:
        cnf_source_deps = deps[args.cnf_source]
        src_dir = '/'.join(args.cnf_source.split('/')[0:-1])
        files = os.listdir(src_dir)
        for d in cnf_source_deps:
            # Dependency is a file
            if '.' in d:
                try:
                    shutil.copy(src_dir + '/' + d, build_dir)
                except FileExistsError:
                    continue
                except:
                    raise Exception(f'Missing dependency {d} in source app folder')
            # Dependency is a folder
            else:
                try:
                    shutil.copytree(src_dir + '/' + d, build_dir + '/' + d)
                except FileExistsError:
                    continue
                except:
                    raise Exception(f'Missing dependency {d} in source app folder')

def main(args):
    # Parse C&F source
    compile_esa()
    qfdfg_file = parse_program(args.cnf_source, output_file=args.output_file, verbose=args.verbose)
    qfdfg_file = select_engine(qfdfg_file, engine_system= args.engine_system, output_file=args.output_file, verbose=args.verbose)
    qfdfg_file = compile_target(args.cnf_source, qfdfg_file, output_file=args.output_file)
    resolve_dependencies(args)
    run_start_time = time.time()
    run_project(qfdfg_file, run_tasks_infinitely= args.infinite, verbose=True)
    print("---Run time: %s seconds ---" % (time.time() - run_start_time))

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Run an application')
    argparser.add_argument('cnf_source',
                           help='C&F source program embedded in Python (.py)')
    argparser.add_argument('-e', '--engine_system',
                           default='esa/engine_system.pb',
                           help='Engine system file (.pb). Default: esa/engine_system.pb')
    argparser.add_argument('-o', '--output_file',
                           default='app.pb',
                           help='Output pb file. Default: app.pb')
    argparser.add_argument('--infinite',
                           action='store_true',
                           help='If provided, runs application tasks in infinite loop')
    argparser.add_argument('-v','--verbose',
                           action='store_true',
                           help='Enables verbose prints throughout')
    args = argparser.parse_args()
    start_time = time.time()
    main(args)
    print("--- Compile and Run time: %s seconds ---" % (time.time() - start_time))

