#!/bin/bash

# Create a temp directory for copying python files to image, because docker can only access current context (current directory)
if [ ! -f MeanFieldModel_multithreading_BO_for_Neuroweaver.py ]; then
    cp ../../cnf/parisa_impl/MeanFieldModel_multithreading_BO_for_Neuroweaver.py .
fi

if [ ! -d GPflow-0.5.0 ]; then
    cp -r ~/GPflow-0.5.0 .
fi

if [ ! -d GPflowOpt ]; then
    cp -r ~/GPflowOpt .
fi


cp -r ~/neuroweaver/{cnf,esa,runtime,compiler,qfdfg,definitions.py,run.sh} .
cp ~/neuroweaver/runtime/{X,Y,param,Flag,pilco,output_q,iteration} .

docker build . -t neuroweaver:bayesian
