## queue notations:
o: output queues, i: input queues, s: state quues

## test_two_components:
A straight-line graph without branches. 
```{python}
[Brain]-(o)->(i)-[SignalSink]
```

## test_straight_line_graph:
A straight-line graph without branches. 
```{python}
queue connection types
o: output queues, i: input queues, s: state quues

[Brain]-(o)->(i)-[SignalToStimulation]-(o)->(i)-[StimulationSink]
```

## test_branching_graph:
A graph with a branch. The graph has only three components
```{python}
[Brain]-(o)->(i)-[Training]-(o)
    \ 
    (o)
      \->(i)-[Sink] 
```

## test_state_queues_graph
```{python}
[Brain]-(o)-(i)->[Training]-(s)-(i)->[Weight update] 
    \ 
    (o)                                                  
      \-(i)->[Inference]                                
                 |
                (o)
```

## test_cyclic_graph:

```{python}
[Brain]-(o)->(i)-[Training]-(s)->(i)->[Weight update] 
    \                                  (o)   
    (o)                                 |
      \->(i)-[Inference]-(s)<-----------|
                |
               (o) 
```

## test_iterations:
A source and a sink of bare bone components handle their input queue and output queue with more than one elements.

## -------------- items below are TODOs --------------

Status: components run as processes can't be connected together directly.
Supported: Comp1(process) -> Comp2 (a thread on main process) -> Comp3 (process)  
Not supported: Comp1 (process) -> Comp2 (process) -> Comp3 (process)

This is because we set up IPC queues for the components on the main process.
This makes per-component processes need the main process to relay the communication between them

Solution: shared memory queue with lock

## test_process_single_iteration:
A simple straight line graph without branches. However, the middle component is run as a separated process.
The dataflow graph runs once from Source to Sink.
```{python}
[Source]-(o)->(i)-[Middle (in another process)]-(o)->(i)-[Sink]
```

## test_process_iterations:
The same dataflow graph like test_process_single_iteration but it runs multiple iterations. The Middle component needs to be joined properly after running `n` iterations.  

Five-Component
```{python} 
[Brain]-(i)->[Training]-(s)-(i)->[Weight update] 
    \                              (o)   
     \                              |
      \-(i)->[Inference]<-(s)-------|
                |
               (o)
                |
               (i)
                |
                V
        [Action to stimlation]    
```