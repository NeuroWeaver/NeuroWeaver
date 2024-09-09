# C&F Compiler

## How to Compile the Component and Flow Program:

![Compile Workflow](./compile-workflow.pdf)

$ python parser.py cnf_source.py [-o qfdfg.pb]

This generates qfdfg.pb file, a Queued Fractalized Dataflow Graph (QF-DFG) serialized to protobuf. Example:

```python parser.py ../cnf/test/test10.py```

$ python engine_selector.py qfdfg.pb [-e engine_system.pb] [-o qfdfg.pb]

This selects engines for all nodes in the QF-DFG. Example:

```python engine_selector.py qfdfg.pb```

$ python python_target_pass.py qfdfg.pb

This generates build/ directory with compiled target file for each component.
Also, updated.pb file is generated. Example:

```python python_target_pass.py qfdfg.pb```


## To Clean:

```$ ./clean```

This removes all *.pb files and build/ directory.
