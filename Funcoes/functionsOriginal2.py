import sqlite3
import bcrypt

def iniciaDB():
    with sqlite3.connect("agapeshop.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                quantidade INTEGER NOT NULL
            )
        """)
        print("Base de dados inicializada com sucesso!")

def login(username, password):
    with sqlite3.connect("agapeshop.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM usuario WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result:
            return bcrypt.checkpw(password.encode(), result[0].encode())
        return False

def cadastro(username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        with sqlite3.connect("agapeshop.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuario (username, password) VALUES (?, ?)", (username, hashed_password.decode()))
            return True
    except sqlite3.IntegrityError:
        return False

def inserirProduto(nome, preco, quantidade):
    try:
        with sqlite3.connect("agapeshop.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)", (nome, preco, quantidade))
            return True
    except sqlite3.Error as e:
        print(f"Erro ao inserir produto: {e}")
        return False

def mostrarProdutos():
    with sqlite3.connect("agapeshop.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nome, preco, quantidade FROM produtos")
        return [{"nome": row[0], "preco": row[1], "quantidade": row[2]} for row in cursor.fetchall()]
