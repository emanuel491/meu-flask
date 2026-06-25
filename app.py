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

@