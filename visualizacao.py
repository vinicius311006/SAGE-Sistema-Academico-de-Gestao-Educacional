import customtkinter as ctk
from database import conectar
import sqlite3
from collections import defaultdict
from dialogos import JanelaConfirmacao 

class Visualizacao(ctk.CTkFrame):
    """
    Frame (tela) para Visualização de Turmas e Alunos.
    Atualizado para o novo design de card.
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

        # --- Painel Direito (Conteúdo - Layout Top-Down) ---
        self.painel_direito = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.painel_direito.pack(side="right", fill="both", expand=True, padx=20, pady=15)
 
        ctk.CTkLabel(self.painel_direito, text="Visualização de Turmas", font=("Segoe UI", 36, "bold"), text_color="#24232F").pack(pady=20)

        self.turmas = self.carregar_turmas()
        self.turma_selecionada = ctk.StringVar(value=self.turmas[0] if self.turmas else "Nenhuma turma cadastrada")
        
        self.dropdown_turma = ctk.CTkOptionMenu(self.painel_direito,
                                                values=self.turmas, 
                                                variable=self.turma_selecionada, 
                                                command=self.carregar_alunos_otimizado, 
                                                width=300, height=40,
                                                fg_color="white", button_color="#E0E0E0",
                                                text_color="#24232F", dropdown_fg_color="white",
                                                dropdown_text_color="#24232F")
        self.dropdown_turma.pack(pady=10)

        self.frame_alunos = ctk.CTkScrollableFrame(self.painel_direito, fg_color="#EAEAEA", corner_radius=10)
        self.frame_alunos.pack(pady=10, fill="both", expand=True)
        
        self.status = ctk.CTkLabel(self.painel_direito, text="", text_color="green")
        self.status.pack(pady=5)

        self.btn_voltar = ctk.CTkButton(self.painel_direito, text="Voltar", command=self.voltar, 
                                        fg_color="#A9A9A9", text_color="#24232F", 
                                        hover_color="#B9B9B9", width=150, height=35, corner_radius=10)
        self.btn_voltar.pack(pady=10)
        # --- Fim do Painel Direito ---

        self.bind("<Visibility>", self.atualizar_visualizacao)

    # (Todas as outras funções (atualizar_visualizacao, carregar_alunos_otimizado, etc.) sem alteração)
    def atualizar_visualizacao(self, event=None):
        print("Atualizando visualização...")
        self.status.configure(text="") 
        turma_anterior = self.turma_selecionada.get()
        self.turmas = self.carregar_turmas()
        default_value = self.turmas[0] if self.turmas else "Nenhuma turma cadastrada"
        if self.turmas:
            self.dropdown_turma.configure(values=self.turmas)
            if turma_anterior in self.turmas:
                self.dropdown_turma.set(turma_anterior)
            else:
                self.dropdown_turma.set(default_value)
            self.carregar_alunos_otimizado(self.dropdown_turma.get())
        else:
            self.dropdown_turma.configure(values=["Nenhuma turma cadastrada"])
            self.dropdown_turma.set("Nenhuma turma cadastrada")
            self.carregar_alunos_otimizado("Nenhuma turma cadastrada")
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
    def carregar_alunos_otimizado(self, turma_str):
        for widget in self.frame_alunos.winfo_children():
            widget.destroy()
        self.status.configure(text="") 
        if not turma_str or turma_str == "Nenhuma turma cadastrada":
            if turma_str == "Nenhuma turma cadastrada":
                ctk.CTkLabel(self.frame_alunos, text="Cadastre uma turma primeiro.", text_color="#555555").pack(pady=10)
            return
        try:
            turma_id = turma_str.split(" - ")[0]
            alunos_dados = defaultdict(lambda: {"nome": "", "registros": [], "id": 0})
            with conectar() as conn:
                cursor = conn.cursor()
                sql = """
                    SELECT a.id, a.nome, au.data, p.presente
                    FROM alunos a
                    LEFT JOIN presencas p ON a.id = p.aluno_id
                    LEFT JOIN aulas au ON p.aula_id = au.id
                    WHERE a.turma_id = ?
                    ORDER BY a.nome, au.data DESC
                """
                cursor.execute(sql, (turma_id,))
                registros = cursor.fetchall()
            if not registros:
                ctk.CTkLabel(self.frame_alunos, text="Nenhum aluno cadastrado nesta turma.", text_color="#555555").pack(pady=10)
                return
            for aluno_id, nome, data, presente in registros:
                alunos_dados[aluno_id]["nome"] = nome
                alunos_dados[aluno_id]["id"] = aluno_id
                if data is not None: 
                    alunos_dados[aluno_id]["registros"].append((data, presente))
            for aluno_id, dados in alunos_dados.items():
                nome = dados["nome"]
                registros = dados["registros"]
                total = len(registros)
                presentes = sum(1 for _, p in registros if p)
                faltas = total - presentes
                frame_aluno = ctk.CTkFrame(self.frame_alunos, fg_color="white", corner_radius=10, border_width=1, border_color="#E0E0E0")
                frame_aluno.pack(fill="x", padx=10, pady=5)
                ctk.CTkLabel(frame_aluno, text=f"👤 {nome} — Presenças: {presentes} | Faltas: {faltas}", font=("Segoe UI", 15, "bold"), text_color="#24232F").pack(anchor="w", padx=10, pady=5)
                for data, presente in registros:
                    status = "✅ Presente" if presente else "❌ Ausente"
                    ctk.CTkLabel(frame_aluno, text=f"{data}: {status}", font=("Segoe UI", 13), text_color="#444444").pack(anchor="w", padx=40)
                btn_frame = ctk.CTkFrame(frame_aluno, fg_color="transparent")
                btn_frame.pack(anchor="e", padx=10, pady=5)
                ctk.CTkButton(btn_frame, text="Editar", command=lambda id=aluno_id, n=nome: self.editar_aluno(id, n), 
                              fg_color="#A9A9A9", text_color="#24232F", hover_color="#B9B9B9", width=80, height=30, corner_radius=8).pack(side="left", padx=5)
                ctk.CTkButton(btn_frame, text="Deletar", command=lambda id=aluno_id: self.deletar_aluno(id), 
                              fg_color="#FF6B6B", text_color="white", hover_color="#FF5252", width=80, height=30, corner_radius=8).pack(side="left", padx=5)
        except sqlite3.Error as e:
            self.status.configure(text=f"Erro ao carregar alunos: {e}", text_color="red")
        except IndexError:
             self.status.configure(text=f"Erro ao processar o nome da turma.", text_color="red")
    def editar_aluno(self, aluno_id, nome_atual):
        dialog = ctk.CTkInputDialog(title="Editar Aluno", text=f"Digite o novo nome para {nome_atual}:")
        novo_nome = dialog.get_input()
        if novo_nome and novo_nome.strip():
            try:
                with conectar() as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE alunos SET nome = ? WHERE id = ?", (novo_nome.strip(), aluno_id))
                self.status.configure(text="Aluno editado com sucesso!", text_color="green")
                self.carregar_alunos_otimizado(self.turma_selecionada.get())
            except sqlite3.Error as e:
                self.status.configure(text=f"Erro ao editar: {str(e)}", text_color="red")
    def deletar_aluno(self, aluno_id):
        dialog = JanelaConfirmacao(self, title="Confirmar Deleção", 
                               text=f"Tem certeza que deseja deletar este aluno?\n(Todas as suas presenças também serão apagadas)")
        self.wait_window(dialog)
        if dialog.obter_resposta(): 
            try:
                with conectar() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM presencas WHERE aluno_id = ?", (aluno_id,))
                    cursor.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
                self.status.configure(text="Aluno deletado com sucesso!", text_color="green")
                self.carregar_alunos_otimizado(self.turma_selecionada.get())
            except sqlite3.Error as e:
                self.status.configure(text=f"Erro ao deletar: {str(e)}", text_color="red")
        else:
            self.status.configure(text="Deleção cancelada.", text_color="#A9A9A9")
    def voltar(self):
        self.status.configure(text="")
        self.controlador.mostrar_tela("MenuPrincipal")