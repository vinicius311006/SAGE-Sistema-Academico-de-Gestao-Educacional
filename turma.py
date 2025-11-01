import customtkinter as ctk
from database import conectar
import sqlite3

class Turma(ctk.CTkFrame):
    """
    Frame (tela) para Cadastro de Turmas.
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

        # --- Painel Direito (Formulário - CENTRALIZADO) ---
        self.painel_direito = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.painel_direito.pack(side="right", fill="both", expand=True, padx=20, pady=15)

        # Frame de conteúdo para centralização
        self.content_frame = ctk.CTkFrame(self.painel_direito, fg_color="transparent")
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center") 
        
        ctk.CTkLabel(self.content_frame, text="Cadastro de Turma", font=("Segoe UI", 36, "bold"), text_color="#24232F").pack(pady=30)

        self.nome = ctk.CTkEntry(self.content_frame,
                                 placeholder_text="Nome da Turma", 
                                 width=300, height=40,
                                 fg_color="white", 
                                 border_color="#E0E0E0", border_width=1,
                                 text_color="#24232F",
                                 placeholder_text_color="#888888")
        self.nome.pack(pady=10)

        self.btn_salvar = ctk.CTkButton(self.content_frame,
                                        text="Salvar", command=self.salvar_turma, 
                                        fg_color="#24232F", hover_color="#3A3A46", 
                                        width=200, height=40, corner_radius=10)
        self.btn_salvar.pack(pady=10)

        self.status = ctk.CTkLabel(self.content_frame, text="", text_color="green")
        self.status.pack(pady=10)

        self.btn_voltar = ctk.CTkButton(self.content_frame,
                                        text="Voltar", command=self.voltar, 
                                        fg_color="#A9A9A9", text_color="#24232F", 
                                        hover_color="#B9B9B9", width=150, height=35, corner_radius=10)
        self.btn_voltar.pack(pady=10)
        # --- Fim do Painel Direito ---

    def salvar_turma(self):
        # (Lógica sem alteração)
        nome = self.nome.get().strip()
        if not nome:
            self.status.configure(text="Preencha o nome da turma.", text_color="red")
            return
        try:
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO turmas (nome) VALUES (?)", (nome,))
            self.status.configure(text="Turma cadastrada com sucesso!", text_color="green")
            self.nome.delete(0, 'end')
        except sqlite3.Error as e:
            self.status.configure(text=f"Erro no banco: {str(e)}", text_color="red")
        except Exception as e:
            self.status.configure(text=f"Erro: {str(e)}", text_color="red")

    def voltar(self):
        # (Lógica sem alteração)
        self.status.configure(text="")
        self.nome.delete(0, 'end')
        self.controlador.mostrar_tela("MenuPrincipal")