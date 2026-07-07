a = 3
b = 9
c  = False
d = not c
e = 9

print(a>9) # false
print(b==9) # true
print(not(a!=3)) # true
print(not(c)) # True
print((a<c) or c) # False
print(not(a+b!=12)) # True
print((b==5) or ((e>10)and(a<8))) # False
print(((b==5) or ((e>10) and (a<8)) or c) and c) # False


