#NOTE: I am using ".aqasm" as my file extension. Only because its fun. it is a portmanteau of aqa and asm.
def parse(line,line_number):
    global labels
    if line=="":
        #print(line,"EMPTY")
        return None,False
    try:
        #print(line)
        stage_2_output=[]
        label=None
        line=line.replace("\n"," ").strip() #remove trailing line break
        #print(line) show line after initial string formatting
        if line[-1:]==":": #assume it is a label. -1: means get the last character of the line
            #print(line[:len(line)-1])
            label = line[:len(line)-1] #remove last character of line
            return label,True #True works to check if this is a label. No other output should be True
        splitted=line.split(" ",1) #splits into opcode and operand in the form ["opcode","operands"] 
        opcode=splitted[0]
        
        if opcode=="HALT":
            return ["INSTRUCTION",["HALT",[]]],False #exit parser. empty array used as empty "operands"
        if opcode[0]!="B":
            stage_2_output.append(opcode) #write the opcode to the line
        else:
            stage_2_output.append(opcode[0])   
        operands=splitted[1] #need to split from str to list   
        #THIS CHECKS FOR WHETHER IT IS BRANCHING TO A LABEL.
        if operands in labels and opcode[0]=="B": #if this is a branch instruction, and it is branching to a label,
            label = operands
            decoded_operands=[labels.get(label)] #replace label with its location in memory 
            if len(opcode)==1: #if its just "B", no condition
                decoded_operands[1]="NO CONDITION"

            else: #implies condition exists
                condition = opcode[1::]
                #print(condition)
                if condition in ["EQ","GT","LT","NE"]: #if invalid condition
                    decoded_operands.append(condition)

                else:
                    print("FATAL ERROR: Invalid condition. The conditions are:\nEQ - Equal to \nGT - Greater Than\nLT - Less Than\nNE - Not Equal To")
                    return ["ERROR","ERROR: Branch command"],False
            return ["INSTRUCTION",["B",decoded_operands]], False

        

        #print(opcode) #show opcode in terminal
        operands=operands.strip().split(",") #separates using ", ". now each operand is distinct.



        for i in range(len(operands)):
            operands[i]=operands[i].strip() #remove whitespace from either side of operand (" r1 " -> "r1")
            #print(operands[i])
        decoded_operands=[]
        address_modes=[] #an array of the address modes of each operand, which will be appended at the end of the instruction
        for operand in operands:
            #print(operand) #show current operand
            try: #this handles whether we are using r2 or rLABELNAME. hacky solutions ftw
                int(operand[1:])
                if operand[0] in ["1","2","3","4","5","6","7","8","9","0"]:
                    operand=int(operand)
                #print(operand,type(operand))
                theRestIsNumber=True
            except:
                theRestIsNumber=False
            if operand[0]=="#": #using immediate addressing (immediate uses the value immediately)
                address_modes.append("IMMEDIATE")  #add type of operand
                decoded_operands.append(int(operand[1::])) #add operand
            elif (operand[0]=="r" or operand[0]=="R") and theRestIsNumber: #operand is a register
                address_modes.append("REGISTER") #add type of operand
                decoded_operands.append(int(operand[1::])) #add operand
            elif theRestIsNumber:
                address_modes.append("DIRECT")
                decoded_operands.append(int(operand))
            else: #assume it is a label
                address_modes.append("LABEL")
                decoded_operands.append(operand) #append it as a string, since that will be what will be called

        if opcode[0]!="B":
            for optype in address_modes: #optype means the type of the operand. not standard 
                decoded_operands.append(optype)
        
        if opcode[0]=="B":
            if len(opcode)==1: #if its just "B", no condition
                decoded_operands[1]="NO CONDITION"
            else: #implies condition exists
                condition = opcode[1::]
                #print(condition)
                if condition in ["EQ","GT","LT","NE"]: #if invalid condition
                    decoded_operands.append(condition)
                else:
                    print("FATAL ERROR: Invalid condition. The conditions are:\nEQ - Equal to \nGT - Greater Than\nLT - Less Than\nNE - Not Equal To")
                    return ["ERROR","ERROR: Branch command"],False

        stage_2_output.append(decoded_operands)
        return ["INSTRUCTION",stage_2_output],False
        #print(output)
    except:

        if len(line.strip())==0:
            return ["DATA",0],False
        if len(splitted)==0:
            print(f"FATAL ERROR: Command written incorrectly. Check for whitespace characters like a space.")
        return ["ERROR","ERROR: Parsing"],False

def getprogramfromfileusingcustomfileextensionbecauseimreallyreallycoolandeveryonelikesme():
    program=[]
    global labels
    labels={}
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
        return program
    else:
        return "ERROR"


if __name__ =="__main__":
    print(getprogramfromfileusingcustomfileextensionbecauseimreallyreallycoolandeveryonelikesme()) #test
    #getprogramfromfileusingcustomfileextensionbecauseimreallyreallycoolandeveryonelikesme()