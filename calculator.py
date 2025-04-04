import math_tools
def calc():
    try:
        num1 = float(input("Enter the number:"))
        num2 = float(input("Enter the number:"))
        operation = input("choose an operation(add, subtract, multiply, divide):").strip().lower()
        if operation == "add":
            result = math_tools.add(num1, num2)
        elif operation == "subtract":
            result = math_tools.subtract(num1, num2)
        elif operation == "multiply":
            result = math_tools.multiply(num1, num2)
        elif operation == "divide":
            result = math_tools.divide(num1, num2)
        else:
            print("invalid operation selected")
            return result
        print(result)
    except ValueError:
        print("invalid input")
calc()