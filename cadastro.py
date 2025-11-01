import customtkinter as ctk
from database import conectar, hash_senha
import re
import sqlite3

class Cadastro(ctk.CTkFrame):
    """
    Frame (tela) de Cadastro de Usuário.
    Atualizado com centralização vertical.
    """
    
    GEOMETRIA = "850x650" # Tamanho Padrão

    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color="#D9D9D9") 
        self.controlador = controlador

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

        # --- Painel Direito (Formulário de Cadastro - CENTRALIZADO) ---
        self.painel_direito = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.painel_direito.pack(side="right", fill="both", expand=True, padx=20, pady=15)

        # Frame de conteúdo para centralização
        self.content_frame = ctk.CTkFrame(self.painel_direito, fg_color="transparent")
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.content_frame, text="CADASTRO", font=("Segoe UI", 36, "bold"), text_color="#24232F").pack(pady=(20, 15))

        # Campo Nome
        self.nome_frame = ctk.CTkFrame(self.content_frame, fg_color="white", border_color="#E0E0E0", border_width=1, corner_radius=10, height=45)
        self.nome_frame.pack(pady=5, fill="x", padx=40)
        self.nome_frame.pack_propagate(False)
        ctk.CTkLabel(self.nome_frame, text="👤", font=("Segoe UI Emoji", 20), text_color="#24232F", fg_color="transparent").pack(side="left", padx=(10, 5))
        self.nome = ctk.CTkEntry(self.nome_frame, placeholder_text="Nome", 
                                 fg_color="white", border_width=0, text_color="#24232F",
                                 placeholder_text_color="#888888", height=40)
        self.nome.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Campo E-mail
        self.email_frame = ctk.CTkFrame(self.content_frame, fg_color="white", border_color="#E0E0E0", border_width=1, corner_radius=10, height=45)
        self.email_frame.pack(pady=5, fill="x", padx=40)
        self.email_frame.pack_propagate(False)
        ctk.CTkLabel(self.email_frame, text="📧", font=("Segoe UI Emoji", 20), text_color="#24232F", fg_color="transparent").pack(side="left", padx=(10, 5))
        self.email = ctk.CTkEntry(self.email_frame, placeholder_text="E-mail", 
                                  fg_color="white", border_width=0, text_color="#24232F",
                                  placeholder_text_color="#888888", height=40)
        self.email.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Campo Senha
        self.senha_frame = ctk.CTkFrame(self.content_frame, fg_color="white", border_color="#E0E0E0", border_width=1, corner_radius=10, height=45)
        self.senha_frame.pack(pady=5, fill="x", padx=40)
        self.senha_frame.pack_propagate(False)
        ctk.CTkLabel(self.senha_frame, text="🔒", font=("Segoe UI Emoji", 20), text_color="#24232F", fg_color="transparent").pack(side="left", padx=(10, 5))
        self.senha = ctk.CTkEntry(self.senha_frame, placeholder_text="Senha (mín. 6 chars)", show="*", 
                                  fg_color="white", border_width=0, text_color="#24232F",
                                  placeholder_text_color="#888888", height=40)
        self.senha.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Campo Confirmar Senha
        self.confirmar_senha_frame = ctk.CTkFrame(self.content_frame, fg_color="white", border_color="#E0E0E0", border_width=1, corner_radius=10, height=45)
        self.confirmar_senha_frame.pack(pady=5, fill="x", padx=40)
        self.confirmar_senha_frame.pack_propagate(False)
        ctk.CTkLabel(self.confirmar_senha_frame, text="🔒", font=("Segoe UI Emoji", 20), text_color="#24232F", fg_color="transparent").pack(side="left", padx=(10, 5))
        self.confirmar_senha = ctk.CTkEntry(self.confirmar_senha_frame, placeholder_text="Confirmar senha", show="*",
                                  fg_color="white", border_width=0, text_color="#24232F",
                                  placeholder_text_color="#888888", height=40)
        self.confirmar_senha.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Botão Cadastrar
        self.btn_cadastrar = ctk.CTkButton(self.content_frame, text="Cadastrar", command=self.cadastrar, 
                                           fg_color="#24232F", hover_color="#3a3a4f", 
                                           text_color="white", width=200, height=40, corner_radius=10)
        self.btn_cadastrar.pack(pady=(20, 10))

        self.status = ctk.CTkLabel(self.content_frame, text="", text_color="red")
        self.status.pack(pady=5)
        
        self.btn_voltar = ctk.CTkButton(self.content_frame, text="entrar", command=self.voltar, 
                                        fg_color="transparent", hover_color="#F0F0F0",
                                        text_color="#24232F", font=("Segoe UI", 13))
        self.btn_voltar.pack(pady=(0, 5))
        # --- Fim do Painel Direito ---

    def cadastrar(self):
        # (Lógica sem alteração)
        nome = self.nome.get().strip()
        email = self.email.get().strip()
        senha = self.senha.get()
        confirmar_senha = self.confirmar_senha.get()

        if not nome or not email or not senha or not confirmar_senha:
            self.status.configure(text="Preencha todos os campos.", text_color="red")
            return
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.status.configure(text="E-mail inválido.", text_color="red")
            return
        if len(senha) < 6:
            self.status.configure(text="Senha deve ter pelo menos 6 caracteres.", text_color="red")
            return
        if senha != confirmar_senha:
            self.status.configure(text="As senhas não coincidem.", text_color="red")
            return
            
        try:
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, hash_senha(senha)))
            self.status.configure(text="Usuário cadastrado com sucesso!", text_color="green")
            self.nome.delete(0, 'end')
            self.email.delete(0, 'end')
            self.senha.delete(0, 'end')
            self.confirmar_senha.delete(0, 'end')
        except sqlite3.IntegrityError:
            self.status.configure(text="Erro: e-mail já cadastrado.", text_color="red")
        except sqlite3.Error as e:
            self.status.configure(text=f"Erro no banco: {str(e)}", text_color="red")
        except Exception as e:
            self.status.configure(text=f"Erro inesperado: {str(e)}", text_color="red")

    def voltar(self):
        # (Lógica sem alteração)
        self.status.configure(text="")
        self.nome.delete(0, 'end')
        self.email.delete(0, 'end')
        self.senha.delete(0, 'end')
        self.confirmar_senha.delete(0, 'end')
        self.controlador.mostrar_tela("Login")