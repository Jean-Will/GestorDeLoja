import sqlite3
import bcrypt



# Função para criar o banco de dados e tabelas, caso ainda não existam
def iniciaDB():

    try:
        with sqlite3.connect("agapeshop.db") as conn:  
            cursor = conn.cursor()

            # Criação da tabela de usuários
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS usuario (
                    usuario_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(100) NOT NULL UNIQUE,
                    password VARCHAR(50) NOT NULL
                ) 
            ''')
            print("Tabela 'usuario' criada com sucesso.")

            # Criação da tabela de categorias
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS categoria (
                    categoria_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_categoria VARCHAR(50) NOT NULL UNIQUE,
                    descricao_categoria TEXT,
                    ativo BOOLEAN DEFAULT 1
                ) 
            ''')
            print("Tabela 'categoria' criada com sucesso.")

            # Popula a tabela de categorias com valores iniciais
            cursor.executemany('''
                INSERT OR IGNORE INTO categoria (categoria_id, nome_categoria, descricao_categoria) 
                VALUES (?, ?, ?)
            ''', [
                (1, 'Livraria', 'Produtos relacionados a livros, material escolar e papelaria'),
                (2, 'Roupas', 'Vestuário em geral incluindo camisas, calças e vestidos'),
                (3, 'Acessórios', 'Complementos como bolsas, cintos e bijuterias')
            ])
            print("Categorias inseridas com sucesso.")


            
            # Criação da tabela de produtos
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS produtos (
                    produto_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_produto TEXT NOT NULL,
                    descricao_produto TEXT,
                    preco REAL NOT NULL CHECK(preco >= 0),
                    quantidade_estoque INTEGER NOT NULL CHECK(quantidade_estoque >= 0),
                    categoria_id INTEGER NOT NULL,
                    FOREIGN KEY (categoria_id) REFERENCES categoria(categoria_id)
                ) 
            ''')
            print("Tabela 'produtos' criada com sucesso.")

            # Criação da tabela de métodos de pagamento
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS tipo_pagamento (
                    pagamento_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metodo_pagamento VARCHAR(50) NOT NULL UNIQUE
                ) 
            ''')
            cursor.executemany('''
                INSERT OR IGNORE INTO tipo_pagamento (pagamento_id, metodo_pagamento) 
                VALUES (?, ?)
            ''', [(1, 'Dinheiro'), (2, 'Multibanco'), (3, 'MB Way')])
            print("Tabela 'tipo_pagamento' criada e métodos inseridos.")

            conn.commit()
            print("Base de dados criada com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao criar banco de dados: {e}")


# Função para login
def login(username, password):
    try:
        with sqlite3.connect("agapeshop.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM usuario WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result:
                return bcrypt.checkpw(password.encode(), result[0].encode())
    except sqlite3.Error as e:
        return False


# Função para cadastrar um novo usuário
def cadastro(username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        with sqlite3.connect("agapeshop.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuario (username, password) VALUES (?, ?)", (username, hashed_password.decode()))
            conn.commit()
    except sqlite3.Error as e:
        return False


# Função para listar todos os produtos
def mostrarProdutos():
    try:
        with sqlite3.connect("agapeshop.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nome_produto, descricao, preco, quantidade_estoque, categoria_id FROM produtos")
            return [{"nome": row[0], "descricao": row[1], "preco": row[2], "quantidade_estoque": row[3], "categoria_id": row[4]} for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Erro ao mostrar produtos: {e}")
        return []


# Função para inserir um produto
def inserirProduto(nome_produto, descricao_produto, preco, quantidade_estoque, categoria_id):
    try:
        with sqlite3.connect("agapeshop.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO produtos (nome_produto, descricao_produto, preco, quantidade_estoque, categoria_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (nome_produto, descricao_produto, preco, quantidade_estoque, categoria_id))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inserir produto: {e}")
        raise


# Função para deletar um produto
def deletarProduto(produto_id):
    try:
        with sqlite3.connect("agapeshop.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM produtos WHERE produto_id = ?", (produto_id,))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao deletar produto: {e}")
        raise