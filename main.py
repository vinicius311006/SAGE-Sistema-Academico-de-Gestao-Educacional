"""
Arquivo Principal (main.py) - SAGE (Sistema Acadêmico de Gestão Educacional)
"""

import customtkinter as ctk
from database import criar_tabelas

# Importa todas as classes de tela dos seus respectivos arquivos .py
from login import Login
from cadastro import Cadastro
from menu import MenuPrincipal
from aluno import Aluno
from turma import Turma
from aula import Aula
from visualizacao import Visualizacao
from relatorio import Relatorio
from chatbot import Chatbot
from atividades import Atividades # <-- 1. IMPORTA A NOVA TELA

class Aplicativo(ctk.CTk):
    """
    Classe principal da aplicação (Controlador).
    """
    
    def __init__(self):
        """
        Inicializa a janela principal e todos os frames.
        """
        super().__init__()
        
        self.title("SAGE - Sistema Acadêmico de Gestão Educacional")
        self.geometry("850x650") 
        self.resizable(False, False) 

        ctk.set_appearance_mode("dark") 
        ctk.set_default_color_theme("blue")

        container = ctk.CTkFrame(self, fg_color="#24232F")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Tupla com todas as classes de tela que devem ser carregadas
        telas = (Login, Cadastro, MenuPrincipal, Aluno, Turma, 
                 Aula, Visualizacao, Relatorio, Chatbot,
                 Atividades) # <-- 2. ADICIONA A NOVA TELA AQUI

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
        Traz um frame (tela) específico para a frente.
        """
        frame = self.frames[nome_tela]
        frame.tkraise()

# Ponto de entrada da aplicação
if __name__ == "__main__":
    print("Criando tabelas do banco de dados (se não existirem)...")
    criar_tabelas() 
    app = Aplicativo() 
    app.mainloop()