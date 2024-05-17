def sum_strings(x: str, y: str) -> str:
    if not x:
        x = "0"
    if not y:
        y = "0"

    x_list = [int(i) for i in x]
    y_list = [int(i) for i in y]

    len_x = len(x_list)
    len_y = len(y_list)

    memory = 0
    product = []

    if len_y <= len_x:
        for i in range(len_y):
            a = x_list[len_x - i - 1] + y_list[len_y - i - 1] + memory
            b = str(a)
            product.insert(0, b)
            if a > 9:
                memory = a - 9

    return "".join(product)


def test_sum_1_1():
    assert sum_strings("1", "1") == "2"
    assert sum_strings("0", "") == "0"
    assert sum_strings("123", "456") == "579"
    assert sum_strings("1234", "456") == "1690"
