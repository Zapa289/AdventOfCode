#!/usr/bin/python3

import time
import math

TOKENS_A = 3
TOKENS_B = 1
PRESS_LIMIT = 100

ADDITIONAL = 10000000000000

def main():
    with open("day13.input", "r") as file:
        machines = [line.replace("Button A:", "").replace("Button B:", "").replace(" X", "").replace(" Y", "").replace("Prize:", "").replace("+", "").replace("=", "").split() for line in file.read().split("\n\n")]

    st = time.time()
    part1(machines)
    print(f"\tTime: {time.time() - st}\n")

    st = time.time()
    part2(machines)
    print(f"\tTime: {time.time() - st}\n")

def part1(machines):
    tokens = 0
    for machine in machines:
        Ax, Ay = tuple(map(int, machine[0].split(",")))
        Bx, By = tuple(map(int, machine[1].split(",")))
        Px, Py = tuple(map(int, machine[2].split(",")))

        # print(f"n{Ax} + m{Bx} = {Px}")
        # print(f"n{Ay} + m{By} = {Py}")

        start = min(math.floor(Px / Bx), math.floor(Py / By), 100)

        solution = (0,0)
        for m in range(start, 1, -1):
            n = int((Px - (m * Bx)) / Ax)

            if n > 100:
                continue

            if n * Ax + m * Bx != Px:
                continue

            if n * Ay + m * By != Py:
                continue

            if solution == (0,0) or solution[1] < m:
                solution = (n, m)

        if solution != (0,0):
            n, m = solution
            tokens += n * TOKENS_A + m * TOKENS_B

    print(f"Part 1: Required tokens = {tokens}")

def part2(machines):
    tokens = 0
    for machine in machines:
        Ax, Ay = tuple(map(int, machine[0].split(",")))
        Bx, By = tuple(map(int, machine[1].split(",")))
        Px, Py = tuple(map(int, machine[2].split(",")))

        Px += ADDITIONAL
        Py += ADDITIONAL

        # print(f"n{Ax} + m{Bx} = {Px}")
        # print(f"n{Ay} + m{By} = {Py}")

        n = int((Py*Bx - By*Px) / (Bx*Ay - Ax*By))
        m = int((Px - n * Ax) / Bx)

        if n * Ax + m * Bx != Px:
            continue

        if n * Ay + m * By != Py:
            continue

        tokens += n * TOKENS_A + m * TOKENS_B
        print(f"Solution: {(n,m)} - tokens {tokens}")

    print(f"Part 2: Required tokens = {tokens}")

def find_factors(number: int, memo) -> list[int]:
    set(
        factor for i in range(1, int(number**0.5) + 1) if number % i == 0
        for factor in (i, number//i)
    )
if __name__ == "__main__":
    main()