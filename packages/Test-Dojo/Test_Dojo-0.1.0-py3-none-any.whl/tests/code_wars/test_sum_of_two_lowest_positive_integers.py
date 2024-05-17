def sum_two_smallest_numbers(numbers: list) -> int:
    sort = sorted(set(numbers))
    return sort[0] + sort[1]


def test_():
    assert sum_two_smallest_numbers([1, 2, 3, 4]) == 3
