import re

lines = [line.strip() for line in open("input/03.txt")]
claims = [list(map(int, re.findall(r'#(\d*) @ (\d*),(\d*): (\d*)x(\d*)', line)[0])) for line in lines]

inches = set()
overlapping_inches = set()

# Part A - find number of overlapping inches
for claim_id, left, top, width, height in claims:
    for (x, y) in ((x, y) for x in range(left, left + width) for y in range(top, top + height)):
        if (x, y) in inches:
            overlapping_inches.add((x, y))
        else:
            inches.add((x, y))

print(len(overlapping_inches))

# Part B - find single claim without overlaps
for claim_id, left, top, width, height in claims:
    overlapping = False
    for (x, y) in ((x, y) for x in range(left, left + width) for y in range(top, top + height)):
        if (x, y) in overlapping_inches:
            overlapping = True
            break
    if not overlapping:
        print(claim_id)
        break
