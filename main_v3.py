import program_parser

#TODO: FINISH COMMANDS, create debug mode, create assembler, cry
#TODO: FIX CMP COMMAND
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
    def __init__(self):
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
    def LDR(self,operands): #(d,memory_ref,!!address_type!!) NOTE: an extra paramter is passed to say the address type
        if operands[2]=="DIRECT":#get value from address pointed to in memory
            if operands[1]>self.memory.getLength()-1: #checking memory_ref does not exceed storage constraint
                print(f"FATAL ERROR: memory_ref ({operands[1]}) exceeds storage size ({len(self.main_memory)-1} data blocks).")
                self.isRunning=False #halt program
                return 0 #exit instruction
            print(f"OPERANDS: {operands}")
            self.r[operands[0]]=self.memory.fetch(operands[1])
        else: #assume it is immediate.
            self.r[operands[0]]=operands[1]
        
    def STR(self,operands): #(d,memory_ref)
        self.main_memory[operands[1]]=self.r[operands[0]]
    
    def ADD(self,operands): #(d,n,operand2)
        self.r[operands[0]]=self.r[operands[1]]+operands[2]
    
    def SUB(self,operands): #(d,n,memory_ref)
        self.r[operands[0]]=self.r[operands[1]]-self.main_memory[operands[2]]

    def MOV(self,operands): #(d,operand2)
        self.r[operands[0]]=operands[1]

    def CMP(self,operands): #(n,operand2)
        self.cmp_output=""
        if self.r[operands[0]]>operands[1]:
            self.cmp_output.append("GT NE ")
        elif self.r[operands[0]]<operands[1]:
            self.cmp_output.append("LT NE ")
        elif self.r[operands[0]]==operands[1]:
            self.cmp_output.append("EQ ")
    def LDR(self,operands): #(d,memory_ref,!!address_type!!) NOTE: an extra paramter is passed to say the address type
        if operands[2]=="DIRECT":#get value from address pointed to in memory
            if operands[1]>len(self.main_memory)-1: #checking memory_ref does not exceed storage constraint
                print(f"FATAL ERROR: memory_ref ({operands[1]}) exceeds storage size ({len(self.main_memory)-1} data blocks).")
                self.isRunning=False #halt program
                return 0 #exit instruction
            self.r[operands[0]]=self.main_memory[operands[1]]
            print(self.r[operands[0]], self.main_memory[operands[1]])
        else: #assume it is immediate.
            self.r[operands[0]]=operands[1]
    
    def STR(self,operands): #(d,memory_ref)
        self.memory.set(operands[1],self.r[operands[0]])
    
    def ADD(self,operands): #(d,n,operand2, !!mode!!) mode checks whether <operand2> is a register
        if operands[3]!="register":
            self.r[operands[0]]=self.r[operands[1]]+operands[2]
        else:
            #print("REGGIE DEGGIE")    #(The program detects a register)
            self.r[operands[0]]=self.r[operands[1]]+self.r[operands[2]]
    def SUB(self,operands): #(d,n,operand2, !!mode!!) mode checks whether <operand2> is a register
        if operands[3]!="register": 
            self.r[operands[0]]=self.r[operands[1]]-operands[2]
        else:
            self.r[operands[0]]=self.r[operands[1]]-self.r[operands[2]]

    def MOV(self,operands): #(d,operand2)
        if operands[2]!="register":
            self.r[operands[0]]=operands[1]
        else:
            self.r[operands[0]]=self.r[operands[1]]

    def CMP(self,operands): #(n,operand2) NEED TO FIX THIS
        self.cmp_output=""
        print(operands)
        if self.r[operands[0]]>operands[1]:
            self.cmp_output+=("GT NE ")
        elif self.r[operands[0]]<operands[1]:
            self.cmp_output+=("LT NE ")
        elif self.r[operands[0]]==operands[1]:
            self.cmp_output+=("EQ ")
        #print(self.cmp_output)

    def B(self,operands): #(label,condition)
        #print(operands[1]) show condition
        if operands[1]=="NO CONDITION":
            self.PC=operands[0]
        else:
            #print(self.cmp_output) #check CMP instruction working
            if operands[1] in self.cmp_output: #if condition matches
                self.PC=operands[0] #move PC to new location
                print(operands[1])
                print(self.cmp_output)
                print(operands[1] in self.cmp_output)
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
        #print(self.command,self.PC)
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
            self.isRunning=False
            return 0
        else: #assume no error
            self.commands[self.command[1][0]](self.command[1][1])

    def run(self):
        while self.isRunning:
            self.fetch_execute_cycle()

main_program=Program()
program_as_an_array=program_parser.getprogramfromfileusingcustomfileextensionbecauseimreallyreallycoolandeveryonelikesme()
#print(program_as_an_array)
i=0
for instruction in program_as_an_array:
    if instruction[0:6]!="ERROR":
        main_program.memory.set(i,instruction)
    i+=1
    #print(instruction)
main_program.run()