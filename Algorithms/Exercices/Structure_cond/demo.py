# variable age: Entier
# age = 30
# SI age >= 18 ET age < 67 ALORS
#     Ecrire("adulte")
# SINONSI age < 18 ALORS
#     Ecrire("enfant")
# SINON
#     Ecrire("retraité")
# FINSI

age = 30

# if age >= 18 and age < 67:
if 18 <= age < 67:
    print("adulte")
elif age < 18:
    print("enfant")
else: 
    print("retraité")


