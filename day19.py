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


def execute_program(instructions, registers, bound_register, stop_ip):
    ip = 0
    while 0 <= ip < len(instructions):
        command, a, b, c = instructions[ip]
        if ip == stop_ip:
            return registers[2]
        registers[bound_register] = ip
        eval(command + "(registers, a, b, c)")
        ip = registers[bound_register] + 1


def sum_of_divisors(number):
    return sum(i for i in range(1, number // 2) if number % i == 0) + number


lines = [line.strip() for line in open("input/19.txt")]
bound_register = int(lines[0].split(" ")[1])

instructions = []
for line in lines[1:]:
    command, a, b, c = line.split(" ")
    instructions.append((command, int(a), int(b), int(c)))

# Part A
registers = [0, 0, 0, 0, 0, 0]
number = execute_program(instructions, registers, bound_register, 3)
print(sum_of_divisors(number))

# Part B
registers = [1, 0, 0, 0, 0, 0]
number = execute_program(instructions, registers, bound_register, 3)
print(sum_of_divisors(number))
