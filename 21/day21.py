#!/usr/bin/python3

import cProfile
import itertools
import pprint
import time
from collections import defaultdict

NUMBER_PAD = [["7", "8", "9"],
              ["4", "5", "6"],
              ["1", "2", "3"],
              ["X", "0", "A"]]
NUMPAD_DEFAULT = (2, 2)
NUMBER_PAD_DEADZONE = (3,0)

KEYPAD = [["X", "^", "A"],
          ["<", "v", ">"]]
KEYPAD_DEFAULT = (0, 2)
KEYPAD_DEADZONE = (0,0)
KEYPAD_MAP = {'<': {'<': 'A',
                   '>': '>>A',
                   'A': '>>^A',
                   '^': '>^A',
                   'v': '>A'
                   },
             '>': {'<': '<<A',
                   '>': 'A',
                   'A': '^A',
                   '^': '^<A',
                   'v': '<A'
                   },
             'A': {'<': 'v<<A',
                   '>': 'vA',
                   'A': 'A',
                   '^': '<A',
                   'v': 'v<A'
                   },
             '^': {'<': 'v<A',
                   '>': '>vA',
                   'A': '>A',
                   '^': 'A',
                   'v': 'vA'
                   },
             'v': {'<': '<A',
                   '>': '>A',
                   'A': '^>A',
                   '^': '^A',
                   'v': 'A'
                   }
            }

MOVEMENTS = {
    (0,1) : ">",
    (0, -1) : "<",
    (1, 0)  : "v",
    (-1, 0) : "^"
}

def main():
    with open("day21.input", "r") as file:
        commands = list(map(str.strip, file.readlines()))

    print(commands)

    st = time.time()

    # Create relational map for numpad
    numpad_map = create_movement_map(NUMBER_PAD, NUMBER_PAD_DEADZONE)

    # Create relational map for keypad
    keypad_map = create_movement_map(KEYPAD, KEYPAD_DEADZONE)

    print(f"Init time: {time.time() - st}s\n")

    st = time.time()
    print(f"Part 1: Complexity = {find_complexity(commands, numpad_map, keypad_map, 3)}")
    print(f"Time: {time.time() - st}s\n")

    st = time.time()
    print(f"Part 2: Complexity = {find_complexity(commands, numpad_map, keypad_map, 26)}")
    print(f"Time: {time.time() - st}s\n")

def keypad_expansion(sequence, depth, memo, keypad_map) -> int:

    if (sequence, depth) in memo:
        return memo[(sequence, depth)]

    if depth == 0:
        return len(sequence)

    length = 0
    bot_position = "A"
    for digit in sequence:
        length += min([keypad_expansion(x, depth - 1, memo, keypad_map) for x in keypad_map[bot_position][digit]])
        bot_position = digit

    memo[(sequence, depth)] = length
    return length

def find_complexity(commands, numpad_map, keypad_map, depth):
    numpad_bot = "A"
    complexity = []
    memo = dict()

    for command in commands:
        numpad_sequences = [""]

        for digit in command:
            sub_sequences = []
            for sequence in numpad_sequences:
                sub_sequences.extend([sequence + x for x in numpad_map[numpad_bot][digit]])
            numpad_bot = digit
            numpad_sequences = sub_sequences

        length = min([keypad_expansion(x, depth - 1, memo, keypad_map) for x in numpad_sequences])
        complexity.append(length * int(command.strip("A")))

    return sum(complexity)

def create_movement_map(pad, deadzone):

    # Create relational map for inputs
    mapping = defaultdict(lambda:dict())

    # For each button...
    for from_row_index, from_row in enumerate(pad):
        for from_col_index, from_char in enumerate(from_row):

            if from_char == 'X':
                continue

            #Find the input map to get to all other buttons
            for to_row_index, to_row in enumerate(pad):
                for to_col_index, to_char in enumerate(to_row):

                    if to_char == 'X':
                        continue

                    if from_char == to_char:
                        mapping[from_char][to_char] = ["A"]

                    move_row, move_col = to_row_index - from_row_index, to_col_index - from_col_index

                    shift_row = 1 if move_row > 0 else -1
                    shift_col = 1 if move_col > 0 else -1

                    movements = [(0, shift_col) for _ in range(abs(move_col))]
                    movements.extend([(shift_row, 0) for _ in range(abs(move_row))])

                    # print(f"Moving from {from_char} to {to_char}")
                    movements = [list(tuple_list) for tuple_list in set(itertools.permutations(movements))]

                    # Remove anything that tries to pass through the deadzone
                    bad_indeces = []
                    for path_index, path in enumerate(movements):
                        check_row, check_col = from_row_index, from_col_index
                        for move_row, move_col in path:
                            if (check_row + move_row, check_col + move_col) == deadzone:
                                bad_indeces.append(path_index)
                            check_row, check_col = check_row + move_row, check_col + move_col

                    for index in bad_indeces:
                        movements.pop(index)

                    mapping[from_char][to_char] = ["".join([MOVEMENTS[x] for x in tuple_list]) + "A" for tuple_list in movements ]

    return mapping

if __name__ == "__main__":
    main()