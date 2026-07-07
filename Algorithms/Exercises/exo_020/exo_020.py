# exo19-À l’aide de la boucle TantQue … Faire, réalisez un algorithme calculant le 
# résultat de N10. N étant un nombre saisi par l’utilisateur



print("Welcome to the ^10 calculator")
input_number = int(input("Enter a number: "))
input_exponent = int(input("Enter the exponent number: "))
n=0
new_number = input_number

while n < input_exponent - 1:
    new_number *= input_number
    n += 1

print(new_number)   