def find_nb(m):
    s = 0
    for i in range(m):
        s = s + (i**3)
        if s == m:
            return i
        elif s > m:
            break
    return -1


def test_find_nb():
    assert find_nb(100) == 4
    assert find_nb(577451452) == -1
    assert find_nb(4183059834009) == 2022
