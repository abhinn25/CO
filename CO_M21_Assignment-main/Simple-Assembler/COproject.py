OPcode = {"add": ("00000", "A"),
          "sub": ("00001", "A"),
          "mul": ("00110", "A"),
          "xor": ("01010", "A"),
          "or": ("01011", "A"),
          "and": ("01100", "A"),
          "movimi": ("00010", "B"),
          "movreg": ("00011", "C"),
          "div": ("00111", "C"),
          "not": ("01101", "C"),
          "cmp": ("01110", "C"),
          "ld": ("00100", "D"),
          "st": ("00101", "D"),
          "jmp": ("01111", "E"),
          "jgt": ("10001", "E"),
          "je": ("10010", "E"),
          "jlt": ("10000", "E"),
          "hlt": ("10011", "F"),
          }

registers = {"R0": ["000", -10],
             "R1": ["001", -10],
             "R2": ["010", -10],
             "R3": ["011", -10],
             "R4": ["100", -10],
             "R5": ["101", -10],
             "R6": ["110", -10],
             "FLAGS": ["111", [0, 0, 0, 0]]  # V / L / G / E
             }

f2 = open("output.txt", "w+")

def addition(reg1, reg2, reg3):
    if registers[reg2][1] + registers[reg3][1] > 255:
        registers[reg1][1] = 0
        registers["flag"][1][0] = 1
    else:
        registers[reg1][1] = registers[reg2][1] + registers[reg3][1]


def subtraction(reg1, reg2, reg3):
    if registers[reg2][1] - registers[reg3][1] < 0:
        registers[reg1][1] = 0
        registers["flag"][1][0] = 1
    else:
        registers[reg1][1] = registers[reg2][1] - registers[reg3][1]


def multiply(reg1, reg2, reg3):
    if registers[reg2][1] * registers[reg3][1] > 255:
        registers[reg1][1] = 0
        registers["flag"][1][0] = 1
    else:
        registers[reg1][1] = registers[reg2][1] * registers[reg3][1]


def divide(reg3, reg4):
    registers["R0"][1] = registers[reg3][1] / registers[reg4][1]
    registers["R1"][1] = registers[reg3][1] % registers[reg4][1]


def right_shift(reg1, Imm):
    registers[reg1][1] = registers[reg1][1] >> Imm


def left_shift(reg1, Imm):
    registers[reg1][1] = registers[reg1][1] << Imm


def Or(reg1, reg2, reg3):
    registers[reg1][1] = registers[reg2][1] | registers[reg3][1]


def And(reg1, reg2, reg3):
    registers[reg1][1] = registers[reg2][1] & registers[reg3][1]


def Xor(reg1, reg2, reg3):
    registers[reg1][1] = registers[reg2][1] ^ registers[reg3][1]


def Invert(reg1, reg2):
    registers[reg1][1] = ~registers[reg2][2]


f = open("input.txt", "r")
lines = [line.rstrip().split() for line in f]

final_input = []

label_list = []  # stores label with its memory address. example - ["label:" ,"11"]
var_list=[]
temp_var_list = []  # stores variable instructions
program_counter = 0
for inst in lines:
    if inst != []:

        if (inst[0] == "var"):
            temp_var_list.append(inst)
            continue
        if(inst[0][-1] ==':'):
            label_list.append([inst[0], program_counter])
            final_input.append(inst)
            program_counter += 1
        else:
            final_input.append(inst)
            program_counter += 1
final_input.extend(temp_var_list)


for i in (range(len(final_input))):
     if final_input[i][0] == "var":
            final_input[i].append(i)
            var_list.append(final_input[i])

#f2.write(var_list)
#f2.write(label_list)
#f2.write(final_input)

for inst in final_input:
    if inst[0] == "add":
        f2.write(OPcode["add"][0] + "00" +registers[inst[1]][0] + registers[inst[2]][0] + registers[inst[3]][0])
        f2.write("\n")

    elif inst[0] == "sub":
        f2.write(OPcode["sub"][0] + "00" +registers[inst[1]][0] + registers[inst[2]][0] + registers[inst[3]][0])
        f2.write("\n")

    elif inst[0] == "mul":
        f2.write(OPcode["mul"][0] + "00" +registers[inst[1]][0] + registers[inst[2]][0] + registers[inst[3]][0])
        f2.write("\n")

    elif inst[0] == "xor":
        f2.write(OPcode["xor"][0] + "00" +registers[inst[1]][0] + registers[inst[2]][0] + registers[inst[3]][0])
        f2.write("\n")

    elif inst[0] == "or":
        f2.write(OPcode["or"][0] + "00" +registers[inst[1]][0] + registers[inst[2]][0] + registers[inst[3]][0])
        f2.write("\n")

    elif inst[0] == "and":
        f2.write(OPcode["and"][0] + "00" +registers[inst[1]][0] + registers[inst[2]][0] + registers[inst[3]][0])
        f2.write("\n")

    elif inst[0] == "div":
        f2.write(OPcode["div"][0] + "00000" +registers[inst[1]][0] + registers[inst[2]][0])
        f2.write("\n")

    elif inst[0] == "not":
        f2.write(OPcode["not"][0] + "00000" +registers[inst[1]][0] + registers[inst[2]][0])
        f2.write("\n")

    elif inst[0] == "cmp":
        f2.write(OPcode["cmp"][0] + "00000" +registers[inst[1]][0] + registers[inst[2]][0])
        f2.write("\n")

    elif inst[0] == "ls":
        value = int((inst[2])[1:])
        s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]

        f2.write(OPcode["ls"][0] + registers[inst[1]][0]+s +"gg")
        f2.write("\n")

    elif inst[0] == "rs":
        value = int((inst[2])[1:])
        s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]

        f2.write(OPcode["rs"][0] + registers[inst[1]][0]+s + "gg")
        f2.write("\n")

    elif inst[0] == "ld":
        varname = inst[2]
        value = None
        for temp in var_list:
            if temp[1] == varname:
                value = temp[2]

        s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]

        f2.write(OPcode["ld"][0] + registers[inst[1]][0]+s)
        f2.write("\n")

    elif inst[0] == "st":
        varname = inst[2]
        value = None
        for temp in var_list:
            if temp[1] == varname:
                value = temp[2]

        s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]

        f2.write(OPcode["st"][0] + registers[inst[1]][0]+s)
        f2.write("\n")

    elif inst[0] == "jmp:":
        labelname = inst[1] + ":"
        value = None
        for temp in label_list:
            if temp[0] == labelname:
                value = temp[1]

        s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]

        f2.write(OPcode["jmp"][0] + "000" + s)
        f2.write("\n")

    elif inst[0] == "jlt:":
        labelname = inst[1] + ":"
        value = None
        for temp in label_list:
            if temp[0] == labelname:
                value = temp[1]

        s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]

        f2.write(OPcode["jlt"][0] + "000" + s)
        f2.write("\n")

    elif inst[0] == "jgt:":
        labelname = inst[1] + ":"
        value = None
        for temp in label_list:
            if temp[0] == labelname:
                value = temp[1]

        s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]

        f2.write(OPcode["jgt"][0] + "000" + s)
        f2.write("\n")

    elif inst[0] == "je:":
        labelname = inst[1]+":"
        value = None
        for temp in label_list:
            if temp[0] == labelname:
                value = temp[1]

        s = "0" * (8-len(bin(value)[2:])) + bin(value)[2:]

        f2.write(OPcode["je"][0] + "000" + s)
        f2.write("\n")

    elif inst[0]=="hlt":
        f2.write(OPcode["hlt"][0]+"00000000000")
        f2.write("\n")

    elif inst[0] == "mov":
        if inst[2][0] == "$":
            value = int((inst[2])[1:])
            s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]
            f2.write(OPcode["movimi"][0] + registers[inst[1]][0] + s)
            f2.write("\n")

        else:
            f2.write(OPcode["movreg"][0] +"00000"+ registers[inst[1]][0] + registers[inst[2]][0])
            f2.write("\n")
