
year = int(input("Enter a year: "))

if (year%4==0) and not (year%100==0) or (year%400==0):
    print("Année bissextile")


else :
    print("Année non bissextile")