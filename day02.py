from collections import Counter
from itertools import combinations

boxes = [line.strip() for line in open("input/02.txt")]

# Part A
char_counts = [Counter(box).values() for box in boxes]
two_count = sum([1 if 2 in count else 0 for count in char_counts])
three_count = sum([1 if 3 in count else 0 for count in char_counts])
print(two_count * three_count)

# Part B
for a, b in combinations(boxes, 2):
    diff_index = -1
    found = False
    for i in range(len(a)):
        if a[i] != b[i] and diff_index == -1:
            found = True
            diff_index = i
        elif a[i] != b[i]:
            found = False
            break
    if found:
        print(a[:diff_index] + a[diff_index+1:])

