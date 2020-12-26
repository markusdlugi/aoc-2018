import re


def minmax_xy(points):
    max_x, max_y, _, _ = [max(index) for index in zip(*points)]
    min_x, min_y, _, _ = [min(index) for index in zip(*points)]
    return min_x, min_y, max_x, max_y


points = []
for line in open("input/10.txt"):
    points.append(list(map(int, re.findall(r'position=<\s*(-?\d*),\s*(-?\d*)> velocity=<\s*(-?\d*),\s*(-?\d*)>', line.strip())[0])))

time = 0
prev_diff = None
jumped = False
while True:
    # Apply velocities to positions
    time += 1
    for point in points:
        point[0] += point[2]
        point[1] += point[3]
    _, min_y, _, max_y = minmax_xy(points)
    new_diff = max_y - min_y

    # Extrapolate based on change rate and skip a few steps
    if prev_diff is not None and not jumped:
        jumped = True
        change = prev_diff - new_diff
        target = 20
        steps = (new_diff - target) // change
        for point in points:
            point[0] += point[2] * steps
            point[1] += point[3] * steps
        time += steps
        _, min_y, _, max_y = minmax_xy(points)
        new_diff = max_y - min_y

    # Break if diff has grown instead of shrinking
    if prev_diff is None or new_diff < prev_diff:
        prev_diff = new_diff
    else:
        break

# Revert last change (since diff has grown again)
for point in points:
    point[0] -= point[2]
    point[1] -= point[3]

min_x, min_y, max_x, max_y = minmax_xy(points)

# Scrap velocities for printing
points = list(zip(*list(zip(*points))[:2]))

# Print points
for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        print("#" if (x, y) in points else " ", sep="", end="")
    print()

print()
print(time - 1)
