def tower_builder(n_floors: int) -> list:
    pyramid = []
    for i in range(n_floors, 0, -1):
        pyramid.insert(0, "*" * (i - 1) * 2 + "*")

    return pyramid


def test_one():
    assert tower_builder(1) == ["*"]


def test_two():
    assert tower_builder(2) == [" * ", "***"]
