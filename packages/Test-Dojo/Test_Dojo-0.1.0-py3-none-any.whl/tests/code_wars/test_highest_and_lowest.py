def high_and_low(numbers):
    string_to_int = []
    for i in numbers.split():
        string_to_int.append(int(i))

    return (
        str(list(reversed(sorted(string_to_int)))[0])
        + " "
        + str(list(sorted(string_to_int))[0])
    )


def test_high_and_low():
    # assert high_and_low("1") == 1
    # assert high_and_low("1 2") == 1
    # assert high_and_low("8 2 1") == 1
    # assert high_and_low("8 2 1") == 1
    # assert high_and_low("1 8 2") == 1

    assert high_and_low("1 8 2") == "8 1"
