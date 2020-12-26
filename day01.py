frequency = 0
seen = set()
seen.add(frequency)
found = False
first_round = True

while not found:
    for line in open("input/01.txt"):
        prev_len = len(seen)
        frequency = eval(str(frequency) + line)
        seen.add(frequency)
        if prev_len == len(seen):
            print(frequency)
            found = True
            break

    if first_round:
        print(frequency)
        first_round = False
