def f():
    return [j
            for i in range(3)
            if i]

def boom():
    raise RuntimeError()

import dis

dis.dis(f)
print(); dis.dis(f.__code__.co_consts[1])

print()
f()
