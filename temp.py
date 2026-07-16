'''
def format_b(number): #the only reason I made this is because when formatting a number to binary, it does not have trailing 0s.
    output=format(number,"b")
    temp_output="0"*(8-len(output)) #remember that a byte has 8 bits (tf length is 8)
    if temp_output!="": #if temp_output has done anything
        output=temp_output+output #add it to the beginning of the output
    return output
value=format_b(int(input("input number to do Funky Shit to >>")))
output=""
for digit in value:
    if digit=="1":
        output+="0"
    elif digit=="0":
        output+="1"
#convert back to denary
counter=0
r_value=0    
for digit in output[::-1]: #[::-1] reverses the list
    r_value+=int(digit)*(2**(counter))
    counter+=1
print(r_value)
'''
number=input("input binary number pls")
shift=int(input("input shift amount"))
number="0"*shift+number
number=number[:8]
print(number)