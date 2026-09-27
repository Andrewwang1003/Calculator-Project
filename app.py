from flask import Flask, render_template, jsonify, request
import sqlite3 

app = Flask(__name__)
conn = sqlite3.connect("equation.db")
conn.row_factory = sqlite3.Row  
c = conn.cursor()
c.execute(""" CREATE TABLE IF NOT EXISTS equations (
        number INTEGER PRIMARY KEY,
        equation TEXT,
        result TEXT,
        time TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
conn.commit()

@app.route("/")
def runapp():
    return render_template("index.html")

@app.route("/api/calculations")
def getcalcs():
    conn = sqlite3.connect("equation.db")
    conn.row_factory = sqlite3.Row    
    c = conn.cursor()
    c.execute("SELECT * FROM equations")
    rows = c.fetchall()
    conn.close()
    listofdicts = [dict(row) for row in rows]
    return jsonify(listofdicts)

@app.route("/api/calculations", methods=["POST"])
def addcalcs():
    data = request.get_json()
    equation_value = data.get("equation")
    result_value = data.get("result")
    if equation_value is None or result_value is None:
        return jsonify('Error'), 400
    conn = sqlite3.connect("equation.db")
    c = conn.cursor()
    c.execute("INSERT INTO equations (equation, result) VALUES (?, ?)", (equation_value, result_value))
    conn.commit()
    conn.close()
    return jsonify("Success"), 201
    
if __name__ == "__main__":
    app.run(debug=True)
