from timeit import default_timer as timer


def addr(registers, a, b, c):
    registers[c] = registers[a] + registers[b]


def addi(registers, a, b, c):
    registers[c] = registers[a] + b


def mulr(registers, a, b, c):
    registers[c] = registers[a] * registers[b]


def muli(registers, a, b, c):
    registers[c] = registers[a] * b


def banr(registers, a, b, c):
    registers[c] = registers[a] & registers[b]


def bani(registers, a, b, c):
    registers[c] = registers[a] & b


def borr(registers, a, b, c):
    registers[c] = registers[a] | registers[b]


def bori(registers, a, b, c):
    registers[c] = registers[a] | b


def setr(registers, a, b, c):
    registers[c] = registers[a]


def seti(registers, a, b, c):
    registers[c] = a


def gtir(registers, a, b, c):
    registers[c] = 1 if a > registers[b] else 0


def gtri(registers, a, b, c):
    registers[c] = 1 if registers[a] > b else 0


def gtrr(registers, a, b, c):
    registers[c] = 1 if registers[a] > registers[b] else 0


def eqir(registers, a, b, c):
    registers[c] = 1 if a == registers[b] else 0


def eqri(registers, a, b, c):
    registers[c] = 1 if registers[a] == b else 0


def eqrr(registers, a, b, c):
    registers[c] = 1 if registers[a] == registers[b] else 0


start = timer()
lines = [line.strip() for line in open("input/21.txt")]

bound_register = int(lines[0].split(" ")[1])
instructions = []
for line in lines[1:]:
    command, a, b, c = line.split(" ")
    instructions.append((command, int(a), int(b), int(c)))

registers = [0, 0, 0, 0, 0, 0]
ip = 0
seen = set()
first = None
last = None
while 0 <= ip < len(instructions):
    # Division to speed up program execution
    if ip == 18:
        e = registers[2] // 256
        registers[4] = e
    # Check for required value at the end of the loop
    if ip == 28:
        # First required value is solution for part A
        if first is None:
            first = registers[1]
        # Check if value has been seen already
        if registers[1] not in seen:
            seen.add(registers[1])
            last = registers[1]
        # Once value has been seen, code will be looping with same values, so previous value will be max
        else:
            break
    command, a, b, c = instructions[ip]
    registers[bound_register] = ip
    eval(command + "(registers, a, b, c)")
    ip = registers[bound_register] + 1

# Part A
print(first)

# Part B
print(last)
end = timer()
print(f'Took {end - start} seconds.')
