

@Component
def thread_1():
    a = 5
    print(f'Thread 1: a = {a}')
    return a


@Component
def thread_2(b):
    print(f'Thread 2: b = {b}')


def main():
    out = thread_1()
    thread_2(out)
