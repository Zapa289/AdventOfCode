#!/usr/bin/python3
import heapq
import time
import pprint

GRID_SIZE = 70
TEST_GRID_SIZE = 6

DIRECTIONS = [
    (-1, 0),    # UP
    (0, 1),     # RIGHT
    (1, 0),     # DOWN
    (0, -1)     # LEFT
]

def main():
    with open("day18.input", "r") as file:
        blocks = [ tuple(int(x) for x in line.strip().split(",")) for line in file]

    st = time.time()
    part1(blocks)
    print(f"\tTime: {time.time() - st}s\n")

    st = time.time()
    part2(blocks)
    print(f"\tTime: {time.time() - st}s\n")

def part1(blocks):
    size = GRID_SIZE

    block_map = [["."] * (size + 1) for _ in range(size + 1)]

    for index in range(1024):
        col, row = blocks[index]
        block_map[row][col] = "#"

    distances = dict()
    start = (0,0)
    end = (size, size)

    for row_index, row in enumerate(block_map):
        for col_index, char in enumerate(row):
            if char == "#":
                continue
            distances[(row_index, col_index)] = [float("inf")] * len(DIRECTIONS)

    print(f"Start = {start}")
    print(f"End = {end}")

    heap:list[tuple[int, tuple[int,int]]] = []
    heapq.heappush(heap, (0, start))

    distances[start][1] = 0

    while heap:
        node_score, node = heapq.heappop(heap)
        node_row, node_col = node

        for move_index, (move_row, move_col) in enumerate(DIRECTIONS):
            next_row, next_col = (node_row + move_row, node_col + move_col)

            if not (0 <= next_row <= size) or not (0 <= next_col <= size):
                continue

            if block_map[next_row][next_col] == '#':
                continue

            node_dists = distances[(next_row, next_col)]
            score = node_score + 1

            if node_dists[move_index] > score:
                node_dists[move_index] = score
                heapq.heappush(heap, (score, (next_row, next_col)))

    # pprint.pprint(distances)
    print(f"Part 1: End score = {min(distances[end])}")

def part2(blocks):
    size = GRID_SIZE

    block_map = [["."] * (size + 1) for _ in range(size + 1)]

    for index in range(1024):
        col, row = blocks[index]
        block_map[row][col] = "#"


    start = (0,0)
    end = (size, size)



    print(f"Start = {start}")
    print(f"End = {end}")

    for index in range(1024, len(blocks)):
        distances = dict()
        for row_index, row in enumerate(block_map):
            for col_index, char in enumerate(row):
                if char == "#":
                    continue
                distances[(row_index, col_index)] = [float("inf")] * len(DIRECTIONS)

        col, row = blocks[index]
        block_map[row][col] = "#"

        heap:list[tuple[int, tuple[int,int]]] = []
        heapq.heappush(heap, (0, start))

        distances[start][1] = 0

        while heap:
            node_score, node = heapq.heappop(heap)
            node_row, node_col = node

            for move_index, (move_row, move_col) in enumerate(DIRECTIONS):
                next_row, next_col = (node_row + move_row, node_col + move_col)

                if not (0 <= next_row <= size) or not (0 <= next_col <= size):
                    continue

                if block_map[next_row][next_col] == '#':
                    continue

                node_dists = distances[(next_row, next_col)]
                score = node_score + 1

                if node_dists[move_index] > score:
                    node_dists[move_index] = score
                    heapq.heappush(heap, (score, (next_row, next_col)))

        if min(distances[end]) == float('inf'):
            print(f"Breaks at {index=} {blocks[index]}")
            break

if __name__ == "__main__":
    main()