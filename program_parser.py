#NOTE: I am using ".aqasm" as my file extension. Only because its fun. it is a portmanteau of aqa and asm.
def parse(line):
    if line=="":
        #print(line,"EMPTY")
        return None
    try:
        #print(line)
        stage_2_output=[]
        line=line.replace("\n"," ") #remove trailing line break
        splitted=line.split(" ",1) #splits into opcode and operand in the form ["opcode","operands"] 
        opcode=splitted[0]
        if opcode=="HALT":
            return ["INSTRUCTION",["HALT",[]]] #exit parser. empty array used as empty "operands"
        if opcode[0]!="B":
            stage_2_output.append(opcode) #write the opcode to the line
        else:
            stage_2_output.append(opcode[0])
        operands=splitted[1] #need to split from str to list
        
        #print(opcode) #show opcode in terminal
        operands=operands.strip().split(",") #separates using ", ". now each operand is distinct.
        
        for i in range(len(operands)):
            operands[i]=operands[i].strip() #remove whitespace from either side of operand (" r1 " -> "r1")
            #print(operands[i])
        decoded_operands=[]
        address_modes=[] #an array of the address modes of each operand, which will be appended at the end of the instruction
        for operand in operands:
            #print(operand) #show current operand
            if operand[0]=="#": #using immediate addressing (immediate uses the value immediately)
                address_modes.append("IMMEDIATE")  #add type of operand
                decoded_operands.append(int(operand[1::])) #add operand
            elif operand[0]=="r" or operand[0]=="R": #operand is a register
                address_modes.append("REGISTER") #add type of operand
                decoded_operands.append(int(operand[1::])) #add operand
            else: #if neither of these, assume direct addressing (pointing to in memory)
                address_modes.append("DIRECT")
                decoded_operands.append(int(operand))
            
            

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
                    return ["ERROR","ERROR: Branch command"]

        stage_2_output.append(decoded_operands)
        return ["INSTRUCTION",stage_2_output]
        #print(output)
    except:
        if len(line.strip())==0:
            return ["DATA",0]
        if len(splitted)==0:
            print(f"FATAL ERROR: Command written incorrectly. Check for whitespace characters like a space.")
        return ["ERROR","ERROR: Parsing"]

def getprogramfromfileusingcustomfileextensionbecauseimreallyreallycoolandeveryonelikesme():
    program=[]
    with open("program.aqasm","r") as f:
        line="placeholder that doesn't matter"
        while line is not None and line!="ERROR":
            readline=f.readline()
            line=parse(readline)
            if line is not None and line!="ERROR":
                program.append(line)
    if line!="ERROR":
        return program
    else:
        return "ERROR"


if __name__ =="__main__":
    print(getprogramfromfileusingcustomfileextensionbecauseimreallyreallycoolandeveryonelikesme()) #test
    #getprogramfromfileusingcustomfileextensionbecauseimreallyreallycoolandeveryonelikesme()