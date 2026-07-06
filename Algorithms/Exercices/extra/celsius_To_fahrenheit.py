def celsius_fahrenheit_converter(temp, from_unit):
    match from_unit:
        case "C":
            return (f"{temp * 9 / 5 + 32} F" )
        case "F":
            return (f"{(temp -32) * 5/9}°C" )


def main():
    print("Welcome to the Celsius Fahrenheit converter")
    while True:
        starting_unit=input("Select your starting unit F or C: ").upper()
        try:
            temperature=int(input(f"Enter the temperature in {starting_unit} to convert: "))
        except ValueError:
            print("please enter a number")
            continue
        print(celsius_fahrenheit_converter(temperature, starting_unit))
        
   
        restart = input('Would you like to start over ? y/N')
        if restart == "y" or restart == "Y":
            continue
        else:
            break

main()