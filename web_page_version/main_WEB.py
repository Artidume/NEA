import program_parser_WEB
global output
output=""
global max_runtime #This will be the max number of lines that can be executed by a program. Change as desired. 
max_runtime=10000

def pseudo_print(string): #highjacking the print statement to simply write to a larger output feels so funky
    global output
    if output!="":
        output+="☃"
    output += (str(string))

'''
TODO:
- MOV: re-read and ensure valid
- CMP: re-read and ensure valid
- B: re-read and ensure valid. Should be working.
- AND: write
- ORR: write
- EOR: write
- MVN: write
- LSL: write
- LSR: write

- DEBUG MODE:
. Go back over and ensure error message are understandable for the user.

- CRASH HANDLER:
. Have a fatal error ACTUALLY crash the program, and not continue runtime. should be simple.

The other instructions seem to be working fine. The parser also functions as intended.

'''
'''NOTE:
    - Pivotted to Von Neumann architecture, worth it to closer mimic original design.
    - This may change in the future, and if so, DELETE THIS MESSAGE.
    - Increment this for every hour wasted not writing anything >> 2  
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
        #pseudo_print(self.memoryArray[location]) check data has been set correctly. Remember format is [TYPE,[Opcode,[operands]]]
    def fetch(self,location):
        return self.memoryArray[location]
    def fetch_data(self,location,data_location=0):
        if self.memoryArray[location][0]=="INSTRUCITON":
            return self.memoryArray[location][1][1][data_location]
        elif self.memoryArray[location][0]=="DATA":
            #pseudo_print(self.memoryArray[location][1]) #not needed anymore. no way schmozé
            return self.memoryArray[location][1]
        elif self.memoryArray[location][0]=="NULL":
            return "Not Initialised"
#Program Composed of ("has-a") Memory
class Program:
    def __init__(self, labels, debug_mode=False):
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
        self.labels=labels
    def LDR(self,operands): #(d,memory_ref,!!address_type1,address_type2!!) NOTE: an extra paramter is passed to say the address type. ignore address_type1
        if self.debug_mode:
            pseudo_print(f"OPERANDS FOR LDR INSTRUCTION: {operands}") #show operands
        if operands[2]!="REGISTER":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. Rd MUST BE A REGISTER.")
        elif operands[0]>12 and operands[2]=="REGISTER":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. Rd IS AN INVALID REGISTER.")
        if operands[3]=="DIRECT":
            if operands[1]<len(self.memory)-1 and operands[0]<13: #if location does not exceed memory, and if the register is a valid register
                self.r[operands[0]]=self.memory.fetch_data(operands[1])
            elif operands[1]>len(self.memory)-1:
                pseudo_print(f"FATAL ERROR AT LINE {self.PC}: MEMORY LOCATION {operands[1]} EXCEEDS THE BOUNDS OF ALLOCATED MEMORY.")
        else:
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. <memory_ref> CANNOT BE A REGISTER OR IMMEDIATE ")
    def STR(self,operands): #(d,memory_ref)
        if self.debug_mode:
            pseudo_print(f"OPERANDS FOR STR INSTRUCTION: {operands}")
        if operands[0]>12:
            pseudo_print(f"FATAL ERROR. r{operands[0]} DOES NOT EXIST. THE REGISTERS ARE NUMBERED 0-12")
        self.memory.set(operands[1],["DATA",self.r[operands[0]]])
    
    def ADD(self,operands): #(d,n,operand2, !!address_type1,address_type2,address_type3!!)
        if self.debug_mode:
            pseudo_print(f"OPERANDS FOR ADD INSTRUCTION {operands}")
            print(f"OPERANDS FOR ADD INSTRUCTION {operands}")
        self.value=0
        
        #d
        if operands[3]!="REGISTER": #if d is not a register
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. YOU MUST BE STORING THE ADD RESULT IN A REGISTER.")
        if operands[0]>12 and operands[3]=="REGISTER":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. Rd IS AN INVALID REGISTER.")
        #n
        if operands[4]!="REGISTER": #if n is not a register
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. Rn MUST BE A REGISTER.")
            if operands[1]>12:
                pseudo_print(f"FATAL ERROR AT LINE {self.PC}. Rn IS AN INVALID REGISTER.")
        #operand2
        if operands[5]=="IMMEDIATE": 
            self.value=int(operands[2])
        if operands[5]=="DIRECT":
            self.value=self.memory.fetch_data(operands[2])
            if self.value=="Not Initialised":
                pseudo_print(f"FATAL ERROR AT LINE {self.PC}. The memory address pointed to by <operand2> ({operands[2]}) is not initialised.")
            #print(self.value)
            else:
                self.value=int(self.value)
        if operands[5]=="REGISTER":
            if operands[2]>12:
                pseudo_print(f"FATAL ERROR AT LINE {self.PC}. The register specified in <operand2> is not a valid register.")
            self.value=self.r[operands[2]]
        if self.debug_mode:
            pseudo_print(f"OPERATION: r{operands[0]} = r{operands[1]} ({self.r[operands[1]]}) + {self.value}")
        self.r[operands[0]]=self.r[operands[1]]+self.value
        if self.debug_mode:
            pseudo_print(f"RESULT: r{operands[0]} = {self.r[operands[0]]}")
    def SUB(self,operands): #(d,n,operand2, !!address_type1,address_type2,address_type3!!)
        if self.debug_mode:
            pseudo_print(f"OPERANDS FOR SUB INSTRUCTION: {operands}")

        #d
        if operands[3]!="REGISTER":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. Rd MUST BE A REGISTER")
        if operands[0]>12 and operands[3]=="REGISTER":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. Rd IS AN INVALID REGISTER.")
        
        #n
        if operands[4]!="REGISTER":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. Rn MUST BE A REGISTER.")
        if operands[1]>12 and operands[4]=="REGISTER":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. Rn MUST BE A VALID REGISTER.")
        
        #operand2
        if operands[5]=="DIRECT":
            self.value=operands[2]
        if operands[5]=="IMMEDIATE":
            self.value=self.memory.fetch_data(operands[2])
        if operands[5]=="REGISTER":
            if operands[2]>12:
                pseudo_print(f"FATAL ERROR AT LINE {self.PC}. THE REGISTER IN <operand2> MUST BE A VALID REGISTER.")
            self.value=self.r[operands[2]]
        
        self.r[operands[0]]==self.r[operands[1]]-self.value
        if self.debug_mode:
            pseudo_print(f"RESULT: r{operands[0]} = {self.r[operands[0]]}")

    def MOV(self,operands): #(d,operand2)
        if self.debug_mode:
            pseudo_print(f"OPERANDS FOR MOV INSTRUCTION: {operands}")
        if operands[3]=="IMMEDIATE":
            self.r[operands[0]]=operands[1]
            if self.debug_mode:
                #pseudo_print(self.r[operands[0]])
                pass
        elif operands[3]=="DIRECT":
            self.r[operands[0]]=self.memory.fetch_data(operands[1])
        elif operands[3]=="REGISTER":
            self.r[operands[0]]=self.r[operands[1]]
        if self.debug_mode:
            pseudo_print(f"RESULT: r{operands[0]} = {self.r[operands[0]]}")
        
    def CMP(self,operands): #(n,operand2) 
        if self.cmp_output != "":
            pseudo_print("ERROR: Comparison previously performed, but not used. The program will ignore the old comparison. Are you missing a branch instruction?")
        self.cmp_output=""
        if self.debug_mode:
            pseudo_print(f"OPERANDS FOR CMP INSTRUCTION: {operands}")

        self.value1=None
        if operands[2]=="REGISTER":
            self.value1=self.r[operands[0]]
        elif operands[2]=="DIRECT":
            self.value1=self.memory.fetch_data(operands[0])
        elif operands[2]=="IMMEDIATE":
            self.value1=operands[0]
        if self.value1==None:
            pseudo_print(f"FATAL ERROR: OPERAND 1 FOR CMP COMMAND HAS NOT BEEN PROPERLY USED. VALUE: {operands[0]}")
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
            pseudo_print(f"FATAL ERROR: OPERAND 2 FOR CMP COMMAND HAS NOT BEEN PROPERLY USED. VALUE: {operands[1]}")
            self.isRunning=False
            return 0
        if self.debug_mode:
            pseudo_print(f"VALUES TO BE COMPARED:\n 1: {self.value1}, 2: {self.value2}")

        #perform comparisons
        if self.value1>self.value2:
            self.cmp_output+="GT NE "
        elif self.value1<self.value2:
            self.cmp_output+="LT NE "
        elif self.value1==self.value2:
            self.cmp_output+="EQ "

        if self.debug_mode:    
            pseudo_print(f"THE COMPARISON FOUND THESE CONDITIONS: {self.cmp_output}") #show result of comparison

    def B(self,operands): #(location,condition,) NOTE: labels are replaced with their corresponding memory locations in memory when parsed.
        #print("wuh!") #branch wasn't working. this helped
        if self.debug_mode:
            pseudo_print(f"OPERANDS FOR BRANCH INSTRUCTION: {operands}") #show all operands [Location,Condition]
        if operands[1]=="NO CONDITION":
            self.PC=operands[0]
            if self.debug_mode:
                pseudo_print(f"BRANCH INSTRUCTION HAS SENT THE PC TO {self.PC}.")
        else:
            #pseudo_print(self.cmp_output) #check CMP instruction working
            if operands[1] in self.cmp_output: #if condition matches
                self.PC=operands[0] #move PC to new location
                self.cmp_output="" #reset comparison flags
                #pseudo_print(operands[1])
                #pseudo_print(self.cmp_output)
                #pseudo_print(operands[1] in self.cmp_output)
            else:
                #pseudo_print("No dice") #(condition failed)
                pass
        #pseudo_print("PC",self.PC) #Test it has moved the PC correctly
        #pseudo_print(self.program_memory[self.PC]) Show instruction at that memory address

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
            pseudo_print(f"OPERANDS FOR OUTPUT INSTRUCTION: {operands}")
        if operands[1]=="REGISTER":
            pseudo_print(self.r[operands[0]])
        elif operands[1]=="IMMEDIATE":
            pseudo_print(operands[0])
        elif operands[1]=="DIRECT":
            pseudo_print(self.memory.fetch_data(operands[0]))
    
    def fetch_execute_cycle(self): #runs FE Cycle once.
        if self.PC>self.memory.getLength():
            pseudo_print(f"FATAL ERROR: Program counter (Currently {self.PC}) exceeded bounds of memory.")
            self.isRunning=False
            return 0
        self.command=self.memory.fetch(self.PC)

        self.PC+=1
        if self.command==["NULL"]:
            pseudo_print(f"FATAL ERROR. NO DATA FOUND AT ADDRESS {self.PC}. Perhaps you missed a HALT instruction?")
            self.isRunning=False
            return 0
        elif self.command[0]=="ERROR":
            pseudo_print(f"PARSING ERROR OCCURED. CHECK YOUR CODE IS WRITTEN AND FORMATTED CORRECTLY. LINE {self.PC}")
            self.isRunning=False
            return 0
        elif self.command[0]=="DATA":
            pseudo_print(f"FATAL ERROR. PC ENCOUNTERED A NON INSTRUCTION AND HAS QUIT. LINE {self.PC}")
            #print(self.command,self.PC)
            self.isRunning=False
            return 0
        else: #assume no error
            #print(self.PC) #show location of PC
    
            self.commands[self.command[1][0]](self.command[1][1])

    def run(self):
        global max_runtime
        self.program_run_time_count=0
        while self.isRunning:
            self.fetch_execute_cycle()
            self.program_run_time_count+=1
            if self.program_run_time_count>=max_runtime: #if it's been running for WAY too long. (ten thousand cycles at the moment)
                pseudo_print("YOUR PROGRAM HAS EXCEEDED MAX RUNTIME. NOTE THAT THIS IS A LARGE NUMBER, SO IT IS LIKELY YOU HAVE AN INFINITE LOOP.")
                self.isRunning=False

def run_program(debug_flag,file):
    global output
    temp=program_parser_WEB.getprogramfromfileusingcustomfileextensionbecauseimreallyreallycoolandeveryonelikesme(file)
    program=temp[0]
    main_program=Program(temp[1],debug_flag) #a True value being parsed means debug mode is active
    #pseudo_print(program)
    program_as_an_array=program
    i=0
    #print(program_as_an_array)
    for instruction in program_as_an_array:
        if instruction[0:6]!="ERROR":
            main_program.memory.set(i,instruction)
        i+=1
        #if instruction[0:5]=="LABEL":
        #pseudo_print(instruction)
    #pseudo_print(main_program.memory.memoryArray)
    main_program.run()
    #print(output)
    return output

if __name__=="__main__":
    '''
    debug_flag = input("Input any character to enable debug mode")
    if debug_flag!="":
        debug_flag=True
    else:
        debug_flag=False
    file = "LDR r2,#3"
    print(run_program(debug_flag,file))'''
    print(run_program(True,"MOV r0, #1\nLabelName:\nOUTPUT r0\nB LabelName\n HALT"))