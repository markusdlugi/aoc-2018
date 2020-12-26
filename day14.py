from timeit import default_timer as timer

puzzle_input = '320851'

recipes = '37'
current_a, current_b = (0, 1)
count = 10
index = None

start = timer()
while len(recipes) < int(puzzle_input) + count or index is None:
    # Add new recipes
    score_a, score_b = (int(recipes[current_a]), int(recipes[current_b]))
    recipes += str(score_a + score_b)

    # Check if input is already in recipes
    if index is None:
        if recipes[-len(puzzle_input):] == puzzle_input:
            index = len(recipes) - len(puzzle_input)
        elif recipes[-len(puzzle_input) - 1:-1] == puzzle_input:
            index = len(recipes) - len(puzzle_input) - 1

    # Change current recipes
    current_a, current_b = ((current_a + 1 + score_a) % len(recipes), (current_b + 1 + score_b) % len(recipes))

print(recipes[int(puzzle_input):int(puzzle_input) + count])
print(index)
end = timer()
print(f'Took {end - start} seconds.')
