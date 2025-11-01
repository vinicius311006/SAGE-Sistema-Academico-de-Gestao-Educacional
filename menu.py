"""
Arquivo da Tela de Menu (menu.py)

Este módulo define a classe 'MenuPrincipal', que serve como
o "hub" de navegação principal após o login do usuário.
"""

import customtkinter as ctk

class MenuPrincipal(ctk.CTkFrame):
    """
    Frame (tela) do Menu Principal.
    Contém botões para navegar para todas as outras
    funcionalidades do sistema.
    """
    
    GEOMETRIA = "850x650" # Tamanho Padrão

    def __init__(self, parent, controlador):
        """
        Inicializa o frame do Menu Principal.
        """
        super().__init__(parent, fg_color="#D9D9D9") 
        self.controlador = controlador

        # --- Layout do Card (Padrão) ---
        self.card_frame = ctk.CTkFrame(self, fg_color="#F0F0F0", corner_radius=20)
        self.card_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

        # --- Painel Esquerdo (SAGE Branding - CENTRALIZADO) ---
        self.painel_esquerdo = ctk.CTkFrame(self.card_frame, fg_color="#24232F", corner_radius=15, width=300)
        self.painel_esquerdo.pack(side="left", fill="both", expand=False, padx=15, pady=15)
        self.painel_esquerdo.pack_propagate(False)

        ctk.CTkFrame(self.painel_esquerdo, fg_color="transparent").pack(side="top", fill="both", expand=True)
        ctk.CTkLabel(self.painel_esquerdo, text="SAGE", font=("Segoe UI", 36, "bold"), text_color="white").pack(pady=(0, 10))
        ctk.CTkLabel(self.painel_esquerdo, text="Sistema Acadêmico\nde Gestão Educacional", 
                     font=("Segoe UI", 16), text_color="#A9A9A9", justify="center").pack()
        ctk.CTkFrame(self.painel_esquerdo, fg_color="transparent").pack(side="bottom", fill="both", expand=True)
        # --- Fim do Painel Esquerdo ---

        # --- Painel Direito (Menu - CENTRALIZADO) ---
        self.painel_direito = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.painel_direito.pack(side="right", fill="both", expand=True, padx=20, pady=15)

        self.content_frame = ctk.CTkFrame(self.painel_direito, fg_color="transparent")
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center") 
        
        ctk.CTkLabel(self.content_frame, text="Menu Principal", font=("Segoe UI", 36, "bold"), text_color="#24232F").pack(pady=30)

        # Dicionário de botões
        botoes = {
            "👤 Cadastrar Aluno": "Aluno",
            "🏫 Cadastrar Turma": "Turma",
            "📚 Registrar Aula": "Aula",
            "📝 Gestão de Atividades": "Atividades",
            "👀 Visualizar Alunos": "Visualizacao",
            "📊 Relatório de Aulas": "Relatorio",
            "🤖 Chatbot Acadêmico": "Chatbot"
        }

        # Cria os botões dinamicamente
        for texto, nome_frame in botoes.items():
            btn = ctk.CTkButton(self.content_frame, 
                                text=texto, 
                                command=lambda f=nome_frame: self.navegar_para(f), 
                                width=250, 
                                height=40,
                                corner_radius=10,
                                fg_color="#24232F", 
                                text_color="white", 
                                hover_color="#3A3A46")
            btn.pack(pady=7)
        # --- Fim do Painel Direito ---

    def navegar_para(self, nome_frame):
        """
        Função genérica de navegação chamada pelos botões.
        """
        print(f"Navegando para {nome_frame}")
        self.controlador.mostrar_tela(nome_frame)