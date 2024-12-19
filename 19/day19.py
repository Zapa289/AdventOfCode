#!/usr/bin/python3

import time

TEST_INPUT = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

def main():
    with open("day19.input", "r") as file:
        patterns, towels = tuple(file.read().split("\n\n"))
        patterns = patterns.split(", ")
        towels = towels.split()

    # patterns, towels = tuple(TEST_INPUT.split("\n\n"))
    # patterns = patterns.split(", ")
    # towels = towels.split()

    st = time.time()
    good_towels = part1(patterns, towels)
    print(f"\tTime: {time.time() - st}s\n")

    st = time.time()
    part2(patterns, good_towels)
    print(f"\tTime: {time.time() - st}s\n")

def part2(patterns, towels):

    def count_matches(patterns: list[str], substring:str, memo) -> int:

        if substring in memo:
            return memo[substring]

        if not substring:
            return -1

        matches = 0
        for pattern in patterns:
            if substring.startswith(pattern):
                sub_match = count_matches(patterns, substring[len(pattern):], memo)
                if sub_match == -1:
                    matches += 1
                else:
                    matches += sub_match
        memo[substring] = matches
        return matches

    total = 0
    for towel in towels:
        memo: dict[str, list[list[str]]] = dict()
        total += count_matches(patterns, towel, memo)

    print(f"Part 2: Total combinations = {total}")



def part1(patterns, towels):

    def pattern_possible(patterns: list[str], match:str) -> bool:
        if not match:
            return True
        for pattern in patterns:
            if match.startswith(pattern):
                if pattern_possible(patterns, match[len(pattern):]):
                    return True
        return False

    good_towels = []
    for towel in towels:
        if pattern_possible(patterns, towel):
            good_towels.append(towel)

    print(f"Part 1: Possible towels = {len(good_towels)}")
    return good_towels

if __name__ == "__main__":
    main()