# Component and Flow programs

In this directory, you can find example Component and Flow programs.


## Directory Structure
Parisa's python implementation files are under parisa_impl/ directory.
test/ has simple programs mainly used for end-to-end testing.
cnf_meanfield.py has the latest implementation for the closed-loop pipeline with Bayesian optimization (corresponds to MeanFieldModel_multithreading_BO_for_Neuroweaver.py)
pilco.py has the latest implementation for the pilco application.


## Bayesian optimization application status
There are 4 "threads" (from Parisa's implementation) to this: thread_1 for data generation, thread_2 for data processing, thread_3 for recording data back to the brain, and thread_4 for Bayesian optimization. Naturally, I thought these 4 threads corresponded directly to a Component of its own. However, I decided to create a series of sub-components (thread2_sub1, Signal_Processing, dsp.fft, and post_processing) under the thread_2 Component. This was necessary for the current design because we want to run the FFT component on an FPGA accelerator (i.e. TABLA), which requires us to use the DSP domain's capability (dsp.fft from line 243) - and I can't use the with Component(...) construct. For now, this is the only way that the CNF parser can recognize dsp.fft() as a Component, but obviously if there's a better design for this then by all means fix it.

All-CPU execution: This _was_ functional before adding the Bayesian Optimization component (thread_4). Here is where we are facing some issues: Currently, the objective of parsing is to figure out what components there are and what Flows (the thing that connects different components) there are. And the only way to figure these out is to have the programmer explicitly "instantiate" components and flows like so:

```a = comp_a()
comp_b(a)```

where the parser can figure out that comp_a and comp_b components have been instantiated, and these two are connected via a Flow named "a". And this information about what Flows are connecting what componets is used by the XLVM runtime, because it maintains a queue for each flow and handles pushing and popping data to/from these Flows. Without the Bayesian optimization component added, I was able to implement the application in this fashion and parsing + execution was successful. However, with the Bayesian optimization component added to the application, the challenge that came up is that the output of thread_4 needs to be pushed to the same queue used as input for thread_3. Currently, there is no programming langauge construct to express two Flows sharing same queue. More generally, there is no way to express global shared variables in the current design of component and flow programming model. Furthermore, there is no way currently to incorporate user-defined custom behaviors to these Flows the same way we can do to queues like in the custom_logic function in line 73. One quick workaround is to write output values to a file and read input values from these files, instead of using the Flow constrcut. Currently there is a bug in this file I/O approach.