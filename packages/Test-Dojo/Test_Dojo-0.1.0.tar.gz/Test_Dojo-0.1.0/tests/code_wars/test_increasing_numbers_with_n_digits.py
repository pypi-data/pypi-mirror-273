def increasing_numbers(digits: int) -> int:
    if 10**digits <= 10:
        return len(range(10**digits))

    counter = 10**digits

    for i in range(10**digits):
        number = str(i)
        for index, k in enumerate(number[1:], start=1):
            print(str(index) + " " + str(k))
            if int(k) < int(number[index - 1]):
                counter -= 1
                break

    return counter


def test_0():
    assert increasing_numbers(0) == 1
    assert increasing_numbers(1) == 10
    assert increasing_numbers(2) == 55
