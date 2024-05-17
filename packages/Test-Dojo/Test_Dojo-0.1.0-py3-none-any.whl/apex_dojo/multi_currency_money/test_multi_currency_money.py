from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class Money:
    _amount: int
    currency: str

    def times(self, multiplier: int) -> Expression:
        return Money(self._amount * multiplier, self.currency)

    @staticmethod
    def dollar(amount: int) -> Money:
        return Money(amount, "USD")

    @staticmethod
    def franc(amount: int) -> Money:
        return Money(amount, "CHF")

    def plus(self, addend: Expression) -> Expression:
        return Sum(self, addend)

    def reduce(self, bank: Bank, to: str) -> Money:
        rate = bank.rate(source=self.currency, target=to)
        return Money(self._amount // rate, to)


@dataclass
class Sum:
    _augend: Expression
    _addend: Expression

    def reduce(self, bank: Bank, to: str) -> Money:
        amount: int = (
            self._augend.reduce(bank, to)._amount
            + self._addend.reduce(bank, to)._amount
        )

        return Money(amount, to)

    def plus(self, addend: Expression) -> Expression:
        return Sum(self, addend)

    def times(self, multiplier: int) -> Expression:
        return Sum(self._augend.times(multiplier), self._addend.times(multiplier))


class Expression(Protocol):
    def reduce(self, bank: Bank, to: str) -> Money:
        pass

    def plus(self, addend: Expression) -> Expression:
        pass

    def times(self, multiplier: int) -> Expression:
        pass


@dataclass
class Bank:
    rates: dict[tuple[str, str], int] = field(default_factory=dict)

    def reduce(self, source: Expression, to: str) -> Money:
        return source.reduce(self, to)

    def add_rate(self, source: str, target: str, rate: int) -> None:
        self.rates[source, target] = rate

    def rate(self, source: str, target: str) -> int:
        if source == target:
            return 1
        return self.rates[source, target]


def test_multiplication() -> None:
    # Given
    five = Money.dollar(5)

    # Then
    assert five.times(2) == Money.dollar(10)
    assert five.times(3) == Money.dollar(15)


def test_equality() -> None:
    assert Money.dollar(5) == Money.dollar(5)
    assert Money.dollar(5) != Money.dollar(6)
    assert Money.dollar(5) != Money.franc(5)
    assert Money.franc(5) == Money.franc(5)


def test_currency() -> None:
    assert Money.dollar(1).currency == "USD"
    assert Money.franc(1).currency == "CHF"


def test_simple_addition() -> None:
    five: Money = Money.dollar(5)
    sum: Expression = five.plus(five)
    bank: Bank = Bank()

    reduced: Money = bank.reduce(sum, "USD")

    assert reduced == Money.dollar(10)


def test_plus_returns_sum() -> None:
    five: Money = Money.dollar(5)

    result: Expression = five.plus(five)
    sum: Sum = result

    assert sum._augend == five
    assert sum._addend == five


def test_reduce_sum() -> None:
    sum: Expression = Sum(Money.dollar(3), Money.dollar(4))
    bank: Bank = Bank()

    result: Money = bank.reduce(sum, "USD")

    assert result == Money.dollar(7)


def test_reduce_money() -> None:
    bank: Bank = Bank()

    result: Money = bank.reduce(Money.dollar(1), "USD")

    assert result == Money.dollar(1)


def test_reduce_money_diff_currency() -> None:
    bank: Bank = Bank()
    bank.add_rate("CHF", "USD", 2)

    result: Money = bank.reduce(Money.franc(2), "USD")

    assert result == Money.dollar(1)


def test_mixed_addition() -> None:
    five_bucks: Expression = Money.dollar(5)
    ten_franc: Expression = Money.franc(10)
    bank: Bank = Bank()
    bank.add_rate("CHF", "USD", 2)

    result = bank.reduce(five_bucks.plus(ten_franc), "USD")

    assert result == Money.dollar(10)


def test_sum_plus_money():
    five_bucks: Expression = Money.dollar(5)
    ten_franc: Expression = Money.franc(10)
    bank: Bank = Bank()
    bank.add_rate("CHF", "USD", 2)
    sum: Expression = Sum(five_bucks, ten_franc).plus(five_bucks)

    result: Money = bank.reduce(sum, "USD")

    assert result == Money.dollar(15)


def test_sum_times():
    five_bucks: Expression = Money.dollar(5)
    ten_franc: Expression = Money.franc(10)
    bank: Bank = Bank()
    bank.add_rate("CHF", "USD", 2)
    sum: Expression = Sum(five_bucks, ten_franc).times(2)

    result: Money = bank.reduce(sum, "USD")

    assert result == Money.dollar(20)
