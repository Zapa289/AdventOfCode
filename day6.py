#!/usr/bin/python3

UP_VECTOR = (-1, 0)
DOWN_VECTOR = (1, 0)
LEFT_VECTOR = (0, -1)
RIGHT_VECTOR = (0, 1)
VECTOR_LIST: list[tuple[int,int]] = [UP_VECTOR, RIGHT_VECTOR, DOWN_VECTOR, LEFT_VECTOR]

starting_pos = (0, 0)
patrol_map = []

from itertools import cycle
import copy
import cProfile

def add_tuples(first, second) -> tuple[int,int]:
    return tuple(map(sum, zip(first, second)))

def get_value(map, location):
    row, col = location
    return map[row][col]

def mark_spot(map, location, char = "X"):
    row, col = location
    map[row][col] = char
    return

def bound(the_map, next_position) -> bool:
    row, col = next_position
    if row < 0 or row >= len(the_map):
        return False

    if col < 0 or col >= len(the_map[0]):
        return False

    return True

def validate_path(bomb) -> bool:
    bomb_row, bomb_col = bomb
    char = patrol_map[bomb_row][bomb_col]
    patrol_map[bomb_row][bomb_col] = "#"

    vectors = cycle(VECTOR_LIST)
    movement_vector = next(vectors)
    current_pos = starting_pos
    next_pos = add_tuples(current_pos, movement_vector)

    path: list[tuple[tuple[int,int], tuple[int,int]]] = []
    while bound(patrol_map, next_pos):
        if get_value(patrol_map, next_pos) == '#':
            if (movement_vector, next_pos) not in path:
                path.append((movement_vector, next_pos))
            else:
                patrol_map[bomb_row][bomb_col] = char
                return False
            movement_vector = next(vectors)
        else:
            current_pos = next_pos
        next_pos = add_tuples(current_pos, movement_vector)

    patrol_map[bomb_row][bomb_col] = char
    return True

def peek(patrol, position, movement_vec):
    next_position = add_tuples(position, movement_vec)

    while bound(patrol, next_position):
        if get_value(patrol, next_position) == "#":
            return True
        next_position = add_tuples(next_position, movement_vec)

    return False

def main():
    global patrol_map
    global starting_pos

    with open("day6.input", "r") as file:
        patrol_map = [list(line.strip()) for line in file]

    print(f"Patrol map row: {len(patrol_map)}")
    print(f"Patrol map col: {len(patrol_map[0])}")

    for row_index, row in enumerate(patrol_map):
        if "^" in row:
            starting_pos = (row_index, row.index("^"))

    print(f"Starting Position: {starting_pos}")

    # Part 1
    new_map = copy.deepcopy(patrol_map)
    total_spots = 1
    vectors = cycle(VECTOR_LIST)
    movement_vector = next(vectors)
    peek_vector = next(vectors)

    current_pos = starting_pos
    next_pos = add_tuples(current_pos, movement_vector)

    potentials = []
    good = []
    while bound(new_map, next_pos):

        if peek(new_map, current_pos, peek_vector) and next_pos not in potentials:
            potentials.append(next_pos)
            # if not validate_path(next_pos):
                # good.append(next_pos)

        if get_value(new_map, current_pos) != 'X':
            mark_spot(new_map, current_pos)
            total_spots += 1

        if get_value(new_map, next_pos) == '#':
            movement_vector = peek_vector
            peek_vector = next(vectors)
        else:
            current_pos = next_pos

        next_pos = add_tuples(current_pos, movement_vector)

    print(f"Part 1: Total spots: {total_spots}")
    if total_spots != 4903:
        print("GO BACK 1")

    # Part 2

    good = [ bomb for bomb in potentials if not validate_path(bomb)]
    #cProfile.runctx('[ bomb for bomb in potentials if not validate_path(bomb)]', globals(), locals())
    if starting_pos in good:
        good.remove(starting_pos)

    print(f"Part 2: Total obstacles: {len(good)}")
    if len(good) != 1911:
        print("GO BACK 2")

if __name__ == "__main__":
    main()
