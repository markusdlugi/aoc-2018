import heapq
from timeit import default_timer as timer

start = timer()

lines = [line.strip() for line in open("input/22.txt")]
depth = int(lines[0].split()[1])
target = tuple(int(x) for x in lines[1].split()[1].split(","))

# Part A
erosion = dict()
types = dict()
risk_index = 0
for x in range(target[0] + 20):
    for y in range(target[1] + 20):
        if (x, y) in [(0, 0), target]:
            geo = 0
        elif y == 0:
            geo = x * 16807
        elif x == 0:
            geo = y * 48271
        else:
            geo = erosion[(x - 1, y)] * erosion[(x, y - 1)]
        lvl = (geo + depth) % 20183
        erosion[(x, y)] = lvl
        types[(x, y)] = lvl % 3

        if x <= target[0] and y <= target[1]:
            risk_index += lvl % 3

print(risk_index)

# Part B
dx, dy = ((0, 1, 0, -1), (-1, 0, 1, 0))

# Required items per type - 0: rocky, 1: wet, 2: narrow
# First item = torch, second item = climbing gear
item_required = {0: [(1, 0), (0, 1)], 1: [(0, 1), (0, 0)],
                 2: [(1, 0), (0, 0)]}
# Forbidden items
item_forbidden = {0: (0, 0), 1: (1, 0), 2: (0, 1)}


def moves(time, x, y, items):
    for d in range(4):
        xx, yy = (x + dx[d], y + dy[d])
        if (xx, yy) not in types:
            continue

        # Check if we need to switch items to go there
        r = types[(x, y)]
        rr = types[(xx, yy)]
        new_items = items
        switch = False
        if items == item_forbidden[rr]:
            switch = True
            if item_required[rr][0] != item_forbidden[r]:
                new_items = item_required[rr][0]
            elif item_required[rr][1] != item_forbidden[r]:
                new_items = item_required[rr][1]

        yield time + 1 + (7 if switch else 0), xx, yy, d, new_items


# Start with torch at 0,0
items = (1, 0)
# Time, x, y, direction, items
start_state = (0, 0, 0, 0, items)
q = [start_state]
# We keep track of x, y, direction and items for visited set
# Additionally, we might revisit a state if we reach it with lower time later on, so use a dict
visited = {start_state[1:5]: 0}
times = []
while q:
    time, x, y, d, items = heapq.heappop(q)
    if (x, y) == target:
        times.append(time if items == (1, 0) else time + 7)
    for m in moves(time, x, y, items):
        t, x, y, d, items = m
        state = m[1:5]
        if state not in visited or visited[state] > t:
            visited[state] = t
            heapq.heappush(q, m)
print(min(times))

end = timer()
print(f'Took {end - start} seconds.')