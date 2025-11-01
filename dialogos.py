import customtkinter as ctk
import sqlite3
from database import conectar
from tkcalendar import Calendar
import datetime
# A LINHA DE IMPORTAÇÃO DAQUI FOI REMOVIDA

class JanelaConfirmacao(ctk.CTkToplevel):
    """
    Uma janela de diálogo modal para confirmação (Sim/Não).
    (Estilo claro)
    """
    def __init__(self, parent, title="Confirmar", text="Tem certeza?"):
        super().__init__(parent)
        self.title(title)
        self.geometry("350x150")
        self.resizable(False, False)
        
        self.configure(fg_color="#F0F0F0") 
        
        self._resultado = False 
        
        self.grab_set() 
        self.attributes("-topmost", True)

        ctk.CTkLabel(self, text=text, font=("Segoe UI", 16), wraplength=330, text_color="#24232F").pack(pady=20, padx=10, fill="x")

        frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_botoes.pack(pady=10)

        ctk.CTkButton(frame_botoes, text="Não", command=self._on_nao, 
                      fg_color="#A9A9A9", text_color="#24232F", hover_color="#B9B9B9").pack(side="left", padx=10)
        ctk.CTkButton(frame_botoes, text="Sim", command=self._on_sim, 
                      fg_color="#FF6B6B", text_color="white", hover_color="#FF5252").pack(side="left", padx=10)

    def _on_sim(self):
        self._resultado = True
        self.destroy()

    def _on_nao(self):
        self._resultado = False
        self.destroy()

    def obter_resposta(self):
        return self._resultado

class JanelaEditarAula(ctk.CTkToplevel):
    """
    Uma janela de diálogo modal para EDITAR os detalhes e a PRESENÇA de uma Aula.
    (Estilo claro, padronizado com o app principal)
    """
    def __init__(self, parent, aula_id, data_atual, tema_atual, desc_atual):
        super().__init__(parent)
        
        self.frame_pai = parent
        self.aula_id = aula_id
        
        self.title("Editar Aula e Frequência")
        self.geometry("600x650") 
        self.resizable(False, False)
        
        self.configure(fg_color="#F0F0F0") 
        
        self.grab_set()
        self.attributes("-topmost", True)

        ctk.CTkLabel(self, text="Editar Detalhes da Aula", font=("Segoe UI", 24, "bold"), text_color="#24232F").pack(pady=10)

        self.data = ctk.CTkEntry(self, width=300, height=40,
                                 fg_color="white", border_color="#E0E0E0", border_width=1,
                                 text_color="#24232F", placeholder_text_color="#888888")
        self.data.insert(0, data_atual)
        self.data.pack(pady=5)
        self.data.bind("<Button-1>", self.abrir_calendario)

        self.tema = ctk.CTkEntry(self, width=300, height=40,
                                 fg_color="white", border_color="#E0E0E0", border_width=1,
                                 text_color="#24232F", placeholder_text_color="#888888")
        self.tema.insert(0, tema_atual)
        self.tema.pack(pady=5)

        self.descricao = ctk.CTkTextbox(self, height=100, width=400,
                                        fg_color="white", border_color="#E0E0E0", border_width=1,
                                        text_color="#24232F")
        self.descricao.pack(pady=5)
        self.desc_placeholder = "Descrição da aula..."
        self.descricao_atual = desc_atual or ""
        
        if self.descricao_atual == "":
            self.restaurar_placeholder(None)
        else:
            self.descricao.insert("0.0", self.descricao_atual)
            self.descricao.configure(text_color="#24232F") 
            
        self.descricao.bind("<FocusIn>", self.limpar_placeholder)
        self.descricao.bind("<FocusOut>", self.restaurar_placeholder)

        ctk.CTkLabel(self, text="Editar Frequência", font=("Segoe UI", 16, "bold"), text_color="#24232F").pack(pady=(15, 5))

        self.frame_alunos = ctk.CTkScrollableFrame(self, fg_color="#EAEAEA", width=500, height=200, corner_radius=10)
        self.frame_alunos.pack(pady=10, fill="x", expand=True, padx=20)
        
        self.alunos_checkboxes = [] 
        self.carregar_presencas() 

        frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_botoes.pack(pady=10)
        
        self.btn_cancelar = ctk.CTkButton(frame_botoes, text="Cancelar", command=self.destroy, 
                                          fg_color="#A9A9A9", text_color="#24232F", hover_color="#B9B9B9")
        self.btn_cancelar.pack(side="left", padx=10)

        self.btn_salvar = ctk.CTkButton(frame_botoes, text="Salvar Alterações", command=self.salvar_alteracoes, 
                                        fg_color="#24232F", text_color="white", hover_color="#3A3A46") 
        self.btn_salvar.pack(side="left", padx=10)
        
        self.status = ctk.CTkLabel(self, text="", text_color="red") 
        self.status.pack(pady=5)

    def carregar_presencas(self):
        try:
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT a.id, a.nome, p.presente
                    FROM alunos a
                    JOIN presencas p ON a.id = p.aluno_id
                    WHERE p.aula_id = ?
                    ORDER BY a.nome
                """, (self.aula_id,))
                presencas = cursor.fetchall()
            
            for aluno_id, nome, presente in presencas:
                var = ctk.BooleanVar(value=bool(presente))
                checkbox = ctk.CTkCheckBox(self.frame_alunos, text=nome, variable=var, 
                                           text_color="#24232F",
                                           border_color="#24232F",
                                           hover_color="#3A3A46",
                                           fg_color="#24232F")
                checkbox.pack(anchor="w", padx=20, pady=5)
                self.alunos_checkboxes.append((aluno_id, var))

        except sqlite3.Error as e:
            self.status.configure(text=f"Erro ao carregar presenças: {e}", text_color="red")


    def salvar_alteracoes(self):
        nova_data = self.data.get().strip()
        novo_tema = self.tema.get().strip()
        nova_desc = self.descricao.get("0.0", "end").strip()

        if nova_desc == self.desc_placeholder:
            nova_desc = ""

        if not nova_data or not novo_tema:
            self.status.configure(text="Data e Tema não podem ser vazios.", text_color="red")
            return

        try:
            with conectar() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE aulas 
                    SET data = ?, tema = ?, descricao = ?
                    WHERE id = ?
                """, (nova_data, novo_tema, nova_desc, self.aula_id))
                
                dados_presenca_atualizados = []
                for aluno_id, var in self.alunos_checkboxes:
                    status_presente = 1 if var.get() else 0
                    dados_presenca_atualizados.append((status_presente, self.aula_id, aluno_id))
                
                cursor.executemany("""
                    UPDATE presencas 
                    SET presente = ? 
                    WHERE aula_id = ? AND aluno_id = ?
                """, dados_presenca_atualizados)
            
            self.frame_pai.status.configure(text="Aula e frequências atualizadas!", text_color="green")
            self.frame_pai.carregar_aulas(self.frame_pai.turma_selecionada.get())
            self.destroy()
            
        except sqlite3.Error as e:
            self.status.configure(text=f"Erro ao salvar: {str(e)}", text_color="red")
            
    def abrir_calendario(self, event=None):
        top_cal = ctk.CTkToplevel(self)
        top_cal.title("Selecionar Data")
        top_cal.geometry("300x320")
        top_cal.grab_set() 
        cal = Calendar(top_cal, selectmode='day', 
                       year=datetime.datetime.now().year,
                       month=datetime.datetime.now().month, 
                       day=datetime.datetime.now().day)
        cal.pack(pady=10, fill="both", expand=True)

        def pegar_data(): # Definida antes de ser usada
            self.data.delete(0, "end")
            self.data.insert(0, cal.get_date())
            top_cal.destroy()

        ctk.CTkButton(top_cal, text="Selecionar", command=pegar_data,
                      fg_color="#24232F", text_color="white", hover_color="#3A3A46").pack(pady=10)
        self.wait_window(top_cal)
        
    def limpar_placeholder(self, event):
        if self.descricao.get("0.0", "end").strip() == self.desc_placeholder:
            self.descricao.delete("0.0", "end")
            self.descricao.configure(text_color="#24232F") 

    def restaurar_placeholder(self, event):
        if self.descricao.get("0.0", "end").strip() == "":
            self.descricao.insert("0.0", self.desc_placeholder)
            self.descricao.configure(text_color="#888888")