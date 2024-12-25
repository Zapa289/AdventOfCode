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
    st = time.time()

    cliques = []
    R = set()
    X = set()
    BronKerbosch(R, set(vertices.keys()), X, vertices, cliques)

    maximum_clique = max(cliques,key=len)
    print("Part 2: Password = ", ",".join(sorted(maximum_clique)))
    print(f"Time: {time.time() - st}s\n")

def is_clique(graph, clique) -> bool:
    for a in clique:
        for b in clique:
            if a == b:
                continue
            if b not in graph[a]:
                return False
    return True

def BronKerbosch(R:set, P:set, X:set, graph, cliques) -> set:
    # First iteration:
    #  R is empty
    #  P is list of vertices
    #  X is empty

    # if P and X are both empty then
    #     report R as a maximal clique
    # for each vertex v in P do
    #     BronKerbosch1(R ⋃ {v}, P ⋂ N(v), X ⋂ N(v))
    #     P := P \ {v}
    #     X := X ⋃ {v})

    # N(v) -> neighbors of v

    if len(P) == 0 and len(X) == 0:
        cliques.append(R)
        return

    for vertex in P.copy():
        next_R = R | {vertex}
        next_P = P & set(graph[vertex])
        next_X = X & set(graph[vertex])

        BronKerbosch( next_R, next_P, next_X, graph, cliques)

        P.remove(vertex)
        X.add(vertex)

if __name__ == "__main__":
    main()