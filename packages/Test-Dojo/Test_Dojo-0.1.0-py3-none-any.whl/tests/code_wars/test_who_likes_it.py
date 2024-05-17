def likes(names: list) -> str:
    if len(names) == 0:
        return "no one likes this"
    if len(names) < 2:
        return f"{names[0]} likes this"
    if len(names) < 3:
        return f"{names[0]} and {names[1]} like this"
    if len(names) < 4:
        return f"{names[0]}, {names[1]} and {names[2]} like this"
    if len(names) > 3:
        return f"{names[0]}, {names[1]} and {len(names) - 2} others like this"


def test_no_likes():
    assert likes([]) == "no one likes this"


def test_one_like():
    assert likes(["Peter"]) == "Peter likes this"


def test_two_likes():
    assert likes(["Jacob", "Alex"]) == "Jacob and Alex like this"


def test_three_likes():
    assert likes(["Max", "John", "Mark"]) == "Max, John and Mark like this"


def test_four_likes():
    assert (
        likes(["Alex", "Jacob", "Mark", "Max"]) == "Alex, Jacob and 2 others like this"
    )
