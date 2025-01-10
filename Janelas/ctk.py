import customtkinter as CTk
from Funcoes.functions import validar_usuario , registrar_usuario , mostrarProdutos,inserirProduto,  consultar_inventario, update, consultar_estoque_por_data , registrar_movimentacao
import sqlite3
from openpyxl import Workbook
from tkinter import filedialog, messagebox



CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("blue")

def start_application():
    login_window()


# Função para abrir a janela de login
def login_window():
    def login_action():
        username = username_entry.get()
        password = password_entry.get()
        # Verificação do usuário
        if validar_usuario(username, password):
            window.destroy()
            menu_principal(username)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")

    def register_action():
        window.destroy()
        register_window()

  

    # Configuração da janela de login
    window = CTk.CTk()
    window.title("Login - Agape Shop")
    window.geometry("400x400")

    CTk.CTkLabel(window, text="Agape Shop", font=("Arial", 20, "bold")).pack(pady=10)
    CTk.CTkLabel(window, text="Username").pack(pady=10)
    username_entry = CTk.CTkEntry(window, width=300)
    username_entry.pack(pady=10)

    CTk.CTkLabel(window, text="Password").pack(pady=10)
    password_entry = CTk.CTkEntry(window, show="*", width=300)
    password_entry.pack(pady=10)

    CTk.CTkButton(window, text="Login", width=300, command=login_action).pack(pady=10)
    CTk.CTkButton(window, text="Registrar", width=300, command=register_action).pack(pady=10)
    

    window.mainloop()


# Janela de Login e registro
def register_window():
    def save_user():
        username = username_entry.get()
        password = password_entry.get()
        registrar_usuario(username, password)
        messagebox.showinfo("Sucesso", "Usuário registrado!")
        window.destroy()
        login_window()

    window = CTk.CTk()
    window.title("Registrar - Agape Shop")
    window.geometry("400x400")

    CTk.CTkLabel(window, text="Registrar Usuário", font=("Arial", 20, "bold")).pack(pady=10)
    CTk.CTkLabel(window, text="Username").pack(pady=10)
    username_entry = CTk.CTkEntry(window, width=300)
    username_entry.pack(pady=10)

    CTk.CTkLabel(window, text="Password").pack(pady=10)
    password_entry = CTk.CTkEntry(window, show="*", width=300)
    password_entry.pack(pady=10)

    CTk.CTkButton(window, text="Registrar", width=300, command=save_user).pack(pady=10)
    CTk.CTkButton(window, text="Voltar", width=300, command=lambda: [window.destroy(), login_window()]).pack(pady=10)

    
    window.mainloop()


# Janela do menu principal
def menu_principal(username):
    def open_consulta_estoque():
        menu.destroy()
        consultar_estoque()

    def open_add_produto():
        menu.destroy()
        adicionar_produto()

    def open_remover_produto():
        menu.destroy()
        remover_produto()

    menu = CTk.CTk()
    menu.title("Menu Principal - Agape Shop")
    menu.geometry("700x600")

    CTk.CTkLabel(menu, text=f"Bem-vindo, {username}!", font=("Arial", 20, "bold")).pack(pady=20)
    CTk.CTkButton(menu, text="Consultar Estoque", width=300, command=open_consulta_estoque).pack(pady=10)
    CTk.CTkButton(menu, text="Adicionar Produto", width=300, command=open_add_produto).pack(pady=10)
    CTk.CTkButton(menu, text="Alterar Produto", width=300, command=update_produto).pack(pady=10)
    CTk.CTkButton(menu, text="Remover Produto", width=300, command=lambda: [menu.destroy(), remover_produto()]).pack(pady=10)
    #CTk.CTkButton(menu, text="Exportar Relatório", width=300,command=lambda: exportar_relatorio_pdf(relatorio_diario, "Relatorio Diario de Vendas")).pack(pady=10)
    CTk.CTkButton(menu, text="Estoque por Data", width=300,command=lambda: mostrar_estoque_por_data()).pack(pady=10)
    CTk.CTkButton(menu, text="Exportar Inventario", width=300,command=lambda: exportar_inventario_por_data()).pack(pady=10)
    CTk.CTkButton(menu, text="Vendas", width=300,command=janela_vendas).pack(pady=35)
    CTk.CTkButton(menu, text="Sair", width=300, command=menu.destroy).pack(pady=25)

    menu.mainloop()


# Janela de consulta de estoque
def consultar_estoque():
    def voltar():
        window.destroy()
        menu_principal("Usuário")

    window = CTk.CTk()
    window.title("Consultar Estoque")
    window.geometry("700x600")

    produtos = mostrarProdutos()

    frame = CTk.CTkScrollableFrame(window, width=750, height=500)
    frame.pack(pady=20)

    if not produtos:
        CTk.CTkLabel(frame, text="Nenhum produto encontrado.").pack(pady=10)
    else:
        for produto in produtos:
            id ,nome , descricao , preco , quantidade , categoria = produto
            CTk.CTkLabel(frame, text=f"ID Produto: {id} \nNome: {nome}\nDescrição:{descricao}\nPreço:€{preco:.2f}\nEstoque:{quantidade}\nCategoria ID: {categoria}", justify="left",font=("Arial",12)).pack(pady=10)

    CTk.CTkButton(window, text="Voltar", width=300, command=voltar).pack(pady=10)

    window.mainloop()


# Janela de adicionar produto
def adicionar_produto():
    def save_product():
        nome = nome_entry.get()
        descricao = descricao_entry.get()
        preco = float(preco_entry.get())
        quantidade = int(quantidade_entry.get())
        categoria = int(categoria_entry.get())

        inserirProduto(nome, descricao, preco, quantidade, categoria)

        # Obter o ID do produto recém-adicionado
        try:
            with sqlite3.connect("agapeshop.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT produto_id FROM produtos WHERE nome_produto = ? ORDER BY produto_id DESC LIMIT 1", (nome,))
                produto_id = cursor.fetchone()

                if produto_id:
                    produto_id = produto_id[0]
                    # Registrar a movimentação no inventário
                    registrar_movimentacao(
                        produto_id=produto_id,
                        quantidade=quantidade,
                        tipo_movimentacao="entrada",
                        observacao="Estoque inicial ao adicionar produto"
                    )

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao registrar no inventário: {e}")

        messagebox.showinfo("Sucesso", "Produto Adicionado!")
        window.destroy()
        menu_principal("Usuário")

    window = CTk.CTk()
    window.title("Adicionar Produto")
    window.geometry("700x700")

    CTk.CTkLabel(window, text="Adicionar Produto", font=("Arial", 20, "bold")).pack(pady=10)

    CTk.CTkLabel(window, text="Nome").pack(pady=10)
    nome_entry = CTk.CTkEntry(window, width=300)
    nome_entry.pack(pady=10)

    CTk.CTkLabel(window, text="Descrição").pack(pady=10)
    descricao_entry = CTk.CTkEntry(window, width=300)
    descricao_entry.pack(pady=10)

    CTk.CTkLabel(window, text="Preço").pack(pady=10)
    preco_entry = CTk.CTkEntry(window, width=300)
    preco_entry.pack(pady=10)

    CTk.CTkLabel(window, text="Quantidade").pack(pady=10)
    quantidade_entry = CTk.CTkEntry(window, width=300)
    quantidade_entry.pack(pady=10)

    CTk.CTkLabel(window, text="Categoria (1: Livraria, 2: Roupas, 3: Acessórios)").pack(pady=10)
    categoria_entry = CTk.CTkEntry(window, width=300)
    categoria_entry.pack(pady=10)

    CTk.CTkButton(window, text="Salvar", width=300, command=lambda: save_product()).pack(pady=10)
    CTk.CTkButton(window, text="Cancelar", width=300, command=lambda: [window.destroy(), menu_principal("Usuário")]).pack(pady=10)

    window.mainloop()


#deleta produto na base de dados
def delete_product_from_db(produto_id):
    """Função para deletar um produto do banco de dados usando o ID."""
    try:
        with sqlite3.connect('agapeshop.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM produtos WHERE produto_id = ?", (produto_id,))
            produto = cursor.fetchone()

            if produto:
                cursor.execute("DELETE FROM produtos WHERE produto_id = ?", (produto_id,))
                conn.commit()
                return True  # Produto deletado com sucesso
            else:
                print(f"Nenhum produto encontrado com o ID {produto_id}.")
                return False  # Produto não encontrado
    except sqlite3.Error as e:
        print(f"Erro ao deletar produto: {e}")
        return False

# Remover produto pela interface
def remover_produto():
    def delete_product():
        try:
            produto_id = int(produto_id_entry.get())  # Valida se o ID é numérico
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um ID válido!")
            return

        # Tenta deletar o produto do banco de dados
        if delete_product_from_db(produto_id):
            messagebox.showinfo("Sucesso", f"Produto com ID {produto_id} removido!")
            window.destroy()
            menu_principal("Usuário")
        else:
            messagebox.showerror("Erro", f"Nenhum produto encontrado com o ID {produto_id}.")

    # Criar a janela para remover produtos
    window = CTk.CTk()
    window.title("Remover Produto")
    window.geometry("400x400")

    # Título e entrada
    CTk.CTkLabel(window, text="Remover Produto", font=("Arial", 20, "bold")).pack(pady=10)
    CTk.CTkLabel(window, text="ID do Produto").pack(pady=10)
    produto_id_entry = CTk.CTkEntry(window, width=300)
    produto_id_entry.pack(pady=10)

    # Botões
    CTk.CTkButton(window, text="Remover", width=300, command=delete_product).pack(pady=10)
    CTk.CTkButton(window, text="Cancelar", width=300, command=lambda: [window.destroy(), menu_principal("Usuário")]).pack(pady=10)

    window.mainloop()

# janela relacionado a vendas
def janela_vendas():
    carrinho = []  # Lista para armazenar os produtos adicionados ao carrinho
    forma_pagamento_var = CTk.StringVar(value="Dinheiro")  # Valor padrão para a forma de pagamento

    def adicionar_ao_carrinho():
        try:
            produto_id = int(produto_id_entry.get())
            quantidade = int(quantidade_entry.get())

            with sqlite3.connect("agapeshop.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT produto_id, nome_produto, preco, quantidade_estoque FROM produtos WHERE produto_id = ?", (produto_id,))
                produto = cursor.fetchone()

                if produto:
                    nome, preco, estoque = produto[1], produto[2], produto[3]
                    if quantidade > estoque:
                        messagebox.showerror("Erro", "Quantidade insuficiente no estoque!")
                        return

                    carrinho.append({"id": produto_id, "nome": nome, "quantidade": quantidade, "preco": preco})
                    atualizar_carrinho()
                else:
                    messagebox.showerror("Erro", "Produto não encontrado.")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos para ID e quantidade.")

    def atualizar_carrinho():
        for widget in carrinho_frame.winfo_children():
            widget.destroy()

        total = 0
        for item in carrinho:
            total += item["quantidade"] * item["preco"]
            CTk.CTkLabel(carrinho_frame, text=f"{item['nome']} - {item['quantidade']} x €{item['preco']}").pack()

        CTk.CTkLabel(carrinho_frame, text=f"Total: €{total:.2f}", font=("Arial", 14, "bold")).pack()

    def finalizar_venda():
        if not carrinho:
            messagebox.showerror("Erro", "O carrinho está vazio!")
            return

        forma_pagamento = forma_pagamento_var.get().strip()
        print(f"Forma de pagamento selecionada: {forma_pagamento}")

        try:
            with sqlite3.connect("agapeshop.db") as conn:
                cursor = conn.cursor()

            # Get the payment method ID
                cursor.execute(
                        "SELECT pagamento_id FROM tipo_pagamento WHERE LOWER(TRIM(metodo_pagamento)) = LOWER(TRIM(?))",
                (forma_pagamento,)
                                    )

                pagamento_id = cursor.fetchone()
                print(f"Resultado do banco de dados: {pagamento_id}")

                if not pagamento_id:
                    messagebox.showerror("Erro", "Forma de pagamento inválida!")
                    return

                pagamento_id = pagamento_id[0]  # Extract the payment method ID

            # Calculate the total and insert the sale record
                total = sum(item["quantidade"] * item["preco"] for item in carrinho)
                cursor.execute("INSERT INTO vendas (total, pagamento_id) VALUES (?, ?)", (total, pagamento_id))
                venda_id = cursor.lastrowid  # Get the ID of the inserted sale

            # Update stock and register in inventory for each product in the cart
                for item in carrinho:
                # Update the product stock
                    cursor.execute(
                        "UPDATE produtos SET quantidade_estoque = quantidade_estoque - ? WHERE produto_id = ?",
                        (item["quantidade"], item["id"])
                    )

                # Register the movement in the inventory
                    registrar_movimentacao(
                        produto_id=item["id"],
                        quantidade=item["quantidade"],
                        tipo_movimentacao="saida",
                        observacao=f"Venda ID {venda_id}"
                    )

                conn.commit()  # Commit the transaction
                messagebox.showinfo("Sucesso", "Venda finalizada com sucesso!")
                carrinho.clear()
                atualizar_carrinho()

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao finalizar venda: {e}")



    # Janela principal
    window = CTk.CTk()
    window.title("Vendas")
    window.geometry("600x700")

    # Seleção de produto
    CTk.CTkLabel(window, text="ID do Produto").pack(pady=5)
    produto_id_entry = CTk.CTkEntry(window, width=300)
    produto_id_entry.pack(pady=5)

    CTk.CTkLabel(window, text="Quantidade").pack(pady=5)
    quantidade_entry = CTk.CTkEntry(window, width=300)
    quantidade_entry.pack(pady=5)

    CTk.CTkButton(window, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho).pack(pady=10)

    # Carrinho
    CTk.CTkLabel(window, text="Carrinho de Compras", font=("Arial", 16, "bold")).pack(pady=10)
    carrinho_frame = CTk.CTkScrollableFrame(window, width=500, height=200)
    carrinho_frame.pack(pady=10)

    # Seleção de forma de pagamento
    CTk.CTkLabel(window, text="Forma de Pagamento").pack(pady=10)
    CTk.CTkRadioButton(window, text="Dinheiro", variable=forma_pagamento_var, value="Dinheiro").pack()
    CTk.CTkRadioButton(window, text="Multibanco", variable=forma_pagamento_var, value="Multibanco").pack()
    CTk.CTkRadioButton(window, text="Mb Way", variable=forma_pagamento_var, value="Mb Way").pack()

    # Botões
    CTk.CTkButton(window, text="Finalizar Venda", command=finalizar_venda).pack(pady=10)
    CTk.CTkButton(window, text="Cancelar", command=window.destroy).pack(pady=10)

    window.mainloop()


def mostrar_inventario():
    try:
        inventario = consultar_inventario()
        
        if not inventario:
            messagebox.showinfo("Inventário", "Não há dados no inventário.")
            return

        window = CTk.CTk()
        window.title("Inventário")
        window.geometry("700x500")

        frame = CTk.CTkScrollableFrame(window, width=650, height=400)
        frame.pack(pady=20)

        # Cabeçalhos
        CTk.CTkLabel(frame, text="ID | Produto | Quantidade | Tipo | Data | Observação", font=("Arial", 14, "bold")).pack(pady=5)

        # Dados do inventário
        for row in inventario:
            CTk.CTkLabel(frame, text=f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}").pack(pady=5)

        CTk.CTkButton(window, text="Fechar", command=window.destroy).pack(pady=10)

        window.mainloop()

    except Exception as e:
        messagebox.showerror("Erro",f"Erro ao carregar o inventário:{e}")


def update_produto():
    try:
        window = CTk.CTk()
        window.title("Atualizar Produto")
        window.geometry("700x600")

        # Campo de entrada para o ID do produto
        CTk.CTkLabel(window, text="ID do Produto").pack(pady=10)
        produto_id_entry = CTk.CTkEntry(window, width=300)
        produto_id_entry.pack(pady=10)

        # Campo de entrada para o novo nome
        CTk.CTkLabel(window, text="Novo Nome").pack(pady=10)
        novo_nome_entry = CTk.CTkEntry(window, width=300)
        novo_nome_entry.pack(pady=10)

        # Campo de entrada para o novo preço
        CTk.CTkLabel(window, text="Novo Preço").pack(pady=10)
        novo_preco_entry = CTk.CTkEntry(window, width=300)
        novo_preco_entry.pack(pady=10)

        # Campo de entrada para a nova quantidade em estoque
        CTk.CTkLabel(window, text="Nova Quantidade").pack(pady=10)
        nova_quantidade_entry = CTk.CTkEntry(window, width=300)
        nova_quantidade_entry.pack(pady=10)

        # Botão para atualizar o produto
        CTk.CTkButton(
            window,
            text="Atualizar Produto",
            command=lambda: update(
                produto_id_entry.get(),
                novo_nome_entry.get(),
                novo_preco_entry.get(),
                nova_quantidade_entry.get(),
                window
            ),
        ).pack(pady=10)

        window.mainloop()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir a janela: {e}")


def mostrar_estoque_por_data():
    def buscar():
        data_limite = data_entry.get()
        if not data_limite:
            messagebox.showerror("Erro", "Por favor, insira uma data válida.")
            return

        estoque = consultar_estoque_por_data(data_limite)  #$ ATUALMENTE USANDO ESSE POREM NAO APARECE A QUANTIDADE DO ESTOQUE
        #estoque = consultar_estoque() #TESTANDO PARA VER SE APARECE QUANTIDADE DO ESTOQUE mostra o estoque atual
        if not estoque:
            messagebox.showinfo("Estoque", "Nenhum registro encontrado para a data fornecida.")
            return

        for widget in frame.winfo_children():
            widget.destroy()



        for item in estoque:
            produto_id, nome, descricao, preco, quantidade = item
            CTk.CTkLabel(
                frame, 
                text=f"ID: {produto_id} | Nome: {nome} | Descrição: {descricao}| Estoque: {quantidade} | Preço: €{preco:.2f} ",
                font=("Arial", 12)
            ).pack(pady=5) 

            

    window = CTk.CTk()
    window.title("Consultar Estoque por Data")
    window.geometry("800x700")

    CTk.CTkLabel(window, text="Consultar Estoque por Data", font=("Arial", 16, "bold")).pack(pady=10)
    CTk.CTkLabel(window, text="Data (YYYY-M-DD):").pack(pady=5)
    data_entry = CTk.CTkEntry(window, width=300)
    data_entry.pack(pady=5)

    CTk.CTkButton(window, text="Buscar", command=buscar).pack(pady=10)
    
    frame = CTk.CTkScrollableFrame(window, width=650, height=400)
    frame.pack(pady=20)

    CTk.CTkButton(window, text="Fechar", command=window.destroy).pack(pady=10)

    window.mainloop()
    

def exportar_inventario_por_data():
    def buscar():
        data_limite = data_entry.get()
        if not data_limite:
            messagebox.showerror("Erro", "Por favor, insira uma data válida.")
            return

        # Consulta o inventário por data
        inventario = consultar_estoque_por_data(data_limite)
        if not inventario:
            messagebox.showinfo("Inventário", "Nenhum registro encontrado para a data fornecida.")
            return

        # Salvar arquivo Excel
        salvar_arquivo_excel(inventario, data_limite)

    def salvar_arquivo_excel(inventario, data_limite):
        # Solicitar local para salvar o arquivo
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            title="Salvar Relatório como"
        )
        if not arquivo:
            return  # Se o usuário cancelar, não faz nada

        # Criar o arquivo Excel
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = f"Inventário {data_limite}"

        # Cabeçalhos
        sheet.append(["ID Produto", "Nome", "Descrição", "Preço (€)", "Estoque Atual"])

        # Dados do inventário
        for item in inventario:
            produto_id, nome, descricao, preco, estoque_atual = item
            sheet.append([produto_id, nome, descricao, f"{preco:.2f}", estoque_atual])

        # Salvar o arquivo Excel
        workbook.save(arquivo)
        messagebox.showinfo("Sucesso", f"Relatório exportado como Excel em: {arquivo}")

    # Janela para selecionar data
    window = CTk.CTk()
    window.title("Exportar Inventário por Data")
    window.geometry("400x300")

    CTk.CTkLabel(window, text="Exportar Inventário por Data", font=("Arial", 16, "bold")).pack(pady=10)
    CTk.CTkLabel(window, text="Data (YYYY-M-DD):").pack(pady=5)
    data_entry = CTk.CTkEntry(window, width=300)
    data_entry.pack(pady=10)

    CTk.CTkButton(window, text="Exportar", command=buscar).pack(pady=10)
    CTk.CTkButton(window, text="Cancelar", command=window.destroy).pack(pady=5)

    window.mainloop()


def consultar_estoque_por_data(data_limite):
    try:
        with sqlite3.connect("agapeshop.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    p.produto_id, 
                    p.nome_produto, 
                    p.descricao_produto, 
                    p.preco, 
                    COALESCE(SUM(CASE WHEN i.tipo_movimentacao = 'entrada' THEN i.quantidade
                                     WHEN i.tipo_movimentacao = 'saida' THEN -i.quantidade
                                     ELSE 0 END), 0) AS estoque_atual
                FROM produtos p
                LEFT JOIN inventario i ON p.produto_id = i.produto_id AND i.data_movimentacao <= ?
                GROUP BY p.produto_id, p.nome_produto, p.descricao_produto, p.preco
                ORDER BY p.produto_id;
            ''', (data_limite,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao consultar estoque: {e}")
        return []
