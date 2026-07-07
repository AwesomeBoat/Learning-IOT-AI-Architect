# // Avoir un tableau d'entrée
# // iterate each element (n) of the array
#     // Check if it's last element
#         // put the value to index 0 and continue
#     // Save the n+1 index 
#     // Assign the n+1 index with the current element


array_to_rotate=[1,2,3,4,5,6,7,8,9]

# for element in array_to_rotate:
#     curr_index = array_to_rotate.index(element)
#     if curr_index==len(array_to_rotate)-1:
#         array_to_rotate[0], array_to_rotate[curr_index]= element, array_to_rotate[0]
#         array_to_rotate[curr_index]=element
#         continue
#     next=array_to_rotate[curr_index+1]
#     array_to_rotate[curr_index]=element

# print(array_to_rotate)

array_to_rotate = array_to_rotate[-1:] + array_to_rotate[:-1]

print(array_to_rotate)

array2=[1,2,3,4,5]