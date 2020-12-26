from itertools import combinations
import networkx as nx

coordinates = [tuple(int(x) for x in line.strip().split(",")) for line in open("input/25.txt")]


def dist(a, b):
    return sum(abs(a[i] - b[i]) for i in range(len(a)))


G = nx.Graph()

for coord in coordinates:
    G.add_node(coord)
for a, b in combinations(coordinates, 2):
    if dist(a, b) <= 3:
        G.add_edge(a, b)

print(len(list(nx.connected_components(G))))
