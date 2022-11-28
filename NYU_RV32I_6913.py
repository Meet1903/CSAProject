import os
import argparse

MemSize = 1000 # memory size, in reality, the memory size should be 2^32, but for this lab, for the space resaon, we keep it as this large number, but the memory is still 32-bit addressable.

class InsMem(object):
    def __init__(self, name, ioDir):
        self.id = name
        
        with open(ioDir + "/imem.txt") as im:
            self.IMem = [data.replace("\n", "") for data in im.readlines()]
            # print(self.IMem)
            self.readInstr(0)

    def readInstr(self, ReadAddress):
        #read instruction memory
        #return 32 bit hex val
        str2 = ''.join(self.IMem[ReadAddress:ReadAddress + 4])
        # return hex(int(str2,2))
        return str2
        pass
          
class DataMem(object):
    def __init__(self, name, ioDir):
        self.id = name
        self.ioDir = ioDir
        with open(ioDir + "/dmem.txt") as dm:
            self.DMem = [data.replace("\n", "") for data in dm.readlines()]

    def readInstr(self, ReadAddress):
        #read data memory
        #return 32 bit hex val
        str2 = ''.join(self.DMem[ReadAddress:ReadAddress + 4])
        # return hex(int(str2,2))
        return str2
        pass
        
    def writeDataMem(self, Address, WriteData):
        # write data into byte addressable memory
        # # Assuming WriteData is in int format
        self.DMem[Address] = str(bin(WriteData)[2:])
        pass
                     
    def outputDataMem(self):
        resPath = self.ioDir + "/" + self.id + "_DMEMResult.txt"
        with open(resPath, "w") as rp:
            rp.writelines([str(data) + "\n" for data in self.DMem])

class RegisterFile(object):
    def __init__(self, ioDir):
        self.outputFile = ioDir + "RFResult.txt"
        self.Registers = [0x0 for i in range(32)]
    
    def readRF(self, Reg_addr):
        # Fill in
        return self.Registers[Reg_addr]
        pass
    
    def writeRF(self, Reg_addr, Wrt_reg_data):
        # Fill in
        # # Assuming Wrt_reg_data is in decimal format
        self.Registers[Reg_addr] = str(bin(Wrt_reg_data)[2:])
        pass
         
    def outputRF(self, cycle):
        op = ["-"*70+"\n", "State of RF after executing cycle:" + str(cycle) + "\n"]
        op.extend([str(val)+"\n" for val in self.Registers])
        if(cycle == 0): perm = "w"
        else: perm = "a"
        with open(self.outputFile, perm) as file:
            file.writelines(op)

class State(object):
    def __init__(self):
        self.IF = {"nop": False, "PC": 0}
        self.ID = {"nop": False, "Instr": 0}
        self.EX = {"nop": False, "Read_data1": 0, "Read_data2": 0, "Imm": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "is_I_type": False, "rd_mem": 0, 
                   "wrt_mem": 0, "alu_op": 0, "wrt_enable": 0}
        self.MEM = {"nop": False, "ALUresult": 0, "Store_data": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "rd_mem": 0, 
                   "wrt_mem": 0, "wrt_enable": 0}
        self.WB = {"nop": False, "Wrt_data": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "wrt_enable": 0}

class Core(object):
    def __init__(self, ioDir, imem, dmem):
        self.myRF = RegisterFile(ioDir)
        self.cycle = 0
        self.halted = False
        self.ioDir = ioDir
        self.state = State()
        self.nextState = State()
        self.ext_imem = imem
        self.ext_dmem = dmem

class SingleStageCore(Core):
    def __init__(self, ioDir, imem, dmem):
        super(SingleStageCore, self).__init__(ioDir + "/SS_", imem, dmem)
        self.opFilePath = ioDir + "/StateResult_SS.txt"

    def step(self):
        # Your implementation
        print("Cycle= ", self.cycle)
        ## fetched instruction in 32 bit string format
        instruction = self.ext_imem.readInstr(self.cycle * 4)
        print("Instruction= ", instruction)
        print(int(instruction[0:5], 2))
        opcode = instruction[25:32]
        print("opcode= ", opcode)
        if opcode == '0110011':
            ## Code for Instruction type R 
            rs2 = int(instruction[7:12], 2)
            rs1 = int(instruction[12:17], 2)
            rd = int(instruction[20:25], 2)
            funct3 = int(instruction[17:20], 2)
            funct7 = int(instruction[0:7], 2)
            if funct3 == '000':
                ## Code implementation for ADD & SUB
                if funct7 == '0000000':
                    ## Code implementation for ADD
                    pass
                else:
                    ## Code implementation for SUB
                    pass
                pass
            elif funct3 == '100':
                ## Code implementation for XOR
                pass
            elif funct3 == '110':
                ## Code implementation for OR
                pass
            elif funct3 == '111':
                ## Code implementation for AND
                pass
            pass
        elif opcode == '0010011':
            ## Code for Instruction type I
            rs1 = int(instruction[12:17], 2)
            rd = int(instruction[20:25], 2)
            funct3 = int(instruction[17:20], 2)
            imm = int(instruction[20:], 2)
            if funct3 == '000':
                ## Code implementation for ADDI
                pass
            elif funct3 == '100':
                ## Code implementation for XORI
                pass
            elif funct3 == '110':
                ## Code implementation for ORI
                pass
            elif funct3 == '111':
                ## Code implementation for ANDI
                pass
            pass
        elif opcode == '1101111':
            ## Code for Instruction type J
            rd = int(instruction[20:25], 2)
            immString = str(instruction[11]) + instruction[21:31] + str(instruction[20]) + instruction[12:20]
            imm = int(immString, 2)
            pass
        elif opcode == '1100011':
            ## Code for Instruction type B
            rs2 = int(instruction[7:12], 2)
            rs1 = int(instruction[12:17], 2)
            funct3 = int(instruction[17:20], 2)
            immString =  str(instruction[19]) + instruction[21:27] + instruction[27:31] + str(instruction[20])
            imm = int(immString, 2)
            pass
        elif opcode == '0000011':
            ## Code for Instruction type I 2
            rs1 = int(instruction[12:17], 2)
            rd = int(instruction[20:25], 2)
            funct3 = int(instruction[17:20], 2)
            imm = int(instruction[20:], 2)
            pass
        elif opcode == '0100011':
            ## Code for Instruction type S
            rs2 = int(instruction[7:12], 2)
            rs1 = int(instruction[12:17], 2)
            funct3 = int(instruction[17:20], 2)
            immString = instruction[20:27] + instruction[27:32]
            imm = int(immString, 2)
            pass
        elif opcode == '1111111':
            ## cpde for Halt
            pass


        self.halted = True
        if self.state.IF["nop"]:
            self.halted = True
            
        self.myRF.outputRF(self.cycle) # dump RF
        self.printState(self.nextState, self.cycle) # print states after executing cycle 0, cycle 1, cycle 2 ... 
            
        self.state = self.nextState #The end of the cycle and updates the current state with the values calculated in this cycle
        self.cycle += 1

    def printState(self, state, cycle):
        printstate = ["-"*70+"\n", "State after executing cycle: " + str(cycle) + "\n"]
        printstate.append("IF.PC: " + str(state.IF["PC"]) + "\n")
        printstate.append("IF.nop: " + str(state.IF["nop"]) + "\n")
        
        if(cycle == 0): perm = "w"
        else: perm = "a"
        with open(self.opFilePath, perm) as wf:
            wf.writelines(printstate)

class FiveStageCore(Core):
    def __init__(self, ioDir, imem, dmem):
        super(FiveStageCore, self).__init__(ioDir + "/FS_", imem, dmem)
        self.opFilePath = ioDir + "/StateResult_FS.txt"

    def step(self):
        # Your implementation
        # --------------------- WB stage ---------------------
        
        
        
        # --------------------- MEM stage --------------------
        
        
        
        # --------------------- EX stage ---------------------
        
        
        
        # --------------------- ID stage ---------------------
        
        
        
        # --------------------- IF stage ---------------------
        
        self.halted = True
        if self.state.IF["nop"] and self.state.ID["nop"] and self.state.EX["nop"] and self.state.MEM["nop"] and self.state.WB["nop"]:
            self.halted = True
        
        self.myRF.outputRF(self.cycle) # dump RF
        self.printState(self.nextState, self.cycle) # print states after executing cycle 0, cycle 1, cycle 2 ... 
        
        self.state = self.nextState #The end of the cycle and updates the current state with the values calculated in this cycle
        self.cycle += 1

    def printState(self, state, cycle):
        printstate = ["-"*70+"\n", "State after executing cycle: " + str(cycle) + "\n"]
        printstate.extend(["IF." + key + ": " + str(val) + "\n" for key, val in state.IF.items()])
        printstate.extend(["ID." + key + ": " + str(val) + "\n" for key, val in state.ID.items()])
        printstate.extend(["EX." + key + ": " + str(val) + "\n" for key, val in state.EX.items()])
        printstate.extend(["MEM." + key + ": " + str(val) + "\n" for key, val in state.MEM.items()])
        printstate.extend(["WB." + key + ": " + str(val) + "\n" for key, val in state.WB.items()])

        if(cycle == 0): perm = "w"
        else: perm = "a"
        with open(self.opFilePath, perm) as wf:
            wf.writelines(printstate)

if __name__ == "__main__":
     
    #parse arguments for input file location
    parser = argparse.ArgumentParser(description='RV32I processor')
    parser.add_argument('--iodir', default="", type=str, help='Directory containing the input files.')
    args = parser.parse_args()

    ioDir = os.path.abspath(args.iodir)
    print("IO Directory:", ioDir)

    imem = InsMem("Imem", ioDir)
    dmem_ss = DataMem("SS", ioDir)
    dmem_fs = DataMem("FS", ioDir)
    
    ssCore = SingleStageCore(ioDir, imem, dmem_ss)
    fsCore = FiveStageCore(ioDir, imem, dmem_fs)

    while(True):
        if not ssCore.halted:
            ssCore.step()
        
        if not fsCore.halted:
            fsCore.step()

        if ssCore.halted and fsCore.halted:
            break
    
    # dump SS and FS data mem.
    dmem_ss.outputDataMem()
    dmem_fs.outputDataMem()