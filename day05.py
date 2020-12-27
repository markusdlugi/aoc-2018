import re
from timeit import default_timer as timer

opposites = dict()
for char in map(chr, range(ord('a'), ord('z')+1)):
    opposites[char] = char.upper()
    opposites[char.upper()] = char


def is_unit(a, b):
    return opposites[a] == b


def react_units(polymer, i):
    if i < 0 or i >= len(polymer):
        return (polymer, i)
    a = polymer[i:i + 1]
    b = polymer[i + 1:i + 2]
    if is_unit(a, b):
        polymer = polymer[:i] + polymer[i+2:]
        return react_units(polymer, i - 1)
    else:
        return (polymer, i)


def react_units_with_stack(polymer):
    stack = []
    for c in polymer:
        if stack and is_unit(stack[-1], c):
            stack.pop()
        else:
            stack.append(c)
    return stack


polymer = open("input/05.txt").read()


# Part A - find minimum length by reducing all units
def solve_old():
    start = timer()
    current = polymer
    i = 0
    while i < len(current):
        current, i = react_units(current, i)
        i += 1
    print(len(current))

    # Part B - find minimum length after removing all units of specific type
    min_length = None
    for char in map(chr, range(ord('a'), ord('z')+1)):
        current = re.sub(f'[{char}{char.upper()}]', '', polymer)
        i = 0
        while i < len(current):
            current, i = react_units(current, i)
            i += 1
        if min_length is None or len(current) < min_length[0]:
            min_length = (len(current), char)
    print(min_length[0])
    end = timer()
    print(f'Took {end - start} seconds.')
    print()


# Stack-based solution without changing strings
# Part A
start = timer()
stack = react_units_with_stack(polymer)
print(len(stack))

# Part B
min_length = None
for char in map(chr, range(ord('a'), ord('z')+1)):
    current = re.sub(f'[{char}{char.upper()}]', '', polymer)
    stack = react_units_with_stack(current)
    if min_length is None or len(stack) < min_length[0]:
        min_length = (len(stack), char)
print(min_length[0])
end = timer()
print(f'Took {end - start} seconds.')
