#!/usr/bin/python3
import time

puzzle = []

def add_tuples(first, second) -> tuple[int,int]:
    return tuple(map(sum, zip(first, second)))

def bound(next_position) -> bool:
    row, col = next_position
    if row < 0 or row >= len(puzzle):
        return False

    if col < 0 or col >= len(puzzle[0]):
        return False

    return True

def find_antinodes(input: list[tuple[int, int]]) -> list[tuple[int, int]]:
    remains = input.copy()
    antinodes = []
    for node_row, node_col in input:
        remains.remove((node_row, node_col))
        for check_row, check_col in remains:
            diff_row = check_row - node_row
            diff_col = check_col - node_col
            anti1 = (node_row - diff_row, node_col - diff_col)
            anti2 = (check_row + diff_row, check_col + diff_col)
            if bound(anti1) : antinodes.append(anti1)
            if bound(anti2) : antinodes.append(anti2)

    return antinodes

def find_antinodes_p2(input: list[tuple[int, int]]) -> list[tuple[int, int]]:
    remains = input.copy()
    antinodes = []
    for node_row, node_col in input:
        remains.remove((node_row, node_col))

        for check_row, check_col in remains:
            diff_row = check_row - node_row
            diff_col = check_col - node_col

            anti_row = check_row - diff_row
            anti_col = check_col - diff_col
            anti = (anti_row, anti_col)
            while bound(anti):
                antinodes.append(anti)
                anti_row, anti_col = anti
                anti = (anti_row - diff_row, anti_col - diff_col)

            anti_row = node_row + diff_row
            anti_col = node_col + diff_col
            anti = (anti_row, anti_col)
            while bound(anti):
                antinodes.append(anti)
                anti_row, anti_col = anti
                anti = (anti_row + diff_row, anti_col + diff_col)

    return antinodes

def main():
    global puzzle
    with open("day8.input", "r") as file:
        puzzle = [line.strip() for line in file]

    print(f"Map rows: {len(puzzle)}")
    print(f"Map col: {len(puzzle[0])}")

    # for line in puzzle:
    #     print(line)

    freqs: dict[str, list[tuple[int, int]]] = dict()
    antinodes = []


    for row, line in enumerate(puzzle):
        for col, char in enumerate(line):
            if char == ".":
                continue

            if char in freqs:
                freqs[char].append((row, col))
            else:
                freqs[char] = [(row, col)]

    st = time.time()
    for freq in freqs:
        antinodes.extend(find_antinodes(freqs[freq]))
    antinodes = list(set(antinodes))
    et = time.time()

    print(f"Part 1: {len(antinodes)}, time {et - st}")
    if len(antinodes) != 276:
        print("PART 1 FAILED")

    st = time.time()
    for freq in freqs:
        antinodes.extend(find_antinodes_p2(freqs[freq]))
    antinodes = list(set(antinodes))
    et = time.time()

    print(f"Part 2: {len(antinodes)}, time {et - st}")
    if len(antinodes) != 991:
        print("PART 2 FAILED")

if __name__ == "__main__":
    main()