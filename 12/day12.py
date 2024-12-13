#!/usr/bin/python3

import time

CARDINALS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def main():
    with open("day12.input", "r") as file:
        garden = [[x for x in line.strip()] for line in file.readlines()]

    # for line in garden:
    #     print("".join(line))
    st = time.time()
    part1(garden)
    print(f"\tTime: {time.time() - st}s\n")

    st = time.time()
    part2(garden)
    print(f"\tTime: {time.time() - st}s\n")

def part1(garden):
    species: dict[str, list[tuple[int, int]]] = dict()

    for row, line in enumerate(garden):
        for col, char in enumerate(line):
            if char in species:
                species[char].append((row, col))
            else:
                species[char] = [(row,col)]

    total_price = 0
    for specie, cells in species.items():
        regions:list[list[tuple[int, int]]] = []
        while len(cells) != 0:
            cell = cells.pop()
            region = find_neighbors(cell, cells)
            regions.append(region)

        for region in regions:
            perimeter = 0
            for cell_row, cell_col in region:
                found = 0
                for direction in CARDINALS:
                    dir_row, dir_col = direction
                    if (cell_row + dir_row, cell_col + dir_col) in region:
                        found += 1
                perimeter += 4 - found

            #print(f"Region {specie}: {len(region)} : {perimeter}")
            total_price += len(region) * perimeter

    print(f"Part 1 total price: {total_price}")
    if total_price != 1930 and total_price != 1573474:
        print("FAIL")

def part2(garden):
    species: dict[str, list[tuple[int, int]]] = dict()

    for row, line in enumerate(garden):
        for col, char in enumerate(line):
            if char in species:
                species[char].append((row, col))
            else:
                species[char] = [(row,col)]

    total_price = 0
    for species, cells in species.items():
        # regions:list[list[tuple[int, int]]] = []
        while len(cells) != 0:
            cell = cells.pop()
            region = find_neighbors(cell, cells)
            sides = 0

            for node_row, node_col in region:
                # Logic: Is X a corner?
                #
                #    A | B
                #    - + -
                #    C | X
                #
                #   !B!C + !ABC

                # 2x2 frame
                # Bottom Right
                # BR -> TL = (-1, -1) BR -> TR = (-1, 0), BR -> BL = (0, -1)
                if (
                    (   # Cross is empty, adjacents are filled
                        ((node_row - 1, node_col - 1) not in region)
                        and ((node_row - 1, node_col) in region)
                        and ((node_row, node_col - 1) in region)
                    )
                    or  # Adjacent nodes are empty
                    (
                        ((node_row - 1, node_col) not in region)
                        and ((node_row, node_col - 1) not in region)
                    )
                ):
                    sides += 1

                # Bottom Left
                # BL -> TR = (-1, 1) BL -> TL = (-1, 0), BL -> BR = (0, 1)
                if (
                    (
                        ((node_row - 1, node_col + 1) not in region)
                        and ((node_row - 1, node_col) in region)
                        and ((node_row, node_col + 1) in region)
                    )
                    or
                    (
                        ((node_row - 1, node_col) not in region)
                        and ((node_row, node_col + 1) not in region)
                    )
                ):
                    sides += 1

                # Top Right
                # TR -> BL = (1, -1) TR -> BR = (1, 0), TR -> TL = (0, -1)
                if (
                    (
                        (node_row + 1, node_col - 1) not in region
                        and ((node_row + 1, node_col) in region)
                        and ((node_row, node_col - 1) in region)
                    )
                    or
                    (
                        ((node_row + 1, node_col) not in region)
                        and ((node_row, node_col - 1) not in region)
                    )
                ):
                    sides += 1

                # Top Left
                # TL -> BR = (1, 1) TL -> BL = (1, 0), TL -> TR = (0, 1)
                if (
                    (
                        ((node_row + 1, node_col + 1) not in region)
                        and ((node_row + 1, node_col) in region)
                        and ((node_row, node_col + 1) in region)
                    )
                    or
                    (
                        ((node_row + 1, node_col) not in region)
                        and ((node_row, node_col + 1) not in region)
                    )
                ):
                    sides += 1

            #print(f"Region {species}: {len(region)} : {sides}\n")
            total_price += len(region) * sides

    print(f"Part 2 total price: {total_price}")
    if total_price != 1206 and total_price != 966476:
        print("FAIL")

def find_neighbors(cell, values:list[tuple[int,int]]) -> list[tuple[int,int]]:
    cell_row, cell_col = cell
    region = [cell]
    for direction in CARDINALS:
        dir_row, dir_col = direction
        if (cell_row + dir_row, cell_col + dir_col) in values:
            values.remove((cell_row + dir_row, cell_col + dir_col))
            region.extend(find_neighbors((cell_row + dir_row, cell_col + dir_col), values))

    return region

if __name__ == "__main__":
    main()