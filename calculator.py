import math
import re
import sqlite3


tokens = []
just_calculated = False

conn = sqlite3.connect("equation.db")
c = conn.cursor()
c.execute("CREATE TABLE equations (equation text)")


def is_number(s):
    if not isinstance(s, str) or s == "":
        return False
    try:
        return not math.isnan(float(s))
    except ValueError:
        return False

def is_int(s):
    return is_number(s) and "." not in s

def is_digit(s):
    return isinstance(s, str) and re.fullmatch(r"[0-9]", s) is not None

def is_percent(s):
    return isinstance(s, str) and s.endswith("%") and is_number(s[:-1])

def is_operand(s):
    return is_number(s) or is_percent(s)

def to_value(s):
    return float(s[:-1]) / 100 if is_percent(s) else float(s)

def format_number(n):
    return str(int(n)) if float(n).is_integer() else str(n)

def append_char(value):
    global tokens, just_calculated
    if just_calculated and (is_digit(value) or value == "."):
        tokens = []
    just_calculated = False

    last = tokens[-1] if tokens else None
    last_is_num = is_number(last)
    add_decimal = is_int(last) and value == "."

    if value == "%":
        if last_is_num:
            tokens[-1] += "%"
    elif (last_is_num and is_digit(value)) or add_decimal:
        tokens[-1] += value
    elif value == ".":
        pass
    elif is_digit(value):
        if not is_operand(last):
            tokens.append(value)
    else:
        if is_operand(last):
            tokens.append(value)

def delete_char():
    if not tokens:
        return
    trimmed = tokens[-1][:-1]
    if trimmed == "":
        tokens.pop()
    else:
        tokens[-1] = trimmed

    update_display()

def clear_all():
    global tokens, just_calculated
    tokens = []
    just_calculated = False

def reverse():
    if tokens and is_operand(tokens[-1]):
        tokens[-1] = tokens[-1][1:] if tokens[-1].startswith("-") else "-" + tokens[-1]

def result():
    equation = ''
    for x in tokens:
        equation += x 
    if not tokens:
        return 0
    stack = [to_value(tokens[0])]
    for i in range(1, len(tokens) - 1, 2):
        op = tokens[i]
        num = to_value(tokens[i + 1])
        if op == "*":
            stack.append(stack.pop() * num)
        elif op == "/":
            if num == 0:
                return "Can't divide by Zero"
            stack.append(stack.pop() / num)
        elif op == "+":
            stack.append(num)
        elif op == "-":
            stack.append(-num)
    total = sum(stack)
    c.execute("INSERT INFO equations VALUES (equation + '=' + math.floor(total * 1000 + 0.5) / 1000)")
    c.execute("SELECT * FROM equations")
    conn.commit()
    conn.close()
    return math.floor(total * 1000 + 0.5) / 1000

def equals():
    global tokens, just_calculated
    answer = result()
    tokens = []
    if isinstance(answer, (int, float)):
        tokens.append(format_number(answer))
        just_calculated = True
    return answer

def update_display():
    print(" ".join(tokens))

def show_result():
    answer = equals()
    print(format_number(answer) if isinstance(answer, (int, float)) else answer)