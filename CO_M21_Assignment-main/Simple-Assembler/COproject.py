OPcode = {"add": ("00000", "A"),
          "sub": ("00001", "A"),
          "mul": ("00110", "A"),
          "xor": ("01010", "A"),
          "or": ("01011", "A"),
          "and": ("01100", "A"),
          "rs": ("01000", "B"),
          "ls": ("01001", "B"),
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

register_wo_flag = {"R0": ["000", -10],
                    "R1": ["001", -10],
                    "R2": ["010", -10],
                    "R3": ["011", -10],
                    "R4": ["100", -10],
                    "R5": ["101", -10],
                    "R6": ["110", -10],
                    }


f2 = open("output.txt", "w+")

def errorlno(lno):
    for i in range(len(lines2)):
        if lines2[i] == lines[lno]:
            return i+1

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

def halt_checker(lis):
    flag = 0
    for j in range(len(lis)):
        if "hlt" in lis[j]:
            if(flag==0):
                lno = j
            flag += 1

    if flag == 0:
        print("hlt missing")
        return False
    elif(flag == 1):
        if lis[-1][-1] == "hlt":
            return True
        else:
            print("hlt before termination" , errorlno(lno))
            return False
    else:
        print("hlt before termination" , errorlno(lno))
        return False


def var_checker(lis):
    flag = 0
    count = 0

    if(lis[0][0] == "var"):

        for i in range(len(lis)):
            if lis[i][0] == "var"  and len(lis[i]) == 3 and lis[i][1] in OPcode.keys() :
                print("inst error" , errorlno(i))
                return False
            if(lis[i][0] == "var" ):
                count += 1

        continous_var=0
        j=0
        while j <len(lis)-1 and (lis[j][0] == lis[j + 1][0]) and lis[j][0] == "var":
            j+=1
            continous_var+=1
        continous_var+=1


        if(continous_var!=count):

            for t1 in range(j+1 , len(lis)):
                if (lis[t1][0] == "var"):
                    lno = t1
                    break
            print("var discont" , errorlno(t1))
            return False
    else:
        for i in range(len(lis)):
            if(lis[i][0]=="var"):
                print("var beech me h" , errorlno(i))
                return False




def errorA(lisa, lno):
    if len(lisa) == 4:
        if lisa[1] in register_wo_flag.keys() and lisa[2] in register_wo_flag.keys() and lisa[3] in register_wo_flag.keys():
            return True
        else:
            print("register name error", errorlno(lno))
            return False
    else:
        print("wrong syntax error", errorlno(lno))
        return False


def errorB(lisb, lno):
    if len(lisb) == 3:
        if lisb[1] in register_wo_flag.keys() and lisb[2][0] == "$" and lisb[2][1:].isnumeric() and 0 <= int(lisb[2][1:]) <= 255:
            return True
        elif(lisb[2][1:].isnumeric() == False):
            print("syntax error" , errorlno(lno))
            return False

        elif int(lisb[2][1:])<0 or int(lisb[2][1:])>255:
            print("IMMEDIATE out of range",errorlno(lno))
            return False
        else:
            print("register name error", errorlno(lno))
            return False

    else:
        print("wrong syntax error", errorlno(lno))
        return False


def errorC(lisa, lno):
    if len(lisa) == 3:
        if lisa[1] in register_wo_flag.keys() and lisa[2] in register_wo_flag.keys():
            return True
        else:
            print("register name error", errorlno(lno))
            return False
    else:
        print("wrong syntax error", errorlno(lno))
        return False


def errorD(lisd, lno):
    if len(lisd) == 3:
        if lisd[1] in register_wo_flag.keys() and lisd[2] in var_dic.keys():
            return True
        elif lisd[1] not in register_wo_flag.keys():
             print("register error", errorlno(lno))
             return False
        elif lisd[1] in register_wo_flag.keys() and lisd[2]+":" in label_dic.keys():
            print("misuse of label as variable ", errorlno(lno))
            return False
        else:
            print("use of un defined variable" , errorlno(lno) )
            return False

    else:
        print("wrong syntax error", errorlno(lno) )
        return False


def errorE(lise, lno):
    if len(lise) == 2:
        if lise[1] in label_dic:
            return True
        else:
            print("Use of undefined label ", errorlno(lno) )
            return False
    else:
        print("wrong syntax error", errorlno(lno) )
        return False


def error(lis):

    if var_checker(lis) == False:
        return False

    for i in range(len(lis)):
        ins = lis[i]
        if ins[0] == "mov":
            if len(ins) == 3:
                if ins[1] in register_wo_flag.keys() and (ins[2] in registers.keys() or (ins[2][0] == "$" and 0 <= int(ins[2][1:]) <= 255)):
                   continue # have to deal intermeditae error here

                else:
                    print("register name error", errorlno(i) )

                    return False

            else:
                print("wrong syntax error", errorlno(i))

                return False

        if ins[0][-1] == ":":

            if len(ins) == 1:
                print("invalid ins")
                return False

            if ins[1] in OPcode.keys():
                if OPcode[ins[1]][1] == "A":

                    if errorA(ins[1:], i) == False:
                        return False
                elif OPcode[ins[1]][1] == "B":
                    if errorB(ins[1:], i) == False:
                        return False
                elif OPcode[ins[1]][1] == "C":
                    if errorC(ins[1:], i) == False:
                        return False
                elif OPcode[ins[1]][1] == "D":
                    if errorD(ins[1:], i) == False:
                        return False
                elif OPcode[ins[1]][1] == "E":
                    if errorE(ins[1:], i) == False:
                        return False
            elif(ins[1] != "var"):
                print("type a typo in inst" , errorlno(i))
                return False

        elif ins[0] in OPcode.keys():
            if OPcode[ins[0]][1] == "A":
                if errorA(ins, i) == False:
                    return False
            elif OPcode[ins[0]][1] == "B":
                if errorB(ins, i) == False:
                    return False
            elif OPcode[ins[0]][1] == "C":
                if errorC(ins, i) == False:
                    return False
            elif OPcode[ins[0]][1] == "D":
                if errorD(ins, i) == False:
                    return False
            elif OPcode[ins[0]][1] == "E":
                if errorE(ins, i) == False:
                    return False
        # elif OPcode[ins[0]][1] == "F":
        #   errorF(ins)
        elif(ins[0] != "var"):
            print("type a typo in inst", errorlno(i))
            return False
    if halt_checker(lis) == False:
        return False
    var_checker(lis)
    return True




f = open("input.txt", "r")
lines = []
lines2 = [line.rstrip().split() for line in f]

for i in lines2:
    if i!=[]:
        lines.append(i)

final_input = []
label_list = []  # stores label with its memory address. example - ["label:" ,"11"]
label_dic = {}
var_dic = {}
var_list = []
temp_var_list = []  # stores variable instructions
program_counter = 0


for inst in lines:
        if (inst[0] == "var"):
                temp_var_list.append(inst)
                continue
        if (inst[0][-1] == ':'):
                label_dic[inst[0]] = program_counter
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
            var_dic[final_input[i][1]] = i
            var_list.append(final_input[i])


print(lines)
print(lines2)
if error(lines) == True:
    for inst in final_input:

        if inst[0] == "add":
            print(OPcode["add"][0] + "00" + registers[inst[1]][0] + registers[inst[2]][0] + registers[inst[3]][0])

        elif inst[0] == "sub":
            print(OPcode["sub"][0] + "00" + registers[inst[1]][0] + registers[inst[2]][0] + registers[inst[3]][0])

        elif inst[0] == "mul":
            print(OPcode["mul"][0] + "00" + registers[inst[1]][0] + registers[inst[2]][0] + registers[inst[3]][0])

        elif inst[0] == "xor":
            print(OPcode["xor"][0] + "00" + registers[inst[1]][0] + registers[inst[2]][0] + registers[inst[3]][0])

        elif inst[0] == "or":
            print(OPcode["or"][0] + "00" + registers[inst[1]][0] + registers[inst[2]][0] + registers[inst[3]][0])

        elif inst[0] == "and":
            print(OPcode["and"][0] + "00" + registers[inst[1]][0] + registers[inst[2]][0] + registers[inst[3]][0])

        elif inst[0] == "div":
            print(OPcode["div"][0] + "00000" + registers[inst[1]][0] + registers[inst[2]][0])

        elif inst[0] == "not":
            print(OPcode["not"][0] + "00000" + registers[inst[1]][0] + registers[inst[2]][0])

        elif inst[0] == "cmp":
            print(OPcode["cmp"][0] + "00000" + registers[inst[1]][0] + registers[inst[2]][0])

        elif inst[0] == "ls":
            value = int((inst[2])[1:])
            s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]
            print(OPcode["ls"][0] + registers[inst[1]][0] + s + "gg")

        elif inst[0] == "rs":
            value = int((inst[2])[1:])
            s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]
            print(OPcode["rs"][0] + registers[inst[1]][0] + s + "gg")

        elif inst[0] == "ld":
            varname = inst[2]
            value = None
            for temp in var_list:
                if temp[1] == varname:
                    value = temp[2]
            s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]
            print(OPcode["ld"][0] + registers[inst[1]][0] + s)

        elif inst[0] == "st":
            varname = inst[2]
            value = None
            for temp in var_list:
                if temp[1] == varname:
                    value = temp[2]
            s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]
            print(OPcode["st"][0] + registers[inst[1]][0] + s)

        elif inst[0] == "jmp:":
            labelname = inst[1] + ":"
            value = None
            for temp in label_list:
                if temp[0] == labelname:
                    value = temp[1]
            s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]
            print(OPcode["jmp"][0] + "000" + s)

        elif inst[0] == "jlt:":
            labelname = inst[1] + ":"
            value = None
            for temp in label_list:
                if temp[0] == labelname:
                    value = temp[1]
            s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]
            print(OPcode["jlt"][0] + "000" + s)

        elif inst[0] == "jgt:":
            labelname = inst[1] + ":"
            value = None
            for temp in label_list:
                if temp[0] == labelname:
                    value = temp[1]
            s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]
            print(OPcode["jgt"][0] + "000" + s)

        elif inst[0] == "je:":
            labelname = inst[1] + ":"
            value = None
            for temp in label_list:
                if temp[0] == labelname:
                    value = temp[1]
            s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]
            print(OPcode["je"][0] + "000" + s)

        elif inst[0] == "hlt":
            print(OPcode["hlt"][0] + "00000000000")

        elif inst[0] == "mov":
            if inst[2][0] == "$":
                value = int((inst[2])[1:])
                s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]
                print(OPcode["movimi"][0] + registers[inst[1]][0] + s)

            else:
                print(OPcode["movreg"][0] + "00000" + registers[inst[1]][0] + registers[inst[2]][0])
