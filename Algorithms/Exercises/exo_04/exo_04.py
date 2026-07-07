# Algorithme inversionTwoVar
# DEBUT
#     Variable a, b : Entier
#     a = a * b / b 
#     b = a * b / a
    
# FIN

a = 5
b = 7

a = a + b
b = a - b
a = a - b
print(f"The value of a is : {a}, value of b is : {b}")