def sort_by_length(arr):
    return sorted(arr, key=len)


def test_sort_by_length():
    assert sort_by_length(["bc", "a"]) == ["a", "bc"]
    assert sort_by_length(["def", "bc", "a"]) == ["a", "bc", "def"]
