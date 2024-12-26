import sqlite3

import pwinput
from time import sleep



# Cria a base de dados com a tabela se nao existir
def iniciarDB():
    with sqlite3.connect("agapeshop.db") as conn:  
        cursor = conn.cursor()
        

        #1 Tabela Usuario
        cursor.execute(''' CREATE TABLE IF NOT EXISTS usuario (
                       usuario_id INTEGER PRIMARY KEY AUTOINCREMENT ,
                       nome VARCHAR(100),
                       senha VARCHAR(50)) ''')
        print("Tabela usuario criada com suceso ")


        # 2 Categoria dos produtos      
        cursor.execute(''' CREATE TABLE IF NOT EXISTS categoria (
                        categoria_id INTEGER PRIMARY KEY AUTOINCREMENT,  
                        livraria VARCHAR(50), 
                        roupas  VARCHAR(50),
                        acessorios VARCHAR(50) )''')
        print("Tabela categoria Criada com Sucesso1 ")   ### MUDEI A CATEGORIA JA DEFININDO AS PARA TENTAr FAZER UM SELECT

        #3 TABELA DE PRODUTOS
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS produtos(
                        produto_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome_produto TEXT,
                        descricao_produto VARCHAR(100),   
                        preco DECIMAL,
                        quantidade_estoque INTEGER,
                        categoria_id INTEGER,
                        FOREIGN KEY (categoria_id) REFERENCES categoria (categoria_id) )''')
        print("Tabela Produtos para Agape Shop Criada com Sucesso")
        

        #4 Tabela de  Fatura
        cursor.execute(''' CREATE TABLE IF NOT EXISTS fatura(
                       fatura_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       data_venda DATE,
                       total_venda DECIMAL,
                       usuario_id INTEGER,
                       pagamento_id INTEGER,
                       FOREIGN KEY (usuario_id) REFERENCES usuario (usuario_id),
                       FOREIGN KEY (pagamento_id) REFERENCES tipo_pagamento (pagamento_id) )''')
        print("Tabela Fatura Criada com sucesso ")


        #5 Tabela Itens da venda
        cursor.execute(''' CREATE TABLE IF NOT EXISTS item_venda (
                       item_venda_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       quantidade_venda INTEGER,
                       preco_unidade DECIMAL,
                       fatura_id INTEGER,
                       produto_id INTEGER,
                       FOREIGN KEY (fatura_id) REFERENCES fatura (fatura_id),
                       FOREIGN KEY (produto_id) REFERENCES produtos (produto_id) )''')
        print("Tabela Item venda criada com sucesso ")


        #6 Tipo de Pagamento 
        cursor.execute(''' CREATE TABLE IF NOT EXISTS tipo_pagamento (
                            pagamento_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            metodo_pagamento VARCHAR(50) UNIQUE )''')
        print("Tabela tipo de pagamento Criada com sucesso ")
        
        
        cursor.execute(''' 
                       INSERT OR IGNORE INTO categoria (categoria_id, livraria, roupas, acessorios)
                       VALUES (1,'livraria', NULL , NULL),
                       (2, NULL, 'Roupas', NULL),
                       (3, NULL, NULL , 'Acessorios')''') 
        
        cursor.execute('''
                       INSERT OR IGNORE INTO tipo_pagamento(metodo_pagamento)
                       VALUES 
                       ('Dinheiro'),
                       ('Multibanco'),
                       ('Mbway')''')    


        conn.commit()
        print("BASE DA DADOS CRAIADA COM SUCESSO ! ")





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
    



# Menu para o usuário inserir produtos
def menu():
    while True:
        print("1. Inserir Produto")
        print("2. Alterar Produto")
        print("3. Mostrar Produtos")
        print("4. Apagar Produto")
        print("5. Sair")
        
        escolha = input("Escolha uma opção: ").strip()

        if escolha == '1':
            print("Categorias disponíveis:")
            print("1. Livraria")
            print("2. Roupas")
            print("3. Acessórios")
            cat_opcao = input("Escolha uma categoria (1, 2, 3): ").strip()
            
            # Mapeamento direto do número para o ID da categoria
            categoria_id = int(cat_opcao) if cat_opcao in ['1', '2', '3'] else None

            if categoria_id:
                nome_produto = input("Nome do Produto: ").strip().title()
                descricao_produto = input("Descrição do Produto: ").strip()
                preco = float(input("Preço do Produto: ").strip())
                quantidade_estoque = int(input("Quantidade em Estoque: ").strip())
                
                insert(nome_produto, descricao_produto, preco, quantidade_estoque, categoria_id)
            else:
                print("Categoria inválida. Tente novamente.")

        elif escolha == '2':
            update()
        elif escolha == '3':
            mostrarProdutos()
            print()
        elif escolha == '4':
            delete()
        elif escolha == '5':
            print("saindo da Agape Shop ...\n")
            break
        else:
            print("Opção inválida, tente novamente.\n")
    print()

   


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
          
        

# Insere um novo produto
def insert(nome_produto, descricao_produto, preco, quantidade_estoque, categoria_id):
    try:
        with sqlite3.connect('agapeshop.db') as conn:  
            cursor = conn.cursor()
            
            cursor.execute('''  
                INSERT INTO produtos(nome_produto, descricao_produto, preco, quantidade_estoque, categoria_id)
                VALUES (?, ?, ?, ?, ?) 
            ''', (nome_produto, descricao_produto, preco, quantidade_estoque, categoria_id))
            conn.commit()

            print("Novo produto inserido com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao inserir produto: {e}")



# Atualiza um produto
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

            cursor.execute('SELECT * FROM produtos')
            produtos = cursor.fetchall()

            if not produtos:
                print("Nenhum produto encontrado .")
                return produtos
            
            for produto in produtos:
                print(f"\nNome: {produto[1]} \nDescricão: {produto[2]} \nPreco: {produto[3]} €  \nEstoque: {produto[4]}\n ")  #0Categoria 1Nome do produto,3preco do produto, 4 estoque do produto
            return produtos

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

# Função para inserir um novo produto
def insert(nome, descricao, preco, quantidade, categoria_id):
    """
    Adiciona um novo produto ao estoque.
    """
    try:
        with sqlite3.connect("agapeshop.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO produtos (nome_produto, descricao_produto, preco, quantidade_estoque, categoria_id)
                VALUES (?, ?, ?, ?, ?)
            """, (nome, descricao, preco, quantidade, categoria_id))
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"Erro ao inserir produto: {e}")
        return False

# Função para exibir todos os produtos
def mostrarProdutos():
    """
    Retorna todos os produtos do estoque.
    """
    with sqlite3.connect("agapeshop.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.nome_produto, p.descricao_produto, p.preco, p.quantidade_estoque, c.nome_categoria
            FROM produtos p
            LEFT JOIN categoria c ON p.categoria_id = c.id
        """)
        return cursor.fetchall()

# Função para buscar produtos por categoria
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
                    