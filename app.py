from Janelas.ctk import start_application
from Funcoes.functions import iniciaDB


if __name__ == "__main__":
    # Inicializa o banco de dados
    iniciaDB()

    # Inicia a interface
    start_application()
    