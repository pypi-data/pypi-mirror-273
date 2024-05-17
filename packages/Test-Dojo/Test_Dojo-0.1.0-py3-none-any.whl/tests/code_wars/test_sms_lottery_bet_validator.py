def validate_bet(game: list, text: str) -> list | None:
    text = text.replace(" ", ",")
    lst = [i for i in text.split(",")]
    lst2 = [int(i) for i in lst if i.isnumeric()]

    if 0 in lst2 or len(lst2) != game[0]:
        return None

    for i in lst2:
        if lst2.count(i) > 1 or i > game[1]:
            return None

    return sorted(lst2)


def test_():
    assert validate_bet([2, 10], "1, 2") == [1, 2]
    assert validate_bet([2, 10], "1, 2, 15") == None
    assert validate_bet([5, 90], "1 2 3 4 5") == [1, 2, 3, 4, 5]
    assert validate_bet([5, 90], "1, 2, 3; 4, 5") == None
    assert validate_bet([5, 90], "5 , 3, 1  4,2") == [1, 2, 3, 4, 5]
    assert validate_bet([2, 10], "0, 2") == None
    assert validate_bet([2, 10], "2, 2") == None
