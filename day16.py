from collections import defaultdict


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


commands = ["addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori", "setr", "seti", "gtir", "gtri", "gtrr",
           "eqir", "eqri", "eqrr"]

lines = [line.strip() for line in open("input/16.txt")]

# Read all instructions in first part of input
instructions = []
i = 0
while i < len(lines):
    if lines[i] == '':
        break
    before = list(map(int, lines[i].split('[')[1][0:-1].split(', ')))
    after = list(map(int, lines[i + 2].split('[')[1][0:-1].split(', ')))
    instruction = list(map(int, lines[i + 1].split(' ')))
    instructions.append((instruction, before, after))
    i += 4
i += 2

# Create options for each opcode by trying out all possible commands
opcode_options = defaultdict(set)
result_a = 0
for instruction, before, after in instructions:
    option_count = 0
    for op in commands:
        current_opcode, a, b, c = instruction
        registers = before.copy()
        command = op + "(registers, a, b, c)"
        eval(command)
        if registers == after:
            option_count += 1
            opcode_options[current_opcode].add(op)
    if option_count >= 3:
        result_a += 1

print(result_a)

# Find out actual mapping from opcode to command
opcode_dict = dict()
while len(opcode_dict) < len(commands):
    found = None
    for opcode, option_count in opcode_options.items():
        if len(option_count) == 1:
            command = list(option_count)[0]
            opcode_dict[opcode] = command
            found = command
            break
    if found is not None:
        for opcode, option_count in opcode_options.items():
            if found in option_count:
                option_count.remove(found)
#print(opcode_dict)

# Execute script in second part of input
registers = [0, 0, 0, 0]
while i < len(lines):
    opcode, a, b, c = list(map(int, lines[i].split(" ")))
    command = opcode_dict[opcode] + "(registers, a, b, c)"
    eval(command)
    i += 1
print(registers[0])
