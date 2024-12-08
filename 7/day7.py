#!/usr/bin/python3
import copy
import time

def recurse_find(calibration: int, numbers: list[int], total) -> bool:

    downstream = numbers.copy()
    number = downstream.pop(0)

    if len(downstream) == 0:
        if number * total == calibration:
            return True
        if number + total == calibration:
            return True
        return False

    return recurse_find(calibration, downstream, total + number) or recurse_find(calibration, downstream, total * number)

def recurse_find_v2(calibration: int, numbers: list[int], total) -> bool:

    if total > calibration:
        return False

    downstream = numbers.copy()
    number = downstream.pop(0)

    if len(downstream) == 0:
        if number * total == calibration:
            return True
        if number + total == calibration:
            return True
        if int("".join([str(total), str(number)])) == calibration:
            return True
        return False

    return recurse_find_v2(calibration, downstream, total + number) or recurse_find_v2(calibration, downstream, total * number) or recurse_find_v2(calibration, downstream, int("".join([str(total), str(number)])))

def main():
    calibrations = []
    numbers: list[list[int]] = []
    with open("day7.input", "r") as file:
        for line in file.readlines():
            equation = line.strip().split(":")
            calibrations.append(int(equation[0]))
            numbers.append([int(x) for x in equation[1].split()])

    st = time.time()
    winners = []
    p1_numbers = copy.deepcopy(numbers)

    for index in range(len(calibrations)):
        if recurse_find(calibrations[index], p1_numbers[index][1:], p1_numbers[index][0]):
            winners.append(calibrations[index])

    print(f"Part 1: Sum of valid calibrations: {sum(winners)}")
    if sum(winners) != 4555081946288 and sum(winners) != 3749:
        print("PART 1 FAILED\n")
    et = time.time()
    print(f"Time: {et - st}\n")

    st = time.time()
    winners = []
    for index in range(len(calibrations)):
        if recurse_find_v2(calibrations[index], numbers[index][1:], numbers[index][0]):
            winners.append(calibrations[index])

    print(f"Part 2: Sum of valid calibrations: {sum(winners)}")
    if sum(winners) != 227921760109726:
        print("Part 2 FAILED\n")
    et = time.time()
    print(f"Time: {et - st}\n")

if __name__ == "__main__":
    st = time.time()
    main()
