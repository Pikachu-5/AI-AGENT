def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b if b != 0 else "Error: Division by zero"

FUNCTIONS = {"add": add,"subtract": subtract,"multiply": multiply,"divide": divide,}

def call_function(name, *args):
    if name in FUNCTIONS:
        return FUNCTIONS[name](*args)
    return "Error: Unknown function"
