# https://codingdojo.org/kata/Potter/


def total_price(books):
    total = 0
    duplicated_books = []
    sett = []
    loop = 0

    while loop < max(books):
        count = 0
        for i in books:
            if i > 0:
                count += 1
                i -= 1
        loop += 1
        sett.append(count)
    # while i < max(books):
    #     for k in books:
    #         index = 0
    #         if k > 0:
    #             sett.append(1)
    #
    #     i += 1

    # for i in books:
    #     if i >= 1:
    #         duplicated_books.append(1)
    #
    # for i in books:
    #     if duplicated_books.count(i) == 2:
    #         total += 8 * i * 0.95
    #     elif duplicated_books.count(i) == 3:
    #         total += 8 * i * 0.90
    #     elif duplicated_books.count(i) == 4:
    #         total += 8 * i * 0.80
    #     elif duplicated_books.count(i) == 5:
    #         total += 8 * i * 0.75
    #     else:
    #         total += 8 * i

    return sett


def test_one():
    assert total_price([1, 0, 0, 0, 0]) == 8


def test_two_same():
    assert total_price([2, 0, 0, 0, 0]) == 16


#
def test_two_different():
    assert total_price([1, 1, 0, 0, 0]) == 15.2
    assert total_price([2, 2, 0, 0, 0]) == 30.4


def test_three_different():
    assert total_price([1, 1, 1, 0, 0]) == 21.6
    assert total_price([2, 2, 2, 0, 0]) == 43.2


def test_four_different():
    assert total_price([1, 1, 1, 1, 0]) == 25.6
    assert total_price([2, 2, 2, 2, 0]) == 51.2


def test_five_different():
    assert total_price([1, 1, 1, 1, 1]) == 30
    assert total_price([2, 2, 2, 2, 2]) == 60


def test_two_different_2():
    assert total_price([2, 1, 0, 0, 0]) == 23.2
