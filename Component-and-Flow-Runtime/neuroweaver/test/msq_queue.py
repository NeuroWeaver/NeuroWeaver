### using posix_ipc message_queue for inter-process communication
### the main process (the one our runtime is on) (1) sets up/ unlinks the queues
### (2) make sure the resource limits and mqueue specific limits are set properly.
### the other child processes just open them with passed names of the message_queue

import posix_ipc 
# link to module source code https://github.com/osvenskan/posix_ipc
# link to moduele doc https://semanchuk.com/philip/posix_ipc/#message_queue
import os, resource
import multiprocessing as mp

import numpy as np
import pickle
from gym.spaces import Box
from stable_baselines3.common.buffers import RolloutBuffer

def execute_fn1(q_name, q_name2):
    mq = posix_ipc.MessageQueue(q_name, posix_ipc.O_CREAT)
    msg, p=mq.receive()
    rlt2 = pickle.loads(msg)
    pid = os.getpid()
    print(f"pid {pid} has msg {rlt2}")
    print(rlt2.__dict__)
    mq.close()

    # mq2 = posix_ipc.MessageQueue(q_name2, posix_ipc.O_CREAT)
    # message = 'Oli is cute+'
    # byte_message = bytes(message, 'utf-8')    
    # mq2.send(byte_message)
    # print(f"pid {pid} sent msg {message}")
    # mq2.close()

def execute_fn2(q_name2):
    mq = posix_ipc.MessageQueue(q_name2, posix_ipc.O_CREAT)
    print(f"mq.name: {mq.name}")
    #msg, p=mq.receive()
    #pid = os.getpid()
    #print(f"pid {pid} has msg {msg}")
    mq.close()

# https://stackoverflow.com/questions/40342569/cannot-create-more-than-10-mqueues
# See https://www.man7.org/linux/man-pages/man2/getrlimit.2.html for rlimit information
# https://man7.org/linux/man-pages/man7/mq_overview.7.html for mqueue information
# and https://docs.python.org/3/library/resource.html for usage

# print(resource.getrlimit(resource.RLIMIT_MSGQUEUE))
# limit=80000*25
# resource.setrlimit(resource.RLIMIT_MSGQUEUE, (limit, limit))
# print(resource.getrlimit(resource.RLIMIT_MSGQUEUE))

q_name = '/message_queue0' # abs path: /dev/mqueue/message_queue0
mq = posix_ipc.MessageQueue(q_name, posix_ipc.O_CREX, max_message_size=8000) #80000)

q_name2 = '/message_queue1' # abs path: /dev/mqueue/message_queue1
#ipcq = posix_ipc.MessageQueue(q_name2, posix_ipc.O_CREX, max_message_size=8000) #80000)

action_space = Box(low=-1, high=1, shape=(1,), dtype=np.float32)
observation_space = Box(low=-1.5, high=1.5, shape=(2,), dtype=np.float32)

rlt = RolloutBuffer(2, observation_space, action_space)
brlt = pickle.dumps(rlt)
mq.send(brlt)

#message = 'Python is fun-'
## make it bytes so we don't care about what inside ther anymore, any type can pass
#byte_message = bytes(message, 'utf-8')
#mq.send(byte_message)

# message2 = 'Python is fun+'
# byte_message2 = bytes(message2, 'utf-8')
# mq.send(byte_message2)

#comp_process = mp.Process(target=execute_fn1, args=(q_name,q_name2))
#comp_process.start()

comp_process2 = mp.Process(target=execute_fn2, args=(q_name2,))
comp_process2.start()

#comp_process.join()
comp_process2.join()

mq.close()
mq.unlink()
# ipcq.close()
# ipcq.unlink()