#!/usr/bin/python3

import time

def main():
    with open("day11.input", "r") as file:
        stones = file.read().strip().split()

    memo: dict[tuple[str,int], int] = dict()

    st = time.time()
    total = 0
    for stone in stones:
        total += find_blink(stone, 25, memo)
    print(f"Part 1 total: {total}")
    print(f"Part 1 time: {time.time() - st}s\n")

    st = time.time()
    total = 0
    for stone in stones:
        total += find_blink(stone, 75, memo)
    print(f"Part 2 total: {total}")
    print(f"Part 2 time: {time.time() - st}s\n")

def find_blink(stone:str, blink_num, memo: dict[tuple[str,int], int]) -> int:
    # Check memo for stone, blink number
    if (stone, blink_num) in memo:
        return memo[(stone,blink_num)]

    # Terminate recursion
    if blink_num == 1:
        if stone == '0':
            return 1
        if len(stone) % 2 == 0:
            return 2
        return 1

    # Recurse for new values at blink - 1
    total = 0
    if stone == '0':
        total = find_blink('1', blink_num - 1, memo)
    elif len(stone) % 2 == 0:
        total += find_blink(stone[0:int(len(stone)/2)], blink_num - 1, memo)
        total += find_blink(str(int(stone[int(len(stone)/2):])), blink_num - 1, memo)
    else:
        total = find_blink(str(int(stone) * 2024), blink_num - 1, memo)

    # Record the memo
    memo[(stone, blink_num)] = total

    return total

if __name__ == "__main__":
    main()
