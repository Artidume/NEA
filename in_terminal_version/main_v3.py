import program_parser_terminal

#TODO: FINISH COMMANDS, create debug mode, create assembler, cry
#TODO: FIX CMP COMMAND
#TODO: Add debug mode to all instrucitons
'''NOTE:
    - Pivotted to Von Neumann architecture, worth it to closer mimic original design.
    - This may change in the future, and if so, DELETE THIS MESSAGE.
    - Increment this for every hour wasted not writing anything >> 1   
'''
class Memory:
    def __init__(self,max_size=256):
        self.memoryArray=[]
        for i in range(0,max_size):
            self.memoryArray.append(["NULL"])
        self.length=max_size
    def getLength(self):
        return self.length
    def set(self,location,data):
        self.memoryArray[location]=data
        #print(self.memoryArray[location]) check data has been set correctly. Remember format is [TYPE,[Opcode,[operands]]]
    def fetch(self,location):
        return self.memoryArray[location]
    def fetch_data(self,location,data_location=0):
        if self.memoryArray[location][0]=="INSTRUCITON":
            return self.memoryArray[location][1][1][data_location]
        elif self.memoryArray[location][0]=="DATA":
            #print(self.memoryArray[location][1]) #not needed anymore. no way schmozé
            return self.memoryArray[location][1]
        elif self.memoryArray[location][0]=="NULL":
            return "Not Initialised"
#Program Composed of ("has-a") Memory
class Program:
    def __init__(self,debug_mode=False):
        self.debug_mode=debug_mode #will show all "output" types, incl. PC
        self.memory = Memory()
        self.isRunning=True
        self.PC=0
        self.r=[0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.cmp_output=""
        self.commands={
            "LDR":self.LDR,
            "STR":self.STR,
            "ADD":self.ADD,
            "SUB":self.SUB,
            "MOV":self.MOV,
            "CMP":self.CMP,
            "B":self.B,
            "AND":self.AND,
            "ORR":self.ORR,
            "EOR":self.EOR,
            "MVN":self.MVN,
            "LSL":self.LSL,
            "LSR":self.LSR,
            "HALT":self.HALT,
            "OUTPUT":self.OUTPUT, 
            "HALT":self.HALT,
        }
    def LDR(self,operands): #(d,memory_ref,!!address_type1,address_type2!!) NOTE: an extra paramter is passed to say the address type. ignore address_type1
        if self.debug_mode:
            print(f"OPERANDS FOR LDR INSTRUCTION: {operands}") #show operands
        if operands[3]=="DIRECT":#get value from address pointed to in memory
            if operands[1]>self.memory.getLength()-1: #checking memory_ref does not exceed storage constraint
                print(f"FATAL ERROR: memory_ref ({operands[1]}) exceeds storage size ({self.memory.getLength()-1} data blocks).")
                self.isRunning=False #halt program
                return 0 #exit instruction
            if self.debug_mode:
                print(f"DATA FOUND AT LOCATION {operands[1]}: {self.memory.fetch_data(operands[1])}") #show what is present at memory location
            self.r[operands[0]]=self.memory.fetch_data(operands[1])
        

    def STR(self,operands): #(d,memory_ref)
        if self.debug_mode:
            print(f"OPERANDS FOR STR INSTRUCTION: {operands}")
        if operands[0]>12:
            print(f"FATAL ERROR. r{operands[0]} DOES NOT EXIST. THE REGISTERS ARE NUMBERED 0-12")
        self.memory.set(operands[1],["DATA",self.r[operands[0]]])
    
    def ADD(self,operands): #(d,n,operand2, !!mode!!) mode checks whether <operand2> is a register
        if operands[3]!="REGISTER":
            self.r[operands[0]]=self.r[operands[1]]+operands[2]
        else:
            self.r[operands[0]]=self.r[operands[1]]+self.r[operands[2]]
    def SUB(self,operands): #(d,n,operand2, !!mode!!) mode checks whether <operand2> is a register
        if self.debug_mode:
            print(f"OPERANDS FOR SUB INSTRUCTION: {operands}")
        if operands[5]!="REGISTER": 
            self.r[operands[0]]=self.r[operands[1]]-operands[2]
        else:
            self.r[operands[0]]=self.r[operands[1]]-self.r[operands[2]]
        if self.debug_mode:
            print(f"RESULT: r{operands[0]} = {self.r[operands[0]]}")

    def MOV(self,operands): #(d,operand2)
        if self.debug_mode:
            print(f"OPERANDS FOR MOV INSTRUCTION: {operands}")
        if operands[3]=="IMMEDIATE":
            self.r[operands[0]]=operands[1]
            if self.debug_mode:
                #print(self.r[operands[0]])
                pass
        elif operands[3]=="DIRECT":
            self.r[operands[0]]=self.memory.fetch_data(operands[1])
        elif operands[3]=="REGISTER":
            self.r[operands[0]]=self.r[operands[1]]
        if self.debug_mode:
            print(f"RESULT: r{operands[0]} = {self.r[operands[0]]}")
        
    def CMP(self,operands): #(n,operand2) 
        if self.cmp_output != "":
            print("ERROR: Comparison previously performed, but not used. The program will ignore the old comparison. Are you missing a branch instruction?")
        self.cmp_output=""
        if self.debug_mode:
            print(f"OPERANDS FOR CMP INSTRUCTION: {operands}")

        self.value1=None
        if operands[2]=="REGISTER":
            self.value1=self.r[operands[0]]
        elif operands[2]=="DIRECT":
            self.value1=self.memory.fetch_data(operands[0])
        elif operands[2]=="IMMEDIATE":
            self.value1=operands[0]
        if self.value1==None:
            print(f"FATAL ERROR: OPERAND 1 FOR CMP COMMAND HAS NOT BEEN PROPERLY USED. VALUE: {operands[0]}")
            self.isRunning=False
            return 0 
        self.value2=None
        if operands[3]=="REGISTER":
            self.value2=self.r[operands[1]]
        elif operands[3]=="DIRECT":
            self.value2=self.memory.fetch_data(operands[1])
        elif operands[3]=="IMMEDIATE":
            self.value2=operands[1]
        if self.value2==None:
            print(f"FATAL ERROR: OPERAND 2 FOR CMP COMMAND HAS NOT BEEN PROPERLY USED. VALUE: {operands[1]}")
            self.isRunning=False
            return 0
        if self.debug_mode:
            print(f"VALUES TO BE COMPARED:\n 1: {self.value1}, 2: {self.value2}")

        #perform comparisons
        if self.value1>self.value2:
            self.cmp_output+="GT NE "
        elif self.value1<self.value2:
            self.cmp_output+="LT NE "
        elif self.value1==self.value2:
            self.cmp_output+="EQ "

        if self.debug_mode:    
            print(f"THE COMPARISON FOUND THESE CONDITIONS: {self.cmp_output}") #show result of comparison

    def B(self,operands): #(location,condition,) NOTE: labels are replaced with their corresponding memory locations in memory when parsed.
        #print(f"OPERANDS FOR BRANCH INSTRUCTION: {operands}") #show all operands [Location,Condition]
        if operands[1]=="NO CONDITION":
            self.PC=operands[0]
        else:
            #print(self.cmp_output) #check CMP instruction working
            if operands[1] in self.cmp_output: #if condition matches
                self.PC=operands[0] #move PC to new location
                self.cmp_output="" #reset comparison flags
                #print(operands[1])
                #print(self.cmp_output)
                #print(operands[1] in self.cmp_output)
            else:
                #print("No dice") #(condition failed)
                pass
        #print("PC",self.PC) #Test it has moved the PC correctly
        #print(self.program_memory[self.PC]) Show instruction at that memory address

    def AND(self,operands): #(d,n,operand2)
        self.r[operands[0]]=self.r[operands[1]] & operands[2] # & = bitwise and

    def ORR(self,operands): #(d,n,operand2)
        self.r[operands[0]]=self.r[operands[1]] | operands[2] # | = bitwise or
    
    def EOR(self,operands): #(d,n,operand2)
        self.r[operands[0]]=self.r[operands[1]] ^ operands[2] # ^ = bitwise xor
    
    def MVN(self,operands): #(d,operand2)
        self.r[operands[0]]= ~operands[1] # ~ = bitwise not
    
    def LSL(self,operands): #(d,n,operand2)
        self.r[operands[0]]=self.r[operands[1]] << operands[2] # << = bitwise shift left
    
    def LSR(self,operands): #(d,n,operand2)
        self.r[operands[0]]=self.r[operands[1]] >> operands[2] # >> = bitwise shift right
    
    def HALT(self,operands):
        self.isRunning=False
    def OUTPUT(self,operands):
        if self.debug_mode:
            print(f"OPERANDS FOR OUTPUT INSTRUCTION: {operands}")
        if operands[1]=="REGISTER":
            print(self.r[operands[0]])
        elif operands[1]=="IMMEDIATE":
            print(operands[0])
        elif operands[1]=="DIRECT":
            print(self.memory.fetch_data(operands[0]))
    
    def fetch_execute_cycle(self): #runs FE Cycle once.
        if self.PC>self.memory.getLength():
            print(f"FATAL ERROR: Program counter (Currently {self.PC}) exceeded bounds of memory.")
            self.isRunning=False
            return 0
        self.command=self.memory.fetch(self.PC)
        self.PC+=1
        if self.command==["NULL"]:
            print(f"FATAL ERROR. NO DATA FOUND AT ADDRESS {self.PC}. Perhaps you missed a HALT instruction?")
            self.isRunning=False
            return 0
        elif self.command[0]=="ERROR":
            print(f"PARSING ERROR OCCURED. CHECK YOUR CODE IS WRITTEN AND FORMATTED CORRECTLY.")
            self.isRunning=False
            return 0
        elif self.command[0]=="DATA":
            print(f"FATAL ERROR. PC ENCOUNTERED A NON INSTRUCTION AND HAS QUIT.")
            print(self.command,self.PC)
            self.isRunning=False
            return 0
        else: #assume no error
            #print(self.PC) #show location of PC
    
            self.commands[self.command[1][0]](self.command[1][1])

    def run(self):
        while self.isRunning:
            self.fetch_execute_cycle()

debug_check = input("Input any character to enable debug mode")
if debug_check!="":
    debug_check=True
else:
    debug_check=False

main_program=Program(debug_check) #a True value being parsed means debug mode is active
program=program_parser_terminal.getprogramfromfileusingcustomfileextensionbecauseimreallyreallycoolandeveryonelikesme()
program_as_an_array=program
i=0
for instruction in program_as_an_array:
    if instruction[0:6]!="ERROR":
        main_program.memory.set(i,instruction)
    i+=1
    #if instruction[0:5]=="LABEL":
    #print(instruction)
#print(main_program.memory.memoryArray)
main_program.run()