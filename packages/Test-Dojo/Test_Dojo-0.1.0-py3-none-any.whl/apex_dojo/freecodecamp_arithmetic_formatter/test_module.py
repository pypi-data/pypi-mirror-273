import pytest

from apex_dojo.freecodecamp_arithmetic_formatter.arithmetic_arranger import (
    arithmetic_arranger,
)


def test_one_problem_arrangement0():
    assert arithmetic_arranger(["7 - 2"]) == "  7\n- 2\n---"
    assert arithmetic_arranger(["100 - 1"]) == "  100\n-   1\n-----"
    assert arithmetic_arranger(["1 - 10"]) == "   1\n- 10\n----"


def test_two_problems_arrangement1():
    assert (
        arithmetic_arranger(["3801 - 2", "123 + 49"])
        == "  3801      123\n-    2    +  49\n------    -----"
    )


def test_two_problems_arrangement2():
    assert (
        arithmetic_arranger(["1 + 2", "1 - 9380"])
        == "  1         1\n+ 2    - 9380\n---    ------"
    )


def test_four_problems_arrangement():
    assert (
        arithmetic_arranger(["3 + 855", "3801 - 2", "45 + 43", "123 + 49"])
        == "    3      3801      45      123\n+ 855    -    2    + 43    +  49\n-----    ------    ----    -----"
    )


def test_five_problems_arrangement():
    assert (
        arithmetic_arranger(["11 + 4", "3801 - 2999", "1 + 2", "123 + 49", "1 - 9380"])
        == "  11      3801      1      123         1\n+  4    - 2999    + 2    +  49    - 9380\n----    ------    ---    -----    ------"
    )


def test_too_many_problems():
    assert (
        arithmetic_arranger(
            ["44 + 815", "909 - 2", "45 + 43", "123 + 49", "888 + 40", "653 + 87"]
        )
        == "Error: Too many problems."
    )


def test_incorrect_operator():
    assert (
        arithmetic_arranger(["98 + 3g5", "3801 - 2", "45 + 43", "123 + 49"])
        == "Error: Operator must be '+' or '-'."
    )


def test_too_many_digits():
    assert (
        arithmetic_arranger(["24 + 85215", "3801 - 2", "45 + 43", "123 + 49"])
        == "Error: Numbers cannot be more than four digits."
    )


def test_only_digits():
    assert (
        arithmetic_arranger(["98 + 3g5", "3801 - 2", "45 + 43", "123 + 49"])
        == "Error: Numbers must only contain digits."
    )


def test_one_problem_with_solution():
    assert arithmetic_arranger(["7 - 2"], True) == "  7\n- 2\n---\n  5"


def test_two_problems_with_solutions():
    assert (
        arithmetic_arranger(["3 + 855", "988 + 40"], True)
        == "    3      988\n+ 855    +  40\n-----    -----\n  858     1028"
    )


def test_five_problems_with_solutions():
    assert (
        arithmetic_arranger(
            ["32 - 698", "1 - 3801", "45 + 43", "123 + 49", "988 + 40"], True
        )
        == "   32         1      45      123      988\n- 698    - 3801    + 43    +  49    +  40\n-----    ------    ----    -----    -----\n -666     -3800      88      172     1028"
    )
