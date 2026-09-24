let tokens = [];
let justCalculated = false;

function isNumber(s) {
  return typeof s === "string" && s !== "" && !Number.isNaN(Number(s));
}

function isInt(s) {
  return isNumber(s) && !s.includes(".");
}

function isDigit(s) {
  return /^[0-9]$/.test(s);
}

function isPercent(s) {
  return typeof s === "string" && s.endsWith("%") && isNumber(s.slice(0, -1));
}

function isOperand(s) {
  return isNumber(s) || isPercent(s);
}

function toValue(s) {
  return isPercent(s) ? Number(s.slice(0, -1)) / 100 : Number(s);
}

function appendChar(value) {
  if (justCalculated && (isDigit(value) || value === ".")) {
    tokens = [];
  }
  justCalculated = false;

  const last = tokens[tokens.length - 1];
  const lastIsNum = isNumber(last);
  const addDecimal = isInt(last) && value === ".";
//you can simplify this function nigga 
  if (value === "%") {
    if (lastIsNum) tokens[tokens.length - 1] += "%";
  } else if ((lastIsNum && isDigit(value)) || addDecimal) {
    tokens[tokens.length - 1] += value;
  } else if (value === ".") { 
  } else if (isDigit(value)) {
    if (!isOperand(last)) tokens.push(value);
  } else {
    if (isOperand(last)) tokens.push(value);
  }
}

function deleteChar() {
  if (tokens.length === 0) return;       
  const last = tokens[tokens.length - 1];
  const trimmed = last.slice(0, -1);       
  if (trimmed === "") {
    tokens.pop();                          
  } else {
    tokens[tokens.length - 1] = trimmed;
  }

  updateDisplay();
}

function clearAll() {
  tokens = [];
  justCalculated = false;
}

function reverse() {
  const i = tokens.length - 1;
  if (isOperand(tokens[i])) {
    tokens[i] = tokens[i].startsWith("-") ? tokens[i].slice(1) : "-" + tokens[i];
  }
}

function result() {
  if (tokens.length === 0) return 0;
  const stack = [toValue(tokens[0])];
  for (let i = 1; i < tokens.length - 1; i += 2) {
    const op = tokens[i];
    const num = toValue(tokens[i + 1]);
    if (op === "*") {
      stack.push(stack.pop() * num);
    } else if (op === "/") {
      if (num === 0) return "Can't divide by Zero";
      stack.push(stack.pop() / num);
    } else if (op === "+") {
      stack.push(num);
    } else if (op === "-") {
      stack.push(-num);
    }
  }
  const total = stack.reduce((sum, n) => sum + n, 0);
  return Math.round(total * 1000) / 1000;
}

function equals() {
  const answer = result();
  tokens = [];
  if (typeof answer === "number") {
    tokens.push(String(answer));
    justCalculated = true;
  }
  return answer;
}

function updateDisplay() {
  document.getElementById("display").textContent = tokens.join(" ");
}

function showResult() {
  document.getElementById("display").textContent = equals();
}