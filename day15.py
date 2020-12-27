import heapq
from collections import deque
from copy import deepcopy

cavern = set()
units = dict()
original_units = dict()
size = 0


class Unit:

    def __init__(self, elf, atk, hp):
        self.elf = elf
        self.atk = atk
        self.hp = hp


def moves(x, y, check_collisions):
    # Up, left, right, down to enforce "reading order"
    dx, dy = ((0, -1, 1, 0), (-1, 0, 0, 1))
    result = []
    for i in range(4):
        xx, yy = (x + dx[i], y + dy[i])
        if (xx, yy) in cavern and (not check_collisions or (xx, yy) not in units):
            result.append((xx, yy))
    return result


def sort_by_reading_order(positions):
    positions.sort(key=lambda x: (x[1], x[0]))


def get_targets(elf):
    return list(filter(lambda x: units[x].elf != elf, list(units.keys())))


def get_in_range_squares(targets):
    squares = set()
    for x, y in targets:
        squares.update(moves(x, y, True))
    return squares


def get_nearest_reachable_squares(x, y, squares):
    visited = set()
    q = deque()
    q.append((x, y, 0))
    result = []
    distance = None
    while q:
        x, y, dist = q.popleft()
        if (x, y) in squares:
            if distance is None or dist < distance:
                distance = dist
                result.clear()
                result.append((x, y))
            elif distance is not None and dist == distance:
                result.append((x, y))
            elif distance is not None and dist > distance:
                break
        for m in moves(x, y, True):
            if m not in visited:
                visited.add(m)
                q.append((*m, dist + 1))
    return result


def is_in_range_of_target(x, y, targets):
    for target in targets:
        if (x, y) in moves(*target, False):
            return True
    return False


def get_targets_in_range(elf, x, y):
    targets = get_targets(elf)
    targets_in_range = list(filter(lambda target: (x, y) in moves(*target, False), targets))
    min_hp = None
    min_hp_units = []
    for target in targets_in_range:
        unit = units[target]
        if min_hp is None or unit.hp < min_hp:
            min_hp = unit.hp
            min_hp_units = [target]
        elif unit.hp == min_hp:
            min_hp_units.append(target)
    sort_by_reading_order(min_hp_units)
    return min_hp_units


def dist(x, y, xx, yy):
    return abs(xx - x) + abs(yy - y)


def compute_path(x, y, target):
    if not target or (x, y) == target:
        return None

    old_x, old_y = (x, y)
    min_path = None
    min_path_length = None
    for (x, y) in moves(x, y, True):
        result = None
        visited = set()
        visited.add((old_x, old_y))
        visited.add((x, y))
        q = []
        heapq.heappush(q, (dist(x, y, *target), x, y, [(x, y)]))
        while q:
            _, xx, yy, path = heapq.heappop(q)
            if (xx, yy) == target:
                result = path
                break
            for m in moves(xx, yy, True):
                if m not in visited:
                    visited.add(m)
                    new_path = path.copy()
                    new_path.append(m)
                    heapq.heappush(q, (len(new_path) + dist(*m, *target), *m, new_path))
        if result is not None:
            if min_path_length is None or len(result) < min_path_length:
                min_path_length = len(result)
                min_path = result

    if min_path is not None:
        return min_path
    return None


def perform_turn(x, y, unit, elf_death_unacceptable):
    targets = get_targets(unit.elf)
    if len(targets) == 0:
        return False
    if not is_in_range_of_target(x, y, targets):
        squares = get_nearest_reachable_squares(x, y, get_in_range_squares(targets))
        if squares:
            sort_by_reading_order(squares)
            path = compute_path(x, y, squares[0])
            if path is not None:
                del units[(x, y)]
                x, y = path[0]
                units[(x, y)] = unit
    if is_in_range_of_target(x, y, targets):
        victim_pos = get_targets_in_range(unit.elf, x, y)[0]
        victim = units[victim_pos]
        attacker = units[(x, y)]
        victim.hp -= attacker.atk
        if victim.hp <= 0:
            del units[victim_pos]
            if victim.elf and elf_death_unacceptable:
                return False
    return True


def show():
    for y in range(size + 1):
        for x in range(size + 1):
            c = "G" if (x, y) in units and not units[(x, y)].elf else "E" if (x, y) in units and units[(x, y)].elf \
                else "." if (x, y) in cavern else "#"
            print(c, sep='', end='')
        print()
    print()


def combat(atk, elf_death_unacceptable):
    for pos, unit in units.items():
        units[pos].atk = atk if unit.elf else 3
    turn = 0
    continue_combat = True
    while continue_combat:
        unit_positions = list(units.keys())
        sort_by_reading_order(unit_positions)
        for pos in unit_positions:
            if pos not in units:
                continue
            continue_combat = perform_turn(*pos, units[pos], elf_death_unacceptable)
            if not continue_combat:
                break
        else:
            turn += 1

    if elf_death_unacceptable:
        original_elf_count = len(list(filter(lambda x: x.elf, original_units.values())))
        elf_count = len(list(filter(lambda x: x.elf, units.values())))
        if elf_count < original_elf_count:
            #print(f'An elf dies with {atk} attack power.')
            return False
    hp_sum = 0
    elves = False
    for unit in units.values():
        hp_sum += unit.hp
        elves = unit.elf
    #print(f'Combat ends after {turn} full rounds with elf attack power {atk}')
    #print(f'{"Elves" if elves else "Goblins"} win with {hp_sum} total hit points left')
    #print(f'Outcome: {turn} * {hp_sum} = {turn * hp_sum}')
    print(f"{turn * hp_sum}")
    return True


for y, line in enumerate(open("input/15.txt")):
    for x, c in enumerate(line):
        if c == ".":
            cavern.add((x, y))
        elif c == "G":
            cavern.add((x, y))
            units[(x, y)] = Unit(False, 3, 200)
        elif c == "E":
            cavern.add((x, y))
            units[(x, y)] = Unit(True, 3, 200)
    size = y

original_units = deepcopy(units)

# Part A
combat(3, False)

# Part B
found = False
atk = 3
while not found:
    atk += 1
    units = deepcopy(original_units)
    found = combat(atk, True)
