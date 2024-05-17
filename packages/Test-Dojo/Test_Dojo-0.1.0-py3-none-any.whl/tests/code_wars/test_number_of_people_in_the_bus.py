def number(bus_stops):
    stops_dict = dict(bus_stops)
    return sum(stops_dict.keys()) - sum(stops_dict.values())


def test_number():
    assert (
        number(
            [
                [31, 0],
                [85, 21],
                [80, 95],
                [1, 39],
                [35, 18],
                [36, 43],
                [31, 22],
                [92, 49],
                [36, 42],
                [49, 4],
                [0, 7],
                [14, 104],
                [6, 38],
                [3, 10],
                [96, 2],
                [74, 96],
                [16, 56],
                [68, 14],
                [28, 29],
            ]
        )
        == 92
    )
