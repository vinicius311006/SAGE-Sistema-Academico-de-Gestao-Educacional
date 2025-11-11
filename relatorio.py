"""
Arquivo da Tela de Relatório (relatorio.py)

Este módulo define a classe 'Relatorio', que permite:
1. Visualizar todas as aulas registradas para uma turma.
2. Ver a lista de presença de cada aula.
3. Chamar a janela de edição de aula (de 'dialogos.py').
4. Deletar uma aula (e suas presenças).
5. Exportar a frequência da turma para um arquivo CSV.
"""

import customtkinter as ctk
from database import conectar
import pandas as pd # Usado para exportar CSV
import sqlite3
from tkinter.filedialog import asksaveasfilename # Para salvar o CSV
from dialogos import JanelaConfirmacao, JanelaEditarAula # Importa os pop-ups

class Relatorio(ctk.CTkFrame):
    """
    Frame (tela) para Relatório de Aulas e Frequência.
    Atualizado para o novo design de card.
    """
    
    GEOMETRIA = "850x650" # Tamanho Padrão

    def __init__(self, parent, controlador):
        """
        Inicializa o frame de Relatório.

        Args:
            parent (ctk.CTkFrame): O frame container principal.
            controlador (Aplicativo): A instância da aplicação principal.
        """
        super().__init__(parent, fg_color="#D9D9D9") 
        self.controlador = controlador

        # --- Layout do Card (Padrão) ---
        self.card_frame = ctk.CTkFrame(self, fg_color="#F0F0F0", corner_radius=20)
        self.card_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

        # --- Painel Esquerdo ---
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
        
        ctk.CTkLabel(self.painel_direito, text="Relatório de Aulas", font=("Segoe UI", 36, "bold"), text_color="#24232F").pack(pady=20)

        # Dropdown de Turmas
        self.turmas = self.carregar_turmas()
        self.turma_selecionada = ctk.StringVar(value=self.turmas[0] if self.turmas else "Nenhuma turma cadastrada")
        
        self.dropdown_turma = ctk.CTkOptionMenu(self.painel_direito,
                                                values=self.turmas, 
                                                variable=self.turma_selecionada, 
                                                command=self.carregar_aulas, 
                                                width=300, height=40,
                                                fg_color="white", button_color="#E0E0E0",
                                                text_color="#24232F", dropdown_fg_color="white",
                                                dropdown_text_color="#24232F")
        self.dropdown_turma.pack(pady=10)

        # Frame de Rolagem para os cards das aulas
        self.frame_relatorio = ctk.CTkScrollableFrame(self.painel_direito, fg_color="#EAEAEA", corner_radius=10)
        self.frame_relatorio.pack(pady=10, fill="both", expand=True)

        # Botão Exportar
        self.btn_exportar = ctk.CTkButton(self.painel_direito, text="Exportar para CSV", command=self.exportar_csv, 
                                          fg_color="#24232F", hover_color="#3A3A46", 
                                          height=35, corner_radius=10)
        self.btn_exportar.pack(pady=10)
        
        self.status = ctk.CTkLabel(self.painel_direito, text="", text_color="green")
        self.status.pack(pady=5)

        # Botão Voltar
        self.btn_voltar = ctk.CTkButton(self.painel_direito, text="Voltar", command=self.voltar, 
                                        fg_color="#A9A9A9", text_color="#24232F", 
                                        hover_color="#B9B9B9", width=150, height=35, corner_radius=10)
        self.btn_voltar.pack(pady=10)
        # --- Fim do Painel Direito ---
        
        self.bind("<Visibility>", self.atualizar_relatorio)

    def atualizar_relatorio(self, event=None):
        """
        Recarrega a lista de turmas e o relatório da turma selecionada.
        """
        print("Atualizando relatório...")
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
            self.carregar_aulas(self.dropdown_turma.get())
        else:
            self.dropdown_turma.configure(values=["Nenhuma turma cadastrada"])
            self.dropdown_turma.set("Nenhuma turma cadastrada")
            self.carregar_aulas("Nenhuma turma cadastrada")

    def carregar_turmas(self):
        """
        Busca a lista de turmas no banco de dados.
        
        Returns:
            list: Lista de strings formatadas "ID - Nome" ou lista vazia.
        """
        try:
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome FROM turmas ORDER BY nome")
                turmas = cursor.fetchall()
                return [f"{id} - {nome}" for id, nome in turmas]
        except sqlite3.Error as e:
            self.status.configure(text=f"Erro ao carregar turmas: {e}", text_color="red")
            return []

    def carregar_aulas(self, turma_str):
        """
        Carrega todas as aulas e presenças da turma selecionada.
        
        Args:
            turma_str (str): A string da turma selecionada (ex: "1 - 3º Ano A").
        """
        for widget in self.frame_relatorio.winfo_children():
            widget.destroy()
        
        # Não limpa o status se for uma mensagem de sucesso (ex: "Aula deletada")
        if self.status.cget("text_color") != "green":
             self.status.configure(text="")

        if not turma_str or turma_str == "Nenhuma turma cadastrada":
            if turma_str == "Nenhuma turma cadastrada":
                ctk.CTkLabel(self.frame_relatorio, text="Cadastre uma turma primeiro.", text_color="#555555").pack(pady=10)
            return

        try:
            turma_id = turma_str.split(" - ")[0]
            with conectar() as conn:
                cursor = conn.cursor()
                # Busca todas as aulas da turma
                cursor.execute("SELECT id, data, tema, descricao FROM aulas WHERE turma_id = ? ORDER BY data DESC", (turma_id,))
                aulas = cursor.fetchall()
                
                if not aulas:
                    ctk.CTkLabel(self.frame_relatorio, text="Nenhuma aula registrada para esta turma.", text_color="#555555").pack(pady=10)
                    return

                # Cria um card para cada aula encontrada
                for aula_id, data, tema, descricao in aulas:
                    aula_frame = ctk.CTkFrame(self.frame_relatorio, fg_color="white", corner_radius=10, border_width=1, border_color="#E0E0E0")
                    aula_frame.pack(fill="x", padx=10, pady=5)
                    
                    # Frame para alinhar textos à esquerda e botões à direita
                    content_frame = ctk.CTkFrame(aula_frame, fg_color="transparent")
                    content_frame.pack(fill="x", padx=10, pady=5)
                    text_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                    text_frame.pack(side="left", fill="x", expand=True)
                    btn_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                    btn_frame.pack(side="right")
                    
                    # Detalhes da Aula
                    ctk.CTkLabel(text_frame, text=f"📅 {data} | 🧠 {tema}", font=("Segoe UI", 16, "bold"), text_color="#24232F").pack(anchor="w")
                    ctk.CTkLabel(text_frame, text=f"📝 {descricao or 'Sem descrição'}", font=("Segoe UI", 14), text_color="#444444", wraplength=400, justify="left").pack(anchor="w")

                    # Botões de Ação
                    ctk.CTkButton(btn_frame, text="Editar", width=60, height=30, corner_radius=8,
                                  command=lambda id=aula_id, d=data, t=tema, desc=descricao: self.abrir_janela_edicao(id, d, t, desc),
                                  fg_color="#A9A9A9", text_color="#24232F", hover_color="#B9B9B9").pack(pady=2)
                    ctk.CTkButton(btn_frame, text="Deletar", width=60, height=30, corner_radius=8,
                                  command=lambda id=aula_id: self.deletar_aula(id),
                                  fg_color="#FF6B6B", text_color="white", hover_color="#FF5252").pack(pady=2)
                    
                    # Busca as presenças para *esta* aula específica
                    cursor.execute("""
                        SELECT alunos.nome, presencas.presente
                        FROM presencas
                        JOIN alunos ON presencas.aluno_id = alunos.id
                        WHERE presencas.aula_id = ?
                        ORDER BY alunos.nome
                    """, (aula_id,))
                    presencas = cursor.fetchall()
                    
                    # Exibe a lista de presença
                    if presencas:
                        presenca_label = ctk.CTkLabel(aula_frame, text="Frequência:", font=("Segoe UI", 13, "italic"), text_color="#555555")
                        presenca_label.pack(anchor="w", padx=20, pady=(5,0))
                    
                    for nome, presente in presencas:
                        status = "✅ Presente" if presente else "❌ Ausente"
                        ctk.CTkLabel(aula_frame, text=f"{nome}: {status}", font=("Segoe UI", 13), text_color="#24232F").pack(anchor="w", padx=40)
                    
                    ctk.CTkLabel(aula_frame, text="").pack(pady=2) # Espaçador
                    
        except sqlite3.Error as e:
            self.status.configure(text=f"Erro ao carregar aulas: {e}", text_color="red")

    def deletar_aula(self, aula_id):
        """
        Deleta uma aula e suas presenças associadas após confirmação.

        Args:
            aula_id (int): O ID da aula a ser deletada.
        """
        dialog = JanelaConfirmacao(self, title="Confirmar Deleção", 
                               text=f"Tem certeza que deseja deletar esta aula?\n(Toda a frequência registrada nela será perdida)")
        
        self.wait_window(dialog) 
        
        if dialog.obter_resposta(): # Se clicou "Sim"
            try:
                with conectar() as conn:
                    cursor = conn.cursor()
                    # O "ON DELETE CASCADE" no DB cuida de deletar as presenças
                    cursor.execute("DELETE FROM aulas WHERE id = ?", (aula_id,))
                
                self.status.configure(text="Aula deletada com sucesso!", text_color="green")
                self.carregar_aulas(self.turma_selecionada.get()) # Recarrega
            except sqlite3.Error as e:
                self.status.configure(text=f"Erro ao deletar: {str(e)}", text_color="red")
        else:
            self.status.configure(text="Deleção cancelada.", text_color="#A9A9A9")

    def abrir_janela_edicao(self, aula_id, data, tema, descricao):
        """
        Abre a janela pop-up 'JanelaEditarAula' para editar a aula selecionada.

        Args:
            aula_id (int): ID da aula.
            data (str): Data atual da aula.
            tema (str): Tema atual da aula.
            descricao (str): Descrição atual da aula.
        """
        self.status.configure(text="")
        # Cria e espera a janela de edição (que é modal)
        edit_window = JanelaEditarAula(self, aula_id, data, tema, descricao)
        self.wait_window(edit_window)
        
    def exportar_csv(self):
        """
        Exporta os dados de frequência da turma selecionada para um arquivo CSV.
        """
        turma_str = self.turma_selecionada.get()
        if not turma_str or turma_str == "Nenhuma turma cadastrada":
            self.status.configure(text="Selecione uma turma para exportar.", text_color="red")
            return

        try:
            turma_id = turma_str.split(" - ")[0]
            turma_nome = turma_str.split(" - ")[1]
            
            # Query complexa para pegar todos os dados de uma vez
            query = """
                SELECT aulas.data, aulas.tema, alunos.nome, 
                       CASE presencas.presente WHEN 1 THEN 'Presente' ELSE 'Ausente' END AS status
                FROM aulas
                JOIN presencas ON aulas.id = presencas.aula_id
                JOIN alunos ON presencas.aluno_id = alunos.id
                WHERE aulas.turma_id = ?
                ORDER BY aulas.data DESC, alunos.nome
            """
            
            with conectar() as conn:
                # O Pandas lê diretamente da query SQL para um DataFrame
                df = pd.read_sql_query(query, conn, params=(turma_id,))

            if df.empty:
                self.status.configure(text="Não há dados para exportar.", text_color="red")
                return

            # Abre a janela "Salvar Como..."
            filepath = asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")],
                initialfile=f"relatorio_frequencia_{turma_nome.replace(' ', '_')}.csv",
                title="Salvar Relatório CSV"
            )

            if not filepath: # Se o usuário cancelar
                self.status.configure(text="Exportação cancelada.", text_color="#A9A9A9")
                return

            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            self.status.configure(text=f"Relatório exportado com sucesso!", text_color="green")

        except sqlite3.Error as e:
            self.status.configure(text=f"Erro no banco: {e}", text_color="red")
        except Exception as e:
            self.status.configure(text=f"Erro ao exportar: {e}", text_color="red")

    def voltar(self):
        """
        Navega de volta para o Menu Principal.
        """
        self.status.configure(text="")
        self.controlador.mostrar_tela("MenuPrincipal")