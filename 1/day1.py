#!/usr/bin/python3

def calc_diff(first:list[int], second: list[int]):
    list1 = first.copy()
    list2 = second.copy()

    list1.sort()
    list2.sort()

    diff_list = []
    for index in range(len(list1)):
        diff_list.append(abs(list1[index] - list2[index]))

    total_diff = sum(diff_list)
    print(f"Total Difference = {total_diff}")

def calc_sim_score(first:list[int], second: list[int]):
    list1 = first.copy()
    list2 = second.copy()

    sim_score = []
    for num in list1:
        count = list2.count(num)
        sim_score.append(count * num)

    print(f"Total Similarity Score = {sum(sim_score)}")

def main():

    list1 = []
    list2 = []

    with open("day1.input", "r") as file:
        for line in file:
            nums = line.split()

            list1.append(nums[0])
            list2.append(nums[1])

    list1 = [ int(x) for x in list1]
    list2 = [ int(x) for x in list2]

    calc_diff(list1, list2)

    calc_sim_score(list1, list2)

if __name__ == "__main__":
    main()