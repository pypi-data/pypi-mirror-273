def people_with_age_drink(age):
    if age <= 13:
        return "drink toddy"

    if age < 18:
        return "drink coke"

    if age < 21:
        return "drink beer"

    if age >= 21:
        return "drink whisky"


def test_1():
    assert people_with_age_drink(12) == "toddy"


def test_2():
    assert people_with_age_drink(17) == "coke"


def test_3():
    assert people_with_age_drink(20) == "beer"


def test_4():
    assert people_with_age_drink(29) == "whisky"
