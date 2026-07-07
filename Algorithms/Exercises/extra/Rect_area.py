







def calculate_area(length, width, unit):
    return f"The area of this rectangle is {length * width} {unit}^2"


# Main loop
def main():
    print("Hi, welcome to the Area calculator program")
    running = True
    while running:
        width = int(input("Enter the width of the rectangle: \n"))
        length = int(input("Enter the length of the rectangle: \n"))
        unit = input("Which unit is the rectangle mm, cm, m, km ?: ")

        print(calculate_area(length=length, width=width, unit=unit))
    
        restart = input('Would you like to start over ? y/N')
        if restart == "y" or restart == "Y":
            continue
        else:
            running=False



# Script starts here            
main()