def arithmetic_arranger(problems: list, solution: bool = False) -> str:
    if len(problems) > 5:
        return "Error: Too many problems."

    lines: list[list[str]] = [[], [], [], []]
    separator = 4 * " "

    for i in range(len(problems)):
        a, operator, b = problems[i].split()

        if operator != "+" and operator != "-":
            return "Error: Operator must be '+' or '-'."

        if len(a) > 4 or len(b) > 4:
            return "Error: Numbers cannot be more than four digits."

        try:
            answer = str(int(a) - int(b)) if operator == "-" else str(int(a) + int(b))
        except ValueError:
            return "Error: Numbers must only contain digits."

        total_length = max(len(a), len(b)) + 2

        lines[0].append((total_length - len(a)) * " " + a)
        lines[1].append(operator + (total_length - 1 - len(b)) * " " + b)
        lines[2].append(total_length * "-")
        lines[3].append((total_length - len(answer)) * " " + answer)

    arrangement = f"{separator.join(lines[0])}\n{separator.join(lines[1])}\n{separator.join(lines[2])}"

    if solution:
        arrangement += f"\n{separator.join(lines[3])}"

    return arrangement
