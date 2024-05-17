def find_dups_miss(arr: list) -> list:
    unique_from_duplicated = sorted({i for i in arr if arr.count(i) > 1})

    lst2 = [i for i in range(min(arr), max(arr)) if i not in arr]

    lst2.append(unique_from_duplicated)
    return lst2


def test_only_one_duplicates():
    assert find_dups_miss([1, 1]) == [[1]]


def test_one_duplicate_and_one_random_number():
    assert find_dups_miss([1, 1, 2]) == [[1]]


def test_two_elements():
    assert find_dups_miss([1, 1, 2, 4]) == [3, [1]]


def test_unordered_elements():
    assert find_dups_miss([4, 4, 1, 1, 6, 3]) == [2, 5, [1, 4]]


def test_missing_numbers():
    assert find_dups_miss([1, 1, 2, 2, 3, 3]) == [[1, 2, 3]]
