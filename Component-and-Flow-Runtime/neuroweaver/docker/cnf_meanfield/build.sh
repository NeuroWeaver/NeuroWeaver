#!/bin/bash

cp -r ../../{cnf,esa,runtime,compiler,qfdfg,definitions.py,run_app.py} .
sudo docker build . -t neuroweaver:cnf_meanfield
