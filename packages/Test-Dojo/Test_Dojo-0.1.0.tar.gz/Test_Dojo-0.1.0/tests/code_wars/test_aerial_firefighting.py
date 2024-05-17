import math


def waterbombs(fire: str, w: int) -> int:
    return sum(math.ceil(i.count("x") / w) for i in fire.split("Y"))


def test_no_fire():
    assert waterbombs("Y", 1) == 0


def test_no_building():
    assert waterbombs("x", 1) == 1


def test_one_width():
    assert waterbombs("xY", 1) == 1
    assert waterbombs("xxxxxxxYxxxxxxx", 1) == 14


def test_two_width():
    assert waterbombs("xxYYxx", 2) == 2


def test_three_width():
    assert waterbombs("xxYxx", 3) == 2


def test_four_width():
    assert waterbombs("xxxxYxxxYxxx", 4) == 3
