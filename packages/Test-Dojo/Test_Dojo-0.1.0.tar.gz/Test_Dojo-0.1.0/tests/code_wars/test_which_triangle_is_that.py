def type_of_triangle(a, b, c):
    if not (
        isinstance(a, (int, float))
        and isinstance(b, (int, float))
        and isinstance(c, (int, float))
    ):
        return "Not a valid triangle"

    if (a >= b + c) or (b >= a + c) or (c >= a + b):
        return "Not a valid triangle"

    if a == b == c:
        return "Equilateral"
    elif a != b != c != a:
        return "Scalene"
    else:
        return "Isosceles"


def test_type_of_triangle():
    assert type_of_triangle(2, 2, 3) == "Isosceles"
    assert type_of_triangle(1, 2, 3) == "Not a valid triangle"
    assert type_of_triangle(3, 4, 5) == "Scalene"
    assert type_of_triangle(3, 3, 3) == "Equilateral"
    assert type_of_triangle("3", 3, 3) == "Not a valid triangle"
