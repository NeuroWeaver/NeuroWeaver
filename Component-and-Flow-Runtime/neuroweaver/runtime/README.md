### Python requirement
we'll neeed Python 3.8 or higher

### module requirements
install posix-ipc module (https://semanchuk.com/philip/posix_ipc/)   
`python3.8 -m pip install posix-ipc`

### modify the msgqueue limit on Ubuntu Linux  
`vim /etc/security/limits.conf`   
append this line    
`* hard msgqueue 9437184000`  
you’ll need restart the shell or even restart the machine to make it effective.  
This can sustain over reboot.  

### system setup on Ubuntu Linux
`sudo su`   
`echo 3145728 > /proc/sys/fs/mqueue/msgsize_max`   
`echo 2048 > /proc/sys/fs/mqueue/msg_max`   
These configuration needs to done after every reboot   
The first line is the limit on msg size, the second line is the limit on queue length.

### shell setup
run `ulimit -q` to check the current resource limit of msg queue   
`ulimit -q 9437184000` to set it to the system hard limit we configured above.   

### mqueue and shm clean-up during debugging
clean up msg queue and shared memory after a crashed or hang run   
`rm /dev/mqueue/*`  
`rm /dev/shm/msgq_dtype`  

### debug hung processes taken GPU memory 
`sudo fuser -v /dev/nvidia*`   
find the PID with user name   
`sudo kill -9 $PID`  

### Debugging notes
```
Traceback (most recent call last):
  File "ppruntime_tests.py", line 83, in <module>
    run_two_comp()
  File "ppruntime_tests.py", line 68, in run_two_comp
    runtime.initialize() ## visit the graph and create all the posix msq_queues 
  File "/home/stingw/yinyang/runtime/process_runtime.py", line 208, in initialize
    mq = posix_ipc.MessageQueue('/' + queue_name, posix_ipc.O_CREAT, max_message_size=max_msg_size)
OSError: This process already has the maximum number of files open
```
This is mostly because the msg_size in msg_queue is set up too big. The system couldn't handle it 
