import enum
from logging import raiseExceptions
from typing import Any, List, Dict
import multiprocessing as mp
# use queue instead of deque (also thread-safe) for compatibility with multiprocessing.Queue 
import queue 
import numpy as np

class FlowQueue(object):
    QUEUE_TYPES = ["input", "state", "output"]
    def __init__(self, name, shape, queue_type:str = None, interprocess:bool = False, gate_cond=None):
        self._name = name
        assert isinstance(shape, tuple) and len(shape) > 0 and all([s > 0 and isinstance(s, int) for s in shape])
        self._shape = shape
        if queue_type:
            assert queue_type in FlowQueue.QUEUE_TYPES
        self._queue_type = queue_type
        if queue_type == "state": ## TODO: handle state_queue with non-array item
            self._state = None #np.zeros(shape, dtype=np.float32)
        ## TODO: how do we express pop if qsize > 10 here?
        self._gate_cond = gate_cond
        self._is_interprocess = interprocess
        if interprocess:
            self._queue = mp.Queue()
        else:
            self._queue = queue.Queue()
    
    @property
    def is_interprocess(self) -> bool:
        return self._is_interprocess

    @property
    def queue(self): # -> queue.Queue | mp.Queue: need python 3.10
        return self._queue    

    @queue.setter
    def queue_setter(self, queue):
        self._queue = queue

    def push(self, item: Any, item_shape):
        if(item_shape == self._shape):
            atype = type(self._queue)
            # print(f"pushed item:{item}")
            # print(f"push in queue type:{atype}")
            self._queue.put(item)
        else:
            print(f"FlowQueue {self._name} of {self._shape} shape can't push with wrong shape {item_shape}")

    def pop_if(self) -> Any:
        if self._gate_cond == True: 
            return self._queue.get()
        else:
            print(f"FlowQueue {self._name} can't push with given gate cond")

    def pop(self) -> Any:  
        if self._queue_type == "state":
            if self._queue.empty() == False:
                self._state = self._queue.get()
            return self._state
        else:
           atype = type(self._queue)
           #print(f"pop in queue type:{atype}")
           item = self._queue.get()
           #print(f"popped item:{item}")
           return item
           #return self._queue.get()

        # if self._gate_cond is None: 
        #    return self._queue.get()
        # else:
        #    self.pop_if(self)
    
    def empty(self) -> bool:
        return self._queue.empty()

    def qsize(self) -> int:
        return self._queue.qsize()

    @property
    def shape(self):
        return self._shape

    @property
    def name(self) -> str:
        return self._name

    @property
    def gate_condition(self):
        return self._gate_cond

    @property
    def queue_type(self):
        return self._queue_type

    @queue_type.setter
    def queue_type(self, qtype):
        assert qtype in FlowQueue.QUEUE_TYPES
        self._queue_type = qtype


class Flow(object):
    FLOW_IDS = 0

    def __init__(self, name:str, src:queue.Queue, dst:queue.Queue, child_cid:int):
        self._fid = Flow.FLOW_IDS
        Flow.FLOW_IDS += 1
        self._src_queue = src
        self._dst_queue = dst
        self._name = name
        self._child_cid = child_cid

    @property
    def src_queue(self) -> str:
        return self._src_queue

    @property
    def dst_queue(self) -> str:
        return self._dst_queue

    @property
    def name(self) -> str:
        return self._name

    @property
    def child_cid(self) -> int:
        return self._child_cid
