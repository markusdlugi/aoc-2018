from collections import defaultdict
from timeit import default_timer as timer

serial_number = 4455


def compute_power(x, y):
    rack_id = x + 10
    power = rack_id * y + serial_number
    power *= rack_id
    power = 0 if power < 100 else int(str(power)[-3])
    return power - 5


# Compute all powers in grid
start = timer()
powers = defaultdict(int)
for y in range(1, 301):
    for x in range(1, 301):
        powers[(x, y)] = compute_power(x, y)

# Build partial sums
sums = defaultdict(int)
for y in range(1, 301):
    for x in range(1, 301):
        # A B C
        # D E F
        # G H I
        # sums(I) = sums(H) + sums(F) - sums(E) + powers(I)
        sums[(x, y)] = sums[(x - 1, y)] + sums[(x, y - 1)] - sums[(x - 1, y - 1)] + powers[(x, y)]

max_power = max_power_square = max_power_square_3 = None
for size in range(300):
    for y in range(1, 301 - size):
        for x in range(1, 301 - size):
            # Square from x to xx and y to yy
            yy = y + size
            xx = x + size

            # A B C
            # D E F
            # G H I
            # power(square(E, F, H, I)) = sums(I) - sums(G) - sums(C) + sums(A)
            power = sums[(xx, yy)] - sums[(x - 1, yy)] - sums[(xx, y - 1)] + sums[(x - 1, y - 1)]

            if max_power is None or power > max_power:
                max_power = power
                max_power_square = (x, y, size + 1)
                if size == 2:
                    max_power_square_3 = max_power_square[:2]

print(*max_power_square_3, sep=',')
print(*max_power_square, sep=',')
end = timer()
print(f'Took {end - start} seconds.')
