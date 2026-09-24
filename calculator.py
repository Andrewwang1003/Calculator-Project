tokens = []
just_calculated = False
def appendChar(value):
    global just_calculated
    if just_calculated and (value.isdigit() or value == "."):
        tokens.clear()
    just_calculated = False
    last_is_num = tokens and is_number(tokens[-1])
    add_decimal = tokens and is_int(tokens[-1]) and value == "."
    if (last_is_num and value.isdigit()) or add_decimal :
        tokens[-1]+=value
    elif (last_is_num or value.isdigit()) and value != '.':
        tokens.append(value)
    
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def deleteChar():
    if tokens:
        tokens.pop()

def clear():
    if tokens: 
        tokens.clear()

def reverse():
    if tokens and is_number(tokens[-1]):
        if tokens[-1][0] == "-":
            tokens[-1] = tokens[-1][1:]
        else:
            tokens[-1] = "-" + tokens[-1]

def result():
    if tokens: 
        stack = [tokens[0]]
        for i in range(1, len(tokens)-1, 2):
            op = tokens[i]
            digit = float(tokens[i+1])
            if op =="*":
                stack.append(float(stack.pop()) * digit)
            if op =="/":
                try:
                    stack.append(float(stack.pop()) / digit)
                except ZeroDivisionError:
                    return "Can't divide by Zero"
            if op =="+":
                stack.append(digit)
            elif op =="-":
                stack.append(-1*digit)
        total = round(sum([float(value) for value in stack]), 3)
        if total.is_integer():
            return int(total)
        return total
    return 0 

def equals():
    global just_calculated
    answer = result()
    tokens.clear()
    if not isinstance(answer, str):
        tokens.append(str(answer))
        just_calculated = True
    return answer

