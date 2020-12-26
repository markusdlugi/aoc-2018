from collections import deque


def moves(x, y, d, clay, water, wet, min_y, max_y):
    dx, dy = ([0, 1, 0, -1], [-1, 0, 1, 0])

    # We might have filled this spot already, then do nothing
    # Important so we don't run into any infinite loops
    if (x, y) in water:
        return []

    # If we are out of screen, stop
    target = (x + dx[d], y + dy[d])
    if target[1] > max_y:
        return []

    # If below is blocked, check if we can fill
    below = (x + dx[2], y + dy[2])
    if below in clay or below in water:
        wet.add((x, y))
        added = {(x, y)}
        holes = []
        # Go to both sides until we hit clay
        for dd in [1, 3]:
            xx, yy = x, y
            while (xx + dx[dd], yy + dy[dd]) not in clay:
                xx, yy = (xx + dx[dd], yy + dy[dd])
                wet.add((xx, yy))
                added.add((xx, yy))
                # Ensure there is always clay or water below, otherwise there's a hole
                below = (xx + dx[2], yy + dy[2])
                if below not in clay and below not in water:
                    holes.append((xx, yy))
                    break
        if not holes:
            # No holes, fill up everything between the two walls
            for (xx, yy) in added:
                water.add((xx, yy))
                wet.remove((xx, yy))
            # Go one up to check if we can fill next row
            up = (x + dx[0], y + dy[0])
            return [(*up, 0)]
        else:
            # There are some holes (at least one), don't fill but go down the holes
            return list(map(lambda x: (*x, 2), holes))
    # Else go all the way down until we hit something
    elif d == 2:
        xx, yy = x, y
        while (xx, yy) not in clay and (xx, yy) not in water and min_y <= yy <= max_y:
            wet.add((xx, yy))
            xx, yy = (xx + dx[d], yy + dy[d])
        yy -= 1
        return [(xx, yy, d)]
    else:
        return []


def show(min_xy, max_xy, clay, water, wet):
    for y in range(min_xy[1], max_xy[1] + 1):
        for x in range(min_xy[0], max_xy[0] + 1):
            if (x, y) == (463, 208):
                print("!", end='')
            else:
                print("#" if (x, y) in clay else "~" if (x, y) in water else "|" if (x, y) in wet else " ", end='')
        print()
    print()


clay = set()
for line in open("input/17.txt"):
    x = y = 0
    for assignment in line.strip().split(", "):
        if assignment.startswith("x="):
            x = assignment[2:]
            x = list(map(int, x.split(".."))) if ".." in x else int(x)
        else:
            y = assignment[2:]
            y = list(map(int, y.split(".."))) if ".." in y else int(y)
    if isinstance(x, list):
        for i in range(x[0], x[1] + 1):
            clay.add((i, y))
    else:
        for i in range(y[0], y[1] + 1):
            clay.add((x, i))

min_xy = (min(clay, key=lambda x: x[0])[0], min(clay, key=lambda x: x[1])[1])
max_xy = (max(clay, key=lambda x: x[0])[0], max(clay, key=lambda x: x[1])[1])

spring = (500, min_xy[1])
water = set()
wet = {spring}
q = deque()
q.append((*spring, 2))
while q:
    x, y, d = q.popleft()
    result = moves(x, y, d, clay, water, wet, min_xy[1], max_xy[1])
    for m in result:
        q.append(m)

min_xy = (min(wet, key=lambda x: x[0])[0], min(wet, key=lambda x: x[1])[1])
max_xy = (max(wet, key=lambda x: x[0])[0], max(wet, key=lambda x: x[1])[1])
#show(min_xy, max_xy, clay, water, wet)
print(len(wet) + len(water))
print(len(water))
