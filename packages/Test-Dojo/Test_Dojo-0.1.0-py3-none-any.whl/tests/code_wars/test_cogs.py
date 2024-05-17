def cog_RPM(cogs: list) -> float:
    rpm = cogs[0] / cogs[-1]
    return rpm if len(cogs) % 2 > 0 else -rpm


def test_even_cogs():
    assert cog_RPM([100, 75]) == -4 / 3
