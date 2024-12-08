#!/usr/bin/python3
def going_up(num1:int, num2:int):
    return (num1 - num2 < 0)

def valid_items(num1:int, num2:int, goingup:bool):
    if (num1 == num2):
        return False

    if (going_up(num1, num2) != goingup):
        return False

    diff = abs(num1 - num2)
    if (diff < 1 or diff > 3):
        return False

    return True

def dampen(report: list[int]) -> bool:
    for index in range(len(report)):
        temp = report.copy()
        temp.pop(index)

        if is_safe(temp):
            return True

    return False


def is_safe_dampened(report:list[int]) -> bool:
    updown = going_up(report[0], report[1])

    for index in range(len(report)-1):

        if not valid_items(report[index], report[index+1], updown):
            return dampen(report)

    return True

def is_safe(report:list[int]) -> bool:
    updown = going_up(report[0], report[1])
    for index in range(len(report) -1):
        if not valid_items(report[index], report[index + 1], updown):
            return False
    return True

def main():
    levels:list[list[int]] = []
    with open("day2.input", "r") as file:
        for line in file:
            temp = line.split()
            temp = [int(x) for x in temp]
            levels.append(temp)


    # Detect safety
    safe_reports = 0
    for report in levels:
        if (is_safe(report)):
            safe_reports += 1

    print(f"Safe Reports = {safe_reports}")

    # Use Dampener
    safe_reports = 0
    for report in levels:
        if (is_safe_dampened(report)):
            safe_reports += 1
    print(f"Safe Reports (dampened) = {safe_reports}")

if __name__ == "__main__":
    main()