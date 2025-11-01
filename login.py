import customtkinter as ctk
from database import conectar, verificar_senha
import re
import sqlite3

class Login(ctk.CTkFrame):
    """
    Frame (tela) de Login.
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

        # Spacer superior para empurrar o conteúdo para o meio
        ctk.CTkFrame(self.painel_esquerdo, fg_color="transparent").pack(side="top", fill="both", expand=True)

        ctk.CTkLabel(self.painel_esquerdo, text="SAGE", font=("Segoe UI", 36, "bold"), text_color="white").pack(pady=(0, 10))
        ctk.CTkLabel(self.painel_esquerdo, text="Sistema Acadêmico\nde Gestão Educacional", 
                     font=("Segoe UI", 16), text_color="#A9A9A9", justify="center").pack()

        # Spacer inferior para empurrar o conteúdo para o meio
        ctk.CTkFrame(self.painel_esquerdo, fg_color="transparent").pack(side="bottom", fill="both", expand=True)
        # --- Fim do Painel Esquerdo ---

        # --- Painel Direito (Formulário de Login - CENTRALIZADO) ---
        self.painel_direito = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.painel_direito.pack(side="right", fill="both", expand=True, padx=20, pady=15)

        # Frame de conteúdo para centralização
        self.content_frame = ctk.CTkFrame(self.painel_direito, fg_color="transparent")
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.content_frame, text="LOGIN", font=("Segoe UI", 36, "bold"), text_color="#24232F").pack(pady=(30, 20))

        # Campo E-mail
        self.email_frame = ctk.CTkFrame(self.content_frame, fg_color="white", border_color="#E0E0E0", border_width=1, corner_radius=10, height=45)
        self.email_frame.pack(pady=10, fill="x", padx=40)
        self.email_frame.pack_propagate(False)
        ctk.CTkLabel(self.email_frame, text="👤", font=("Segoe UI Emoji", 20), text_color="#24232F", fg_color="transparent").pack(side="left", padx=(10, 5))
        self.email = ctk.CTkEntry(self.email_frame, placeholder_text="E-mail", 
                                  fg_color="white", border_width=0, text_color="#24232F",
                                  placeholder_text_color="#888888", height=40)
        self.email.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Campo Senha
        self.senha_frame = ctk.CTkFrame(self.content_frame, fg_color="white", border_color="#E0E0E0", border_width=1, corner_radius=10, height=45)
        self.senha_frame.pack(pady=10, fill="x", padx=40)
        self.senha_frame.pack_propagate(False)
        ctk.CTkLabel(self.senha_frame, text="🔒", font=("Segoe UI Emoji", 20), text_color="#24232F", fg_color="transparent").pack(side="left", padx=(10, 5))
        self.senha = ctk.CTkEntry(self.senha_frame, placeholder_text="Senha", show="*",
                                  fg_color="white", border_width=0, text_color="#24232F",
                                  placeholder_text_color="#888888", height=40)
        self.senha.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Botão Entrar
        self.btn_login = ctk.CTkButton(self.content_frame, text="Entrar", command=self.verificar_login,
                                       fg_color="#24232F", hover_color="#3A3A46", 
                                       text_color="white", width=200, height=40, corner_radius=10)
        self.btn_login.pack(pady=(20, 10))
        
        # Botão Cadastrar (como texto)
        self.btn_cadastro = ctk.CTkButton(self.content_frame, text="cadastrar", command=self.abrir_cadastro, 
                                          fg_color="transparent", hover_color="#F0F0F0",
                                          text_color="#24232F", font=("Segoe UI", 13))
        self.btn_cadastro.pack(pady=(0, 5))

        # Label de Status
        self.status = ctk.CTkLabel(self.content_frame, text="", text_color="red")
        self.status.pack(pady=5)
        # --- Fim do Painel Direito ---

    def verificar_login(self):
        # (Lógica sem alteração)
        email = self.email.get().strip()
        senha = self.senha.get()

        if not email or not senha:
            self.status.configure(text="Preencha todos os campos.", text_color="red")
            return
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.status.configure(text="E-mail inválido.", text_color="red")
            return
        try:
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT senha FROM usuarios WHERE email = ?", (email,))
                result = cursor.fetchone()
            if result and verificar_senha(senha, result[0]):
                self.status.configure(text="Login bem-sucedido!", text_color="green")
                self.email.delete(0, 'end')
                self.senha.delete(0, 'end')
                self.after(1000, lambda: self.controlador.mostrar_tela("MenuPrincipal"))
            else:
                self.status.configure(text="Email ou senha incorretos.", text_color="red")
        except sqlite3.Error as e:
            self.status.configure(text=f"Erro no banco de dados: {e}", text_color="red")
        except Exception as e:
            self.status.configure(text=f"Erro: {e}", text_color="red")

    def abrir_cadastro(self):
        # (Lógica sem alteração)
        self.status.configure(text="")
        self.controlador.mostrar_tela("Cadastro")