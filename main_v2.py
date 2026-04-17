#TODO: Debug mode, finish commands, flesh out parser, Online server
class Program:
    def __init__(self,max_size=10000):
        self.main_memory=[]
        for i in range(0,max_size): #initialising MAIN MEM
            self.main_memory.append(bytes(0))
        #init registers, PC, and <flags (TBD)>
        self.isRunning=True
        self.PC=0
        self.r=[0,0,0,0,0,0,0,0,0,0,0,0] #List of registers 1 through 12
        self.cmp_output=0 #Output of compare function. 0=Null, otherwise follows AQA standard.
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
            "HALT":self.HALT
        }
        self.labels={} # Will store key:value pairs of labels and their locations.
    def ADD(self,d,n,operand2):
        self.r[d]=self.r[n]+operand2
    def LDR(self,d,memory_ref):
        self.r[d]=self.main_memory[memory_ref]
    def STR(self,d,memory_ref):
        self.main_memory[memory_ref]=self.r[d]
    def SUB(self,d,n,operand2):
        self.r[d]=self.r[n]-self.main_memory[operand2]
    def MOV(self,d,operand2):
        self.r[d]=operand2
    def CMP(self,n,operand2):
        self.cmp_output=""
        if self.r[n]>operand2:
            self.cmp_output.append("GT NE ")
        elif self.r[n]<operand2:
            self.cmp_output.append("LT NE ")
        elif self.r[n]==operand2:
            self.cmp_output.append("EQ ")
    def B(self,label,condition=0):
        if condition==0:
            self.PC=label
        else:
            if condition.upper()==self.cmp_output: #condition met. .upper() to allow for "eq" and "EQ" to evaluate correctly.
                self.PC=label
    def AND(self,d,n,operand2):
        self.r[d]=self.r[n] & operand2 # & = bitwise and
    def ORR(self,d,n,operand2):
        self.r[d]=self.r[n] | operand2 # | = bitwise or
    def EOR(self,d,n,operand2):
        self.r[d]=self.r[n] ^ operand2 # ^ = bitwise xor
    def MVN(self,d,operand2):
        self.r[d]= ~operand2 # ~ = bitwise not
    def LSL(self,d,n,operand2):
        self.r[d]=self.r[n] << operand2 # << = bitwise shift left
    def LSR(self,d,n,operand2):
        self.r[d]=self.r[n] >> operand2 # >> = bitwise shift right
    def HALT(self):
        self.isRunning=False # will be checked next loop.