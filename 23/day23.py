#!/usr/bin/python3

import pprint
import time
from collections import defaultdict
from itertools import combinations


def main():
    with open("day23.input", "r") as file:
        edges = [tuple(line.strip().split("-")) for line in file]

    vertices = defaultdict(lambda:list())
    for comp1, comp2 in edges:
        vertices[comp1].append(comp2)
        vertices[comp2].append(comp1)

    # pprint.pprint(vertices)
    st = time.time()

    combos = combinations(vertices.keys(), 3)
    valid_cliques = set()
    for combo in combos:
        if is_clique(vertices, combo):
            for node in combo:
                if node.startswith("t"):
                    valid_cliques.update([combo])
                    break

    print(f"Part 1: Size 3 cliques = {len(valid_cliques)}")
    print(f"Time: {time.time() - st}s\n")

def is_clique(graph, clique) -> bool:
    for a in clique:
        for b in clique:
            if a == b:
                continue
            if b not in graph[a]:
                return False
    return True

if __name__ == "__main__":
    main()