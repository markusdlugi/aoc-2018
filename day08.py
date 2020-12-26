def get_metadata(numbers, i):
    metadata = 0
    children_count, metadata_count = numbers[i:i + 2]
    i += 2
    for c in range(children_count):
        child_meta, i = get_metadata(numbers, i)
        metadata += child_meta
    metadata += sum(numbers[i:i + metadata_count])
    return metadata, i + metadata_count


def get_value(numbers, i):
    value = 0
    children_count, metadata_count = numbers[i:i + 2]
    i += 2
    if children_count == 0:
        value = sum(numbers[i:i + metadata_count])
    else:
        child_values = []
        for c in range(children_count):
            child_value, i = get_value(numbers, i)
            child_values.append(child_value)
        value += sum(child_values[meta - 1] for meta in numbers[i:i + metadata_count] if 0 < meta <= children_count)
    return value, i + metadata_count


numbers = list(map(int, open("input/08.txt").read().split()))

# Part A
print(get_metadata(numbers, 0)[0])

# Part B
print(get_value(numbers, 0)[0])
