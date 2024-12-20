#!/usr/bin/python3

import time
import pprint
from collections import defaultdict

DIRS = [
    (-1, 0),    # UP
    (0, 1),     # RIGHT
    (1, 0),     # DOWN
    (0, -1)     # LEFT
]

def main():
    with open("day20.input", "r") as file:
        map = [list(line.strip()) for line in file]

    start = next((row_index, col_index) for row_index, row in enumerate(map) for col_index, char in enumerate(row) if char == "S")
    map[start[0]][start[1]] = 0

    end = next((row_index, col_index) for row_index, row in enumerate(map) for col_index, char in enumerate(row) if char == "E")

    node = start
    step = 1
    walk = [start]
    while node != end:
        node_row, node_col = node

        for (dir_row, dir_col) in DIRS:
            next_row, next_col = (node_row + dir_row, node_col + dir_col)

            if map[next_row][next_col] == "." or (next_row, next_col) == end:
                map[next_row][next_col] = step
                step += 1
                walk.append((next_row, next_col))
                node = (next_row, next_col)
    map[end[0]][end[1]] = step - 1

    st = time.time()
    part1(map, walk)
    print(f"\tTime: {time.time() - st}s\n")

    st = time.time()
    part2(map, walk)
    print(f"\tTime: {time.time() - st}s\n")

def part1(map, walk):
    map_width = len(map[0])
    map_height = len(map)
    print(f"{map_width=}, {map_height=}")

    savings:dict[int, int] = defaultdict(lambda:0)

    for node in walk:
        node_row, node_col = node

        for (dir_row, dir_col) in DIRS:
            cheat_row, cheat_col = (node_row + 2*dir_row, node_col + 2*dir_col)
            if not (0 < cheat_row < (map_height - 1)) or not (0 < cheat_col < (map_width - 1)) or (cheat_row, cheat_col) not in walk:
                continue

            dist = abs(cheat_row - node_row) + abs(cheat_col - node_col)

            saved = map[cheat_row][cheat_col] - map[node_row][node_col] - (dist)
            if saved >= 100:
                savings[saved] += 1

    print(f"Part 1: Total +100ps savings: {sum(savings.values())}")

def part2(map, walk: list):

    savings:dict[int, int] = defaultdict(lambda:0)

    while walk:
        node = walk.pop(0)
        node_row, node_col = node

        for (cheat_row, cheat_col) in walk:
            dist = abs(cheat_row - node_row) + abs(cheat_col - node_col)

            if dist > 20:
                continue

            saved = map[cheat_row][cheat_col] - map[node_row][node_col] - (dist)
            if saved >= 100:
                savings[saved] += 1

    print(f"Part 2: Total +100ps savings: {sum(savings.values())}")

if __name__ == "__main__":
    main()