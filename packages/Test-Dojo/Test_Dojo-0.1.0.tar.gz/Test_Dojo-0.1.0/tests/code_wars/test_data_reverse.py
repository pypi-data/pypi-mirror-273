# def data_reverse(data: []) -> list:
# #     bit = 8
# #     i = 0
# #     lst = []
# #     lst_2 = []
# #     while i < len(data) / 8:
# #         lst.append(data[bit - 8 : bit])
# #         bit += 8
# #         i += 1
# #     lst.reverse()
# #     for i in lst:
# #         lst_2 += i
# #
# #     return lst_2
def data_reverse(inp):
    out = []
    while len(inp):
        out = inp[0:8] + out
        inp = inp[8:]
    return out


def test_1():
    assert data_reverse(
        [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            1,
            1,
            1,
            1,
            1,
            0,
            1,
            0,
            1,
            0,
            1,
            0,
        ]
    ) == [
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
    ]
