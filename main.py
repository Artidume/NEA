class Program:
    def __init__(self,max_size=100):
        self.prog_list=[]
        self.size=0
        self.max_size=max_size
        #self.commands is a list of functions and the input to call them. add to this as new functions are added.
        self.commands={
            "add":self.add,
            "sub":self.sub,
            "eq":self.eq,
            "lda":self.lda
        }
        self.prog_list.append("END")
        self.accumulator=0 #general purpose register
    #all functions up to hyphens are to make the Stack for the program work.-----------------
    def push(self,value):
        if not(self.isFull()):
            self.size+=1
            self.prog_list.append(value)
        else:
            return False
    def pop(self):
        if not(self.isEmpty()):
            self.size-=1
            return self.prog_list.pop()
        else:
            return False
    def peek(self):
        return self.prog_list[-1]
    def getSize(self):
        return self.size
    def isEmpty(self):
        if self.size==0:
            return True
        else:
            return False
    def isFull(self):
        if self.size==self.max_size:
            return True
        else:
            return False
    #----------------------------------------------------------------
    #All functions until hyphens are for handling commands
    def performInstruction(self):
        self.operation=self.pop()
        #print(self.operation)
        if self.operation==False:
            return "FAILED INSTRUCTION. IMPROPER SYNTAX"
        self.value=int(self.pop())
        self.commands[self.operation](self.value) #this allows for the operation to be treated as a function! yippee!
    def add(self,x):
        self.accumulator+=x
        print(self.accumulator)
    def sub(self,x):
        self.accumulator-=x
        print(self.accumulator)
    def eq(self,x):
        if self.accumulator==x:
            print("TRUE")
        else:
            print("FALSE")
    def lda(self,x):
        self.accumulator=x
    #-------------------------------------------------------------
    def LOOP(self): #MAIN LOOP. Will run until "END" is encountered.
        self.isRunning=True
        while self.isRunning:
            if self.peek()=="END":
                self.isRunning=False
            else:
                self.performInstruction()
main=Program()
main.push("23")
main.push("eq")
main.push("20")
main.push("add")
main.push("3")
main.push("lda")
main.LOOP()