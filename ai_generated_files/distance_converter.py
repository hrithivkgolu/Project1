def miles_to_kilometers(miles):
    return miles * 1.60934

def kilometers_to_miles(kilometers):
    return kilometers / 1.60934

def main():
    print("Distance Converter")
    choice = input("Convert from (1) Miles to Kilometers or (2) Kilometers to Miles? Enter 1 or 2: ")
    if choice == '1':
        miles = float(input("Enter distance in miles: "))
        print(f"{miles} miles is {miles_to_kilometers(miles):.2f} kilometers.")
    elif choice == '2':
        kilometers = float(input("Enter distance in kilometers: "))
        print(f"{kilometers} kilometers is {kilometers_to_miles(kilometers):.2f} miles.")
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
