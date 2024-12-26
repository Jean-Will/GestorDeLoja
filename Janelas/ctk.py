import customtkinter as CTk

from Funcoes.functions import validar_usuario , registrar_usuario , mostrarProdutos , insert


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
            CTk.CTkMessagebox.show_error("Erro", "Usuário ou senha incorretos!")

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


# Janela de registro
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

    #CTk.CTkButton(window, text="Registrar", width=300, command=save_user).pack(pady=20) ESSA FUNCIONA SO NAO FECHA A JANELA
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

    menu = CTk.CTk()
    menu.title("Menu Principal - Agape Shop")
    menu.geometry("400x400")

    CTk.CTkLabel(menu, text=f"Bem-vindo, {username}!", font=("Arial", 20, "bold")).pack(pady=20)
    CTk.CTkButton(menu, text="Consultar Estoque", width=300, command=open_consulta_estoque).pack(pady=10)
    CTk.CTkButton(menu, text="Adicionar Produto", width=300, command=open_add_produto).pack(pady=10)
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
    for produto in produtos:
        CTk.CTkLabel(frame, text=f"{produto[1]} - {produto[3]} em estoque").pack(pady=5)

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

        insert(nome, descricao, preco, quantidade, categoria)
        CTk.CTkMessagebox.show_info("Sucesso", "Produto Adicionado!")
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

    CTk.CTkButton(window, text="Salvar", width=300, command=save_product).pack(pady=10)
    CTk.CTkButton(window, text="Cancelar", width=300, command=lambda: [window.destroy(), menu_principal("Usuário")]).pack(pady=10)

    window.mainloop()
