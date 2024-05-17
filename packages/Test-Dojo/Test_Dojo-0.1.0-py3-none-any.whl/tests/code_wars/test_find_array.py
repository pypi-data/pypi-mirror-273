def find_array(arr1: list, arr2: list) -> list:
    if len(arr1) == 0 or len(arr2) == 0:
        return []

    lst = []
    for i in arr2:
        try:
            lst.append(arr1[i])
        except IndexError:
            pass
    return lst


def test_1():
    assert find_array([], []) == []


def test_2():
    assert find_array([2], [0]) == [2]


def test_3():
    assert find_array([2, 7, 3], [0, 1]) == [2, 7]


def test_4():
    assert find_array([1], []) == []
    assert find_array([], [2]) == []
    assert find_array([], []) == []


def test_5():
    assert find_array([0, 1], [3]) == []
