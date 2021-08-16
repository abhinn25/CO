f = open("input.txt", "r")
lines = [line.rstrip() for line in f]
#print(lines)
OPcode = {"00000": ("add", "A"),
          "00001": ("sub", "A"),
          "00110": ("mul", "A"),
          "01010": ("xor", "A"),
          "01011": ("or", "A"),
          "01100": ("and", "A"),
          "01000": ("rs", "B"),
          "01001": ("ls", "B"),
          "00010": ("mov", "B"),
          "00011": ("mov", "C"),
          "00111": ("div", "C"),
          "01101": ("not", "C"),
          "01110": ("cmp", "C"),
          "00100": ("ld", "D"),
          "00101": ("st", "D"),
          "01111": ("jmp", "E"),
          "10001": ("jgt", "E"),
          "10010": ("je", "E"),
          "10000": ("jlt", "E"),
          "10011": ("hlt", "F"),
          }
registers = {"000": ["R0", 0],
             "001": ["R1", 0],
             "010": ["R2", 0],
             "011": ["R3", 0],
             "100": ["R4", 0],
             "101": ["R5", 0],
             "110": ["R6", 0],
             "111": ["FLAGS", [0, 0, 0, 0]]  # V / L / G / E
             }

PC = 0
mem = ["0000000000000000"]*256

for i in range(len(lines)):
        mem[i] = lines[i]

#print(registers)
#print(mem , len(mem))

def binaryToDecimal(n):
    return int(n,2)

def a_type(inst):

    if OPcode[instruction[0:5]][0] == "add":
        registers[inst[7:10]][1] = registers[inst[10:13]][1] + registers[inst[13:]][1]
        if registers[inst[7:10]][1] > 255:
            registers[inst[7:10]][1] = 0
            registers["111"][0] = 1

    elif OPcode[instruction[0:5]][0] == "sub":
        registers[inst[7:10]][1] = registers[inst[10:13]][1]-registers[inst[13:]][1]
        if registers[inst[7:10]][1] < 0:
            registers[inst[7:10]][1] = 0
            registers["111"][0] = 1

    elif OPcode[instruction[0:5]][0] == "mul":
        registers[inst[7:10]][1] = registers[inst[10:13]][1] * registers[inst[13:]][1]
        if registers[inst[7:10]][1] > 255:
            registers[inst[7:10]][1] = 0
            registers["111"][0] = 1

    elif OPcode[instruction[0:5]][0] == "or":
        registers[inst[7:10]][1] = registers[inst[10:13]][1] | registers[inst[13:]][1]


    elif OPcode[instruction[0:5]][0] == "and":
        registers[inst[7:10]][1] = registers[inst[10:13]][1] & registers[inst[13:]][1]

    elif OPcode[instruction[0:5]][0] == "xor":
        registers[inst[7:10]][1] = registers[inst[10:13]][1] ^ registers[inst[13:]][1]

def b_type(inst):
    if OPcode[instruction[0:5]][0] == "mov":
        registers[instruction[5:8]][1] = binaryToDecimal(instruction[8:])

    elif OPcode[instruction[0:5]][0] == "rs":
        registers[instruction[5:8]][1] = registers[instruction[5:8]][1]>>binaryToDecimal(instruction[8:])

    elif OPcode[instruction[0:5]][0] == "ls":
        registers[instruction[5:8]][1] = registers[instruction[5:8]][1]<<binaryToDecimal(instruction[8:])

def c_type(inst):
    if OPcode[instruction[0:5]][0] == "div":
        registers["R0"][1] = binaryToDecimal(instruction[10:13])/binaryToDecimal(instruction[13:])
        registers["R1"][1] = binaryToDecimal(instruction[10:13])%binaryToDecimal(instruction[13:])


    elif OPcode[instruction[0:5]][0] == "not":
        registers[instruction[10:13]][1] = ~binaryToDecimal(instruction[13:])

    elif OPcode[instruction[0:5]][0] == "cmp":
        registers[instruction[10:13]][1] = ~binaryToDecimal(instruction[13:])
        if registers[instruction[10:13]][1] > registers[instruction[13:]][1]:
            registers["FLAGS"][1][2]=1
        elif registers[instruction[10:13]][1] < registers[instruction[13:]][1]:
            registers["FLAGS"][1][2] = 1
        elif registers[instruction[10:13]][1] == registers[instruction[13:]][1]:
            registers["FLAGS"][1][3] = 1
    elif OPcode[instruction[0:5]][0] == "mov":
        registers[instruction[10:13]][1] = registers[instruction[13:]][1]
