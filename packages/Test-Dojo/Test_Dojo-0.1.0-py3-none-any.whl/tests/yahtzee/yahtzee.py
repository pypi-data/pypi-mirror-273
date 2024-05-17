from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class Roll:
    dice: [int]

    def __post_init__(self) -> None:
        self.dice.sort()

    @property
    def frequency(self) -> [int]:
        return [self.count(d) for d in range(1, 7)]

    def sum(self) -> int:
        return sum(self.dice)

    def count(self, dice: int) -> int:
        return self.dice.count(dice)

    def is_small_straight(self) -> bool:
        return self.dice == [1, 2, 3, 4, 5]

    def is_large_straight(self) -> bool:
        return self.dice == [2, 3, 4, 5, 6]

    def is_yahtzee(self) -> bool:
        return 5 in self.frequency

    def is_full_house(self) -> bool:
        return all(i in self.frequency for i in [2, 3])

    def pick_n_of_a_kind(self, frequency: int) -> Combo:
        result = FixedScoreCombo(0)
        for dice, actual_frequency in enumerate(self.frequency, 1):
            if actual_frequency >= frequency:
                result = NOfAKindCombo(dice, frequency)

        return result

    def pick_two_pairs(self) -> Combo:
        dice = [dice for dice, f in enumerate(self.frequency, 1) if f >= 2]
        return TotalScoreCombo(dice * 2) if len(dice) == 2 else FixedScoreCombo(0)

    def pick_small_straight(self) -> Combo:
        return FixedScoreCombo(15 if self.is_small_straight() else 0)

    def pick_large_straight(self) -> Combo:
        return FixedScoreCombo(20 if self.is_large_straight() else 0)

    def pick_yahtzee(self) -> Combo:
        return FixedScoreCombo(50 if self.is_yahtzee() else 0)

    def pick_full_house(self) -> Combo:
        return (
            TotalScoreCombo(self.dice) if self.is_full_house() else FixedScoreCombo(0)
        )


@dataclass
class TotalScoreCombo:
    dice: [int]

    def score(self) -> int:
        return sum(self.dice)


@dataclass
class NOfAKindCombo:
    dice: int

    frequency: int

    def __post_init__(self) -> None:
        assert 0 < self.dice < 7

    def score(self) -> int:
        return self.dice * self.frequency


class Combo(Protocol):
    def score(self) -> int:
        pass


@dataclass
class FixedScoreCombo:
    value: int

    def score(self) -> int:
        return self.value


@dataclass
class Yahtzee:
    roll: Roll

    def chance(self) -> int:
        return self.roll.sum()

    def ones(self) -> int:
        return self._pick(1)

    def twos(self) -> int:
        return self._pick(2)

    def threes(self) -> int:
        return self._pick(3)

    def fours(self) -> int:
        return self._pick(4)

    def fives(self) -> int:
        return self._pick(5)

    def sixes(self) -> int:
        return self._pick(6)

    def _pick(self, dice: int) -> int:
        return self.roll.count(dice) * dice

    def two_pairs(self) -> int:
        return self.roll.pick_two_pairs().score()

    def one_pair(self) -> int:
        return self.roll.pick_n_of_a_kind(2).score()

    def three_of_a_kind(self) -> int:
        return self.roll.pick_n_of_a_kind(3).score()

    def four_of_a_kind(self) -> int:
        return self.roll.pick_n_of_a_kind(4).score()

    def full_house(self) -> int:
        return self.roll.pick_full_house().score()

    def small_straight(self) -> int:
        return self.roll.pick_small_straight().score()

    def large_straight(self) -> int:
        return self.roll.pick_large_straight().score()

    def yahtzee(self) -> int:
        return self.roll.pick_yahtzee().score()
