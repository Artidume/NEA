#TODO: FINISH COMMANDS, create debug mode, create assembler, cry
'''NOTE:
    - Harvard Architecture used because I do not deem it necessary to include executing data as instructions.
    - This may change in the future, and if so, DELETE THIS MESSAGE.
    - Increment this for every hour wasted not writing anything >> 1   
'''

class Program:
    def __init__(self,max_size=256): #"max_size=256" defines the default max space to be 256 commands. 256 is not signficant for the code, but it's thematically very cool.
        self.main_memory=[]
        for i in range(0,max_size): #initialising MAIN MEM. not done via bytes bc its too hard
            self.main_memory.append(0)
        self.program_memory=[] 
        for i in range(0,max_size): #initialising PROGRAM MEM. decided to use harvard architecture since the program should not be able to self-modify.
            self.program_memory.append([0,0])
        #init registers, PC, and <flags (TBD)>
        self.isRunning=True 
        self.PC=0 #program counter
        self.r=[0,0,0,0,0,0,0,0,0,0,0,0] #List of registers 1 through 12
        self.cmp_output=0 #Output of compare function. 0=Null, otherwise follows AQA standard ("EQ","NE","GT","LT").
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
            "OUTPUT":self.OUTPUT 
        }
        self.labels={} # Will store key:value pairs of labels and their locations.
    
    #I believe LDR is complete.
    def LDR(self,operands): #(d,memory_ref,!!address_type!!) NOTE: an extra paramter is passed to say the address type
        if operands[2]=="DIRECT":#get value from address pointed to in memory
            if operands[1]>len(self.main_memory)-1: #checking memory_ref does not exceed storage constraint
                print(f"FATAL ERROR: memory_ref ({operands[1]}) exceeds storage size ({len(self.main_memory)-1} data blocks).")
                self.isRunning=False #halt program
                return 0 #exit instruction
            self.r[operands[0]]=self.main_memory[operands[1]]
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

    def B(self,operands): #(label,condition)
        #the way this works is by trying to use a condition. If it doesn't exist, assume it is a branch with no condition, and branch.
        try: 
            if operands[1].upper()==self.cmp_output: #condition met. .upper() to allow for "eq" and "EQ" to evaluate correctly.
                self.PC=operands[0]
        except:
            self.PC=operands[0]


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
    
    def HALT(self,operands): #no operands with command, but python needs the arg otherwise it cries.
        self.isRunning=False # will be checked next loop.
    
    #-------------------------------------------- BELOW ARE UNNOFFICIAL INSTRUCTIONS USED TO AID THE PROGRAMMER. --------------------------------------------
    def OUTPUT(self,operands): #(register_number)
        print(self.r[operands[0]])
    
    def fetch_execute_cycle(self): #This works off the principles of the Fetch (Decode) Execute cycle. The execute and decode happen currently at the same line.
        
        if self.PC>len(self.main_memory)-1: #check PC in range of memory. If not, throw an error.
                print(f"FATAL ERROR: Program counter (Currently {self.PC}) exceeded storage size ({len(self.program_memory)-1} instructions).\nRemember to have a HALT instruction to end your code, and don't exceed storage limits!")
                self.isRunning=False #disable program execution
                return 0 #exit function before trying to run non-existent instruction
        
        self.command=self.program_memory[self.PC] #fetch command and operand (array of <opcode>,<operand(s)>)
        self.PC+=1 #increment PC
        
        if self.command[0]==0: #check that instruction present at memory location pointed to by PC
            print(f"FATAL ERROR: No command found at location {self.PC}.")
            self.isRunning=False #disable program execution
            return 0#exit function before trying to run non-existent instruction
        #print(self.command,self.PC) #debug to check it is running the proper command.
        self.commands[self.command[0]](self.command[1]) #perform command
        print(self.r[0]) #check contents of R1
    
    def run_program(self):
        while self.isRunning: #isRunning only stops once a HALT is reached.
            self.fetch_execute_cycle()
            self.PC=256 #just fucken around really
            

    #Notice the Harvard Architecture, so that I do not need to introduce my own binary table for instructions, or running data as instructions.
    #This is because it will not be used within an exam question, or at least hasn't been so far. 
    def set_program_memory(self,location,opcode,operand):
        self.program_memory[location]=[opcode,operand]
    def set_main_memory(self,location,data):
        self.main_memory[location]=data

test_program=Program()

#Test program to check LDR operating as intended.
'''
test_program.set_program_memory(0,"LDR",[0,1,"IMMEDIATE"])
test_program.set_main_memory(2,20)
test_program.set_program_memory(1,"LDR",[0,2,"DIRECT"])
#test_program.set_program_memory(2,"HALT",[])
test_program.run_program()
'''