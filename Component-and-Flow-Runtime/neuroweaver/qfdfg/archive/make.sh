#!/bin/bash

protoc --python_out=. qfdfg.proto types.proto
sed -i -r -E 's/^(import.*_pb2)/from . \1/' *.py
