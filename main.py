import customtkinter as ctk
from database import criar_tabelas

# Importa todas as "telas" (que são Frames)
from login import Login
from cadastro import Cadastro
from menu import MenuPrincipal
from aluno import Aluno
from turma import Turma
from aula import Aula
from visualizacao import Visualizacao
from relatorio import Relatorio
from chatbot import Chatbot

class Aplicativo(ctk.CTk):
    """
    Classe principal da aplicação (Controlador).
    Esta janela única gerencia todos os "frames" (telas) da aplicação,
    trocando entre eles conforme a necessidade.
    """
    def __init__(self):
        super().__init__()
        
        self.title("SAGE - Sistema Acadêmico de Gestão Educacional")
        self.geometry("850x650") # Geometria padrão inicial

        ctk.set_appearance_mode("dark") # Mantemos 'dark' para a barra de título
        ctk.set_default_color_theme("blue")

        # Container principal onde todos os frames (telas) serão empilhados
        container = ctk.CTkFrame(self, fg_color="#24232F")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dicionário para armazenar todas as telas
        self.frames = {}

        # Lista de todas as classes de tela para inicializar
        telas = (Login, Cadastro, MenuPrincipal, Aluno, Turma, 
                 Aula, Visualizacao, Relatorio, Chatbot)

        # Itera sobre as classes de tela, criando uma instância de cada
        for F in telas:
            nome_tela = F.__name__
            frame = F(parent=container, controlador=self) 
            self.frames[nome_tela] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        print("App inicializada. Mostrando tela de Login.")
        self.mostrar_tela("Login")

    def mostrar_tela(self, nome_tela):
        """
        Traz um frame (tela) para a frente e ajusta o tamanho da janela.
        """
        frame = self.frames[nome_tela]
        
        if hasattr(frame, 'GEOMETRIA'):
            self.geometry(frame.GEOMETRIA)
        else:
            self.geometry("700x600") 
            
        frame.tkraise()

if __name__ == "__main__":
    print("Criando tabelas do banco de dados (se não existirem)...")
    criar_tabelas() 
    app = Aplicativo()
    app.mainloop()