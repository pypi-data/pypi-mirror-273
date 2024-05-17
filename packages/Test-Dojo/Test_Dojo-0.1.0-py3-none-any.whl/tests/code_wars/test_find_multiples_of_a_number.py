def find_multiples(integer, limit):
    return [i for i in range(integer, limit + 1) if i % integer == 0]


def test_find_multiples():
    assert find_multiples(10, 120) == [
        10,
        20,
        30,
        40,
        50,
        60,
        70,
        80,
        90,
        100,
        110,
        120,
    ]
