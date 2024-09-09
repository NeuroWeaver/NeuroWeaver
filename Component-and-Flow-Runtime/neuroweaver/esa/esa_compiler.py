from pathlib import Path
from esa.abstract_domain_parser import parse_abstract_domain
from esa.engine_spec_parser import parse_engine_spec
from esa.add_domain_pass import add_domain
from esa.add_engine_pass import add_engine

CWD = Path(f"{__file__}").parent
ESA_DIR = f"{CWD}"
ABSTRACT_DOMAIN_PARSER_BIN = f"{ESA_DIR}/abstract_domain_parser.py"
ENGINE_SPEC_PARSER_BIN = f"{ESA_DIR}/engine_spec_parser.py"
ENGINE_ADD_BIN = f"{ESA_DIR}/add_engine_pass.py"
DOMAIN_ADD_BIN = f"{ESA_DIR}/add_domain_pass.py"

ABSTRACT_DOMAIN_DIR = f"{ESA_DIR}/abstract_domains"
DEEP_LEARNING_DOMAIN_FILE = f"{ABSTRACT_DOMAIN_DIR}/deep_learning.domain"
DEEP_LEARNING_PB_FILE = f"{ESA_DIR}/deep_learning.pb"
CV_DOMAIN_FILE = f"{ABSTRACT_DOMAIN_DIR}/computer_vision.domain"
CV_PB_FILE = f"{ESA_DIR}/computer_vision.pb"
ANALYTICS_DOMAIN_FILE = f"{ABSTRACT_DOMAIN_DIR}/analytics.domain"
ANALYTICS_PB_FILE = f"{ESA_DIR}/analytics.pb"
DSP_DOMAIN_FILE = f"{ABSTRACT_DOMAIN_DIR}/digital_signal_processing.domain"
DSP_PB_FILE = f"{ESA_DIR}/digital_signal_processing.pb"

ENGINE_DIR = f"{ESA_DIR}/engines"
TF_ENGINE_FILE = f"{ENGINE_DIR}/tensorflow.engine"
TF_ENGINE_PB_FILE = f"{ESA_DIR}/tf_engine.pb"
CUDA_ENGINE_FILE = f"{ENGINE_DIR}/cuda.engine"
CUDA_ENGINE_PB_FILE = f"{ESA_DIR}/cuda_engine.pb"
DNNWEAVER_ENGINE_FILE = f"{ENGINE_DIR}/dnnweaver.engine"
DNNWEAVER_ENGINE_PB_FILE = f"{ESA_DIR}/dnnweaver_engine.pb"
TABLA_ENGINE_FILE = f"{ENGINE_DIR}/tabla.engine"
TABLA_ENGINE_PB_FILE = f"{ESA_DIR}/tabla_engine.pb"

ENGINE_SET_PB_FILE = f"{ESA_DIR}/engine_system.pb"


def run_abstract_domain_parser():
    # Run the abstract domain parser
    parse_abstract_domain(DEEP_LEARNING_DOMAIN_FILE, output_file=DEEP_LEARNING_PB_FILE)
    parse_abstract_domain(ANALYTICS_DOMAIN_FILE, output_file=ANALYTICS_PB_FILE)
    parse_abstract_domain(CV_DOMAIN_FILE, output_file=CV_PB_FILE)


def run_engine_spec_parser():
    parse_engine_spec(TF_ENGINE_FILE, output_file=TF_ENGINE_PB_FILE)
    parse_engine_spec(TABLA_ENGINE_FILE, output_file=TABLA_ENGINE_PB_FILE)


def add_engine_spec_for_domain():
    add_engine(engine_file=TF_ENGINE_PB_FILE, domain_file=DSP_PB_FILE, output_file=DSP_PB_FILE)
    add_engine(engine_file=TABLA_ENGINE_PB_FILE, domain_file=ANALYTICS_PB_FILE, output_file=ANALYTICS_PB_FILE)


def add_domain_to_eng_system():
    domain_files = [DSP_PB_FILE, ANALYTICS_PB_FILE, DSP_PB_FILE]
    add_domain(domain_files=domain_files)


'''
Function does the following:
1. Parse abstract domains to generate protobuf files for each domain <domain>.pb in ESA dir
2. For each engine: [domain1, domain2, ..], 
    a. Parse the engine spec and generate _engine.pb files
    b. Add engine to all the corresponding domains
3. Add domains to engine_system.pb (Why?)
'''


def compile_esa():
    parsed_domains = ['deep_learning', 'analytics', 'computer_vision', 'digital_signal_processing']
    for pd in parsed_domains:
        parse_abstract_domain(f"{ABSTRACT_DOMAIN_DIR}/{pd}.domain", f"{ESA_DIR}/{pd}.pb")

    engine_specs = {"tensorflow_dsp": ["digital_signal_processing"], "tensorflow_nn": ["deep_learning"],
                    "tabla": ["analytics"], "genesys": ["deep_learning"]}
    for es, domains in engine_specs.items():
        # if "tensorflow" in es:
        #    parse_engine_spec(f"{ENGINE_DIR}/{es}.engine", f"{ESA_DIR}/tensorflow_engine.pb")
        # else:
        parse_engine_spec(f"{ENGINE_DIR}/{es}.engine", f"{ESA_DIR}/{es}_engine.pb")
        for d in domains:
            # if "tensorflow" in es:
            # add_engine(engine_file=f"{ESA_DIR}/tensorflow_engine.pb",domain_file=f"{ESA_DIR}/{d}.pb")
            # else:
            add_engine(engine_file=f"{ESA_DIR}/{es}_engine.pb", domain_file=f"{ESA_DIR}/{d}.pb",
                       output_file=f"{ESA_DIR}/{d}.pb")
    domain_files = [DEEP_LEARNING_PB_FILE, DSP_PB_FILE]
    add_domain(domain_files=domain_files, output_file=f"{ESA_DIR}/engine_system.pb", verbose=True)
