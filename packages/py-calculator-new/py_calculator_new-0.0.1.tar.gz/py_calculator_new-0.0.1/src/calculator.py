# import pandas as pd
# import numpy as np


def add(x, y):
    """Addition"""
    return x + y

def subtract(x, y):
    """Subtraction"""
    return x - y

def multiply(x, y):
    """Multiplication"""
    return x * y


def divide(x, y):
    """Division"""
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

def calculator_():
    """Calculator program"""
    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")

    while True:
        choice = input("Enter choice (1/2/3/4): ")

        if choice in ('1', '2', '3', '4'):
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if choice == '1':
                print("Result:", add(num1, num2))
            elif choice == '2':
                print("Result:", subtract(num1, num2))
            elif choice == '3':
                print("Result:", multiply(num1, num2))
            elif choice == '4':
                try:
                    print("Result:", divide(num1, num2))
                except ValueError as e:
                    print("Error:", e)
            break
        else:
            print("Invalid input")

if __name__ == "__main__":
    calculator_()
