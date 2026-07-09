#NOTE: I am using ".aqasm" as my file extension. Only because its fun. it is a portmanteau of aqa and asm.
def find_type(operand):
    try:
        int(operand)
        isInt=True
        return "DIRECT"
    except:
        if operand[0]=="#":
            try:
                int(operand[1:])
                return "IMMEDIATE"
            except:
                return "WHAT. NO. STOP THAT."
        if operand[0].upper()=="R":
            try:
                int(operand[1:])
                return "REGISTER"
            except:
                return "WHAT. NO. STOP THAT."


def parse(line,line_number):
    global labels
    #print(labels)
    if line=="":
        #print(line,"EMPTY")
        return None,False
    try:
        stage_2_output=[]
        label=None
        line=line.replace("\n"," ").strip() #remove trailing line break
        #print(line) show line after initial string formatting
        
        splitted=line.split(" ",1) #splits into opcode and operand in the form ["opcode","operands"] 
        opcode=splitted[0].upper().strip()
        #print(opcode)
        if opcode=="MEM": #MEM is a pseudo-instruction to place data in memory. 
            operands=splitted[1]
            operands=operands.strip().split(",") #separates using ", ". now each operand is distinct.
            #print("ARGH 2!")
            #print(f"operands {operands}")
            if find_type(operands[0]) != "DIRECT":
                    return "ERROR: MEM OPERAND1 MUST BE DIRECT"
            
            if find_type(operands[1])!="IMMEDIATE":
                return "ERROR: MEM OPERAND 2 MUST BE IMMEDIATE"
            else:
                return ["MEM",[operands[0],[operands[1][1:]]]],False
        if opcode=="HALT":
            return ["INSTRUCTION",["HALT",[]]],False #exit parser. empty array used as empty "operands"
        if opcode[0]!="B" and opcode[0]!="MEM":
            stage_2_output.append(opcode) #write the opcode to the line
        elif opcode[0]=="B":
            stage_2_output.append(opcode[0])   
        



        operands=splitted[1] #need to split from str to list   
        #THIS CHECKS FOR WHETHER IT IS BRANCHING TO A LABEL.

        if operands in labels and opcode[0]=="B": #if this is a branch instruction, and it is branching to a label,
            #print("branch insctructions",line)
            label = operands
            decoded_operands=[]
            decoded_operands.append(labels.get(label)) #replace label with its location in memory 
            #print(decoded_operands)
            #print(len(opcode))

            if len(opcode)==1: #if its just "B", no condition
                decoded_operands.append("NO CONDITION")
                #print(decoded_operands)

            else: #implies condition exists
                condition = opcode[1::]
                #print(condition)
                if condition in ["EQ","GT","LT","NE"]: #if valid condition
                    decoded_operands.append(condition)

                else:
                    
                    return "ERROR: Invalid condition. The conditions are:\nEQ - Equal to \nGT - Greater Than\nLT - Less Than\nNE - Not Equal To"

            return ["INSTRUCTION",["B",decoded_operands]], False
        
        

        

        #print(opcode) #show opcode in terminal
        operands=operands.strip().split(",") #separates using ", ". now each operand is distinct.
        #print(operands)


        for i in range(len(operands)):
            operands[i]=operands[i].strip() #remove whitespace from either side of operand (" r1 " -> "r1")
            #print(operands[i])
        decoded_operands=[]
        address_modes=[] #an array of the address modes of each operand, which will be appended at the end of the instruction
        #print(operands)
        for operand in operands:
            #print(operand)
            try: #checking if characters after 1st are integers (i.e r3, #25, etc)
                if isinstance(int(operand[1:]),int): #hacky solution
                    theRestIsNumber=True
            except:
                theRestIsNumber=False
            finally:
                try:
                    int(operand)
                    operand_is_int = True
                except:
                    operand_is_int = False




                if operand_is_int: #if it is only a number, it will have no starting "#","r", which would cause it to error. this fixes this problem.
                    address_modes.append("DIRECT")
                    decoded_operands.append(int(operand))
                    #print("direct")
                elif operand[0]=="#": #using immediate addressing (immediate uses the value immediately)
                    address_modes.append("IMMEDIATE")  #add type of operand
                    decoded_operands.append(int(operand[1::])) #add operand
                    #print("immediate")
                elif (operand[0]=="r" or operand[0]=="R") and theRestIsNumber: #operand is a register
                    address_modes.append("REGISTER") #add type of operand
                    decoded_operands.append(int(operand[1::])) #add operand
                else: #assume it is a label
                    address_modes.append("LABEL")
                    print(f"The program thinks {operand} is a label.")
                    decoded_operands.append(operand) #append it as a string, since that will be what will be called
        #print(decoded_operands)
        if opcode[0]!="B":
            for optype in address_modes: #optype means the type of the operand. not standard 
                decoded_operands.append(optype)
        
        if opcode[0]=="B":
            #print("b_eez unts")
            #print(line,":",operand,":",opcode)
            if len(opcode)==1: #if its just "B", no condition
                decoded_operands[1]="NO CONDITION"
            else: #implies condition exists
                condition = opcode[1::]
                #print(condition)
                if condition in ["EQ","GT","LT","NE"]: #if invalid condition
                    decoded_operands.append(condition)
                else:

                    return "FATAL ERROR: Invalid condition. The conditions are:\nEQ - Equal to \nGT - Greater Than\nLT - Less Than\nNE - Not Equal To"
        

        stage_2_output.append(decoded_operands)
        return ["INSTRUCTION",stage_2_output],False
        #print(output)
    except:
        #print(splitted)
        #print(f"Es gibt ein Fehler: {operand}")
        if len(line.strip())==0:
            return ["DATA",0],False
        if len(splitted)==0:
            print(f"FATAL ERROR: Command written incorrectly. Check for whitespace characters like a space.")
        return "ERROR: Parsing"

def getLabels(label_f):
    line_number=0
    labels={}
    for label in label_f:
        label=label.strip()
        if label[-1:]==":": #assume label
            #print("THIS LINE IS A LABEL")
            #print(line_number)

            stage_2=label[0:len(label)-1].strip() #get all of opcode, except for ":". .strip() removes whitespace
            labels.update({stage_2:line_number})
        line_number+=1
    #print(labels)
    return labels

def getprogramfromfileusingcustomfileextensionbecauseimreallyreallycoolandeveryonelikesme(file):
    program=[]
    global labels
    labels={}
    if file != False:
        f=file.split("\n")
        #print(f)
        line="placeholder"
        line_number=0
        labels=getLabels(f)
        i=0
        while line != (None,False) and line[0:6]!="ERROR":
            try:
                readline=f[i]
                i+=1
            except:
                readline=None
            if readline==None:
                line=(None,False)
            else:
                line=parse(readline,line_number)

                if line != (None,False) and line!="ERROR" and line[1]==False:
                    program.append(line[0])
                if type(line)==str:
                    program.append(line)
                line_number+=1
    else:
        with open("program.aqasm","r") as f:
            line="placeholder that doesn't matter"
            line_number=0
            while line != (None,False) and line!="ERROR":
                readline=f.readline()
                line=parse(readline,line_number)
                #print(line)
                if line != (None,False) and line!="ERROR" and line[1]==False:
                    program.append(line[0])
                elif line != (None,False): #assume it is a label
                    #print(line[1])
                    labels.update({line[0]:line_number})
                line_number+=1
    if line!="ERROR":
        #print(program)
        #print(labels)
        return program,labels
    else:
        return "ERROR"


if __name__ =="__main__":
    print(getprogramfromfileusingcustomfileextensionbecauseimreallyreallycoolandeveryonelikesme("MEM 100,220\nOUTPUT 100\nHalt")) #test <OUTPUT #2\nB labelname \n HALT\n jjjj \n labelname: \n OUTPUT labelname \n HALT\n>

    #getLabels("Label1:\nLabel2:\nLabel3 :\n") test for getLabels(). Should produce {"Label1": 0, "Label2": 1, "Label3": 2}