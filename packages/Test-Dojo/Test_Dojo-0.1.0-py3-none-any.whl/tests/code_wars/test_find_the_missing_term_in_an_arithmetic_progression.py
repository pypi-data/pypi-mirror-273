def find_missing(sequence: list) -> int:
    d = sequence[-1] - sequence[-2]
    # return [i for i in range(sequence[0], sequence[-1], d) if i not in sequence][0]
    for i, number in enumerate(sequence):
        if number + d != sequence[i + 1]:
            return number + d


def test_():
    assert find_missing([1, 2, 3, 4, 6, 7, 8, 9]) == 5
