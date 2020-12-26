from collections import deque


def show(facility):
    max_xy = (max(facility.keys(), key=lambda x: x[0])[0], max(facility.keys(), key=lambda x: x[1])[1])
    min_xy = (min(facility.keys(), key=lambda x: x[0])[0], min(facility.keys(), key=lambda x: x[1])[1])
    for y in range(min_xy[1] - 1, max_xy[1] + 2):
        for x in range(min_xy[0] - 1, max_xy[0] + 2):
            if (x, y) not in facility:
                print("#", sep='', end='')
            else:
                print(facility[(x, y)], sep='', end='')
        print()


def moves(x, y, facility):
    dx, dy = ((0, 1, 0, -1), (-1, 0, 1, 0))
    for i in range(4):
        # Door position
        xx, yy = (x + dx[i], y + dy[i])
        if (xx, yy) not in facility:
            continue
        # Room position
        yield (xx + dx[i], yy + dy[i])


line = open("input/20.txt").read().strip()

compass = {"N": 0, "E": 1, "S": 2, "W": 3}
dx, dy = ((0, 1, 0, -1), (-1, 0, 1, 0))
facility = {(0, 0): "X"}
q = deque()
x, y = (0, 0)
for c in line:
    if c == "^" or c == "$":
        continue
    elif c == "(":
        q.append((x, y))
    elif c == ")":
        x, y = q.pop()
    elif c == "|":
        x, y = q.pop()
        q.append((x, y))
    else:
        d = compass[c]
        x, y = (x + dx[d], y + dy[d])
        facility[(x, y)] = "|" if d == 1 or d == 3 else "-"
        x, y = (x + dx[d], y + dy[d])
        facility[(x, y)] = "."

# show(facility)

x, y = (0, 0)
q = deque([(0, x, y)])
visited = {(x, y)}
room_dist = dict()
while q:
    d, x, y = q.popleft()
    room_dist[(x, y)] = d
    for m in moves(x, y, facility):
        if m not in visited:
            visited.add(m)
            q.append((d + 1, *m))

print(max(room_dist.values()))
print(sum(1 for x in room_dist.values() if x >= 1000))
