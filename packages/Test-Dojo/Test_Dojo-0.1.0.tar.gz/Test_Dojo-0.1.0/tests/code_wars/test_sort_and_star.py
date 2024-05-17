def two_sort(array: list) -> str:
    return "***".join([i for i in sorted(array)[0]])


def test_tw0_sort():
    assert two_sort([""]) == ""
    assert two_sort(["B", "A"]) == "A"
    assert two_sort(["B", "A", "a"]) == "A"
    assert two_sort(["B", "Aa", "a"]) == "A***a"
