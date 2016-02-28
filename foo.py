def f():
    class C():
        def ff():
            pass

    boom(
        1)

import dis

def boom():
    raise RuntimeError()

dis.dis(f)
print(); dis.dis(f.__code__.co_consts[1])

#f()
