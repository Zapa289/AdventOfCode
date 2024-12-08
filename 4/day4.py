#!/usr/bin/python3

VECTOR_LIST = [(x,y) for x in range(-1,2) for y in range(-1,2)]
VECTOR_LIST.remove((0,0))

VECS = [(-1, -1), (1, 1), (-1, 1), (1, -1)]

def check_SAM(coords) -> bool:
    row, col = coords

    for vec in VECS:
        if not check_vector(coords, vec):
            return False

    test = "".join([word_search[row - 1][col - 1],
                    word_search[row][col],
                    word_search[row + 1][col + 1]])
    if test != "MAS" and test != "SAM":
        return False

    test = "".join([word_search[row - 1][col + 1],
                    word_search[row][col],
                    word_search[row + 1][col - 1]])
    if test != "MAS" and test != "SAM":
        return False

    return True

def check_vector(coords, vector) -> bool:
    row, col = coords
    vec_row, vec_col = vector

    if row + vec_row < 0:
        return False
    if col + vec_col < 0:
        return False

    try:
        temp = word_search[row + vec_row][col + vec_col]
    except IndexError:
        return False

    return True

def detect_xmas(coords: tuple[int, int], vector: tuple[int, int]) -> bool:
    vec_row, vec_col = vector
    new_row, new_col = coords

    if not check_vector(coords, (3 * vec_row, 3 * vec_col)):
        return False

    for char in "MAS":
        new_row += vec_row
        new_col += vec_col

        if word_search[new_row][new_col] != char:
            return False

    return True

def main():
    global word_search
    with open("day4.input", "r") as file:
        word_search = [ row.strip() for row in file]

    print(f"Rows = {len(word_search)}")
    print(f"Cols = {len(word_search[0])}")

    # Part 1
    total = 0
    for row_index, row in enumerate(word_search):
        for col_index, character in enumerate(row):
            if character == 'X':
                for vector in VECTOR_LIST:
                    if detect_xmas((row_index, col_index), vector):
                        total += 1

    print(f"Number of XMAS: {total}")

    # Part 2
    hits = [(row_index, col_index) for row_index, row in enumerate(word_search) for col_index, character in enumerate(row) if character == 'A']

    total = 0
    for hit in hits:
        if check_SAM(hit):
            total += 1
    print(f"Number X-MAS: {total}")

if __name__ == "__main__":
    main()