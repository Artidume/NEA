import program_parser_WEB
global output
output=""
global max_runtime #This will be the max number of lines that can be executed by a program. Change as desired. 
max_runtime=10000

def pseudo_print(string): #highjacking the print statement to simply write to a larger output feels so funky
    global output
    global running_locally
    if output!="":
        if running_locally:
            output+="\n"
        else:
            output+="☃" #magic ascii character which I am using to represent a newline. Gets replaced in the HTML using Django.
    output += (str(string))

def format_b(number): #the only reason I made this is because when formatting a number to binary, it does not have trailing 0s.
    output=format(number,"b")
    temp_output="0"*(8-len(output)) #remember that a byte has 8 bits (tf length is 8)
    if temp_output!="": #if there are leading 0s
        output=temp_output+output #add them to the start of the number
    return output
'''
TODO:
- MOV: re-read and ensure valid DONE!
- CMP: re-read and ensure valid
- B: re-read and ensure valid. Should be working.
- AND: write DONE!
- ORR: write DONE!
- EOR: write DONE!
- MVN: write DONE!
- LSL: write DONE!
- LSR: write DONE!

- DEBUG MODE:
. Go back over and ensure error message are understandable for the user.

- CRASH HANDLER:
. Have a fatal error ACTUALLY crash the program, and not continue runtime. should be simple.

The other instructions seem to be working fine. The parser also functions as intended.

'''
'''NOTE:
    - Pivotted to Von Neumann architecture, worth it to closer mimic original design.
    - This may change in the future, and if so, DELETE THIS MESSAGE.
    - Increment this for every hour wasted not writing anything >> 3  
    - ALSO NOTE. AFTER LOOKING THROUGH ALL AVAILABLE PAST PAPERS FOR AQA VIA https://www.physicsandmathstutor.com/past-papers/a-level-computer-science/ 
      , I HAVE FOUND NO MENTION OF BITWISE NOT, AND ALSO NO MENTION OF THE USE OF NEGATIVE NUMBERS, BESIDES COMPARING THEM WITH 0. DUE TO THIS, I HAVE
      CHOSEN TO NOT IMPLEMENT NEGATIVE NUMBERS DURING BITWISE INSTRUCTIONS (i.e take them as unsigned, during bitwise arithmetic). THIS IS MAYBE SILLY,
      BUT IT HAS NOT ONCE BEEN REQUIRED DURING AN EXAM, AND SINCE THIS PROJECT AIMS TO HELP PEOPLE WITH THEIR EXAMS, I SEE NO NEED TO TEACH THEM SOMETHING
      THEY DO NOT NEED TO KNOW. THANKYOU. :)
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
        #print(self.memoryArray) #show all of memory
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
            if operands[1]<self.memory.length-1 and operands[0]<13: #if location does not exceed memory, and if the register is a valid register
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
            if self.debug_mode:
                pseudo_print(f"VALUE AT MEMORY LOCATION {operands[2]}: {self.value}") #show value which has been fetched
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
            pseudo_print(f"OPERANDS FOR SUB INSTRUCTION: {operands[0]}:{operands[3]},{operands[1]}:{operands[4]},{operands[2]}:{operands[5]}")

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
        if operands[5]=="IMMEDIATE":
            self.value=operands[2]
        if operands[5]=="DIRECT":
            self.value=self.memory.fetch_data(operands[2])
        if operands[5]=="REGISTER":
            if operands[2]>12:
                pseudo_print(f"FATAL ERROR AT LINE {self.PC}. THE REGISTER IN <operand2> MUST BE A VALID REGISTER.")
            self.value=self.r[operands[2]]
        
        if self.debug_mode:
            pseudo_print(f"VALUE FOUND: {self.value}")
        
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
        elif operands[3]=="DIRECT": #this isn't supported by original spec.
            pseudo_print(f"ERROR AT LINE {self.PC}. THE MOV INSTRUCTION DOES NOT SUPPORT DIRECT MEMORY ACCESS IN THE AQA SPECIFICATION.")
            self.isRunning=False
        elif operands[3]=="REGISTER":
            self.r[operands[0]]=self.r[operands[1]]
        if self.debug_mode:
            pseudo_print(f"RESULT: r{operands[0]} = {self.r[operands[0]]}")
        
    def CMP(self,operands): #(n,operand2,optype1,optype2)
        #note on cmp_output. It stores all flags (GT, LT, NE, etc) in one string, separated by spaces. 
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

    def AND(self,operands): #(d,n,operand2,!!optype1,optype2,optype3!!)
        if self.debug_mode:
            pseudo_print(f"OPERANDS FOR AND INSTRUCTION: {operands}")
        if operands[3]!="REGISTER":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. AND instruction operand d must be a register.")
            self.isRunning=False
        if operands[4]!="REGISTER":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC} AND instruction operand n must be a register.")
            self.isRunning=False
        if operands[5]=="DIRECT":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC} AND instruction does not support direct addressing, according to the specification.")
            self.isRunning=False
        if self.isRunning==False: #if crash
            self.value=0 #exclusively here so that the program doesn't blow up.
        
        if self.isRunning: #if haven't already crashed
            if operands[2]<0 or self.r[operands[0]]<0 or self.r[operands[1]]<0: 
                pseudo_print(f"FATAL ERROR AT LINE {self.PC}. Negative numbers are not known to be supported in the AQA Specification during assembly code, so they have not been implemented.")
                self.isRunning=False

        if operands[5]=="IMMEDIATE":
            self.value=operands[2]
        elif operands[5]=="REGISTER":
            self.value=self.r[operands[2]]
        self.r[operands[0]]=self.r[operands[1]] & self.value # & = bitwise and
        if self.debug_mode:
            if self.isRunning:
                pseudo_print(f"r{operands[0]}={self.r[operands[0]]}. r{[operands[1]]} ({self.r[operands[1]]},{format_b(self.r[operands[1]])}) & value ({self.value},{format_b(self.value)}) = {self.r[operands[0]]} ({format_b(self.r[operands[0]])})")

    def ORR(self,operands): #(d,n,operand2,!!optype1,optype2,optype3!!)#
        if self.debug_mode:
            pseudo_print(f"OPERANDS FOR ORR INSTRUCTION: {operands}")
        if operands[3]!="REGISTER": #if d is not a register
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. AND instruction operand d must be a register.")
            self.isRunning=False
        if operands[4]!="REGISTER":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. AND instruction operand n must be a register.")
            self.isRunning=False
        if operands[5]=="DIRECT": #not supported by spec
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. AND instruction operand <operand2> cannot be direct addressing memory. It is not supported by AQA Specification.")
        if self.isRunning==False:
            self.value=0
        else:
            if operands[2]<0 or self.r[operands[0]]<0 or self.r[operands[1]]<0:
                pseudo_print(f"FATAL ERROR AT LINE {self.PC}. Negative numbers are not known to be supported by the AQA Specification during assembly coding, so have not been implemented.")
                self.isRunning=False
        if operands[5]=="REGISTER":
            self.value=self.r[operands[2]]
        elif operands[5]=="IMMEDIATE":
            self.value=operands[2]
        self.r[operands[0]]=self.r[operands[1]] | self.value # | = bitwise or
        if self.debug_mode and self.isRunning:
            pseudo_print(f"r{operands[0]} = {self.r[operands[0]]}. r{operands[1]} ({self.r[operands[1]]},{format_b(self.r[operands[1]])}) | value ({self.value},{format_b(self.value)}) = {self.r[operands[0]]} ({format_b(self.r[operands[0]])})")
    
    def EOR(self,operands): #(d,n,operand2,!!optype1,optype2,optype3!!)
        if self.debug_mode:
            pseudo_print(f"OPERANDS FOR EOR INSTRUCTION: {operands}")
        if operands[3]!="REGISTER":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. EOR instruction operand d must be a register.")
            self.isRunning=False
        if operands[4]!="REGISTER":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. EOR instruction operand n must be a register.")
            self.isRunning=False
        if operands[5]=="DIRECT":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. <operand2> can not be direct, according to AQA Specification.")
            self.isRunning=False
            self.value=0 #just.. ignore it.
        if self.isRunning: #haven't yet crashed
            if self.r[operands[0]]<0 or self.r[operands[1]]<0 or operands[2]<0:
                pseudo_print(f"FATAL ERROR AT LINE {self.PC}. Negative numbers are not known to be supported by the AQA Specification, so have not been implemented.")
        if operands[5]=="IMMEDIATE":
            self.value=operands[2]
        elif operands[5]=="REGISTER":
            self.value=self.r[operands[2]]
        self.r[operands[0]]=self.r[operands[1]] ^ operands[2] # ^ = bitwise xor
        if self.debug_mode and self.isRunning:
            pseudo_print(f"r{operands[0]} = {self.r[operands[0]]}. r{operands[1]} ({self.r[operands[1]]},{format_b(self.r[operands[1]])}) ^ value ({self.value},{format_b(self.value)}) = {self.r[operands[0]]} ({format_b(self.r[operands[0]])})")

    def MVN(self,operands): #(d,operand2,!!optype1,optype2!!)
        if self.debug_mode:
            pseudo_print(f"OPERANDS FOR MVN INSTRUCTION: {operands}")
        if operands[2]!="REGISTER":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. MVN instruction operand d must be a register.")
            self.isRunning=False
        if operands[3]=="DIRECT":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. MVN instruction operand <operand2> can not be directly addressing memory.")
            self.isRunning=False
        if operands[3]=="IMMEDIATE":
            self.value=operands[1]
        elif operands[3]=="REGISTER":
            self.value=self.r[operands[1]]
            
        self.value=format_b(self.value) #convert to binary
        self.output=""
        for digit in self.value: #bitwise not
            if digit=="1":
                self.output+="0"
            elif digit=="0":
                self.output+="1"

        #convert back to denary
        '''
        2^7 , 2^6, 2^5, 2^4, 2^3, 2^2, 2^1, 2^0 (2^counter)
        - Reverse list
        remembering that digit is either 1 or 0,
        - loop through, +counter per loop through, add digit*2^counter to sum
        - return sum
        '''
        self.counter=0
        self.r_value=0
        for digit in self.output[::-1]: #[::-1] reverses the list
            self.r_value+=int(digit)*(2**(self.counter))
            self.counter+=1
        self.r[operands[0]]=self.r_value


        if self.debug_mode and self.isRunning:
            pseudo_print(f"r{operands[0]}={self.r[operands[0]]}. ~ {operands[1]} ({format_b(operands[1])}) = {self.r_value} ({format_b(self.r_value)}) ")

    def LSL(self,operands): #(d,n,operand2,!!optype1,optype2,optype3!!)
        if self.debug_mode:
            pseudo_print(f"OPERANDS FOR LSL INSTRUCTION: {operands}")
        if operands[3]!="REGISTER":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. LSL instruction operand d must be a register.")
            self.isRunning=False
        if operands[4]!="REGISTER":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. LSL instruction operand n must be a register.")
            self.isRunning=False
        if operands[5]=="DIRECT":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. LSL instruction operand <operand2> can not be directly addressing memory.")
            self.isRunning=False
        if operands[5]=="REGISTER":
            self.value=self.r[operands[2]]
        elif operands[5]=="IMMEDIATE":
            self.value=operands[2]
        
        if operands[0]==operands[1]: 
            self.temp_register=self.r[operands[0]]

        #bitwise shift left
        self.number = str(format_b(self.r[operands[1]]))
        for i in range(0,self.value): #shift "value" many times
            self.number+="0"
        self.number=self.number[-8:] #solution courtesy of https://www.geeksforgeeks.org/python/python-get-last-n-characters-of-a-string/ . I was considering using a while loop and a bunch of logic, but this is just plain faster.
        
        #convert number back to denary
        self.counter=0
        self.output=0
        for digit in self.number[::-1]:
            self.output+=int(digit)*(2**self.counter)
            self.counter+=1

        self.r[operands[0]]=self.output
        if self.debug_mode and self.isRunning:
            if operands[0]==operands[1]:
                pseudo_print(f"r{operands[0]}={self.r[operands[0]]}.  r{operands[1]} ({self.temp_register},{format_b(self.temp_register)}) << {self.value} = {self.r[operands[0]]} ({format_b(int(self.r[operands[0]]))}) ")
                
            else:
                pseudo_print(f"r{operands[0]}={self.r[operands[0]]}.  r{operands[1]} ({self.r[operands[1]]},{format_b(self.r[operands[1]])}) << {self.value} = {self.r[operands[0]]} ({format_b(int(self.r[operands[0]]))}) ")

    def LSR(self,operands): #(d,n,operand2 !!address_type1,address_type2,address_type3!!)
        if self.debug_mode:
            pseudo_print(f"OPERANDS FOR LSR INSTRUCTION: {operands}")
        if operands[3]!="REGISTER":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. LSR instruction operand d must be a register.")
            self.isRunning=False
        if operands[4]!="REGISTER":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. LSR instruciton operand n must be a register.")
            self.isRunning=False
        if operands[5]=="DIRECT":
            pseudo_print(f"FATAL ERROR AT LINE {self.PC}. LSR instruction operand <operand2> cannot directly access memory.")
            self.isRunning=False
        if operands[5]=="REGISTER":
            self.value=self.r[operands[2]]
        elif operands[5]=="IMMEDIATE":
            self.value=operands[2]
        
        if operands[0]==operands[1]: 
            self.temp_register=self.r[operands[0]]

        #bitwise shift right
        self.number=str(format_b(self.r[operands[1]]))
        self.number="0"*self.value+self.number #put on leading 0s
        self.number=self.number[:8] #this one, I actually figured out myself

        #convert number back to denary
        self.counter=0
        self.output=0
        for digit in self.number[::-1]:
            self.output+=int(digit)*(2**self.counter)
            self.counter+=1

        self.r[operands[0]]=self.output
        if self.debug_mode and self.isRunning:
            if operands[0]==operands[1]:
                pseudo_print(f"r{operands[0]}={self.r[operands[0]]}.  r{operands[1]} ({self.temp_register},{format_b(self.temp_register)}) >> {self.value} = {self.r[operands[0]]} ({format_b(int(self.r[operands[0]]))}) ")
                
            else:
                pseudo_print(f"r{operands[0]}={self.r[operands[0]]}.  r{operands[1]} ({self.r[operands[1]]},{format_b(self.r[operands[1]])}) >> {self.value} = {self.r[operands[0]]} ({format_b(int(self.r[operands[0]]))}) ")
        
    
    def HALT(self,operands):
        self.isRunning=False
    def OUTPUT(self,operands):
        if self.debug_mode:
            pseudo_print(f"OPERANDS FOR OUTPUT INSTRUCTION: {operands}")
        if operands[1]=="REGISTER":
            print(self.r[operands[0]])
            pseudo_print(self.r[operands[0]])
        elif operands[1]=="IMMEDIATE":
            pseudo_print(operands[0])
        elif operands[1]=="DIRECT":
            print(operands)
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
        elif self.command[0]=="LABEL":
            pass
        else: #assume no error
            #print(self.PC) #show location of PC
            #print(f"COMMAND {self.command}")
            if self.command[0]=="MEM": #skip MEM instruction
                pass
            else:
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
    output=""
    program_decompiled=program_parser_WEB.getprogramfromfileusingcustomfileextensionbecauseimreallyreallycoolandeveryonelikesme(file) #[(PROGRAM),(Labels)]
    program=program_decompiled[0]
    main_program=Program(program_decompiled[1],debug_flag) #debug_flag True -> debug mode is on.

    program_as_an_array=program
    i=0

    for instruction in program_as_an_array:
        if type(instruction)!=str: #The only way the instruction should be a string is if there is an error (as errors report as "ERROR: .....", which is a string)
            if instruction[0]=="MEM":
                
                main_program.memory.set(int(instruction[1][0]),["DATA",instruction[1][1][1:]])
            main_program.memory.set(i,instruction)
        else: #if parser finds an error
            output=instruction+f" (at line {i})" 
            return output #quit before execution
        i+=1
        #if instruction[0:5]=="LABEL":
        #pseudo_print(instruction)
    pseudo_print(main_program.memory.memoryArray)
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
    
    global running_locally
    running_locally=True
    print(run_program(True,"MOV r1,#25\nMOV r2,#3\n LSR r1,r1,r2\nOUTPUT r1\nB END\nEND:\nOUTPUT #360\nHALT"))