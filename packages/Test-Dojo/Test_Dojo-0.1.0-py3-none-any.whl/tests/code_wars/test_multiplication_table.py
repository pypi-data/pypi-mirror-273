def multiplication_table(size: int) -> list:
    one_to_size_list = []
    bolo_list = []
    for number in range(1, size + 1):
        one_to_size_list.append(number)
    for num in one_to_size_list:
        multiples_list = []
        for numb in range(1, size + 1):
            multiples_list.append(num * numb)
        bolo_list.append(multiples_list)
    return bolo_list


def test_multiplication_table():
    assert multiplication_table(1) == [[1]]
    assert multiplication_table(2) == [[1, 2], [2, 4]]
    assert multiplication_table(3) == [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
