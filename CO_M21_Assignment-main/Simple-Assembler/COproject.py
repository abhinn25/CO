OPcode = {"add":{"00000","A"} ,
          "sub":{"00001","A"} ,
          "mul":{"00110","A"} ,
          "xor":{"01010","A"} ,
          "or":{"01011", "A"} ,
          "and":{"01100","A"} ,
          "mov"
          "mov":{"00011","C"} ,
          "div":{"00111","C"} ,
          "not":{"01101","C"} ,
          "cmp":{"01110","C"} ,
          "ld":{"00100", "D"} ,
          "st":{"00101", "D"} ,
          "jmp":{"01111","E"} ,
          "jgt":{"10001","E"} ,
          "je":{"10010", "E"} ,
          "jlt":{"10000","E"} ,
          "hlt":{"10011","F"} ,

          }

registers = {"R0":["000",-1],
             "R1":["001",-1],
             "R2":["010",-1],
             "R3":["011",-1],
             "R4":["100",-1],
             "R5":["101",-1],
             "R6":["110",-1]
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


