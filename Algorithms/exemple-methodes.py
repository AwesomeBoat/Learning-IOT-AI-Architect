"""
Les méthodes se divisent en deux familles:
- Procédures
=> effectuent un traitement mais ne retournent pas de résultats
"""

def print_bonjour():
    print("Bonjour")

"""
- Les fonctions
=> les fcts effectuent un traitement ET retournent un résultat


"""
def sum(a : int, b : int) -> int:
    return a + b, "random scnd element"

summ, other_return = sum(1,5) 

