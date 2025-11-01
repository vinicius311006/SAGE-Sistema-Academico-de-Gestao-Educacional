import customtkinter as ctk
from database import conectar
from tkcalendar import Calendar
import datetime
import sqlite3

class Aula(ctk.CTkFrame):
    """
    Frame (tela) para Registro de Aulas e Presenças.
    Atualizado com o layout corrigido.
    """
    
    GEOMETRIA = "850x650" # Tamanho Padrão

    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color="#D9D9D9")
        self.controlador = controlador

        # --- Card e Painel Esquerdo (Sem alteração) ---
        self.card_frame = ctk.CTkFrame(self, fg_color="#F0F0F0", corner_radius=20)
        self.card_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.9)

        self.painel_esquerdo = ctk.CTkFrame(self.card_frame, fg_color="#24232F", corner_radius=15, width=300)
        self.painel_esquerdo.pack(side="left", fill="both", expand=False, padx=15, pady=15)
        self.painel_esquerdo.pack_propagate(False)

        ctk.CTkFrame(self.painel_esquerdo, fg_color="transparent").pack(side="top", fill="both", expand=True)
        ctk.CTkLabel(self.painel_esquerdo, text="SAGE", font=("Segoe UI", 36, "bold"), text_color="white").pack(pady=(0, 10))
        ctk.CTkLabel(self.painel_esquerdo, text="Sistema Acadêmico\nde Gestão Educacional", 
                     font=("Segoe UI", 16), text_color="#A9A9A9", justify="center").pack()
        ctk.CTkFrame(self.painel_esquerdo, fg_color="transparent").pack(side="bottom", fill="both", expand=True)
        # --- Fim do Painel Esquerdo ---

        # --- Painel Direito (Layout Corrigido) ---
        self.painel_direito = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.painel_direito.pack(side="right", fill="both", expand=True, padx=20, pady=15)

        # --- 1. Conteúdo do Topo ---
        ctk.CTkLabel(self.painel_direito, text="Registro de Aula", font=("Segoe UI", 36, "bold"), text_color="#24232F").pack(pady=20)

        self.turmas = self.carregar_turmas()
        default_value = self.turmas[0] if self.turmas else "Nenhuma turma cadastrada"
        self.turma_selecionada = ctk.StringVar(value=default_value)
        
        self.dropdown_turma = ctk.CTkOptionMenu(self.painel_direito,
                                                values=self.turmas, 
                                                variable=self.turma_selecionada, 
                                                command=self.carregar_alunos,
                                                height=40,
                                                fg_color="white", button_color="#E0E0E0",
                                                text_color="#24232F", dropdown_fg_color="white",
                                                dropdown_text_color="#24232F")
        self.dropdown_turma.pack(fill="x", padx=20, pady=(0, 10)) # pack fill="x"

        self.data = ctk.CTkEntry(self.painel_direito, placeholder_text="Clique para escolher a data", 
                                 height=40,
                                 fg_color="white", border_color="#E0E0E0", border_width=1,
                                 text_color="#24232F", placeholder_text_color="#888888")
        self.data.pack(fill="x", padx=20, pady=10) # pack fill="x"
        self.data.bind("<Button-1>", self.abrir_calendario)

        self.tema = ctk.CTkEntry(self.painel_direito, placeholder_text="Tema da Aula", 
                                 height=40,
                                 fg_color="white", border_color="#E0E0E0", border_width=1,
                                 text_color="#24232F", placeholder_text_color="#888888")
        self.tema.pack(fill="x", padx=20, pady=10) # pack fill="x"

        self.descricao = ctk.CTkTextbox(self.painel_direito, height=80,
                                        fg_color="white", border_color="#E0E0E0", border_width=1,
                                        text_color="#24232F")
        self.descricao.pack(pady=10, fill="x", padx=20)
        self.descricao.insert("0.0", "Descrição da aula...")
        self.descricao.configure(text_color="#888888")
        self.descricao.bind("<FocusIn>", self.limpar_placeholder)
        self.descricao.bind("<FocusOut>", self.restaurar_placeholder)

        # --- 2. Conteúdo de Baixo (Empacotado ANTES do meio) ---
        self.status = ctk.CTkLabel(self.painel_direito, text="", text_color="red")
        self.status.pack(pady=5, side="bottom")

        self.botoes_frame = ctk.CTkFrame(self.painel_direito, fg_color="transparent")
        self.botoes_frame.pack(fill="x", padx=20, side="bottom")

        self.btn_voltar = ctk.CTkButton(self.botoes_frame, text="Voltar", command=self.voltar, 
                                        fg_color="#A9A9A9", text_color="#24232F", 
                                        hover_color="#B9B9B9", width=150, height=35, corner_radius=10)
        self.btn_voltar.pack(side="left", pady=10)

        self.btn_salvar = ctk.CTkButton(self.botoes_frame, text="Salvar Aula + Presença", command=self.salvar_aula, 
                                        fg_color="#24232F", hover_color="#3A3A46", 
                                        height=35, corner_radius=10)
        self.btn_salvar.pack(side="right", pady=10)
        
        # --- 3. Conteúdo do Meio (Empacotado por ÚLTIMO) ---
        self.frame_alunos = ctk.CTkScrollableFrame(self.painel_direito, fg_color="#EAEAEA", corner_radius=10)
        self.frame_alunos.pack(pady=10, fill="both", expand=True, padx=20)

        self.alunos_checkboxes = [] 
        
        self.bind("<Visibility>", self.atualizar_turmas)
        
        print(f"Carregando alunos da turma padrão na inicialização: {default_value}")
        self.carregar_alunos(default_value)

    # --- (Restante das funções sem alteração) ---

    def limpar_placeholder(self, event):
        if self.descricao.get("0.0", "end").strip() == "Descrição da aula...":
            self.descricao.delete("0.0", "end")
            self.descricao.configure(text_color="#24232F")

    def restaurar_placeholder(self, event):
        if self.descricao.get("0.0", "end").strip() == "":
            self.descricao.insert("0.0", "Descrição da aula...")
            self.descricao.configure(text_color="#888888")

    def abrir_calendario(self, event=None):
        top = ctk.CTkToplevel(self)
        top.title("Selecionar Data")
        top.geometry("300x320")
        top.grab_set() 
        cal = Calendar(top, selectmode='day', 
                       year=datetime.datetime.now().year,
                       month=datetime.datetime.now().month, 
                       day=datetime.datetime.now().day)
        cal.pack(pady=10, fill="both", expand=True)
        def pegar_data():
            self.data.delete(0, "end")
            self.data.insert(0, cal.get_date())
            top.destroy() 
        ctk.CTkButton(top, text="Selecionar", command=pegar_data, 
                      fg_color="#24232F", hover_color="#3A3A46").pack(pady=10)
        self.wait_window(top)
    
    def atualizar_turmas(self, event=None):
        print("Atualizando lista de turmas (evento Visibility)...")
        turma_anterior = self.turma_selecionada.get()
        self.turmas = self.carregar_turmas()
        default_value = self.turmas[0] if self.turmas else "Nenhuma turma cadastrada"
        if self.turmas:
            self.dropdown_turma.configure(values=self.turmas)
            if turma_anterior in self.turmas:
                self.dropdown_turma.set(turma_anterior)
                self.carregar_alunos(turma_anterior)
            else:
                self.dropdown_turma.set(default_value)
                self.carregar_alunos(default_value)
        else:
             self.dropdown_turma.configure(values=["Nenhuma turma cadastrada"])
             self.dropdown_turma.set("Nenhuma turma cadastrada")
             self.carregar_alunos("Nenhuma turma cadastrada")

    def carregar_turmas(self):
        try:
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome FROM turmas ORDER BY nome")
                turmas = cursor.fetchall()
                return [f"{id} - {nome}" for id, nome in turmas]
        except sqlite3.Error as e:
            self.status.configure(text=f"Erro ao carregar turmas: {e}", text_color="red")
            return []

    def carregar_alunos(self, turma_str):
        print(f"Carregando alunos para: {turma_str}")
        for widget in self.frame_alunos.winfo_children():
            widget.destroy()
        self.alunos_checkboxes.clear()
        
        if not turma_str or turma_str == "Nenhuma turma cadastrada":
            if turma_str == "Nenhuma turma cadastrada":
                ctk.CTkLabel(self.frame_alunos, text="Cadastre uma turma primeiro.", text_color="#555555").pack(pady=10)
            return
            
        try:
            turma_id = turma_str.split(" - ")[0]
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome FROM alunos WHERE turma_id = ? ORDER BY nome", (turma_id,))
                alunos = cursor.fetchall()
            if not alunos:
                ctk.CTkLabel(self.frame_alunos, text="Nenhum aluno cadastrado nesta turma.", text_color="#555555").pack(pady=10)
                return
            for aluno_id, nome in alunos:
                var = ctk.BooleanVar(value=True) 
                checkbox = ctk.CTkCheckBox(self.frame_alunos, text=nome, variable=var, 
                                           text_color="#24232F",
                                           border_color="#24232F",
                                           hover_color="#3A3A46",
                                           fg_color="#24232F")
                checkbox.pack(anchor="w", padx=20, pady=5)
                self.alunos_checkboxes.append((aluno_id, var))
        except sqlite3.Error as e:
            self.status.configure(text=f"Erro ao carregar alunos: {e}", text_color="red")
        except IndexError:
             self.status.configure(text=f"Erro ao processar o nome da turma.", text_color="red")

    def salvar_aula(self):
        turma_str = self.turma_selecionada.get()
        data = self.data.get().strip()
        tema = self.tema.get().strip()
        descricao = self.descricao.get("0.0", "end").strip()
        
        if descricao == "Descrição da aula...":
            descricao = "" 
        if not data or not tema:
            self.status.configure(text="Preencha data e tema.", text_color="red")
            return
        if not turma_str or turma_str == "Nenhuma turma cadastrada":
            self.status.configure(text="Selecione uma turma válida.", text_color="red")
            return
        if not self.alunos_checkboxes:
            self.status.configure(text="Não há alunos nesta turma para salvar.", text_color="red")
            return
            
        try:
            turma_id = turma_str.split(" - ")[0]
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO aulas (turma_id, data, tema, descricao) VALUES (?, ?, ?, ?)", (turma_id, data, tema, descricao))
                aula_id = cursor.lastrowid 
                presencas_data = []
                for aluno_id, var in self.alunos_checkboxes:
                    presente = 1 if var.get() else 0
                    presencas_data.append((aula_id, aluno_id, presente))
                cursor.executemany("INSERT INTO presencas (aula_id, aluno_id, presente) VALUES (?, ?, ?)", presencas_data)
            self.status.configure(text="Aula e presença registradas com sucesso!", text_color="green")
            self.data.delete(0, 'end')
            self.tema.delete(0, 'end')
            self.descricao.delete("0.0", 'end')
            self.restaurar_placeholder(None)
        except sqlite3.Error as e:
            self.status.configure(text=f"Erro ao salvar: {str(e)}", text_color="red")
        except Exception as e:
            self.status.configure(text=f"Erro inesperado: {str(e)}", text_color="red")

    def voltar(self):
        self.status.configure(text="")
        self.data.delete(0, 'end')
        self.tema.delete(0, 'end')
        self.descricao.delete("0.0", 'end')
        self.restaurar_placeholder(None)
        for widget in self.frame_alunos.winfo_children():
            widget.destroy()
        self.alunos_checkboxes.clear()
        
        self.controlador.mostrar_tela("MenuPrincipal")