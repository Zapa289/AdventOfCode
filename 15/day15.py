#!/usr/bin/python3

import time

DIRECTIONS = {
    "^" : (-1, 0),
    ">" : (0, 1),
    "<" : (0, -1),
    "v" : (1, 0)
}

def main():
    with open("day15.input", "r") as file:
        raw_map, instructions = file.read().split("\n\n")

    instructions = instructions.replace("\n", "")

    obstacles: list[tuple[int,int]] = []
    walls: list[tuple[int,int]] = []

    robot_row = 0
    robot_col = 0

    # Parse map
    robo_map = raw_map.split()
    map_width = len(robo_map[0])
    map_height = len(robo_map)

    st = time.time()
    for row_index, row in enumerate(robo_map):
        for col_index, char in enumerate(row):
            if char == "#":
                walls.append((row_index, col_index))
                continue

            if char == "O":
                obstacles.append((row_index, col_index))
                continue

            if char == "@":
                robot_row, robot_col = row_index, col_index

    print(f"Map is {map_width} x {map_height}, robot starts at {(robot_row, robot_col)}")

    for move in instructions:
        move_row, move_col = DIRECTIONS[move]

        move_list:list[tuple[int,int]] = []
        blocked = False
        check_row = move_row + robot_row
        check_col = move_col + robot_col

        if (check_row, check_col) in walls:
            # Trying to move into a wall
            continue

        while True:
            if (check_row, check_col) in walls:
                #Hit the wall, clear the move list and get out
                move_list.clear()
                blocked = True
                break

            if (check_row, check_col) not in obstacles:
                # This cell is empty and we can move stuff
                blocked = False
                break

            move_list.append((check_row, check_col))
            check_row += move_row
            check_col += move_col

        if not blocked:
            robot_col += move_col
            robot_row += move_row

        if move_list:
            first = move_list[0]
            last_row, last_col = move_list[-1]

            obstacles.remove(first)
            obstacles.append((last_row + move_row, last_col + move_col))

    gps = 0
    for row, col in obstacles:
        gps += (100 * row) + col

    print(f"Part 1: GPS sum = {gps}")
    print(f"\tTime: {time.time() - st}")
if __name__ == "__main__":
    main()