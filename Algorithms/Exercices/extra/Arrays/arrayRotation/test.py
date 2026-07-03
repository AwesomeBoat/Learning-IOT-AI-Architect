myArray = [0,1,2,3,4,5]

# print(myArray[-1:]) #5

# print(myArray[:1]) #0

# print(myArray[:3]) # 0,1,2
# print(myArray[:-2]) # 0, 5,  ? 
# print(myArray[:5]) # 0,1,2,3,4
# print(myArray[5:]) # []
# print(myArray[2:]) # 3,4,5
# print(myArray[-2:]) # 4,5 ?



# print(myArray[-3:])


print(myArray[-2::])

# myArray[start:stop:step]

print(list(reversed(myArray)))
