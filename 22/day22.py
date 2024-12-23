#!/usr/bin/python3

import pprint
import time


def main():
    with open("day22.input", "r") as file:
        starting_numbers = [int(line.strip()) for line in file]
    # starting_numbers = [123]

    results = []
    memo = dict()
    st = time.time()

    banana_values = []
    differences = []
    max_values = []

    for number_index, secret_number in enumerate(starting_numbers):
        result = secret_number
        banana_values.append([])
        differences.append([])
        max_values.append(dict())

        for _ in range(2000):
            banana_values[number_index].append(result % 10)
            result = next_number(result, memo)

        differences[number_index] = [banana_values[number_index][x] - banana_values[number_index][x-1] for x in range(1, len(banana_values[number_index]))]

        for index in range(3, len(differences[number_index])):
            diffs = differences[number_index]
            cur_index = (diffs[index - 3], diffs[index - 2], diffs[index - 1], diffs[index])

            if cur_index not in max_values[number_index]:
                max_values[number_index][cur_index] = banana_values[number_index][index + 1]

        results.append(result)

    print(f"Init time: {time.time() - st}s\n")
    st = time.time()

    unique_keys = set()
    for thing in max_values:
        unique_keys.update(thing.keys())

    max_bananas = 0
    for key in unique_keys:

        new_max = 0
        for max_dict in max_values:
            new_max += max_dict[key] if key in max_dict else 0

        if new_max > max_bananas:
            print(f"New max key: {key}")
            max_bananas = new_max

        for thing in max_values:
            thing.pop(key, None)

    print(f"Part 2: Max bananas = {max_bananas}")
    print(f"Part 1: Sum of 2000th secret nums = {sum(results)}")
    print(f"Time: {time.time() - st}s\n")

def next_number(number, memo) -> int:
    if number in memo:
        return memo[number]

    next_number = mix_prune(number * 64, number)
    next_number = mix_prune(next_number // 32, next_number)
    next_number = mix_prune(next_number * 2048, next_number)
    memo[number] = next_number

    return next_number


def mix_prune(number, next_number) -> int:
    return (next_number ^ number) % 16777216

if __name__ == "__main__":
    main()