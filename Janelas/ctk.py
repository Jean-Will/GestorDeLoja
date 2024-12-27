import customtkinter as CTk
from Funcoes.functions import validar_usuario , registrar_usuario , mostrarProdutos,inserirProduto
import sqlite3
from tkinter import messagebox
from fpdf import FPDF
from tkinter import filedialog


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
        CTk.CTkMessagebox.show_info("Sucesso", "Usuário registrado!")
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

    CTk.CTkButton(window, text="Registrar", width=300, command=save_user).pack(pady=20)
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
    menu.geometry("400x400")

    CTk.CTkLabel(menu, text=f"Bem-vindo, {username}!", font=("Arial", 20, "bold")).pack(pady=20)
    CTk.CTkButton(menu, text="Consultar Estoque", width=300, command=open_consulta_estoque).pack(pady=10)
    CTk.CTkButton(menu, text="Adicionar Produto", width=300, command=open_add_produto).pack(pady=10)
    CTk.CTkButton(menu, text="Remover Produto", width=300, command=lambda: [menu.destroy(), remover_produto()]).pack(pady=10)
    CTk.CTkButton(menu, text="Vendas", width=300,command=janela_vendas).pack(pady=10)
    CTk.CTkButton(menu, text="Exportar Relatório", width=300,command=lambda: exportar_relatorio_pdf(relatorio_diario, "Relatorio Diario de Vendas")).pack(pady=10)
    CTk.CTkButton(menu, text="Sair", width=300, command=menu.destroy).pack(pady=20)

    menu.mainloop()


# Janela de consulta de estoque
def consultar_estoque():
    def voltar():
        window.destroy()
        menu_principal("Usuário")

    window = CTk.CTk()
    window.title("Consultar Estoque")
    window.geometry("600x400")

    produtos = mostrarProdutos()

    frame = CTk.CTkScrollableFrame(window, width=550, height=300)
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
        messagebox.showinfo("Sucesso", "Produto Adicionado!")
        window.destroy()
        menu_principal("Usuário")

    window = CTk.CTk()
    window.title("Adicionar Produto")
    window.geometry("500x650")

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

        forma_pagamento = forma_pagamento_var.get()

        try:
            with sqlite3.connect("agapeshop.db") as conn:
                cursor = conn.cursor()

            # Obter o ID da forma de pagamento baseado no nome
                cursor.execute("SELECT pagamento_id FROM tipo_pagamento WHERE metodo_pagamento = ?", (forma_pagamento,))
                pagamento_id = cursor.fetchone()

                if not pagamento_id:
                    messagebox.showerror("Erro", "Forma de pagamento inválida!")
                    return

                pagamento_id = pagamento_id[0]  # Obtem o ID real da tupla retornada

            # Atualizar o estoque para cada produto no carrinho
                for item in carrinho:
                    cursor.execute("UPDATE produtos SET quantidade_estoque = quantidade_estoque - ? WHERE produto_id = ?", (item["quantidade"], item["id"]))

            # Inserir a venda na tabela de vendas
                total = sum(item["quantidade"] * item["preco"] for item in carrinho)
                cursor.execute("INSERT INTO vendas (total, pagamento_id) VALUES (?, ?)", (total, pagamento_id))

                conn.commit()
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
    CTk.CTkRadioButton(window, text="Mbway", variable=forma_pagamento_var, value="Mb Way").pack()

    # Botões
    CTk.CTkButton(window, text="Finalizar Venda", command=finalizar_venda).pack(pady=10)
    CTk.CTkButton(window, text="Cancelar", command=window.destroy).pack(pady=10)

    window.mainloop()


def exportar_relatorio_pdf(relatorio_funcao, titulo="Relatório de Vendas"):
    relatorio = relatorio_funcao()

    if not relatorio:
        messagebox.showerror("Erro", "Não há dados para exportar.")
        return
    
        # Escolher o local para salvar o PDF
    arquivo = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Salvar Relatório como"
    )

    if not arquivo:  # Se o usuário cancelar
        return
    
    #incialização do pdf
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    #Titulo do relatório
    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(200, 10, txt=titulo, ln=True, align="C")

    #Espaço
    pdf.ln(10)

    # Cabeçalhos do Relatório
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(30, 10, "ID Venda", border=1)
    pdf.cell(40, 10, "Produto", border=1)
    pdf.cell(30, 10, "Quantidade", border=1)
    pdf.cell(30, 10, "Preço Unitário", border=1)
    pdf.cell(30, 10, "Total", border=1)
    pdf.cell(30, 10, "Pagamento", border=1)
    pdf.ln()

    # Dados do Relatório
    pdf.set_font("Arial", size=12)
    for venda in relatorio:
        venda_id, total, metodo_pagamento, data_venda, nome_produto, quantidade, preco_unitario = venda
        pdf.cell(30, 10, str(venda_id), border=1)
        pdf.cell(40, 10, nome_produto, border=1)
        pdf.cell(30, 10, str(quantidade), border=1)
        pdf.cell(30, 10, f"€{preco_unitario:.2f}", border=1)
        pdf.cell(30, 10, f"€{quantidade * preco_unitario:.2f}", border=1)
        pdf.cell(30, 10, metodo_pagamento, border=1)
        pdf.ln()

        #Total da Geral
        pdf.ln(10)
        total_geral = sum(venda[5] * venda[6] for venda in relatorio)
        pdf.cell(200, 10, txt=f"Total Geral: €{total_geral:.2f}", ln=True, align="R")

        # salva o arquivo PDF
        pdf.output("relatorio_vendas.pdf")
        messagebox.showinfo("Sucesso", "Relatório exportado com sucesso!")

        #exportar o relatório
        exportar_relatorio_pdf(relatorio_diario, "Relatório de Vendas")



def relatorio_diario():
    """
    Retorna um relatório com todas as vendas realizadas no dia atual,
    incluindo tipo de pagamento.
    """
    try:
        with sqlite3.connect("agapeshop.db") as conn:
            cursor = conn.cursor()
            # Consulta ajustada para incluir o tipo de pagamento
            query = '''
                SELECT v.venda_id, v.total, tp.metodo_pagamento, v.data_venda,
                       p.nome_produto, iv.quantidade, iv.preco_unitario
                FROM vendas v
                JOIN itens_venda iv ON v.venda_id = iv.venda_id
                JOIN produtos p ON iv.produto_id = p.produto_id
                JOIN tipo_pagamento tp ON v.pagamento_id = tp.pagamento_id
                WHERE DATE(v.data_venda) = DATE('now')
                ORDER BY v.data_venda DESC
            '''
            cursor.execute(query)
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao gerar relatório diário: {e}")
        return []
