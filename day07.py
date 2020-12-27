import networkx as nx
from collections import deque
from heapq import heappush, heappop

words = [line.strip().split() for line in open("input/07.txt")]
steps = [(word[1], word[7]) for word in words]

# Part A
G = nx.DiGraph()
G.add_edges_from(steps)
print(*list(nx.lexicographical_topological_sort(G)), sep='')

# Part B
weights = dict()
for char in range(ord('A'), ord('Z') + 1):
    weights[chr(char)] = 61 + char - ord('A')

total_time = 0
task_queue = deque()
start_nodes = [node for node in G.nodes if len(G.in_edges(node)) == 0]
worker_heap = []
for node in start_nodes:
    heappush(worker_heap, [weights[node], node])

while worker_heap:
    weight, n = heappop(worker_heap)
    total_time += weight
    for parallel_step in worker_heap:
        parallel_step[0] -= weight
    targets = [target for source, target in G.out_edges(n)]
    targets.sort()
    task_queue.extend([target for target in targets if target not in task_queue and len(G.in_edges(target)) <= 1])
    while task_queue and len(worker_heap) < 5:
        target = task_queue.popleft()
        heappush(worker_heap, [weights[target], target])
    G.remove_node(n)
print(total_time)
