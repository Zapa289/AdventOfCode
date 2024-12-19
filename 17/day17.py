#!/usr/bin/python3
INPUT = """Register A: 105843716614554
Register B: 0
Register C: 0

Program: 2,4,1,5,7,5,1,6,0,3,4,0,5,5,3,0"""

TEST_INPUT ="""Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

def main():
    input = INPUT.replace("Register A: ", "").replace("Register B: ", "").replace("Register C: ","").replace("Program: ","").split("\n\n")

    registers:list[int] = [int(x) for x in input[0].split()]
    print(registers)

    # Out buffer

    registers.append([])

    program = [int(x) for x in input[1].split(",")]
    print(program)

    print(run_program(program, registers))

    # Part 2
    def run_cycle(value) -> list[int]:
        output = []
        a = value

        while a:
            b = a % 8
            b ^= 5
            c = a // 2**b
            b ^= 6
            a = a // 8
            b ^= c
            output.append(b % 8)

        return output


    valid_a = {0}

    for value in reversed(program):
        test_a = set()
        for test_value in valid_a:
            shifted = test_value * 8
            for test in range(shifted, shifted + 8):
                output = run_cycle(test)
                if output and output[0] == value:
                    test_a.add(test)

        valid_a = test_a

    print(min(valid_a))

def run_program(program, registers) -> list[int]:
    ip = 0
    while True:
        if ip >= len(program):
            print(f"End of Program")
            break

        opcode = program[ip]
        input = program[ip + 1]

        new_ip:int|None = OPCODES[opcode](input, registers, ip)

        if new_ip is not None:
            ip = new_ip
        else:
            ip += 2

    return registers[3]

def adv(combo:int, registers:list[int], _):
    divisor = 2 ** decode_combo(combo, registers)
    print(f"Op 0 ({combo}): A = A / 2**combo = {registers[0] // divisor}")
    registers[0] = registers[0] // divisor

    return None

def bxl(literal:int, registers, _):
    print(f"Op 1 (lit {literal}): B = B xor {literal} = {registers[1] ^ literal}")
    registers[1] = registers[1] ^ literal

    return None

def bst(combo, registers, _):
    value = decode_combo(combo, registers) % 8
    print(f"Op 2 ({combo}): B = combo mod 8 = {value % 8}")
    registers[1] = value

    return None

def jnz(literal:int, registers, _):
    if registers[0] == 0:
        return None

    print(f"Op 3: Jumping to {literal}")
    return literal

def bxc(input, registers, ip):
    print(f"Op 4: B = B xor C = {registers[1] ^ registers[2]}")
    registers[1] = registers[1] ^ registers[2]

    return None

def out(combo, registers, _):
    value = decode_combo(combo, registers) % 8
    print(f"Op 5 ({combo}): Append combo % 8 = {value} to out buffer")
    registers[3].append(value)

    return None

def bdv(combo, registers, _):
    divisor = 2 ** decode_combo(combo, registers)
    print(f"Op 6 ({combo}): B = A / 2**combo = {registers[0] // divisor}")
    registers[1] = registers[0] // divisor

    return None

def cdv(combo, registers, _):
    divisor = 2 ** decode_combo(combo, registers)
    print(f"Op 7 ({combo}): C = A / 2**combo = {registers[0] // divisor}")
    registers[2] = registers[0] // divisor

    return None

def decode_combo(combo: int, registers: list[int]) -> int:
    match combo:
        case 0 | 1 | 2 | 3:
            return combo
        case 4 | 5 | 6:
            return registers[combo - 4]
        case 7 | _:
            print("INVALID OPCODE")
            exit()

if __name__ == "__main__":
    OPCODES = {
    0 : adv,
    1 : bxl,
    2 : bst,
    3 : jnz,
    4 : bxc,
    5 : out,
    6 : bdv,
    7 : cdv
    }
    main()