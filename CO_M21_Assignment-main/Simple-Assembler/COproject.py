OPcode = {"add":    ("00000", "A"),
          "sub":    ("00001", "A"),
          "mul":    ("00110", "A"),
          "xor":    ("01010", "A"),
          "or":     ("01011", "A"),
          "and":    ("01100", "A"),
          "movimi": ("00010", "B"),
          "movreg": ("00011", "C"),
          "div":    ("00111", "C"),
          "not":    ("01101", "C"),
          "cmp":    ("01110", "C"),
          "ld":     ("00100", "D"),
          "st":     ("00101", "D"),
          "jmp":    ("01111", "E"),
          "jgt":    ("10001", "E"),
          "je":     ("10010", "E"),
          "jlt":    ("10000", "E"),
          "hlt":    ("10011", "F"),
          }

registers = {"R0":   ["000", -10],
             "R1":   ["001", -10],
             "R2":   ["010", -10],
             "R3":   ["011", -10],
             "R4":   ["100", -10],
             "R5":   ["101", -10],
             "R6":   ["110", -10],
             "flag": ["111", [0, 0, 0, 0]]  # V / L / G / E
             }

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
    registers[reg1][1] = registers[reg1][1] <<Imm

def Or (reg1, reg2, reg3):
    registers[reg1][1] = registers[reg2][1]|registers[reg2][1]
def And(reg1,reg2,reg3):
    registers[reg1][1] = registers[reg2][1]&registers[reg2][1]
def Xor(reg1,reg2,reg3):
    registers[reg1][1] = registers[reg2][1]^registers[reg2][1]
    

def Invert (reg1, reg2,):
    registers[reg1][1] = ~registers[reg2][2]

f = open("input.txt", "r")
lines = [line.rstrip().split() for line in f]
print(lines)
final_input=[]

label_list=[]       # stores label with its memory address. example - ["label:" ,"11"]

var_list=[]         # stores variable instructions
program_counter=0
for inst in lines:
    if inst!=[]:

        if(inst[0]=="var"):
            var_list.append(inst)
            continue
        if(inst[0][-1]==':'):
            label_list.append([inst[0],program_counter])
            final_input.append(inst)
            program_counter+=1
        else:
            final_input.append(inst)
            program_counter+=1

final_input.extend(var_list)

print(label_list)
print(final_input)

for inst in final_input:
    if inst[0]== "add":
        addition(inst[1], inst[2], inst[3])
    elif inst[0]== "sub":
        subtraction(inst[1], inst[2], inst[3])
    elif inst[0]== "mul":
        multiply(inst[1], inst[2], inst[3])
    elif
