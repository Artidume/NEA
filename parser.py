def parse_line(line):
    print(line)
    for char in line:

with open("program.aqasm","r") as f:
    program=[]
    line=f.readline().replace("\n","")
    parse_line(line)
    while line!="":
        program.append(line)
        line=f.readline().replace("\n","")


print(program)