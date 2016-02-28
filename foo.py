def f():
    [
        boom()
        for x in range(2)
        if x
        ]

import dis

def boom():
    raise RuntimeError()

dis.dis(f.__code__.co_consts[1])

f()
