from collections import Counter


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


coords = [tuple(map(int, line.strip().split(', '))) for line in open("input/06.txt")]

min_x = min((x for x, y in coords))
max_x = max((x for x, y in coords))
min_y = min((y for x, y in coords))
max_y = max((y for x, y in coords))

region = dict()
infinite = set()
safe_region_size = 0
for (x, y) in ((x, y) for x in range(min_x, max_x + 1) for y in range(min_y, max_y + 1)):
    curr_min = None
    curr_min_coord = None
    total_distance = 0
    for i in range(0, len(coords)):
        distance = dist((x, y), coords[i])
        total_distance += distance
        if curr_min is None or distance < curr_min:
            curr_min = distance
            curr_min_coord = i
        elif distance == curr_min:
            curr_min_coord = -1
    region[(x, y)] = curr_min_coord
    if total_distance < 10000:
        safe_region_size += 1
    if x in [min_x, max_x] or y in [min_y, max_y]:
        infinite.add(curr_min_coord)

count = Counter(region.values())
for curr_max, curr_max_size in count.most_common():
    if curr_max == -1 or curr_max in infinite:
        continue
    print(curr_max_size)
    break

print(safe_region_size)
