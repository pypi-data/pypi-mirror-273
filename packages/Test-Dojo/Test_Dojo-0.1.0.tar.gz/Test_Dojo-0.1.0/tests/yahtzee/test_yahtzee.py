from tests.yahtzee.yahtzee import Yahtzee, Roll


def test_chance_scores_sum_of_all_dice():
    assert Yahtzee(Roll([2, 3, 4, 5, 1])).chance() == 15
    assert Yahtzee(Roll([3, 3, 4, 5, 1])).chance() == 16


def test_yahtzee_scores_50():
    assert Yahtzee(Roll([6, 6, 6, 6, 3])).yahtzee() == 0
    assert Yahtzee(Roll([4, 4, 4, 4, 4])).yahtzee() == 50
    assert Yahtzee(Roll([6, 6, 6, 6, 6])).yahtzee() == 50


def test_ones():
    assert Yahtzee(Roll([6, 2, 2, 4, 5])).ones() == 0
    assert Yahtzee(Roll([1, 2, 3, 4, 5])).ones() == 1
    assert Yahtzee(Roll([1, 2, 1, 4, 5])).ones() == 2
    assert Yahtzee(Roll([1, 2, 1, 1, 1])).ones() == 4


def test_twos():
    assert Yahtzee(Roll([1, 3, 4, 5, 6])).twos() == 0
    assert Yahtzee(Roll([1, 2, 3, 2, 6])).twos() == 4
    assert Yahtzee(Roll([2, 2, 2, 2, 2])).twos() == 10


def test_threes():
    assert Yahtzee(Roll([1, 2, 4, 5, 6])).threes() == 0
    assert Yahtzee(Roll([1, 2, 3, 2, 3])).threes() == 6
    assert Yahtzee(Roll([2, 3, 3, 3, 3])).threes() == 12


def test_fours():
    assert Yahtzee(Roll([1, 2, 3, 5, 6])).fours() == 0
    assert Yahtzee(Roll([4, 5, 5, 5, 5])).fours() == 4
    assert Yahtzee(Roll([4, 4, 5, 5, 5])).fours() == 8
    assert Yahtzee(Roll([4, 4, 4, 5, 5])).fours() == 12


def test_fives():
    assert Yahtzee(Roll([1, 2, 3, 4, 6])).fives() == 0
    assert Yahtzee(Roll([4, 4, 4, 5, 5])).fives() == 10
    assert Yahtzee(Roll([4, 4, 5, 5, 5])).fives() == 15
    assert Yahtzee(Roll([4, 5, 5, 5, 5])).fives() == 20


def test_sixes():
    assert Yahtzee(Roll([4, 4, 4, 5, 5])).sixes() == 0
    assert Yahtzee(Roll([4, 4, 6, 5, 5])).sixes() == 6
    assert Yahtzee(Roll([6, 5, 6, 6, 5])).sixes() == 18


def test_one_pair():
    assert Yahtzee(Roll([1, 2, 3, 4, 5])).one_pair() == 0
    assert Yahtzee(Roll([3, 4, 3, 5, 6])).one_pair() == 6
    assert Yahtzee(Roll([5, 3, 3, 3, 5])).one_pair() == 10
    assert Yahtzee(Roll([5, 3, 6, 6, 5])).one_pair() == 12


def test_two_pairs():
    assert Yahtzee(Roll([3, 3, 6, 5, 4])).two_pairs() == 0
    assert Yahtzee(Roll([3, 3, 5, 4, 5])).two_pairs() == 16
    assert Yahtzee(Roll([3, 3, 6, 6, 6])).two_pairs() == 18


def test_three_of_a_kind():
    assert Yahtzee(Roll([1, 2, 3, 4, 5])).three_of_a_kind() == 0
    assert Yahtzee(Roll([3, 3, 3, 4, 5])).three_of_a_kind() == 9
    assert Yahtzee(Roll([3, 3, 3, 3, 5])).three_of_a_kind() == 9
    assert Yahtzee(Roll([5, 3, 5, 4, 5])).three_of_a_kind() == 15


def test_four_of_a_kind():
    assert Yahtzee(Roll([3, 3, 3, 2, 1])).four_of_a_kind() == 0
    assert Yahtzee(Roll([3, 3, 3, 3, 5])).four_of_a_kind() == 12
    assert Yahtzee(Roll([3, 3, 3, 3, 3])).four_of_a_kind() == 12
    assert Yahtzee(Roll([5, 5, 5, 4, 5])).four_of_a_kind() == 20


def test_small_straight():
    assert Yahtzee(Roll([1, 2, 2, 4, 5])).small_straight() == 0
    assert Yahtzee(Roll([1, 2, 3, 4, 5])).small_straight() == 15
    assert Yahtzee(Roll([2, 3, 4, 5, 1])).small_straight() == 15


def test_large_straight():
    assert Yahtzee(Roll([1, 2, 2, 4, 5])).large_straight() == 0
    assert Yahtzee(Roll([6, 2, 3, 4, 5])).large_straight() == 20
    assert Yahtzee(Roll([2, 3, 4, 5, 6])).large_straight() == 20


def test_full_house():
    assert Yahtzee(Roll([2, 3, 4, 5, 6])).full_house() == 0
    assert Yahtzee(Roll([6, 2, 2, 2, 6])).full_house() == 18
    assert Yahtzee(Roll([2, 2, 1, 3, 4])).full_house() == 0
