import program_parser

#TODO: FINISH COMMANDS, create debug mode, create assembler, cry
#TODO: FIX CMP COMMAND
#TODO: Add debug mode to all instrucitons
'''NOTE:
    - Pivotted to Von Neumann architecture, worth it to closer mimic original design.
    - This may change in the future, and if so, DELETE THIS MESSAGE.
    - Increment this for every hour wasted not writing anything >> 1   
'''
class Memory:
    def __init__(self,max_size=16384):
        self.memoryArray=[]
        for i in range(0,max_size):
            self.memoryArray.append("NULL")
        self.length=max_size
    def getLength(self):
        return self.length
    def set(self,location,data):
        self.memoryArray[location]=data
        #print(self.memoryArray[location]) check data has been set correctly. Remember format is [TYPE,[Opcode,[operands]]]
    def fetch(self,location):
        return self.memoryArray[location]
#Program Composed of ("has-a") Memory
class Program:
    def __init__(self,debug_mode=False):
        self.debug_mode=debug_mode #will show all "output" types, incl. PC
        self.memory = Memory()
        self.isRunning=True
        self.PC=0
        self.r=[0,0,0,0,0,0,0,0,0,0,0,0]
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
                print(f"DATA FOUND AT LOCATION {operands[1]}: {self.memory.fetch(operands[1])}") #show what is present at memory location
            self.r[operands[0]]=self.memory.fetch(operands[1])
        else: #assume it is immediate.
            self.r[operands[0]]=operands[1]
    def STR(self,operands): #(d,memory_ref)
        self.memory.set(operands[1],self.r[operands[0]])
    
    def ADD(self,operands): #(d,n,operand2, !!mode!!) mode checks whether <operand2> is a register
        if operands[3]!="REGISTER":
            self.r[operands[0]]=self.r[operands[1]]+operands[2]
        else:
            self.r[operands[0]]=self.r[operands[1]]+self.r[operands[2]]
    def SUB(self,operands): #(d,n,operand2, !!mode!!) mode checks whether <operand2> is a register
        if operands[3]!="REGISTER": 
            self.r[operands[0]]=self.r[operands[1]]-operands[2]
        else:
            self.r[operands[0]]=self.r[operands[1]]-self.r[operands[2]]

    def MOV(self,operands): #(d,operand2)
        if operands[2]!="REGISTER":
            self.r[operands[0]]=operands[1]
        else:
            self.r[operands[0]]=self.r[operands[1]]

    def CMP(self,operands): #(n,operand2) NEED TO FIX THIS
        self.cmp_output=""
        if self.debug_mode:
            print(f"OPERANDS FOR CMP INSTRUCTION: {operands}")

        if operands[2]=="REGISTER" and operands[3]=="REGISTER": #if they are both registers
            if self.r[operands[0]]>self.r[operands[1]]:
                self.cmp_output+="GT NE "
            elif self.r[operands[0]]<self.r[operands[1]]:
                self.cmp_output+="LT NE "
            elif self.r[operands[0]]==self.r[operands[1]]:
                self.cmp_output+="EQ "
        elif operands[2]=="REGISTER" and operands[3]=="IMMEDIATE": #use value2 immediately, no fetch from memory
            if self.r[operands[0]]>operands[1]:
                self.cmp_output+="GT NE "
            elif self.r[operands[0]]<operands[1]:
                self.cmp_output+="LT NE "
            elif self.r[operands[0]]==operands[1]:
                self.cmp_output+="EQ "
        elif operands[2]=="REGISTER" and operands[3]=="DIRECT": #value2 is a pointer to memory
            if self.memory.fetch(operands[1])[0]!="DATA":
                print(f"FATAL ERROR: DATA AT LOCATION {operands[1]} IS EITHER AN INSTRUCTION OR NOT INITIALISED.")
                self.isRunning=False
                return 0 #exit program
            if self.r[operands[0]]>self.memory.fetch(operands[1])[1]:
                self.cmp_output+="GT NE "
            elif self.r[operands[0]]<self.memory.fetch(operands[1])[1]:
                self.cmp_output+="LT NE "
            elif self.r[operands[0]]==self.memory.fetch(operands[1])[1]:
                self.cmp_output+="EQ "
        elif operands[2]=="DIRECT" and operands[3]=="REGISTER": #value1 is a pointer to memory
            if self.memory.fetch(operands[0])[0]!="DATA":
                print(f"FATAL ERROR: DATA AT LOCATION {operands[0]} IS EITHER AN INSTRUCTION OR NOT INITIALISED.")
                self.isRunning=False
                return 0 #exit program
            if self.memory.fetch(operands[0])[1]>self.r[operands[1]]:
                self.cmp_output+="GT NE "
            elif self.memory.fetch(operands[0])[1]<self.r[operands[1]]:
                self.cmp_output+="LT NE "
            elif self.memory.fetch(operands[0])[1]==self.r[operands[1]]:
                self.cmp_output+="EQ "
        


        if self.debug_mode:    
            print(f"THE COMPARISON FOUND THESE CONDITIONS: {self.cmp_output}") #show result of comparison

    def B(self,operands): #(label,condition)
        #print(f"OPERANDS FOR BRANCH INSTRUCTION: {operands}") #show all operands [Location,Condition]
        if operands[1]=="NO CONDITION":
            self.PC=operands[0]
        else:
            #print(self.cmp_output) #check CMP instruction working
            if operands[1] in self.cmp_output: #if condition matches
                self.PC=operands[0] #move PC to new location
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
        print(self.r[operands[0]])
    
    def fetch_execute_cycle(self): #runs FE Cycle once.
        if self.PC>self.memory.getLength():
            print(f"FATAL ERROR: Program counter (Currently {self.PC}) exceeded bounds of memory.")
            self.isRunning=False
            return 0
        self.command=self.memory.fetch(self.PC)

        self.PC+=1
        if self.command=="NULL":
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

main_program=Program()
program_as_an_array=program_parser.getprogramfromfileusingcustomfileextensionbecauseimreallyreallycoolandeveryonelikesme()
#print(program_as_an_array) #output program as it has been parsed
i=0
for instruction in program_as_an_array:
    if instruction[0:6]!="ERROR":
        main_program.memory.set(i,instruction)
    i+=1
    #print(instruction)
main_program.run()