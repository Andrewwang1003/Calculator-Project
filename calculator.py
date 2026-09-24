tokens = []

def appendChar(value):
    last_is_int = tokens and isinstance(tokens[-1],int)
    if isinstance(value, int) and last_is_int:
        tokens[-1] = tokens[-1]*10+value
    elif isinstance(value, int) or last_is_int:
        tokens.append(value)

def deleteChar():
    tokens.pop() 

def clear():
    tokens.clear()

def reverse():
    if isinstance(tokens[-1], int):
        tokens[-1] = tokens[-1]*-1

def result():
    stack = [float(tokens[0])]
    for i in range(1, len(tokens), 2):
        op = tokens[i]
        digit = float(tokens[i+1])
        if op =="*":
            stack.append(stack.pop() * digit)
        if op =="/":
            stack.append(stack.pop() / digit)
        if op =="+":
            stack.append(digit)
        else:
            stack.append(-1*digit)
    return sum(stack)

appendChar(3)
appendChar(3)
appendChar("*")
appendChar(3)
reverse()
appendChar(4)
appendChar("+")
appendChar("-")
appendChar(3)
print(tokens)
"""
need to fix the reverse function/append funciton with negative numbers
currently when we reverse the a digit and then append another digit it gives a incorrect result as the appended number is not negative
i think if the tokens[-1] is negative we should add the negative version of the appended number, so we get the correct result.
"""

