def digital_root(n):
    a = sum(int(i) for i in str(n))
    if len(str(a)) < 2:
        return a
    return digital_root(a)



def test_1():
    assert digital_root(5) == 5
def test_2():
    assert digital_root(16) == 7

def test_3 ():
    assert digital_root(27) == 9

def test_4():
    assert digital_root(168) == 6

def test_5():
    assert digital_root(493193) == 2

