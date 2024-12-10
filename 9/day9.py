#!/usr/bin/python3
import itertools
import time
import cProfile

def main():
    global disk_map
    with open("day9.input", "r") as file:
        disk_map = file.read().strip()

    file_blocks = []
    empty_space = []

    print(len(disk_map))

    for index in range(0, len(disk_map), 2):
        file_blocks.append(int(disk_map[index]))
        try:
            empty_space.append(int(disk_map[index + 1]))
        except IndexError:
            pass

    ids = itertools.count(0, 1)

    expanded_map: list[int] = []
    for index, file_size in enumerate(file_blocks):
        id = next(ids)
        expanded_map.extend([ id for _ in range(file_size)])
        try:
            expanded_map.extend([ -1 for _ in range(empty_space[index])])
        except:
            pass

    #print(expanded_map)

    back_index = len(expanded_map) - 1

    for index, char in enumerate(expanded_map):
        while expanded_map[back_index] == -1:
            back_index -= 1

        if char != -1:
            continue

        if index >= back_index:
            break

        expanded_map[index] = expanded_map[back_index]
        expanded_map[back_index] = -1

        while expanded_map[back_index] == ".":
            back_index -= 1

    #print("".join(str(expanded_map)))


    checksum = sum([ num * index for index, num in enumerate(expanded_map) if num != -1])

    print(f"Checksum: {checksum}")
    if checksum != 6241633730082 and checksum != 1928:
        print("PART 1 FAILED")

def part2():
    file_blocks = []
    empty_space = []

    for index in range(0, len(disk_map), 2):
        file_blocks.append(int(disk_map[index]))
        try:
            empty_space.append(int(disk_map[index + 1]))
        except IndexError:
            pass

    ids = itertools.count(0, 1)

    expanded_map: list[dict[str, int]] = []
    for index, file_size in enumerate(file_blocks):
        id = next(ids)
        expanded_map.append({"id" : id, "size" : file_size})
        try:
            expanded_map.append({"id" : -1, "size" : empty_space[index]})
        except:
            pass
    last_file = next(ids) - 1

    # print([file["id"] for file in expanded_map for _ in range(file["size"]) ])

    for back_index in range(last_file, 0, -1):

        back_file = [ file for file in expanded_map if file["id"] == back_index ][0]
        # print(f"Check {back_file}")

        insert_file = None
        for file in expanded_map:
            if file["id"] != -1:
                continue

            if file["size"] >= back_file["size"]:
                insert_file = file
                break

        if not insert_file:
            # print(f"NO HOLE FOUND for {back_file}")
            continue

        if expanded_map.index(insert_file) > expanded_map.index(back_file):
            continue

        expanded_map.insert(expanded_map.index(insert_file), back_file.copy())

        # print(f'Update size {insert_file["size"]} to {insert_file["size"] - back_file["size"]}')
        if insert_file["size"] - back_file["size"] == 0:
            expanded_map.remove(insert_file)
        else:
            insert_file["size"] = insert_file["size"] - back_file["size"]

        back_file["id"] = -1

    # print([file["id"] for file in expanded_map for _ in range(file["size"]) ])

    condensed_map = []
    condensed_map.extend([file["id"] for file in expanded_map for _ in range(file["size"]) ])
    # print(condensed_map)
    checksum = sum([ num * index for index, num in enumerate(condensed_map) if num != -1])

    print(f"Part2: Formatted Checksum: {checksum}")
    if checksum != 2858 and checksum != 6265268809555:
        print("PART 2 FAILED")
if __name__ == "__main__":
    main()
    # cProfile.run("part2()")
    part2()