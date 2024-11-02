def perform_calculation(num1, num2, operation):
    if operation == '1':
        return num1 + num2
    elif operation == '2':
        return num1 - num2
    elif operation == '3':
        return num1 * num2
    elif operation == '4':
        if num2 == 0:
            raise ValueError("Cannot divide by zero!")
        return num1 / num2
    else:
        raise ValueError("Invalid operation selected!")

def main():
    print("\n=== Simple Calculator ===")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    
    try:
        num1 = float(input("\nEnter first number: "))
        num2 = float(input("Enter second number: "))
        operation = input("Choose operation (1-4): ")
        
        result = perform_calculation(num1, num2, operation)
        
        operation_symbols = {
            '1': '+', '2': '-', '3': '*', '4': '/'
        }
        
        print(f"\nResult: {num1} {operation_symbols[operation]} {num2} = {result}")
        
    except ValueError as e:
        print(f"\nError: {str(e)}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()