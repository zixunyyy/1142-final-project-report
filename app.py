from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# 首頁
@app.route("/")
def index():
    return render_template("index.html")

# 新增日記
@app.route("/add", methods=["POST"])
def add():
    text = request.form["text"]

    # 情緒分析（簡單版）
    if "開心" in text or "快樂" in text:
        emotion = "正向"
    elif "難過" in text or "生氣" in text:
        emotion = "負向"
    else:
        emotion = "中性"

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS diary(text, emotion)")
    c.execute("INSERT INTO diary VALUES (?, ?)", (text, emotion))
    conn.commit()
    conn.close()

    return redirect("/")

# 查詢紀錄
@app.route("/history")
def history():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM diary")
    data = c.fetchall()
    conn.close()
    return render_template("history.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
