from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "segredo123"

def db():
    conn = sqlite3.connect("usuarios.db")
    conn.row_factory = sqlite3.Row
    return conn

with sqlite3.connect("usuarios.db") as conn:
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE, password TEXT, bio TEXT DEFAULT '', foto TEXT DEFAULT '')""")
    conn.execute("""CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER, conteudo TEXT, criado_em DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS curtidas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER, post_id INTEGER, UNIQUE(user_id, post_id))""")
    conn.execute("""CREATE TABLE IF NOT EXISTS seguidores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        seguidor_id INTEGER, seguido_id INTEGER, UNIQUE(seguidor_id, seguido_id))""")

@app.route("/")
def home():
    return redirect("/login")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        user = request.form["username"]
        senha = generate_password_hash(request.form["password"])
        try:
            with sqlite3.connect("usuarios.db") as conn:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, senha))
            return redirect("/login")
        except:
            return render_template("cadastro.html", erro="Usuário já existe")
    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        senha = request.form["password"]
        with sqlite3.connect("usuarios.db") as conn:
            data = conn.execute("SELECT id, password FROM users WHERE username=?", (user,)).fetchone()
        if data and check_password_hash(data[1], senha):
            session["user"] = user
            session["user_id"] = data[0]
            return redirect("/feed")
        return render_template("login.html", erro="Login inválido")
    return render_template("login.html")

@app.rout