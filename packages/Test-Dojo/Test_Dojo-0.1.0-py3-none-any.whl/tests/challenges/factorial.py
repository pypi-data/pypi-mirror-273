# Create a program to calculate the factorial of a given number n with for loop.


def factorial(n):
    result = 1

    for i in range(1, n + 1):
        result *= i
    return result


def test_factorial():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(2) == 2
    assert factorial(3) == 6
    assert factorial(4) == 24
    assert factorial(40) == 815915283247897734345611269596115894272000000000


# Example usage:
# input_n = int(input("Enter a number (n): "))
# result = factorial(input_n)
# print(f"The factorial of {input_n} is: {result}")
