import tkinter as tk

root = tk.Tk()
expression = ""                      # the recorded input
display = tk.StringVar()             # linked to the on-screen label/entry

tk.Entry(root, textvariable=display, font=("Arial", 20), justify="right").grid(row=0, column=0, columnspan=4)

def press(char):
    global expression
    expression += char
    display.set(expression)

def clear():
    global expression
    expression = ""
    display.set("")

def calculate():
    global expression
    try:
        result = str(eval(expression))
        display.set(result)
        expression = result          # lets you keep calculating from the answer
    except Exception:
        display.set("Error")
        expression = ""

buttons = ["7","8","9","/", "4","5","6","*", "1","2","3","-", "0",".","=","+"]
for i, b in enumerate(buttons):
    cmd = calculate if b == "=" else (lambda c=b: press(c))
    tk.Button(root, text=b, width=5, height=2, command=cmd).grid(row=1 + i // 4, column=i % 4)

tk.Button(root, text="C", command=clear).grid(row=5, column=0, columnspan=4, sticky="we")
root.mainloop()