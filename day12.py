def sum_pots(indices, plants):
    pot_sum = 0
    for i, p in enumerate(plants):
        if p == "#":
            pot_sum += indices[i]
    return pot_sum


lines = [line.strip() for line in open("input/12.txt")]

plants = lines[0].split(" ")[2]
rules = []
for line in lines[2:]:
    cond, result = line.split(" => ")
    # Drop rules which lead to plants dying
    if result == ".":
        continue
    rules.append((cond, result))

indices = []
for i in range(len(plants)):
    indices.append(i)

last_total = sum_pots(indices, plants)
last_diff = None
same_diff = 0
for gen in range(1, 500):
    # Ensure we have enough empty pots at start and beginning
    while not "".join(plants[:3]) == "...":
        indices.insert(0, indices[0] - 1)
        plants = "." + plants
    while not "".join(plants[-3:]) == "...":
        indices.append(indices[-1] + 1)
        plants += "."

    # Find pots which will grow plants
    grow = []
    for cond, result in rules:
        for i in range(len(plants)):
            snippet = plants[i - 2:i + 3]
            if snippet == cond:
                grow.append(i)

    # Reset plants
    plants = ""
    for i in range(len(indices)):
        plants += "."
    # Grow new plants
    for i in grow:
        plants = plants[:i] + "#" + plants[i+1:]

    # Compute pot sum and print if we are at 20 (part A)
    total = sum_pots(indices, plants)
    if gen == 20:
        print(total)

    # Compute diff and check if we have a repetition (part B)
    diff = total - last_total
    last_total = total

    if diff == last_diff:
        same_diff += 1
    else:
        same_diff = 0
        last_diff = diff

    # Extrapolate to 50 billion gens if we had 10 times the same value
    if same_diff == 10:
        target_gen = 50_000_000_000
        result = (target_gen - gen) * diff + total
        print(result)
        break
