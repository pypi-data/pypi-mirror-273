def first_non_consecutive(arr):
    for i in range(1, len(arr)):
        if arr[i] != arr[i - 1] + 1:
            return arr[i]
    return None


def test_first_non_consecutive():
    assert first_non_consecutive([1, 2, 3, 4, 6, 7, 8]) == 6
    assert first_non_consecutive([1, 2, 3, 4, 5, 6, 7, 8]) is None
