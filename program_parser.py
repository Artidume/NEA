#NOTE: I am using ".aqasm" as my file extension. Only because its fun. is a portmanteau of aqa and asm.
def parse(line,line_number):
    if line=="":
        return None
    try:
        output=[]
        line=line.replace("\n"," ") #remove trailing line break
        splitted=line.split(" ",1) #splits into opcode and operand in the form ["opcode","operands"] 
        opcode=splitted[0]
        if "B" not in opcode:
            output.append(opcode) #write the opcode to the line
        else:
            output.append(opcode[0])
        if opcode=="HALT":
            return ["HALT",[]] #exit parser. empty array used as empty "operands"
        operands=splitted[1] #need to split from str to list
        operands=operands.split(", ") #separates using ", ". now each operand is distinct.
        decoded_operands=[]
        #print(operands)
        for operand in operands:
            #print(operand)

            if operand[0]=="#": #using immediate addressing (value given, not in memory)
                address_mode="IMMEDIATE"
            elif operand[0]=="r" or operand[0]=="R": #check for lowercase and uppercase
                address_mode="register"
            else: #assume direct (value taken from memory address pointed to with operand)
                address_mode="DIRECT"

            #print(address_mode)
            if address_mode=="register":
                decoded_operands.append(int(operand[1::])) #skips first character of operand, to get only the number
                #print(decoded_operands)
            elif operand[0]=="#":
                decoded_operands.append(int(operand[1::])) #skips first character of operand, to get only the number
            else: #assumer int with no gubbins
                decoded_operands.append(int(operand))
        
        if opcode[0]!="B":
            #print(address_mode)
            decoded_operands.append(address_mode) #done at the end to match with main.py   
        
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
                    return False

        output.append(decoded_operands)
        return output
        #print(output)
    except:
        if len(splitted)==0:
            print(f"FATAL ERROR: Command written incorrectly at line {line_number}. Check for whitespace characters like a space.")
        return "ERROR"

def getprogramfromfileusingcustomfileextensionbecauseimreallyreallycoolandeveryonelikesme():
    program=[]
    with open("program.aqasm","r") as f:
        line=parse(f.readline(),0)
        line_number=1
        while line is not None and line!="ERROR":
            program.append(line)
            line=parse(f.readline(),line_number)
            line_number+=1
    if line!="ERROR":
        return program
    else:
        return "ERROR"
#print(getprogramfromfileusingcustomfileextensionbecauseimreallyreallycoolandeveryonelikesme()) #test
