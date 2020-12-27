# Read track and carts
directions = {"^": 0, ">": 1, "v": 2, "<": 3}
tracks = dict()
carts = dict()
for y, line in enumerate(open("input/13.txt")):
    for x, c in enumerate(line):
        if c == " " or c == "\n":
            continue
        elif c in ["^", "v", "<", ">"]:
            carts[(x, y)] = (directions[c], -1)
            tracks[(x, y)] = "|" if c in ["^", "v"] else "-"
        else:
            tracks[(x, y)] = c

# Direction mapping: 0, 1, 2, 3 -> up, right, down, left
dx, dy = ([0, 1, 0, -1], [-1, 0, 1, 0])
# Mapping for changing direction in curves
curve = {"/": [1, 3, 1, 3], "\\": [3, 1, 3, 1]}
# Carts go left, straight, right
moves = [3, 0, 1]
time = 0
firstCollision = True
while True:
    time += 1
    cart_positions = list(carts.keys())
    cart_positions.sort()
    for old_x, old_y in cart_positions:
        # Might have been removed due to collision
        if (old_x, old_y) not in carts:
            continue
        d, m = carts[(old_x, old_y)]

        # New position
        x, y = (old_x + dx[d], old_y + dy[d])
        assert (x, y) in tracks

        # Check if direction changes due to intersection or curve
        c = tracks[(x, y)]
        if c == "+":
            m += 1
            d = (d + moves[m % len(moves)]) % 4
        elif c == "/" or c == "\\":
            d = (d + curve[c][d]) % 4
        del carts[(old_x, old_y)]

        # Check for collisions
        if (x, y) in carts:
            if firstCollision:
                print(x, y, sep=',')
                firstCollision = False
            del carts[(x, y)]
            #print(f'Collision at position {(x, y)} after {time} ticks, {len(carts)} carts left.')
        else:
            carts[(x, y)] = (d, m)
    if len(carts) == 1:
        print(*list(carts.keys())[0], sep=',')
        break
