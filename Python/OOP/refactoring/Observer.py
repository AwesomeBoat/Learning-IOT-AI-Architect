# ALLER VOIR SUR REFACTOR GURU

# EXEMPLE D'OBSERVEUR : 

class Interrupteur:
    def __init__(self):
        self.ampoules = []
        self.actif = False
 
    def connecter(self, amp: Ampoule):
        if amp not in self.ampoules:
            self.ampoules.append(amp)
            print(f"Ampoule {amp.nom} connectée.")
 
    def actionner(self):
        for amp in self.ampoules:
            if self.actif:
                amp.eteindre()
            else:
                amp.allumer()
        self.actif = not self.actif
 
class Ampoule:
    def __init__(self, nom):
        self.nom = nom
 
    def allumer(self):
        print(f"Ampoule {self.nom} => Allumée")
 
    def eteindre(self):
        print(f"Ampoule {self.nom} => Eteinte")
 
inter = Interrupteur()
 
a1 = Ampoule("philips")
a2 = Ampoule("Toshiba")
a3 = Ampoule("Xiaomi")
 
inter.connecter(a2)
inter.connecter(a3)
 
for i in range(5):
    inter.actionner()