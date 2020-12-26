import re
from collections import namedtuple
from copy import deepcopy

with open("input/24.txt") as field:
    sections = [section.splitlines() for section in field.read().split("\n\n")]

immune = sections[0][1:]
infection = sections[1][1:]

Group = namedtuple("Group", "id army units hp weakness immunity atk atk_type init")
gid = 0


def parse_input(army, immune):
    global gid
    for group in army:
        units, hp, weak_immune, atk, atk_type, init = re.findall(
            r"(\d+) units each with (\d+) hit points (?:\(([^)]*)\) )?with an attack that does (\d+) (\w+) " +
            r"damage at initiative (\d+)", group)[0]
        weakness = set()
        immunity = set()
        if weak_immune:
            for section in weak_immune.split("; "):
                if section.startswith("weak to "):
                    types = section[len("weak to "):]
                    weakness.update(types.split(", "))
                elif section.startswith("immune to "):
                    types = section[len("immune to "):]
                    immunity.update(types.split(", "))
                else:
                    assert False
        yield gid, Group(gid, "immune" if immune else "infection", int(units), int(hp), weakness, immunity, int(atk), atk_type, int(init))
        gid += 1


groups = dict()
for k, v in parse_input(immune, True):
    groups[k] = v
for k, v in parse_input(infection, False):
    groups[k] = v


def select_targets(groups):
    targets = dict()
    sorted_groups = [x[0] for x in sorted(groups.items(), key=lambda x: (x[1].units * x[1].atk, x[1].init), reverse=True)]
    for gid in sorted_groups:
        group = groups[gid]
        power = group.units * group.atk
        dmg = dict()
        for other in groups.values():
            if other.id == group.id or other.army == group.army or other.id in targets.values() or group.atk_type in other.immunity:
                continue
            dmg[other.id] = (2 * power if group.atk_type in other.weakness else power, other.units * other.atk, other.init)
        if dmg:
            targets[group.id] = max(dmg.items(), key=lambda x: x[1])[0]
    return targets


def attack(groups, targets):
    sorted_groups = [x[0] for x in sorted(groups.items(), key=lambda x: (x[1].init), reverse=True)]
    for gid in sorted_groups:
        if gid not in groups:
            continue
        group = groups[gid]
        if group.units <= 0 or group.id not in targets:
            continue
        other = groups[targets[group.id]]
        power = group.units * group.atk
        dmg = 0 if group.atk_type in other.immunity else 2 * power if group.atk_type in other.weakness else power
        lost_units = (dmg // other.hp)
        new_units = other.units - lost_units
        del groups[other.id]
        if new_units > 0:
            groups[other.id] = Group(other.id, other.army, new_units, other.hp, other.weakness, other.immunity, other.atk, other.atk_type, other.init)


original_groups = deepcopy(groups)
winner = None
boost = 0
while winner is None or winner == "infection":
    groups = deepcopy(original_groups)

    for gid, group in groups.items():
        if group.army == "immune":
            groups[gid] = Group(group.id, group.army, group.units, group.hp, group.weakness, group.immunity, group.atk + boost, group.atk_type, group.init)

    immune_count = sum(group.units for group in groups.values() if group.army == "immune")
    infection_count = sum(group.units for group in groups.values() if group.army == "infection")
    tie = False
    while immune_count > 0 and infection_count > 0:
        targets = select_targets(groups)
        attack(groups, targets)
        new_immune_count = sum(group.units for group in groups.values() if group.army == "immune")
        new_infection_count = sum(group.units for group in groups.values() if group.army == "infection")
        if new_immune_count == immune_count and new_infection_count == infection_count:
            tie = True
            break
        else:
            immune_count = new_immune_count
            infection_count = new_infection_count

    winner = next(iter(groups.values())).army if not tie else None
    if boost == 0:
        print(sum(x.units for x in groups.values()))
    boost += 1

print(sum(x.units for x in groups.values()))