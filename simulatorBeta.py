'''
Date : 4/10/2024
Name : Zhao Do
Project 4 Beta: Python Single Cycle Processor Simulator
Last modified date : 4/10/2024
'''

import os
import string
import argparse


def ins_type(reg,bin):  # Define instruction type
    opcode = bin[:6]
    if opcode == '000000':  # R-type instructions
        return r_type(reg,bin)
    elif opcode == '001000':  # I-type instruction specifically addi
        return addi(reg,bin)
    elif opcode == '000100':  # I-type instruction specifically beq
        return beq(reg,bin)
    elif opcode == '000101':  # I-type instruction specifically bne
        return bne(reg,bin)
    elif opcode == '100011':  # I-type instruction specifically lw
        return lw(reg,bin)
    elif opcode == '101011':  # I-type instruction specifically sw
        return sw(reg,bin)


def r_type(reg,bin):  # looking whether it is an add or sub instruction
    funct = int(bin[26:32], 2)
    if funct == 32:
        return add(reg,bin)
    elif funct == 34:
        return sub(reg,bin)


def calculate_registers(bin_data, reg,mem_val):  # calculate current holding values for registers and updated program counter

    opcode = bin_data[:6]
    rs = int(bin_data[6:11], 2)
    rt = int(bin_data[11:16], 2)
    rd = int(bin_data[16:21], 2)
    imm = int(bin_data[16:], 2)

    if imm >= (1 << 15):  # If the immediate value is negative
        imm -= (1 << 16)  # Extend the sign

    funct = int(bin_data[26:32], 2)
    if funct == 32:  # add
        reg[rd] = int(reg[rs]) + int(reg[rt])
    elif funct == 34:  # sub
        reg[rd] = int(reg[rs]) - int(reg[rt])  # handling signed subtraction

    if opcode == '001000':  # addi
        reg[rt] = reg[rs] + imm
    elif opcode == '100011':
        #address = reg[rs] + imm

        reg[rt] = mem_val[reg[rs]+(imm//4)]
        #memory[registers[rs] + (immediate // 4)]

    return reg


def branch(bin_data,reg, pc):  # calculate current holding values for registers and updated program counter

    opcode = bin_data[:6]
    rs = int(bin_data[6:11], 2)
    rt = int(bin_data[11:16], 2)
    rd = int(bin_data[16:21], 2)
    imm = int(bin_data[16:], 2)

    if imm >= (1 << 15):  # If the immediate value is negative
        imm -= (1 << 16)  # Extend the sign

    if opcode == '000100':  # branching equal

        if reg[rs] == reg[rt]:
            shift = 4 * imm
            pc += shift
    elif opcode == '000101':  # branching not equal
        if reg[rs] != reg[rt]:
            shift = 4 * imm
            pc += shift
            if imm == -1:
                pc +=-4
    return pc


def add(reg,bin):  # add instruction control signal

    opcode = bin[:6]
    rs = int(bin[6:11], 2)
    rt = int(bin[11:16], 2)
    rd = int(bin[16:21], 2)
    imm = int(bin[16:], 2)


    zerofromalu = 0

    regdst = 1  # register to destination
    alusrc = 0  # no ALU source
    memtoreg = 0  # no data from memory to register
    regw = 1  # write into register
    memr = 0  # not reading from memory
    memw = 0  # not writing into memory
    branch = 0  # no branching operation
    aluop1 = 1
    aluop2 = 0


    # assign control signal value by shifting value
    control_signal = f"{regdst}{alusrc}{memtoreg}{regw}{memr}{memw}{branch}{aluop1}{aluop2}{zerofromalu}"

    return control_signal


def sub(reg,bin):  # sub instruction control signal

    opcode = bin[:6]
    rs = int(bin[6:11], 2)
    rt = int(bin[11:16], 2)
    rd = int(bin[16:21], 2)
    imm = int(bin[16:], 2)

    zerofromalu = 0

    regdst = 1  # register to destination
    alusrc = 0  # no ALU source
    memtoreg = 0  # no data from memory to register
    regw = 1  # write into register
    memr = 0  # not reading from memory
    memw = 0  # not writing into memory
    branch = 0  # no branching operation
    aluop1 = 1
    aluop2 = 0


    # assign control signal value by shifting value
    control_signal = f"{regdst}{alusrc}{memtoreg}{regw}{memr}{memw}{branch}{aluop1}{aluop2}{zerofromalu}"

    return control_signal


def addi(reg,bin):  # addi instruction control signal

    opcode = bin[:6]
    rs = int(bin[6:11], 2)
    rt = int(bin[11:16], 2)
    rd = int(bin[16:21], 2)
    imm = int(bin[16:], 2)

    if imm == 0:
        zerofromalu = 1  # Zero bit from ALU
    else:
        zerofromalu = 0

    regdst = 0  # register to destination
    alusrc = 1  # ALU source
    memtoreg = 0  # not data from memory to register
    regw = 1  # write into register
    memr = 0  # no memory read
    memw = 0  # no memory write
    branch = 0  # no branching operation
    aluop1 = 0
    aluop2 = 0

    # assign control signal value by shifting value
    control_signal = f"{regdst}{alusrc}{memtoreg}{regw}{memr}{memw}{branch}{aluop1}{aluop2}{zerofromalu}"

    return control_signal

def beq(reg,bin):
    opcode = bin[:6]
    rs = int(bin[6:11], 2)
    rt = int(bin[11:16], 2)
    rd = int(bin[16:21], 2)
    imm = int(bin[16:], 2)

    if reg[rs]-reg[rt] == 0:
        zerofromalu = 1  # Zero bit from ALU
    else:
        zerofromalu = 0

    regdst = 'X'  # register to destination
    alusrc = 0  # ALU source
    memtoreg = 'X'  # not data from memory to register
    regw = 0  # write into register
    memr = 0  # no memory read
    memw = 0  # no memory write
    branch = 1  # no branching operation
    aluop1 = 0
    aluop2 = 1

    # assign control signal value by shifting value
    control_signal = f"{regdst}{alusrc}{memtoreg}{regw}{memr}{memw}{branch}{aluop1}{aluop2}{zerofromalu}"

    return control_signal

def bne(reg,bin):
    opcode = bin[:6]
    rs = int(bin[6:11], 2)
    rt = int(bin[11:16], 2)
    rd = int(bin[16:21], 2)
    imm = int(bin[16:], 2)

    if reg[rs] - reg[rt] == 0:
        zerofromalu = 1  # Zero bit from ALU
    else:
        zerofromalu = 0

    regdst = 'X'  # register to destination
    alusrc = 0  # ALU source
    memtoreg = 'X'  # not data from memory to register
    regw = 0  # write into register
    memr = 0  # no memory read
    memw = 0  # no memory write
    branch = 1  # no branching operation
    aluop1 = 1
    aluop2 = 1

    # assign control signal value by shifting value
    control_signal = f"{regdst}{alusrc}{memtoreg}{regw}{memr}{memw}{branch}{aluop1}{aluop2}{zerofromalu}"

    return control_signal


def lw(reg,bin):
    regdst = 0  # register to destination
    alusrc = 1  # ALU source
    memtoreg = 1  # not data from memory to register
    regw = 1  # write into register
    memr = 1  # no memory read
    memw = 0  # no memory write
    branch = 0  # no branching operation
    aluop1 = 0
    aluop2 = 0
    zerofromalu = 0  # Zero bit from ALU

    # assign control signal value by shifting value
    control_signal = f"{regdst}{alusrc}{memtoreg}{regw}{memr}{memw}{branch}{aluop1}{aluop2}{zerofromalu}"

    return control_signal


def sw(reg,bin):
    regdst = 'X'  # register to destination
    alusrc = 1  # ALU source
    memtoreg = 'X'  # not data from memory to register
    regw = 0  # write into register
    memr = 0  # no memory read
    memw = 1  # no memory write
    branch = 0  # no branching operation
    aluop1 = 0
    aluop2 = 0
    zerofromalu = 0  # Zero bit from ALU

    # assign control signal value by shifting value
    control_signal = f"{regdst}{alusrc}{memtoreg}{regw}{memr}{memw}{branch}{aluop1}{aluop2}{zerofromalu}"

    return control_signal


def write_mem(bin_data, reg,in_mem):  # calculate current holding values for registers and updated program counter

    opcode = bin_data[:6]
    rs = int(bin_data[6:11], 2)
    rt = int(bin_data[11:16], 2)
    rd = int(bin_data[16:21], 2)
    imm = int(bin_data[16:], 2)

    if imm >= (1 << 15):  # If the immediate value is negative
        imm -= (1 << 16)  # Extend the sign
    if opcode == '101011':
        in_mem[(reg[rs] + imm) // 4] = reg[rt]
        #print(in_mem)
    return in_mem

def main():  #main function

    reg = [0, 0, 0, 0, 0, 0, 0, 0]  # intialize registers array from 0-7 with initial value of 0. (I want to use zeroes function of numpy but cannot download package :( )
    pc = 65536  # initialize program counter value at 65536
    in_pc = 65536
    #default_input_file = "alpha.bin"
    parser = argparse.ArgumentParser(prog="Python Single Cycle Processor Simulator", description="Simulation of a Single Cycle Processor")

    #parser.add_argument("--file", help="input filename", type=str, required=True)
    parser.add_argument("--program", help="Path to the input machine code file", type=str, required=True)
    parser.add_argument("--memory", help="Memory for the simulation", type=str, required=True)
    args = parser.parse_args()

    #mem_val = []
    instructions = []
    control = []
    test = []
    in_mem = []
    registers_val = [f"{pc}|{'|'.join(map(str, reg))}"]  # initialize first register value at pc = 65536

    with open(args.memory, 'r') as file:
        for line in file:
            mem = line.strip()
            in_mem.append(mem)
            #mem_val = write_mem(in_mem)

    with open(args.program, 'r') as file:
        for line in file:
            ins = line.strip()
            instructions.append(ins)

    while pc <= len(instructions) * 4 + in_pc:
        print("Current pc:", pc)
        index = (pc - in_pc) // 4
        print("Index:", index)
        if index >= len(instructions):
            print("Index out of range. Breaking loop.")
            break
        bin = instructions[index]
        print("Instruction:", bin)
        test.append(bin)

        if pc < in_pc or pc >= (len(in_mem) * 4 + in_pc - 4):  # Check if PC is out of bounds
            print("PC out of bounds. Breaking loop.")
            control.append("!!! Segmentation Fault !!!\r\n")
            registers_val.append("!!! Segmentation Fault !!!\r\n")
            break

        result = ins_type(reg, bin)
        control.append(str(result))  # Convert binary to string and append control signal values after each instruction
        registers = calculate_registers(bin, reg, in_mem)

        pc = branch(bin, reg, pc)


        if pc < in_pc or pc >= (len(in_mem) * 4 + in_pc - 4):  # Check if PC is out of bounds after branch
            print("PC out of bounds. Breaking loop.")
            control.append("!!! Segmentation Fault !!!\r\n")
            registers_val.append("!!! Segmentation Fault !!!\r\n")
            break


        if pc > in_pc + 4*len(instructions):
            registers_val.append(f"{pc}|{'|'.join(map(str, registers))}")
            break
        pc += 4  # Increment pc by 4 to move to the next instruction
        registers_val.append(f"{pc}|{'|'.join(map(str, registers))}")
        in_mem = write_mem(bin, reg, in_mem)
        print(in_mem)

    if pc > len(instructions) * 4 + in_pc:
        control.append("!!! Segmentation Fault !!!\r\n")
        registers_val.append("!!! Segmentation Fault !!!\r\n")

    with open('out_control.txt', 'w') as output_control:
        output_control.write('\n'.join(control)+ '\n')  # Write control signals to file
    with open('out_registers.txt', 'w') as output_registers:
        output_registers.write('\n'.join(registers_val)+ '\n')  # Write register values to file
    with open('out_memory.txt', 'w') as output_mem:
        output_mem.write('\n'.join(str(mem) for mem in in_mem))  # Write register values to memory file


if __name__ == "__main__":
    main()