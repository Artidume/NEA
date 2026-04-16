class Stack:
    def __init__(self,max_size=100):
        self.stack_list=[]
        self.size=0
        self.max_size=max_size
    def push(self,value):
        if self.size<self.max_size:
            self.size+=1
            self.stack_list.append(value)
        else:
            return False
    def pop(self):
        if self.size>0:
            self.size-=1
            return self.stack_list.pop()
        else:
            return False
    def peek(self):
        return self.stack_list[-1]
    def getSize(self):
        return self.size
    def isEmpty(self):
        if self.size==0:
            return True
        return False
    def isFull(self):
        if self.size==self.max_size:
            return True
        else:
            return False

#BELOW IS A TEST.
'''
test_string=input("Input string >>")
s=Stack(len(test_string))
for letter in test_string:
    s.push(letter)

gnirts_tset=""
for i in range(s.getSize()):
    gnirts_tset+=s.pop()

if gnirts_tset==test_string:
    print(f"{test_string} is a palindrome!")
else:
    print(f"{test_string} is NOT a palindrome :(")
'''