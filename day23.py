import re
from z3 import Int, Optimize, Sum, If, And
from timeit import default_timer as timer

start = timer()
lines = [line.strip() for line in open("input/23.txt")]

nanobots = dict()
for line in lines:
    x, y, z, count = tuple(int(x) for x in re.findall(r"pos=<([-]?\d+),([-]?\d+),([-]?\d+)>, r=([-]?\d+)", line)[0])
    nanobots[(x, y, z)] = count


def get_dist(a, b):
    return sum(abs(a[i] - b[i]) for i in range(3))


def is_in_range(a, b, r):
    return r >= get_dist(a, b)


def count_in_range(pos, nanobots, r=None):
    return sum(1 for k, v in nanobots.items() if is_in_range(pos, k, v if r is None else r))

# Part A
strongest = max(nanobots, key=nanobots.get)
total_in_range = count_in_range(strongest, nanobots, nanobots[strongest])
print(total_in_range)

# Part B
x_values = [n[0] for n in nanobots.keys()]
y_values = [n[1] for n in nanobots.keys()]
z_values = [n[2] for n in nanobots.keys()]

x = Int("x")
y = Int("y")
z = Int("z")
count = Int("count")
dist = Int("dist")

s = Optimize()
s.add(And(min(x_values) <= x, x <= max(x_values)))
s.add(And(min(y_values) <= y, y <= max(y_values)))
s.add(And(min(z_values) <= z, z <= max(z_values)))


def z3_abs(x):
    return If(x >= 0, x, -x)


def z3_dist(x, y, z, xx, yy, zz):
    return Sum([z3_abs(x - xx), z3_abs(y - yy), z3_abs(z - zz)])


def z3_in_range(x, y, z, xx, yy, zz, r):
    return r >= z3_dist(x, y, z, xx, yy, zz)


def z3_count_in_range(x, y, z):
    return Sum([If(z3_in_range(x, y, z, xx, yy, zz, r), 1, 0) for (xx, yy, zz), r in nanobots.items()])


s.add(count == z3_count_in_range(x, y, z))
s.add(dist == z3_dist(x, y, z, 0, 0, 0))

h1 = s.maximize(count)
h2 = s.minimize(dist)
s.check()
m = s.model()
pos = [m.evaluate(v).as_long() for v in [x, y, z]]

print(get_dist(pos, (0, 0, 0)))

end = timer()
print(f'Took {round((end - start) * 1000, 2)} ms.')