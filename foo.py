def boom():
    raise RuntimeError()

def f():
    return [boom()
            for x in range(3)
            if x
            for y in range(x)
            ]

f()

import dis

dis.dis(f)
#print(); dis.dis(f.__code__.co_consts[1])

#f()
