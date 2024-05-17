def find_short(s: str) -> int:
    return min(len(i) for i in s.split())


def test_():
    assert find_short("Let's travel abroad shall we") == 2
