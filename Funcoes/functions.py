import sqlite3

import pwinput
from time import sleep


import sqlite3

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
                    metodo_pagamento TEXT NOT NULL UNIQUE
                ) 
            ''')
            print("Tabela 'tipo_pagamento' criada com sucesso.")


            # Inserção de métodos de pagamento
            cursor.executemany('''
                INSERT OR IGNORE INTO tipo_pagamento (pagamento_id, metodo_pagamento) 
                VALUES (?, ?)
            ''', [(1, 'Dinheiro'), (2, 'Multibanco'), (3, 'MB Way')])
            print("Métodos de pagamento inseridos com sucesso.")
            

            # Criação da tabela de vendas
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS vendas (
                    venda_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    total REAL NOT NULL CHECK(total >= 0),
                    pagamento_id INTEGER NOT NULL,
                    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (pagamento_id) REFERENCES tipo_pagamento(pagamento_id)
                ) 
            ''')
            print("Tabela 'vendas' criada com sucesso.")

            # Criação da tabela de itens de venda
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS itens_venda (
                    item_venda_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    venda_id INTEGER NOT NULL,
                    produto_id INTEGER NOT NULL,
                    quantidade INTEGER NOT NULL CHECK(quantidade > 0),
                    preco_unitario REAL NOT NULL CHECK(preco_unitario >= 0),
                    FOREIGN KEY (venda_id) REFERENCES vendas(venda_id),
                    FOREIGN KEY (produto_id) REFERENCES produtos(produto_id)
                ) 
            ''')
            print("Tabela 'itens_venda' criada com sucesso.")

            conn.commit()
            print("Base de dados criada com sucesso!")

    except sqlite3.Error as e:
        print(f"Erro ao criar banco de dados: {e}")





# Cabeçalho
def cabecalho():
    titulo = "AGAPE SHOP"
    tam = int(len(titulo)/2)+2
    print('--' * tam)
    print(f'  {titulo}  ')
    print('--' * tam)
    sleep(0.5)


# Cadastrar Usuario
def cadastro():
    while True:
        global user_id
        print(f"Deseja fazer Login ou Cadastro?")
        print("1. Login")
        print("2. Cadastro")
        print("3. Sair ")
        

        try:
            opcao = int(input("Escolha uma opção: "))

            if opcao == 1:
                print(" --- LOGIN --- ")
                nome = input("\nDigite o seu nome : ")
                #senha = input("Digite a sua password: ") sem o getpass
                senha = pwinput.pwinput("Digite a sua senha: ", mask="*") 
                print("\nA validar...\n")
                sleep(1)
                
                #conexao ao db e verificacao de user 
                with sqlite3.connect('agapeshop.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT usuario_id FROM usuario WHERE nome = ? AND senha = ?", (nome,senha))
                    user = cursor.fetchone()
                    

                    if user:  # Verifica se o usuário existe
                        user_id = user[0]
                        print("Login efetuado com sucesso!\n")
                        sleep(0.5)
                        break
                    else:
                        print("Nome de usuário ou senha incorretos. Você precisa se cadastrar primeiro.")
                        print("Você deseja se cadastrar? (s/n)")
                        if input().strip().lower() == 's':
                            continue

                
            elif opcao == 2:
                print(" --- CADASTRO --- ")  
                nome = input("Digite seu nome de usuario: ").strip().title()
                senha = input("Digite sua senha: ")

                with sqlite3.connect('agapeshop.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO usuario (nome , senha) VALUES(?, ?)",(nome, senha))
                    conn.commit()
                    print(f"Usuario {nome} cadastrado com suceso! ")

                    return nome
                

            elif opcao == 3:
                print("Saindo... Até a próxima!")
                break

            else:
                print("Opção Inválida! Tente novamente.")

        

        except ValueError:
            print("Erro: Por favor, insira um número válido.")
    





# Insere uma categoria ** e para selecionar a categoria e nao inserir pois ja deifini as categorias na criacao 
def insertCategoria(categoria):
    try:
        with sqlite3.connect('agapeshop.db') as conn:
            cursor = conn.cursor()
            
            # Busca direta pelo ID da categoria
            cursor.execute("SELECT categoria_id FROM categoria WHERE livraria = ? OR roupas = ? OR acessorios = ?", 
                         (categoria, categoria, categoria))
            
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0]
            
            print(f"Categoria {categoria} encontrada com sucesso!")
            return resultado[0]

    except sqlite3.Error as e:
        print(f"Erro ao verificar Categoria: {e}")   
          
        

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
        



# Atualiza um produto NAO APLICADA ATE O MOMENTO
def update():
    try:
        with sqlite3.connect('agapeshop.db') as conn:
            cursor = conn.cursor()
            cursor.execute(''' SELECT * FROM produtos ''')
            produtos = cursor.fetchall()
            
            for produto in produtos:
                print(f'ID: {produto[0]} | NOME: {produto[1]} | DESCRICAO: {produto[2]} | PRECO: {produto[3]} | ESTOQUE: {produto[4]} | CATEGORIA: {produto[5]}')

            alteraProduto = input("Digite o novo nome do produto: ").strip().title()
            novo_preco = float(input("Digite o novo preço: "))
            novo_stock = int(input("Digite o novo estoque: "))
            cursor.execute(''' 
                UPDATE produtos SET preco = ?, stock = ? WHERE nome = ?
            ''', (novo_preco, novo_stock, alteraProduto))
            conn.commit()
            print(f"Produto '{alteraProduto}' alterado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao alterar produto: {e}")




#Mostar produtos 
def mostrarProdutos():
    try:
        with sqlite3.connect('agapeshop.db') as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT produto_id, nome_produto, descricao_produto, preco, quantidade_estoque, categoria_id FROM produtos')
            produtos = cursor.fetchall()

            if not produtos:
                print("Nenhum produto encontrado .")
                return []
            
            return produtos
            
        for produto in produtos:
            print(f"\nNome: {produto[1]} \nDescricão: {produto[2]} \nPreco: {produto[3]} €  \nEstoque: {produto[4]}\n ")  #0Categoria 1Nome do produto,3preco do produto, 4 estoque do produto
        return []

    except sqlite3.Error as e:
        print(f"Erro ao mostrar produtos {e}")        


#funcao para deletar um produto
def delete():
    try:
        nome_produto = input("Digite o nome do produto que deseja deletar: ").strip().title()
       
        with sqlite3.connect('agapeshop.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT produto_id, nome_produto, descricao_produto  FROM produtos WHERE nome_produto = ?", (nome_produto,))
            produtos = cursor.fetchall()

            if produtos:
                print("Produtos encontrados:")
                for produto in produtos:
                    print(f"ID: {produto[0]}, Nome: {produto[1]}, Descrição: {produto[2]}")
                
                # Solicita que o usuário escolha o produto pelo ID
                try:
                    produto_id = int(input("Digite o ID do produto que deseja deletar: "))
                    cursor.execute("SELECT * FROM produtos WHERE produto_id = ?", (produto_id,))
                    produto_selecionado = cursor.fetchone()

                    if produto_selecionado:
                        cursor.execute("DELETE FROM produtos WHERE produto_id = ?", (produto_id,))
                        conn.commit()
                        print(f"Produto com ID {produto_id} excluído com sucesso.")
                    else:
                        print(f"Nenhum produto encontrado com o ID {produto_id}.")
                
                except ValueError:
                    print("ID inválido. Por favor, insira um número inteiro.")

            else:
                print(f"Nenhum produto encontrado com o nome {nome_produto}.")

    except sqlite3.Error as e:
        print(f"Erro ao deletar produto: {e}")

                    

# Função para registrar um novo usuário
def registrar_usuario(username, password):
    """
    Registra um novo usuário no banco de dados.
    """
    try:
        with sqlite3.connect("agapeshop.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuario (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return True  # Sucesso
    except sqlite3.IntegrityError:
        return False  # Usuário já existe    
    
    
# Função para validar login
def validar_usuario(username, password):
    """
    Valida as credenciais do usuário.
    """
    with sqlite3.connect("agapeshop.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE username = ? AND password = ?", (username, password))
        return cursor.fetchone() is not None


# Função para buscar produtos por categoria NAO APLICADA ATE O MOMENTO
def buscarPorCategoria(categoria_id):
    """
    Retorna produtos de uma categoria específica.
    """
    with sqlite3.connect("agapeshop.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nome_produto, descricao_produto, preco, quantidade_estoque 
            FROM produtos WHERE categoria_id = ?
        """, (categoria_id,))
        return cursor.fetchall()    
                    