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
    keypad_map['A']["<"].remove("<v<A")
    keypad_map['<']['A'].remove(">^>A")
    # pprint.pprint(keypad_map)

    def keypad_translation(sequence_list, memo):
        bot_sequence = []
        bot_position = "A"
        for sequence in sequence_list:

            sub_sequences = [""]
            for digit in sequence:
                sub_sequences = [x + y for x in sub_sequences for y in keypad_map[bot_position][digit]]
                # memo[(digit, bot_position)] = sub_sequences
                bot_position = digit

            bot_sequence.extend(sub_sequences)

        #minimum = min(map(len, bot_sequence))
        return bot_sequence
        #return [x for x in bot_sequence if len(x) == minimum]

    for key, values in keypad_map.items():
        for to_key, to_paths in values.items():
            if len(to_paths) == 1:
                continue
            size = []
            for path in to_paths:
                temp = [path]
                temp = keypad_translation(temp, None)
                print(f"{key} -> {to_key}: {path} = {temp}, {list(map(len, temp))}")
                size.append(min(list(map(len, temp))))

            print(size)
            minimum = min(size)
            for index in range(len(size)):
                if size[index] > minimum:
                    keypad_map[key][to_key].pop(index)

            if len(keypad_map[key][to_key]) > 1:
                keypad_map[key][to_key].pop()

            # keypad_map[key][to_key] = keypad_map[key][to_key][0]

    pprint.pprint(keypad_map)
    # quit()

    print(f"Init time: {time.time() - st}s\n")
    st = time.time()

    numpad_bot = "A"
    complexity = []
    memo = dict()

    for command in commands:
        numpad_sequences = [""]
        for digit in command:
            numpad_sequences = [ x + y for x in numpad_sequences for y in numpad_map[numpad_bot][digit]]
            numpad_bot = digit

        bot_sequences = numpad_sequences
        for _ in range(2):
            bot_sequences = keypad_translation(bot_sequences, memo)

        minimum = min(map(len, bot_sequences))
        print(minimum * int(command.strip("A")))
        complexity.append(minimum * int(command.strip("A")))

    print(f"Part 1: Complexity = {sum(complexity)}")
    print(f"Time: {time.time() - st}s\n")

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