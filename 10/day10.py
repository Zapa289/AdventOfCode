#!/usr/bin/python

import time

CARDINALS = [[-1, 0], [0, 1], [1, 0], [0, -1]]

def print_grid(list):
    for row in list:
        print(" ".join(map(str,[len(entry) for entry in row])))

def main():
    with open("day10.input", "r") as file:
        topo_map = [ [int(char) for char in x.strip()] for x in file.readlines() ]
    st = time.time()
    part1(topo_map)
    print(f"Part 1 time: {time.time() - st}s")

    st = time.time()
    part2(topo_map)
    print(f"Part 1 time: {time.time() - st}s")

def find_path(topo_map, start_row :int , start_col :int, memo) -> list[tuple[int, int]]:
    if len(memo[start_row][start_col]) > 0:
        return memo[start_row][start_col]

    cur_value = topo_map[start_row][start_col]
    trail_ends = []

    for direction in CARDINALS:
        dir_row, dir_col = direction[0], direction[1]

        if start_row + dir_row < 0 or start_col + dir_col < 0:
            continue

        try:
            # Next path is incremental increase
            if topo_map[start_row + dir_row][start_col + dir_col] == cur_value + 1:
                # Next path is trail end or path continues
                if topo_map[start_row + dir_row][start_col + dir_col] == 9 and (start_row + dir_row, start_col + dir_col) not in trail_ends:
                    trail_ends.append((start_row + dir_row, start_col + dir_col))
                    memo[start_row + dir_row][start_col + dir_col] = []
                else:
                    trail_ends.extend(find_path(topo_map, start_row + dir_row, start_col + dir_col, memo))
        except IndexError:
            pass

    trail_ends = list(set(trail_ends))

    memo[start_row][start_col] = trail_ends
    return trail_ends

def part1(topo_map):
    num_rows = len(topo_map)
    num_cols = len(topo_map[0])

    memo:list[list[tuple[int,int]]] = []
    trailheads = []
    for row in range(num_rows):
        memo.append([])
        for col in range(num_cols):
            memo[row].append([])
            if topo_map[row][col] == 0:
                trailheads.append((row,col))

    trail_scores = []

    for trail in trailheads:
        start_row, start_col = trail
        trail_scores.append(len(find_path(topo_map, start_row, start_col, memo)))

    print(f"PART 1 : {sum(trail_scores)}")
    if sum(trail_scores) != 36 and sum(trail_scores) != 472:
        print('FAILED')

def count_path(topo_map, start_row :int , start_col :int, memo) -> list[tuple[int, int]]:
    if memo[start_row][start_col] >= 0:
        return memo[start_row][start_col]

    cur_value = topo_map[start_row][start_col]
    total = 0

    for direction in CARDINALS:
        dir_row, dir_col = direction[0], direction[1]

        if start_row + dir_row < 0 or start_col + dir_col < 0:
            continue

        try:
            # Next path is incremental increase
            if topo_map[start_row + dir_row][start_col + dir_col] == cur_value + 1:
                # Next path is trail end or path continues
                if topo_map[start_row + dir_row][start_col + dir_col] == 9:
                    total += 1
                else:
                    total += count_path(topo_map, start_row + dir_row, start_col + dir_col, memo)
        except IndexError:
            pass

    memo[start_row][start_col] = total
    return total

def part2(topo_map):
    num_rows = len(topo_map)
    num_cols = len(topo_map[0])

    memo:list[list[int]] = []
    trailheads = []
    for row in range(num_rows):
        memo.append([])
        for col in range(num_cols):
            memo[row].append(-1)
            if topo_map[row][col] == 0:
                trailheads.append((row,col))

    trail_scores = []

    for trail in trailheads:
        start_row, start_col = trail
        trail_scores.append(count_path(topo_map, start_row, start_col, memo))

    print(f"PART 2 : {sum(trail_scores)}")
    if sum(trail_scores) != 81 and sum(trail_scores) != 969:
        print('FAILED')


if __name__ == "__main__":
    main()