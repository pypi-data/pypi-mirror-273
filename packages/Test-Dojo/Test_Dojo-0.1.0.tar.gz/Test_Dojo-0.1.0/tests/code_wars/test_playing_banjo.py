def are_you_playing_banjo(name):
    if name[0] == "R" or name[0] == "r":
        return f"{name} plays banjo"
    return f"{name} does not play banjo"


def test_1():
    assert are_you_playing_banjo("Robert") == "Robert plays banjo"
    assert are_you_playing_banjo("robert") == "robert plays banjo"
    assert are_you_playing_banjo("Toko") == "Toko does not play banjo"


