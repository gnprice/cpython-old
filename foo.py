def f():
    boom(
        1,
        )

import dis

def boom():
    raise RuntimeError()

dis.dis(f)
