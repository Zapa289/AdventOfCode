#!/usr/bin/python3

import re

MUL = re.compile(r"mul\((?P<num1>\d{1,3}),(?P<num2>\d{1,3})\)")
DO = re.compile(r"do\(\)")
DONT = re.compile(r"don't\(\)")

COMPLETE = re.compile(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)")
def main():
    with open("3/day3.input", "r") as file:
        text = file.read()

    # Part 1
    sum = 0
    muls = MUL.finditer(text)
    for match in muls:
        num1 = match.group("num1")
        num2 = match.group("num2")
        sum += int(num1) * int(num2)
    print(f"All Muls = {sum}")

    # Part 2
    sum = 0

    commands:list[str] = COMPLETE.findall(text)
    disabled = False

    for command in commands:
        if command.startswith("mul") and not disabled:
            num1, num2 = MUL.findall(command)[0]
            sum += int(num1) * int(num2)
        elif command == "don't()":
            disabled = True
        elif command == "do()":
            disabled = False

    print(f"Conditional Muls = {sum}")

if __name__ == "__main__":
    main()