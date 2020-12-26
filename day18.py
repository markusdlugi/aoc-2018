from collections import Counter
from timeit import default_timer as timer


def moves(x, y):
    dx, dy = ((-1, 0, 1, 1, 1, 0, -1, -1), (-1, -1, -1, 0, 1, 1, 1, 0))
    for d in range(8):
        yield (x + dx[d], y + dy[d])


def show(acres, max_x, max_y):
    for y in range(max_y):
        for x in range(max_x):
            c = '.' if acres[(x, y)] == 0 else '|' if acres[(x, y)] == 1 else "#"
            print(c, sep='', end='')
        print()


start = timer()
lines = [line.strip() for line in open("input/18.txt")]

# 0 = open, 1 = trees, 2 = lumber
acres = dict()
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        acres[(x, y)] = 0 if c == "." else 1 if c == "|" else 2
max_x, max_y = (x, y)

seen = {}
minute = 0
target_minute = 1_000_000_000
while minute < target_minute:
    minute += 1

    # Simulate new states of all acres
    new_acres = acres.copy()
    for (x, y), state in acres.items():
        adj_count = Counter(acres[(xx, yy)] for (xx, yy) in moves(x, y) if (xx, yy) in acres)
        if state == 0 and adj_count[1] >= 3:
            state = 1
        elif state == 1 and adj_count[2] >= 3:
            state = 2
        elif state == 2 and (adj_count[1] < 1 or adj_count[2] < 1):
            state = 0
        new_acres[(x, y)] = state
    acres = new_acres

    # Part A
    if minute == 10:
        count = Counter(acres.values())
        print(count[1] * count[2])

    # Part B
    hash = "".join(str(s) for s in acres.values())
    if hash in seen.keys():
        diff = minute - seen[hash]
        minute = minute + diff * ((target_minute - minute) // diff)
    else:
        seen[hash] = minute

count = Counter(acres.values())
print(count[1] * count[2])
end = timer()
print(f'Took {end - start} seconds.')

# show(acres, max_x, max_y)
