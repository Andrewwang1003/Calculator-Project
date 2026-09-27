let tokens = [];
let justCalculated = false;

const isDigit = (s) => /^[0-9]$/.test(s);
const isNumber = (s) => typeof s === "string" && s !== "" && !Number.isNaN(Number(s));
const isInt = (s) => isNumber(s) && !s.includes(".");
const isOperand = (s) => isNumber(s?.replace(/%$/, ""));
const toValue = (s) => parseFloat(s) / (s.endsWith("%") ? 100 : 1);

function appendChar(value) {
  if (justCalculated && (isDigit(value) || value === ".")) tokens = [];
  justCalculated = false;
  const i = tokens.length - 1;
  const last = tokens[i];
  if (value === "%") {
    if (isNumber(last)) tokens[i] += "%";
  } else if (value === ".") {
    if (isInt(last)) tokens[i] += ".";
  } else if (isDigit(value)) {
    if (isNumber(last)) tokens[i] += value;
    else if (!isOperand(last)) tokens.push(value);
  } else if (isOperand(last)) {
    tokens.push(value);
  } else if (last !== undefined) {
    tokens[i] = value;
  }
  updateDisplay();
}

function deleteChar() {
  justCalculated = false;
  const i = tokens.length - 1;
  if (i < 0) return;
  const trimmed = tokens[i].slice(0, -1);
  if (trimmed === "" || trimmed === "-") tokens.pop();
  else tokens[i] = trimmed;
  updateDisplay();
}

function clearAll() {
  tokens = [];
  justCalculated = false;
  updateDisplay();
}

function reverse() {
  const i = tokens.length - 1;
  if (isOperand(tokens[i])) {
    tokens[i] = tokens[i].startsWith("-") ? tokens[i].slice(1) : "-" + tokens[i];
  }
  updateDisplay();
}

function result() {
  if (tokens.length === 0) return 0;
  const stack = [toValue(tokens[0])];
  for (let i = 1; i < tokens.length - 1; i += 2) {
    const op = tokens[i].trim();
    const num = toValue(tokens[i + 1]);
    if (op === "x" || op === "*") {
      stack.push(stack.pop() * num);
    } else if (op === "/") {
      if (num === 0) return "Cannot divide by 0";
      stack.push(stack.pop() / num);
    } else if (op === "+") {
      stack.push(num);
    } else if (op === "-") {
      stack.push(-num);
    } else {
      console.warn("Unknown operator:", JSON.stringify(op));
    }
  }
  const total = stack.reduce((sum, n) => sum + n, 0);
  return Math.round(total * 1000) / 1000;
}

function equals() {
  if (tokens.length && !isOperand(tokens[tokens.length - 1])) tokens.pop();
  if (tokens.length < 3) return tokens.join(" ");

  const equation = tokens.join(" ");
  const answer = result();
  justCalculated = true;
  sendCalc(equation, answer);

  if (typeof answer === "string") {
    tokens = [];
    return answer;
  }
  tokens = [String(answer)];
  return tokens[0];
}

function updateDisplay() {
  document.getElementById("display").textContent = tokens.join(" ");
}

function showResult() {
  document.getElementById("display").textContent = equals();
}

async function sendCalc(equation, answer) {
  try {
    const response = await fetch("/api/calculations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ equation, result: answer })
    });
    if (!response.ok) console.error("Save failed:", response.status, await response.json());
  } catch (err) {
    console.error("Network error:", err);
  }
  returnCalc();
}

async function returnCalc() {
  const response = await fetch("/api/calculations");
  const data = await response.json();
  const container = document.getElementById("history");
  container.innerHTML = "";
  const table = document.createElement("table");
  const headers = ["Number", "Equation", "Result", "Time"];
  const headerRow = document.createElement("tr");
  headers.forEach(headerText => {
    const th = document.createElement("th");
    th.textContent = headerText;
    headerRow.appendChild(th);
  });
  table.appendChild(headerRow);

  data.forEach((row, index) => {
    const tr = document.createElement("tr");
    const localTime = new Date(row.time.replace(" ", "T") + "Z").toLocaleTimeString();
    [index + 1, row.equation, row.result, localTime].forEach(value => {
      const td = document.createElement("td");
      td.textContent = value;
      tr.appendChild(td);
    });
    table.appendChild(tr);
  });

  container.appendChild(table);
}

returnCalc();