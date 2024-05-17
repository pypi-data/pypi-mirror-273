import string


def high(x):
    a = {}
    b = {}
    s = 0
    for i, j in enumerate(list(string.ascii_lowercase)):
        a = {**a, j: i + 1}
    for z in range(len(x.split())):
        for y in x.split()[z]:
            s = s + a[y]
        b = {**b, x.split()[z]: s}
        s = 0
    q = sorted(b)
    w = q.reverse()
    return q[0]

    # return s

    #     if k == x.split()[0][0]:
    #         s = s + v
    #     else:
    #         pass
    # return s

    # if x.split()[0][0] == j:
    #     for l in x.split()[0]:
    # return s

    # for k in x.split()[0][0]:


def test_high():
    # assert high("a") == 1
    # assert high("b") == 2
    # assert high("z") == 26
    # assert high("ab") == 3
    # assert high("abc") == 6
    assert high("abc z a") == 26
