#!/usr/bin/python3

import time
import heapq
import pprint
import itertools

DIRECTIONS = [
    (-1, 0),    # UP
    (0, 1),     # RIGHT
    (1, 0),     # DOWN
    (0, -1)     # LEFT
]

def main():
    with open("day16-test.input", "r") as file:
        maze = [list(line.strip()) for line in file]

    distances = dict()

    start = (len(maze) - 2, 1)
    end = (1, len(maze[0]) - 2)

    for row_index, row in enumerate(maze):
        for col_index, char in enumerate(row):
            if char == "#":
                continue

            distances[(row_index, col_index)] = [float("inf")] * len(DIRECTIONS)
            # distances[(row_index, col_index)] = [float("inf"), []] * len(DIRECTIONS)

    print(f"Start = {start}")
    print(f"End = {end}")

    st = time.time()

    heap:list[tuple[int, tuple[int,int]]] = []
    heapq.heappush(heap, (0, start))

    distances[start][1] = 0
    #distances[start][1] = [0, [start]]

    while heap:
        node_score, node = heapq.heappop(heap)
        node_row, node_col = node
        #previous
        for move_index, (move_row, move_col) in enumerate(DIRECTIONS):
            next_row, next_col = (node_row + move_row, node_col + move_col)

            if maze[next_row][next_col] == '#':
                continue

            node_dists = distances[(next_row, next_col)]
            #previous_state = distances[node][move_index][1]
            score = node_score + (1001 if distances[node][move_index] == float("inf") else 1)

            if node_dists[move_index] > score:
                #node_dists[move_index] = [score, previous_state]
                node_dists[move_index] = score
                heapq.heappush(heap, (score, (next_row, next_col)))
            # elif score == node_dists[move_index][0]:
            #      node_dists[move_index][1].append(previous_state)

    print(f"Part 1: End score = {min(distances[end])}")
    print(f"\tTime: {time.time() - st}s\n")

    pprint.pprint(distances)

    seats = 0
    node = end

    while True:
        seats += 1
        print(f"Check {node}")
        print(distances[node])

        if node == start:
            break

        node_row, node_col = node
        next_nodes = [
                        DIRECTIONS[move_index - 2] for move_index in range(len(DIRECTIONS))
                        if distances[node][move_index] == min(distances[node])
                        or distances[node][move_index] == min(distances[node]) + 1000
                        ]

        print(f"Next Nodes {next_nodes}")
        if len(next_nodes) > 1:
            print(f"Split here: {next_nodes}")

        for move_row, move_col in next_nodes:
            node = (node_row + move_row, node_col + move_col)

        print()

    print(f"Part 2: Seats = {seats}")

def resolve_branch(node1, node2, distances):
    pass

if __name__ == "__main__":
    main()