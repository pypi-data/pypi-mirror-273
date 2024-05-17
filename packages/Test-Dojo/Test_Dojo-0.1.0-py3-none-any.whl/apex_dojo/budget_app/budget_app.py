from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Category:
    name: str
    ledger: list = field(default_factory=list)
    summary: list = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.name)

    def __str__(self) -> str:
        title_design = "*" * ((30 - len(self.name)) // 2)

        self.summary.append(f"{title_design}{self.name}{title_design}\n")

        for i in self.ledger:
            amount = f" {'%.2f' % i['amount']}"
            description = i["description"][: 30 - len(amount)]
            space_between = " " * (30 - len(description) - len(amount))

            self.summary.append(description + space_between + amount + "\n")

        self.summary.append(f"Total: {self.get_balance()}")

        return "".join(self.summary)

    def deposit(self, param: float | int, param1: str = "") -> None:
        self.ledger.append({"amount": param, "description": param1})

    def withdraw(self, param: float | int, param1: str = "") -> bool:
        if self.check_funds(param):
            self.ledger.append({"amount": -param, "description": param1})
            return True

        return False

    def get_balance(self) -> float | int:
        return sum([i["amount"] for i in self.ledger])

    def transfer(self, transfer_amount: float | int, other: Category) -> bool:
        if self.check_funds(transfer_amount):
            self.ledger.append(
                {"amount": -transfer_amount, "description": f"Transfer to {other.name}"}
            )
            other.deposit(transfer_amount, f"Transfer from {self.name}")
            return True

        return False

    def check_funds(self, param: float | int) -> bool:
        return not param > self.get_balance()


def create_spend_chart(categories) -> str:
    spend_chart = create_chart_template(categories)

    all_withdraws = sum(
        abs(i["amount"])
        for category in categories
        for i in category.ledger
        if i["amount"] < 0
    )

    bar_height = []
    for category in categories:
        category_withdraws = [
            abs(i["amount"]) for i in category.ledger if i["amount"] < 0
        ]
        bar_height.append((sum(category_withdraws) / all_withdraws) * 10 // 1)

    padding = 5
    for category_index in range(len(categories)):
        for i in range(11, 1, -1):
            if bar_height[category_index] >= 0:
                spend_chart[i] = (
                    spend_chart[i][:padding] + "o" + spend_chart[i][padding + 1 :]
                )
                bar_height[category_index] -= 1
        padding += 3

    return "\n".join(spend_chart)


def create_chart_template(categories) -> list[str]:
    chart_template: list = ["Percentage spent by category"]

    chart_space = " " * (len(categories) * 3 + 1)
    value_label_rows = [f"{i * 10}|{chart_space}" for i in range(10, -1, -1)]

    for row in value_label_rows:
        padding = " " * (len(value_label_rows[0]) - len(row))
        chart_template.append(padding + row)

    chart_template.append("    " + "-" * len(chart_space))

    category_label_height = max(len(category) for category in categories)
    for i in range(category_label_height):
        category_labels = "     "
        for category in categories:
            category_labels += category.name[i] + "  " if i < len(category) else "   "
        chart_template.append(category_labels)

    return chart_template
