import multiprocessing as mp
from multiprocessing import shared_memory as shm
import time
import posix_ipc
import pickle, os, sys
import numpy as np
from time import sleep
import logging

from scipy.fft import dst
from qfdfg.graph import Graph
from collections import deque
from qfdfg.component import Component, ComponentStatus

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    level=logging.WARNING)
logging.Formatter('%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')

logger = logging.getLogger(__name__)
fh = logging.FileHandler('debug_ppo_runtime.log')
#fh.setLevel(logging.DEBUG)
#fh.setFormatter(fmt='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')
logger.addHandler(fh)

class uidarray(np.ndarray):
    def __new__(cls, input_array, uid=None):
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(input_array).view(cls)
        # add the new attribute to the created instance
        obj.uid = uid
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None: return
        self.uid = getattr(obj, 'uid', None)

# a wrapper for MessageQueue for push()/pop()
class POSIXMsgQueue():
    QUEUE_TYPES = ["input", "state", "output"]
    def __init__(self, name, shape, queue_type:str = None, qid:int = 0, is_queue_observed = False):
        self._name = name
        logger.debug(f"shape:{shape}")
        assert isinstance(shape, tuple) and len(shape) > 0 and all([s > 0 and isinstance(s, int) for s in shape])
        self._shape = shape
        assert queue_type in POSIXMsgQueue.QUEUE_TYPES
        self._queue_type = queue_type
        if queue_type == "state": ## handle state_queue with non-array item
            self._state = None #np.zeros(shape, dtype=np.float32)
        self._qid = qid # qid to lookup dtype information for np.ndarray item
        self._typelist = shm.ShareableList(name='msgq_dtype')
        self._dtype_str = self._typelist[qid]
        ## TODO: how to set this properly when queue is created?
        self._is_queue_observed = is_queue_observed
        #self._dtype_str = np.dtype(np.float32).str
        #logger.info(f"dtype str {self._dtype_str}")

    # no getter/setter for POSIXMsgQueue to mess up self._queue

    # Terminology 
    # split: the same piece of data is repliacted on all branches, i.e. queues
    # e.g. data-0 -> queue-A, data-0 -> queue-B. Each branch has different
    # funtionalities.
    # 
    # merge: aggregate the outcome of same piece of data on bracnhes
    # Question: how to merge if some branches are just slower than others?
    ## naive solution: block and wait until slow branch is ready
    ## improved solution: out-of-order execution
 
    # select: different pieces of data is distributed on branches, i.e. queues
    # e.g. data-0 -> queue-A, data-1 -> queue-B
    # maybe we don't need multiple queues for select. Components can pull 
    # from the same queue if the contention level is acceptable.
    #
    # aggregate: data from all branches is merged with no enforced order
    
    # def init_split_queues(self, queue_list):
    #     self._queue = queue_list
    
    def init_queue(self, queue):
        self._queue = queue

    def __del__(self):
         self._queue.close()

    def push_object(self, item: object):
        pickled = pickle.dumps(item)
        #logger.debug(f"pickled object length:{len(pickled)}")
        self._queue.send(pickled)
    
    # we'll need separate tests for this method
    def state_pop_object(self):
        #print("state_pop_object")
        if self._queue.current_messages > 0:            
            raw, _ = self._queue.receive()
            #logger.debug("state_pop_object:set _state")
            self._state = raw
            return pickle.loads(raw)

        if self._state != None:
            #logger.debug("state_pop_object: return _state pickled")
            return pickle.loads(self._state)
        else:
            #logger.debug("state_pop_object: return _state None")
            return self._state

    def pop_object(self):
        if self._queue_type == "state":
            item = self.state_pop_object()
            return item
        raw, _ = self._queue.receive()
        return pickle.loads(raw)
        
    def push_bytes(self, item: bytes, item_shape: tuple):    
        self._queue.send(item.tobytes())
        if(item.shape != item_shape or self._shape != item_shape):
            raise RuntimeError(f"POSIXMsgQueue {self._name} of {self._shape} \
                shape can't push with wrong arguement item_shape {item_shape} or wrong item.shape {item.shape}")
    
    def push(self, item: np.ndarray, item_shape: tuple):
        self._dtype_str = item.dtype.str
        self._typelist[self._qid] = item.dtype.str
        #logger.debug(f"item dtype.str {item.dtype.str}, typelist[qid] {self._typelist[self._qid]}")
        #item_float64 = item.astype(np.float64)
        item_bytes = item.tobytes()
        if hasattr(item, 'uid'):
            #print(item.uid)
            uid_bytes = item.uid.to_bytes(8, byteorder='little')        
            item_bytes = uid_bytes + item_bytes
        #logger.debug(f"item_bytes size: {len(item_bytes)}")
        self._queue.send(item_bytes)
        if(item.shape != item_shape or self._shape != item_shape):
            raise RuntimeError(f"POSIXMsgQueue {self._name} of {self._shape} \
                shape can't push with wrong arguement item_shape {item_shape} or wrong item.shape {item.shape}")

    def state_pop(self):
        #logger.debug(f"state-pop!")
        if self._queue.current_messages > 0:           
           raw, _ = self._queue.receive()
           #raw, _ = self._queue.receive(timeout = 100)
           #logger.warning("state_pop after timeout 100")
           self._dtype_str = self._typelist[self._qid]
           item = np.frombuffer(raw, dtype=self._dtype_str, count=-1)  
           recv_array = item.reshape(self._shape)
           self._state = recv_array
        return self._state

    # state queue can't have uid as they may supply stored and stalled state items
    def pop(self):
        if self._queue_type == "state":
            item = self.state_pop()
            return item
        raw, _ = self._queue.receive()                
        #print(f"raw recv len {len(raw)} with type {type(raw)} on queue {self.name}")
        self._dtype_str = self._typelist[self._qid]        
        #logger.debug(f"recv data type: {self._dtype_str}")
        # deserialize uid from raw and get the data part out of the raw 
        # handle the uid for ndarray subclass for input and ouput queues
        if self._is_queue_observed == True:
            raw_view = memoryview(raw)
            item = np.frombuffer(raw_view[8:], dtype=self._dtype_str, count=-1)
            recv_array = item.reshape(self._shape) 
            item_uid = int.from_bytes(raw_view[:8], byteorder='little') #change to sys.byteorder if not sure
            recv_array = uidarray(recv_array, uid=item_uid)
        else:        
            item = np.frombuffer(raw, dtype=self._dtype_str, count=-1)  
            recv_array = item.reshape(self._shape)
        #logger.debug(f"recv_array.shape {recv_array.shape} with dtype {self._dtype_str,}")
        return recv_array
    
    @property
    def qid(self):
        return self._qid
    
    @property
    def qsize(self):
        return self._queue.current_messages

    @property
    def shape(self):
        return self._shape

    @property
    def name(self) -> str:
        return self._name

    @property
    def queue_type(self):
        return self._queue_type

## each process can only take 1 callable object, we use this function that takes
## a component in its argument. This is the "main-loop" for the process 
class PPRuntime(object):
    def __init__(self, graph: Graph, iteration=1) -> None:
        self._iterations = iteration
        self._ready_queue = deque() # _ready_queue for BFS once
        self._graph = graph
        self._process_handles = []
        self._posix_msg_queues_table = {}
        self._typelist = None
        self._qid_table = {}
        self.launch_time = time.time()

    def join(self):        
        for handle in self._process_handles:
            logger.debug(f"handle: {handle}")
            handle.join()
        logger.info(f"we've used {len(self._process_handles)} processes")

    def posix_msq_queue_cleanup(self):
        logger.debug(f"called posix_msq_queue_cleanup")
        for name, queue in self._posix_msg_queues_table.items():
            logger.debug(f"queue: {name}")
            queue.unlink()
            queue.close()
        self._typelist.shm.close()
        self._typelist.shm.unlink()
    
    def calculate_latency(self, *args):
        print("latency doing nothing")
        pass
    
    def __del__(self):                     
        self.join()
        self.calculate_latency()
        
        # clean up per component latency list
        for comp in self._graph.components:
            comp.destory()

        self.posix_msq_queue_cleanup()
        end_time = time.time()
        logger.warning(f"runtime elapsed time {end_time - self.launch_time}")
        logger.warning(f"runtime init time {self.init_time}")
        logger.warning(f"component exec time {end_time - self.start_time}")
        logger.debug(f"called __del__")
    
    def ready_queue_push(self, dst_q_list):
        logger = logging.getLogger(__name__)  
        for _ , dst_comp_name in dst_q_list:
            logger.debug(f"component from dst_q_list:{dst_comp_name}")
            dst_comp = self._graph.get_component_byname(dst_comp_name)
            logger.debug(f"dst_comp.status:{dst_comp.component_status}")
            if dst_comp.component_status == ComponentStatus.initialized or \
                dst_comp.component_status == ComponentStatus.running:

                dst_comp.component_status = ComponentStatus.running
                # avoid adding the same component to the _ready_queue multiple times 
                if dst_comp not in self._ready_queue:
                    self._ready_queue.append(dst_comp)
                else:
                    logger.debug("-------- comp existed --------")
                logger.debug(f"pushed component:{dst_comp.name}")
                logger.debug(f"queue len after push:{len(self._ready_queue)}")
            else:
                logger.info("An edge to executed or running component")    		

    def initialize(self, max_msg_count=100, max_msg_size=4000):
        init_start = time.time()
        for comp in self._graph.components:
            comp._component_status = ComponentStatus.initialized 

        # do BFS for all comp
        self._graph.components[0]._component_status = ComponentStatus.running

        self._ready_queue.append(self._graph.components[0])
        while len(self._ready_queue) > 0 :
            comp = self._ready_queue.popleft()
            logger.debug(f"comp.name:{comp.name}")
            logger.debug(f"comp.write_queues:{comp.write_queues}")
            ## outgoing edges based on state and output queues
            for queue_name in comp.write_queues:
                dst_list = self._graph.edges.get((queue_name, comp.name))
                logger.debug(f"dst_list:{dst_list}")
                if dst_list is None: # for state queues with no connected edge to other components
                    mq = posix_ipc.MessageQueue('/' + queue_name, posix_ipc.O_CREAT, max_messages=max_msg_count, 
                        max_message_size=max_msg_size)
                    print(f"dst-list-None,{mq}")
                    self._posix_msg_queues_table[mq.name] = mq
                    logger.debug(self._posix_msg_queues_table.keys())   
                    continue                

                if len(dst_list) > 1: #[TODO] we'll need to handle split and select
                    self.ready_queue_push(dst_list)
                    for dst_q_name, dst_comp in dst_list:
                        posix_ipc.MessageQueue('/' + dst_q_name, posix_ipc.O_CREAT, max_messages=max_msg_count,
                        max_message_size=max_msg_size)            
                elif len(dst_list) == 1:
                    self.ready_queue_push(dst_list)
                    dst_q_name, _ = dst_list[0]
                    if dst_q_name == queue_name:
                        mq = posix_ipc.MessageQueue('/' + queue_name, posix_ipc.O_CREAT, max_messages=max_msg_count,
                            max_message_size=max_msg_size)
                        self._posix_msg_queues_table[mq.name] = mq
                        logger.debug(self._posix_msg_queues_table.keys())
                    else:
                        raise RuntimeError(f"src and dst queue has different names, rename one of them to make the edge valid")
                else:
                    logger.debug("no-edge to worry about!")

            ## to deal with not connected input queues like source or input queue used in testing
            for queue_name in comp.input_names:
                mq = posix_ipc.MessageQueue('/' + queue_name, posix_ipc.O_CREAT, max_messages=max_msg_count, 
                    max_message_size=max_msg_size)
                self._posix_msg_queues_table[mq.name] = mq
                logger.debug(self._posix_msg_queues_table.keys())

            comp._component_status = ComponentStatus.paused

        # dealing with setting types for each msg_queue in _posix_msg_queues_table
        length_of_queues = len(self._posix_msg_queues_table)
        logger.debug(f"before table built, queue length: {length_of_queues}")
        typelist = ['<f4'] * length_of_queues # default type as float32
        self._typelist = shm.ShareableList(typelist, name='msgq_dtype')
        ## build the queue-name -> qid table here!        
        for qid, msg_queue_name in enumerate(self._posix_msg_queues_table):
            self._qid_table[msg_queue_name] = qid
        
        # for queue in self._posix_msg_queues_table:
        #         logger.debug(f"after table built, queue: {queue}")
        self.init_time = time.time() - init_start

    def execute(self):
        self.start_time = time.time()
        #mp.set_start_method('spawn')
        #mp.set_start_method('forkserver', force=True)
        for comp in self._graph.components:
            ## pass queue-name -> qid table here  
            handle = mp.Process(target=self.comp_execute, args=(comp, self._qid_table))
            self._process_handles.append(handle)
            handle.start()
        
    ## pass queue-name -> qid table (fixed before processes are launched) 
    ## Each process use this table to 
    ## (1) name -> qid, then (2) qid to type on shared-memory typelist
    def comp_execute(self, comp, qid_table):
        comp_start = time.time()
        logger = logging.getLogger(__name__) 
        #logger.info('parent process:', os.getppid())
        #logger.info(f"process id:{os.getpid()}")
        logger.info(f"comp.name {comp.name} on process {os.getpid()} started")
        local_typelist = shm.ShareableList(name='msgq_dtype')
        logger.debug(f"qid-table:{qid_table}")

        # assing runtime's iteration to the comp if it's not set implicitly 
        if comp.iterations == -1:
            comp.iterations = self._iterations

        logger.debug(f"start comp init on process {os.getpid()}")
        #logger.info(comp.__dict__)
        if len(comp.init_arg_names) > 0:
            args_tuple = ()
            for state_name in comp.state_names:
                state_shape, is_state_observed = comp.state_queues[state_name]
                qid = qid_table.get('/' + state_name)
                assert qid is not None
                assert qid >= 0 and qid < len(local_typelist)
                state_q = POSIXMsgQueue('/'+state_name, state_shape, "state", qid, is_state_observed)
                mq = posix_ipc.MessageQueue('/'+state_name, posix_ipc.O_CREAT)
                state_q.init_queue(mq)                            
                args_tuple = (*args_tuple, state_q)
            for _, param in comp._parameters.items():
                args_tuple = (*args_tuple, param)
            logger.debug(f"right before initialize() on process {os.getpid()}")
            comp.initialize(*args_tuple)                
        else:
            comp.initialize()
        
        logger.debug(f"end comp init on process {os.getpid()}")

        if len(comp.exec_arg_names) > 0:
            args_tuple = ()                    
            for input_name in comp.input_names:
                qid = qid_table.get('/' + input_name)
                assert qid is not None
                assert qid >= 0 and qid < len(local_typelist)
                input_shape, is_input_observed = comp._input_queues[input_name]
                logger.debug(f"input_shape {input_shape}")
                input_q = POSIXMsgQueue('/'+input_name, input_shape, "input", qid, is_input_observed)
                mq = posix_ipc.MessageQueue('/'+input_name, posix_ipc.O_CREAT)
                input_q.init_queue(mq)
                logger.debug(f"input_queue name: {input_q.name}")
                args_tuple = (*args_tuple, input_q)

            for state_name in comp.state_names:
                qid = qid_table.get('/' + state_name)
                assert qid is not None
                assert qid >= 0 and qid < len(local_typelist)
                state_shape, is_state_observed = comp._state_queues[state_name]
                state_q = POSIXMsgQueue('/'+state_name, state_shape, "state", qid, is_state_observed)
                mq= posix_ipc.MessageQueue('/'+state_name, posix_ipc.O_CREAT)
                state_q.init_queue(mq)
                logger.debug(f"state_queue name: {state_q.name}")
                args_tuple = (*args_tuple, state_q)
    
            for output_name in comp.output_names:
                qid = qid_table.get('/' + output_name)
                assert qid is not None
                assert qid >= 0 and qid < len(local_typelist)
                output_shape, is_output_observed = comp._output_queues[output_name]
                logger.debug(f"output_shape {output_shape}")
                output_q = POSIXMsgQueue('/'+output_name, output_shape, "output", qid, is_output_observed)
                mq = posix_ipc.MessageQueue('/'+output_name, posix_ipc.O_CREAT)
                output_q.init_queue(mq)
                logger.debug(f"output_queue name: {output_q.name}")
                args_tuple = (*args_tuple, output_q)
            
            for queue in self._posix_msg_queues_table:
                logger.debug(f"before exec, queue: {queue}")

            # this may need to run serveral iterations
            #for iter in range(self._iterations):            
            exec_start = time.time()
            for iter in range(comp.iterations):            
                logger.info(f"comp.name {comp.name}, iter: {iter}")
                comp.execute(*args_tuple)
            end = time.time()
            mean_exec_init = (exec_start-comp_start)
            mean_exec_time = (end-exec_start)
            logger.warning(f"{comp.name} init time:{mean_exec_init}")
            logger.warning(f"{comp.name} exec time:{mean_exec_time}")
            #comp.destory()

            # for queue in self._posix_msg_queues_table:
            #     logger.debug(f"after exec, queue: {queue}")

            # TODO: output and state queues_handler for split (and select).
            # this is for each iteration of comp.execute(*args_tuple)
            # components don't push directly into the posix msg queues
            # the runtime will replicate (in the case of split) or assign 
            # (in the case of select) to the right posix msg queue(s)