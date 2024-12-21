#!/usr/bin/python3

import time
import pprint
from collections import defaultdict

NUMBER_PAD = [["7", "8", "9"],
              ["4", "5", "6"],
              ["X", "0", "A"]]
NUMPAD_DEFAULT = (2, 2)

KEYPAD = [["X", "^", "A"],
          ["<", "V", ">"]]
KEYPAD_DEFAULT = (0, 2)

MOVEMENTS = {
    (0,1) : ">",
    (0, -1) : "<",
    (1, 0)  : "V",
    (-1, 0) : "^"
}

def main():
    with open("day21-test.input", "r") as file:
        commands = file.readlines()

    print(commands)

    # Create relational map for inputs
    numpad_map = defaultdict(lambda:dict())

    # For each button...
    for from_row_index, from_row in enumerate(NUMBER_PAD):
        for from_col_index, from_char in enumerate(from_row):

            if from_char == 'X':
                continue

            #Find the input map to get to all other buttons
            for to_row_index, to_row in enumerate(NUMBER_PAD):
                for to_col_index, to_char in enumerate(to_row):

                    if to_char == 'X':
                        continue

                    if from_char == to_char:
                        continue

                    move_row, move_col = to_row_index - from_row_index, to_col_index - from_col_index

                    shift_row = 1 if move_row > 0 else -1
                    shift_col = 1 if move_col > 0 else -1

                    movements = [(0, shift_col) for x in range(abs(move_col))]
                    movements.extend([(shift_row, 0) for x in range(abs(move_row))])

                    numpad_map[from_char][to_char] = "".join([MOVEMENTS[x] for x in movements])

    pprint.pprint(numpad_map)

if __name__ == "__main__":
    main()