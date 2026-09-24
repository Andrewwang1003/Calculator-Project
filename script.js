let equation = "";
function deleteChar(int) {
    equation.splice(0,-1);
}

function clear(){
    equation = ""
}

function appendChar(char){
    equation += char
}

function reverse(equation) {
  return equation.replace(/([+\-*/]|^)(-?)([\d.]+%?)$/, (all, op, neg, num) => {
    if (op === "-") return "+" + num;
    if (op === "+") return "-" + num;
    return op + (neg ? "" : "-") + num;
  });
}

function result(expr) {
  const tokens = expr.match(/\d+\.?\d*|[+\-*/]/g);
  const stack = [Number(tokens[0])];

  for (let i = 1; i < tokens.length; i += 2) {
    const op = tokens[i];
    const num = Number(tokens[i + 1]);
    if (op === '*') stack.push(stack.pop() * num);
    else if (op === '/') stack.push(stack.pop() / num);
    else if (op === '+') stack.push(num);
    else stack.push(-num);      
  }
  return stack.reduce((a, b) => a + b, 0);
}