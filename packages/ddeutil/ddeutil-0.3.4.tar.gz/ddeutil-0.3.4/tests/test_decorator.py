import ddeutil.core.decorator as decorator


def test_deepcopy():
    @decorator.deepcopy
    def foo(a, b, c=None):
        c = c or {}
        a[1] = 3
        b[2] = 4
        c[3] = 5
        return a, b, c

    aa = {1: 2}
    bb = {2: 3}
    cc = {3: 4}

    assert foo(aa, bb, cc) == ({1: 3}, {2: 4}, {3: 5})
