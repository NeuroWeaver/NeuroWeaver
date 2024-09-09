import logging

def preprocess_python_code(raw_string):
    """Given a raw string of Python code, perform the following:
    1) replace \n with ;
    2) remove whitespace in the beginning of the string
    """
    pass

def write_to(path, data, mode='wb'):
    with open(path, mode) as f:
        f.write(data.SerializeToString())

def read_protobuf(path, obj):
    """Obj must be a protobuf object"""
    with open(path, 'rb') as f:
        obj.ParseFromString(f.read())

def read_file(path, mode='r'):
    with open(path, mode) as f:
        s = f.read()
    return s

# Thread-safe logging module
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)-15s [%(levelname)s] (%(threadName)-10s) %(message)s',
# )
