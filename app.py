from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "segredo123"

def db():
    return sqlite3.connect("usuarios.db")

# criar tabela
with db() as conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

@app.route("/")
def home():
    return redirect("/login")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        user = request.form["username"]
        senha = generate_password_hash(request.form["password"])

        try:
            with db() as conn:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, senha))
            return redirect("/login")
        except:
            return "Usuário já existe"
    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        senha = request.form["password"]

        with db() as conn:
            data = conn.execute("SELECT password FROM users WHERE username=?", (user,)).fetchone()

        if data and check_password_hash(data[0], senha):
            session["user"] = user
            return redirect("/dashboard")

        return "Login inválido"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html", user=session["user"])

@app.route("/perfil")
def perfil():
    if "user" not in session:
        return redirect("/login")

    return render_template("perfil.html", user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)