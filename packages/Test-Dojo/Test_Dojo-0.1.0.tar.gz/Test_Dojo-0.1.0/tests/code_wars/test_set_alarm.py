def set_alarm(employed, vacation):
    return True if employed and not vacation else False


def test_set_alarm():
    assert set_alarm(True, True) == False
    assert set_alarm(False, True) == False
    assert set_alarm(False, False) == False
    assert set_alarm(True, False) == True
