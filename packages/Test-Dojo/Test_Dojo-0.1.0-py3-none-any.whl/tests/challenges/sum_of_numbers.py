# Write a program to calculate the sum of all numbers from 1 to a given input n with for loop.


def sum_of_numbers(n):
    return sum(i for i in range(1, n + 1))


def test_sum_of_numbers():
    assert sum_of_numbers(2) == 3
    assert sum_of_numbers(200) == 20100


# Example usage:
# input_n = int(input("Enter a number: "))
# result = sum_of_numbers(input_n)
# print(f"The sum of numbers from 1 to {input_n} is: {result}")
