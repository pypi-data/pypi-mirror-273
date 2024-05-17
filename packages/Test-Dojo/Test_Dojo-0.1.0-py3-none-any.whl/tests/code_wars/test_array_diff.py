def array_diff(a: list, b: list) -> list:
    return [i for i in a if i not in b]


# def array_diff(a, b):
#     for num in b:
#         while num in a:
#             a.remove(num)
#     return a


def test_():
    assert array_diff([1, 2], [1]) == [2]
