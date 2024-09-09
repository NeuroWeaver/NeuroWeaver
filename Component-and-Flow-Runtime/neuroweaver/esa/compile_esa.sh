#!/bin/bash

ROOT_DIR=~/ACTLab/neuroweaver/neuroweaver
ESA_DIR=${ROOT_DIR}/esa

# Abstract Domain Parser directories and files
ABSTRACT_DOMAIN_PARSER_BIN=${ESA_DIR}/abstract_domain_parser.py
ABSTRACT_DOMAIN_DIR=${ESA_DIR}/abstract_domains
DEEP_LEARNING_DOMAIN_FILE=${ABSTRACT_DOMAIN_DIR}/deep_learning.domain
DEEP_LEARNING_PB_FILE=${ESA_DIR}/deep_learning.pb
CV_DOMAIN_FILE=${ABSTRACT_DOMAIN_DIR}/computer_vision.domain
CV_PB_FILE=${ESA_DIR}/computer_vision.pb
ANALYTICS_DOMAIN_FILE=${ABSTRACT_DOMAIN_DIR}/analytics.domain
ANALYTICS_PB_FILE=${ESA_DIR}/analytics.pb
DSP_DOMAIN_FILE=${ABSTRACT_DOMAIN_DIR}/digital_signal_processing.domain
DSP_PB_FILE=${ESA_DIR}/digital_signal_processing.pb


ENGINE_SPEC_PARSER_BIN=${ESA_DIR}/engine_spec_parser.py
ENGINE_DIR=${ESA_DIR}/engines
TF_ENGINE_FILE=${ENGINE_DIR}/tensorflow.engine
TF_ENGINE_PB_FILE=${ESA_DIR}/tf_engine.pb
CUDA_ENGINE_FILE=${ENGINE_DIR}/cuda.engine
CUDA_ENGINE_PB_FILE=${ESA_DIR}/cuda_engine.pb
DNNWEAVER_ENGINE_FILE=${ENGINE_DIR}/dnnweaver.engine
DNNWEAVER_ENGINE_PB_FILE=${ESA_DIR}/dnnweaver_engine.pb
TABLA_ENGINE_FILE=${ENGINE_DIR}/tabla.engine
TABLA_ENGINE_PB_FILE=${ESA_DIR}/tabla_engine.pb

ENGINE_ADD_BIN=${ESA_DIR}/add_engine_pass.py

DOMAIN_ADD_BIN=${ESA_DIR}/add_domain_pass.py
ENGINE_SET_PB_FILE=${ESA_DIR}/engine_system.pb


# Run the abstract domain parser
#echo "python ${ABSTRACT_DOMAIN_PARSER_BIN} ${DEEP_LEARNING_DOMAIN_FILE} -o ${DEEP_LEARNING_PB_FILE}"
#python3.7 ${ABSTRACT_DOMAIN_PARSER_BIN} ${DEEP_LEARNING_DOMAIN_FILE} -o ${DEEP_LEARNING_PB_FILE} 1>/dev/null
echo "python ${ABSTRACT_DOMAIN_PARSER_BIN} ${ANALYTICS_DOMAIN_FILE} -o ${ANALYTICS_PB_FILE}"
python3 ${ABSTRACT_DOMAIN_PARSER_BIN} ${ANALYTICS_DOMAIN_FILE} -o ${ANALYTICS_PB_FILE} 1>/dev/null
echo "python ${ABSTRACT_DOMAIN_PARSER_BIN} ${DSP_DOMAIN_FILE} -o ${DSP_PB_FILE}"
python3 ${ABSTRACT_DOMAIN_PARSER_BIN} ${DSP_DOMAIN_FILE} -o ${DSP_PB_FILE} 1>/dev/null
#echo "python ${ABSTRACT_DOMAIN_PARSER_BIN} ${CV_DOMAIN_FILE} -o ${CV_PB_FILE}"
#python ${ABSTRACT_DOMAIN_PARSER_BIN} ${CV_DOMAIN_FILE} -o ${CV_PB_FILE} 1>/dev/null


# Run the engine specification language parser
echo "python ${ENGINE_SPEC_PARSER_BIN} ${TF_ENGINE_FILE} -o ${TF_ENGINE_PB_FILE}"
python3 ${ENGINE_SPEC_PARSER_BIN} ${TF_ENGINE_FILE} -o ${TF_ENGINE_PB_FILE} 1>/dev/null

#echo "python ${ENGINE_SPEC_PARSER_BIN} ${DNNWEAVER_ENGINE_FILE} -o ${DNNWEAVER_ENGINE_PB_FILE}"
#python3.7 ${ENGINE_SPEC_PARSER_BIN} ${DNNWEAVER_ENGINE_FILE} -o ${DNNWEAVER_ENGINE_PB_FILE} 1>/dev/null

echo "python ${ENGINE_SPEC_PARSER_BIN} ${TABLA_ENGINE_FILE} -o ${TABLA_ENGINE_PB_FILE}"
python3 ${ENGINE_SPEC_PARSER_BIN} ${TABLA_ENGINE_FILE} -o ${TABLA_ENGINE_PB_FILE} 1>/dev/null

# echo "python ${ENGINE_SPEC_PARSER_BIN} ${CUDA_ENGINE_FILE} -o ${CUDA_ENGINE_PB_FILE}"
# python ${ENGINE_SPEC_PARSER_BIN} ${CUDA_ENGINE_FILE} -o ${CUDA_ENGINE_PB_FILE} 1>/dev/null


# Add engine specifications to corresponding domain
echo "python ${ENGINE_ADD_BIN} ${TF_ENGINE_PB_FILE} -d ${DSP_PB_FILE} -o ${DSP_PB_FILE}"
python3 ${ENGINE_ADD_BIN} ${TF_ENGINE_PB_FILE} -d ${DSP_PB_FILE} -o ${DSP_PB_FILE} 1>/dev/null
#echo "python ${ENGINE_ADD_BIN} ${DNNWEAVER_ENGINE_PB_FILE} -d ${DEEP_LEARNING_PB_FILE} -o ${DEEP_LEARNING_PB_FILE}"
#python3.7 ${ENGINE_ADD_BIN} ${DNNWEAVER_ENGINE_PB_FILE} -d ${DEEP_LEARNING_PB_FILE} -o ${DEEP_LEARNING_PB_FILE} 1>/dev/null

echo "python ${ENGINE_ADD_BIN} ${TABLA_ENGINE_PB_FILE} -d ${ANALYTICS_PB_FILE} -o ${ANALYTICS_PB_FILE}"
python3 ${ENGINE_ADD_BIN} ${TABLA_ENGINE_PB_FILE} -d ${ANALYTICS_PB_FILE} -o ${ANALYTICS_PB_FILE} 1>/dev/null

# echo "python ${ENGINE_ADD_BIN} ${CUDA_ENGINE_PB_FILE} -d ${CV_PB_FILE} -o ${CV_PB_FILE}"
# python ${ENGINE_ADD_BIN} ${CUDA_ENGINE_PB_FILE} -d ${CV_PB_FILE} -o ${CV_PB_FILE} 1>/dev/null


# Add a new domain to engine system
echo "python ${DOMAIN_ADD_BIN} ${DSP_PB_FILE} ${ANALYTICS_PB_FILE} -o ${ENGINE_SET_PB_FILE}"
python3 ${DOMAIN_ADD_BIN} ${DSP_PB_FILE} ${ANALYTICS_PB_FILE} -o ${ENGINE_SET_PB_FILE} 1>/dev/null
