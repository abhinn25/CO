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
def errorlno(lno):
    for i in range(len(lines2)):
        if lines2[i] == lines[lno]:
            return i+1

def halt_checker(lis):
    flag = 0
    for j in range(len(lis)):
        if "hlt" in lis[j]:
            if(flag==0):
                lno = j
            flag += 1

    if flag == 0:
        print("Error : hlt Statement Missing")
        return False
    elif(flag == 1):
        if lis[-1][-1] == "hlt":
            return True
        else:
            print("Error : hlt Before Termination in Line " , errorlno(lno))
            return False
    else:
        print("Error : hlt Before Termination in Line " , errorlno(lno))
        return False


def var_checker(lis):
    flag = 0
    count = 0
    for i in range(len(lis)):
        if lis[i][0] == "var" and len(lis[i]) != 3:
            print("Error : Syntax error",errorlno(i))
            return False

    if(lis[0][0] == "var"):

        for i in range(len(lis)):
            if lis[i][0] == "var"  and len(lis[i]) == 3 and lis[i][1] in OPcode.keys() :
                print("Error : Instruction name cannot be used as a variable " , errorlno(i))
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
            print("Error : Variable cannot be declared in Line " , errorlno(t1))
            return False
    else:
        for i in range(len(lis)):
            if(lis[i][0]=="var"):
                print("Error : Variable cannot be declared in Line " , errorlno(i))
                return False


def errorA(lisa, lno):
    if len(lisa) == 4:
        if lisa[1] in register_wo_flag.keys() and lisa[2] in register_wo_flag.keys() and lisa[3] in register_wo_flag.keys():
            return True
        else:
            print("Error : Register name is incorrect in Line ", errorlno(lno))
            return False
    else:
        print("Error : Wrong Syntax in Line ", errorlno(lno))
        return False

def errorB(lisb, lno):
    if len(lisb) == 3:
        if lisb[1] in register_wo_flag.keys() and lisb[2][0] == "$" and lisb[2][1:].isnumeric() and 0 <= int(lisb[2][1:]) <= 255:
            return True
        elif(lisb[2][1:].isnumeric() == False):
            print("Error : Wrong Syntax in Line " , errorlno(lno))
            return False

        elif int(lisb[2][1:])<0 or int(lisb[2][1:])>255:
            print("Error : Value of Immediate is out of range in Line ",errorlno(lno))
            return False
        else:
            print("Error : Register name is incorrect in Line ", errorlno(lno))
            return False

    else:
        print("Error : Wrong Syntax in Line ", errorlno(lno))
        return False


def errorC(lisa, lno):
    if len(lisa) == 3:
        if lisa[1] in register_wo_flag.keys() and lisa[2] in register_wo_flag.keys():
            return True
        else:
            print("Error : Register name is incorrect in Line ", errorlno(lno))
            return False
    else:
        print("Error : Wrong Syntax in Line ", errorlno(lno))
        return False


def errorD(lisd, lno):
    if len(lisd) == 3:
        if lisd[1] in register_wo_flag.keys() and lisd[2] in var_dic.keys():
            return True
        elif lisd[1] not in register_wo_flag.keys():
             print("Error : Register name is incorrect in Line ", errorlno(lno))
             return False
        elif lisd[1] in register_wo_flag.keys() and lisd[2]+":" in label_dic.keys():
            print("Error : Misuse of label as variable in Line ", errorlno(lno))
            return False
        else:
            print("Error : Use of undefined variable in Line " , errorlno(lno) )
            return False
    else:
        print("Error : Wrong Syntax in Line ", errorlno(lno) )
        return False


def errorE(lise, lno):
    if len(lise) == 2:
        if (lise[1]+ ":") in label_dic:
            return True
        elif lise[1]+":" not in label_dic.keys() and lise[1] in var_dic:
            print("Error : Misuse of variable as label in Line ", errorlno(lno))
            return False
        else:
            print("Error : Use of undefined label in Line ", errorlno(lno) )
            return False
    else:
        print("Error : Wrong Syntax in Line ", errorlno(lno) )
        return False


def error(lis):
    if lis==[]:
        print("Error : Input file empty ")
        return False

    if var_checker(lis) == False:
        return False

    for i in range(len(lis)):
        ins = lis[i]
        if ins[0] == "mov":
            if len(ins) == 3:
                if ins[1] in register_wo_flag.keys() and (ins[2] in registers.keys() or (ins[2][0] == "$" and 0 <= int(ins[2][1:]) <= 255)):
                   continue # have to deal intermeditae error here

                elif ins[1] in register_wo_flag.keys() and (ins[2] in registers.keys() or (ins[2][0] == "$" and (0 > int(ins[2][1:]) or  int(ins[2][1:]) > 255))):
                     print("Error : Value of Immediate is out of range in Line", errorlno(i) )
                     return False
                else:
                    print("Error : Register name is incorrect in Line ", errorlno(i) )
                    return False

            else:
                print("Error : Wrong Syntax in Line ", errorlno(i))
                return False

        if ins[0][-1] == ":":

            if len(ins) == 1:
                print("Error : Invalid instruction in Line ",errorlno(i))
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
                print("Error : Invalid instruction in Line " , errorlno(i))
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

        elif(ins[0] != "var"):
            print("Error : Invalid instruction in Line", errorlno(i))
            return False

    if halt_checker(lis) == False:
        return False

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

def print_A(lis):
     print(OPcode[lis[0]][0] + "00" + registers[lis[1]][0] + registers[lis[2]][0] + registers[lis[3]][0])

def print_D(lis):
    varname = lis[2]
    value = None
    for temp in var_list:
        if temp[1] == varname:
            value = temp[2]
    s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]
    print(OPcode[lis[0]][0] + registers[inst[1]][0] + s)

def print_E(lis):

    labelname = lis[1] + ":"
    value = None
    for temp in label_list:
        if temp[0] == labelname:
            value = temp[1]
    s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]
    print(OPcode[lis[0]][0] + "000" + s)

def print_C(lis):
    print(OPcode[lis[0]][0] + "00000" + registers[lis[1]][0] + registers[lis[2]][0])

def print_F(lis):
    print((OPcode["hlt"][0] + "00000000000"))

def print_B(lis):
    value = int((lis[2])[1:])
    s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]
    print(OPcode[lis[0]][0] + registers[inst[1]][0] + s )

if error(lines) == True:

    for inst in final_input:

        if inst[0]=="var":
            continue

        elif inst[0] == "mov":
            if inst[2][0] == "$":
                value = int((inst[2])[1:])
                s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]
                print(OPcode["movimi"][0] + registers[inst[1]][0] + s)

            else:
                print(OPcode["movreg"][0] + "00000" + registers[inst[1]][0] + registers[inst[2]][0])

        elif inst[0][-1]==":":
            inst=inst[1:]
            if inst[0] == "var":
                continue

            elif inst[0] == "mov":
                if inst[2][0] == "$":
                    value = int((inst[2])[1:])
                    s = "0" * (8 - len(bin(value)[2:])) + bin(value)[2:]
                    print(OPcode["movimi"][0] + registers[inst[1]][0] + s)

                else:
                    print(OPcode["movreg"][0] + "00000" + registers[inst[1]][0] + registers[inst[2]][0])

            elif OPcode[inst[0]][1] == "A":
                print_A(inst)

            elif OPcode[inst[0]][1] == "B":
                print_B(inst)

            elif OPcode[inst[0]][1] == "C":
                print_C(inst)

            elif OPcode[inst[0]][1] == "D":
                print_D(inst)

            elif OPcode[inst[0]][1] == "E":
                print_E(inst)

            elif OPcode[inst[0]][1] == "F":
                print_F(inst)

        elif OPcode[inst[0]][1] == "A":
            print_A(inst)

        elif OPcode[inst[0]][1] == "B":
            print_B(inst)

        elif OPcode[inst[0]][1] == "C":
            print_C(inst)

        elif OPcode[inst[0]][1] == "D":
            print_D(inst)

        elif OPcode[inst[0]][1] == "E":
            print_E(inst)

        elif OPcode[inst[0]][1] == "F":
            print_F(inst)


