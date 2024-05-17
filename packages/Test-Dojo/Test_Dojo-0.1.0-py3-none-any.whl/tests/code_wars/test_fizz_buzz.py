# def fizz_buzz(number):
#     lst = []
#     for i in range(1, number + 1):
#         if i % 3 == 0 and i % 5 == 0:
#             lst.append("FizzBuzz")
#         elif i % 3 == 0:
#             lst.append("Fizz")
#         elif i % 5 == 0:
#             lst.append("Buzz")
#         elif i % 3 != 0 or i % 5 != 0:
#             lst.append(i)
#
#     return lst


def fizz_buzz(number):
    if number % 3 == 0 and number % 5 == 0:
        return "FizzBuzz"
    elif number % 3 == 0:
        return "Fizz"
    elif number % 5 == 0:
        return "Buzz"
    return number


def make_list(number):
    # lst = []
    # for i in range(1, number + 1):
    #     lst.append(fizz_buzz(i))
    # return lst
    return [fizz_buzz(i) for i in range(1, number + 1)]


# def test_():
#     assert fizz_buzz(1) == "1"
#     assert fizz_buzz(2) == "2"
#     assert fizz_buzz(3) == "Fizz"
#     assert fizz_buzz(4) == "4"
#     assert fizz_buzz(5) == "Buzz"
#     assert fizz_buzz(6) == "Fizz"
#     assert fizz_buzz(10) == "Buzz"
#     assert fizz_buzz(15) == "FizzBuzz"
#     assert fizz_buzz(30) == "FizzBuzz"


def test_list():
    assert make_list(3) == [1, 2, "Fizz"]
    assert make_list(5) == [1, 2, "Fizz", 4, "Buzz"]
