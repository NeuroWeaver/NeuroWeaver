import sys

sys.path.append("../..") #add ../.. to python path
sys.path.append("..")
print(sys.path)

import numpy as np
import posix_ipc
from collections import deque
from multiprocessing import shared_memory as shm
from runtime.process_runtime import POSIXMsgQueue, uidarray

# https://numpy.org/doc/1.21/user/basics.subclassing.html
class C:
    def __new__(cls, *args):
        print('Cls in __new__:', cls)
        print('Args in __new__:', args)
        # The `object` type __new__ method takes a single argument.
        return object.__new__(cls)

    def __init__(self, *args):
        print('type(self) in __init__:', type(self))
        print('Args in __init__:', args)


# class InfoArray(np.ndarray):

#     def __new__(subtype, shape, dtype=float, buffer=None, offset=0,
#                 strides=None, order=None, info=None):
#         # Create the ndarray instance of our type, given the usual
#         # ndarray input arguments.  This will call the standard
#         # ndarray constructor, but return an object of our type.
#         # It also triggers a call to InfoArray.__array_finalize__
#         obj = super().__new__(subtype, shape, dtype,
#                               buffer, offset, strides, order)
#         # set the new 'info' attribute to the value passed
#         obj.info = info
#         # Finally, we must return the newly created object:
#         return obj

#     def __array_finalize__(self, obj):
#         # ``self`` is a new object resulting from
#         # ndarray.__new__(InfoArray, ...), therefore it only has
#         # attributes that the ndarray.__new__ constructor gave it -
#         # i.e. those of a standard ndarray.
#         #
#         # We could have got to the ndarray.__new__ call in 3 ways:
#         # From an explicit constructor - e.g. InfoArray():
#         #    obj is None
#         #    (we're in the middle of the InfoArray.__new__
#         #    constructor, and self.info will be set when we return to
#         #    InfoArray.__new__)
#         if obj is None: return
#         # From view casting - e.g arr.view(InfoArray):
#         #    obj is arr
#         #    (type(obj) can be InfoArray)
#         # From new-from-template - e.g infoarr[:3]
#         #    type(obj) is InfoArray
#         #
#         # Note that it is here, rather than in the __new__ method,
#         # that we set the default value for 'info', because this
#         # method sees all creation of default objects - with the
#         # InfoArray.__new__ constructor, but also with
#         # arr.view(InfoArray).
#         self.info = getattr(obj, 'info', None)
#         # We do not need to return anything


# class uidarray(np.ndarray):

#     def __new__(cls, input_array, uid=None):
#         # Input array is an already formed ndarray instance
#         # We first cast to be our class type
#         obj = np.asarray(input_array).view(cls)
#         # add the new attribute to the created instance
#         obj.uid = uid
#         # Finally, we must return the newly created object:
#         return obj

#     def __array_finalize__(self, obj):
#         # see InfoArray.__array_finalize__ for comments
#         if obj is None: return
#         self.uid = getattr(obj, 'uid', None)

arr = np.arange(10)
print(arr.dtype)
item = uidarray(arr, uid=777)
print(f"item has uid: {hasattr(item, 'uid')}")

item2 = np.arange(10)
#print(item)
#print(item.info)
#item_bytes = item.tobytes()
#print(f"item_bytes size: {len(item_bytes)}")
#print(item is np.ndarray)

llist = ['<i8'] * 2 # default type as float32
typelist = shm.ShareableList(llist, name='msgq_dtype')

#q_name = '/message_queue0' # abs path: /dev/mqueue/message_queue0
#mq = posix_ipc.MessageQueue(q_name, posix_ipc.O_CREX, max_message_size=8000)

#def __init__(self, name, shape, queue_type:str = None, qid:int = 0):
mq = posix_ipc.MessageQueue('/testq0', posix_ipc.O_CREX, max_messages=20, max_message_size=1000)
print(mq.max_messages)
state_q = POSIXMsgQueue("/testq0", (10,), "input", 0)
state_q.init_queue(mq)

# print(item)
# item_bytes= item.tobytes()
# item_bytes = item.tobytes()
# print(f"item_bytes size: {len(item_bytes)}")

# print(f"type:{type(item.uid)}")
# uid_bytes = item.uid.to_bytes(8,sys.byteorder)
# print(f"uid_bytes size: {len(uid_bytes)}")
# item_bytes = uid_bytes + item_bytes
# print(f"all bytes size: {len(item_bytes)}")

# item_view = memoryview(item_bytes)
# recovered_int = int.from_bytes(item_view[:8],sys.byteorder)
# print(recovered_int)
# #recovered_int2 = int.from_bytes(uid_bytes,sys.byteorder)
# #print(recovered_int2)
# recovered = np.frombuffer(item_view[8:],dtype='<i8', count=-1)
# print(recovered)


state_q.push(item, (10,))
pop_item = state_q.pop()
print(f"item has uid: {hasattr(pop_item, 'uid')} and uid: {pop_item.uid}")
pop_item = pop_item.reshape((1,10))
print(f"pop_item shape: {pop_item.shape}")

#state_q.push(item2, (10,))

mq.unlink()
typelist.shm.close()
typelist.shm.unlink()

#queue1 = POSIXMsgQueue("testq1", (10,), "state", 1)