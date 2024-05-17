def sort_array(source_array):
    if not source_array:
        return []

    list_of_odd_numbers = []
    list_of_indexes = []

    for j, i in enumerate(source_array):
        if i % 2 == 1:
            list_of_odd_numbers.append(i)
            list_of_indexes.append(j)

    list_of_odd_numbers.sort()

    for k, odd_number in zip(list_of_indexes, list_of_odd_numbers):
        source_array[k] = odd_number

    return source_array


def test_sort_array():
    assert sort_array([]) == []
    assert sort_array([1, 2]) == [1, 2]
    assert sort_array([3, 1, 2]) == [1, 3, 2]
