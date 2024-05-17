def seven_wonders_science(compasses, gears, tablets):
    return (
        min(compasses, gears, tablets) * 7 + compasses**2 + gears**2 + tablets**2
    )


def test_seven_wonders_science():
    assert seven_wonders_science(0, 0, 0) == 0
    assert seven_wonders_science(1, 1, 1) == 10
    assert seven_wonders_science(2, 1, 1) == 13
    assert seven_wonders_science(4, 2, 2) == 38
