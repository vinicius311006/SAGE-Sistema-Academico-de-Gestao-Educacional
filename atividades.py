"""
Arquivo da Tela de Atividades (atividades.py)

Este módulo define a classe 'Atividades', cumprindo o requisito do PIM
de "Cadastro e consulta de atividades". Permite:
1. Cadastrar uma nova atividade (ex: Prova, Trabalho) para uma turma.
2. Consultar, editar e deletar atividades existentes.
"""

import customtkinter as ctk
from database import conectar
from tkcalendar import Calendar
import datetime
import sqlite3
# Importa os pop-ups de diálogo que vamos usar
from dialogos import JanelaConfirmacao, JanelaEditarAtividade 

class Atividades(ctk.CTkFrame):
    """
    Frame (tela) para Cadastro e Consulta de Atividades.
    """
    
    GEOMETRIA = "850x650" # Tamanho Padrão

    def __init__(self, parent, controlador):
        """
        Inicializa o frame de Atividades.

        Args:
            parent (ctk.CTkFrame): O frame container principal.
            controlador (Aplicativo): A instância da aplicação principal.
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

        # --- Painel Direito (Conteúdo) ---
        self.painel_direito = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.painel_direito.pack(side="right", fill="both", expand=True, padx=20, pady=15)
        
        ctk.CTkLabel(self.painel_direito, text="Gestão de Atividades", font=("Segoe UI", 36, "bold"), text_color="#24232F").pack(pady=10)

        # --- Frame para o Formulário de Cadastro ---
        self.form_frame = ctk.CTkFrame(self.painel_direito, fg_color="transparent")
        self.form_frame.pack(fill="x", padx=20)

        self.turmas = self.carregar_turmas()
        default_value = self.turmas[0] if self.turmas else "Nenhuma turma cadastrada"
        self.turma_selecionada = ctk.StringVar(value=default_value)
        
        self.dropdown_turma = ctk.CTkOptionMenu(self.form_frame,
                                                values=self.turmas, 
                                                variable=self.turma_selecionada,
                                                command=self.carregar_atividades, # Comando para recarregar a lista
                                                height=40,
                                                fg_color="white", button_color="#E0E0E0",
                                                text_color="#24232F", dropdown_fg_color="white",
                                                dropdown_text_color="#24232F")
        self.dropdown_turma.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.data_entrega = ctk.CTkEntry(self.form_frame, placeholder_text="Data de Entrega", 
                                         height=40, width=180,
                                         fg_color="white", border_color="#E0E0E0", border_width=1,
                                         text_color="#24232F", placeholder_text_color="#888888")
        self.data_entrega.pack(side="left")
        self.data_entrega.bind("<Button-1>", self.abrir_calendario)

        self.nome_atividade = ctk.CTkEntry(self.painel_direito, placeholder_text="Nome da Atividade (ex: PIM, Prova 1)", 
                                           height=40,
                                           fg_color="white", border_color="#E0E0E0", border_width=1,
                                           text_color="#24232F", placeholder_text_color="#888888")
        self.nome_atividade.pack(fill="x", padx=20, pady=10)

        self.descricao = ctk.CTkTextbox(self.painel_direito, height=60,
                                        fg_color="white", border_color="#E0E0E0", border_width=1,
                                        text_color="#24232F")
        self.descricao.pack(pady=10, fill="x", padx=20)
        self.descricao.insert("0.0", "Descrição da atividade...")
        self.descricao.configure(text_color="#888888") # Cor do placeholder
        self.descricao.bind("<FocusIn>", self.limpar_placeholder)
        self.descricao.bind("<FocusOut>", self.restaurar_placeholder)
        
        self.btn_salvar = ctk.CTkButton(self.painel_direito, text="Salvar Nova Atividade", 
                                        command=self.salvar_atividade, 
                                        fg_color="#24232F", hover_color="#3A3A46", 
                                        height=35, corner_radius=10)
        self.btn_salvar.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(self.painel_direito, text="Atividades Cadastradas", font=("Segoe UI", 16, "bold"), text_color="#24232F").pack(pady=(10,0))
        
        # --- INÍCIO DA CORREÇÃO DE LAYOUT ---
        # 1. Empacota os widgets de baixo (Botão Voltar e Status) PRIMEIRO
        
        self.status = ctk.CTkLabel(self.painel_direito, text="", text_color="red")
        self.status.pack(pady=5, side="bottom")
        
        self.btn_voltar = ctk.CTkButton(self.painel_direito, text="Voltar", command=self.voltar, 
                                        fg_color="#A9A9A9", text_color="#24232F", 
                                        hover_color="#B9B9B9", width=150, height=35, corner_radius=10)
        self.btn_voltar.pack(pady=10, side="bottom")

        # 2. Empacota o frame de rolagem (meio) por ÚLTIMO, para que ele expanda
        self.frame_atividades = ctk.CTkScrollableFrame(self.painel_direito, fg_color="#EAEAEA", corner_radius=10)
        self.frame_atividades.pack(pady=10, fill="both", expand=True, padx=20)
        # --- FIM DA CORREÇÃO DE LAYOUT ---

        # --- Carga Inicial ---
        self.bind("<Visibility>", self.atualizar_tela)
        self.carregar_atividades(self.turma_selecionada.get())

    # --- Funções de Placeholder ---
    def limpar_placeholder(self, event):
        if self.descricao.get("0.0", "end").strip() == "Descrição da atividade...":
            self.descricao.delete("0.0", "end")
            self.descricao.configure(text_color="#24232F")

    def restaurar_placeholder(self, event):
        if self.descricao.get("0.0", "end").strip() == "":
            self.descricao.insert("0.0", "Descrição da atividade...")
            self.descricao.configure(text_color="#888888")

    # --- Funções Principais (CRUD) ---
    def carregar_turmas(self):
        """Busca e retorna a lista de turmas do banco."""
        try:
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome FROM turmas ORDER BY nome")
                turmas = cursor.fetchall()
                return [f"{id} - {nome}" for id, nome in turmas]
        except sqlite3.Error as e:
            self.status.configure(text=f"Erro ao carregar turmas: {e}", text_color="red")
            return []

    def salvar_atividade(self):
        """Salva a nova atividade no banco de dados."""
        turma_str = self.turma_selecionada.get()
        data = self.data_entrega.get().strip()
        nome = self.nome_atividade.get().strip()
        descricao = self.descricao.get("0.0", "end").strip()
        
        if descricao == "Descrição da atividade...":
            descricao = "" 

        if not data or not nome or not turma_str or turma_str == "Nenhuma turma cadastrada":
            self.status.configure(text="Preencha turma, data e nome da atividade.", text_color="red")
            return
            
        try:
            turma_id = turma_str.split(" - ")[0]
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO atividades (turma_id, nome, data_entrega, descricao) 
                    VALUES (?, ?, ?, ?)
                """, (turma_id, nome, data, descricao))
            
            self.status.configure(text="Atividade salva com sucesso!", text_color="green")
            # Limpa os campos
            self.data_entrega.delete(0, 'end')
            self.nome_atividade.delete(0, 'end')
            self.descricao.delete("0.0", 'end')
            self.restaurar_placeholder(None)
            # Recarrega a lista
            self.carregar_atividades(turma_str)
            
        except sqlite3.Error as e:
            self.status.configure(text=f"Erro ao salvar atividade: {str(e)}", text_color="red")

    def carregar_atividades(self, turma_str):
        """Carrega e exibe as atividades da turma selecionada."""
        for widget in self.frame_atividades.winfo_children():
            widget.destroy()
        
        if not turma_str or turma_str == "Nenhuma turma cadastrada":
            if turma_str == "Nenhuma turma cadastrada":
                ctk.CTkLabel(self.frame_atividades, text="Cadastre uma turma primeiro.", text_color="#555555").pack(pady=10)
            return

        try:
            turma_id = turma_str.split(" - ")[0]
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome, data_entrega, descricao FROM atividades WHERE turma_id = ? ORDER BY data_entrega DESC", (turma_id,))
                atividades = cursor.fetchall()
                
            if not atividades:
                ctk.CTkLabel(self.frame_atividades, text="Nenhuma atividade registrada para esta turma.", text_color="#555555").pack(pady=10)
                return

            # Cria um card para cada atividade
            for ativ_id, nome, data, desc in atividades:
                card = ctk.CTkFrame(self.frame_atividades, fg_color="white", corner_radius=10, border_width=1, border_color="#E0E0E0")
                card.pack(fill="x", padx=10, pady=5)
                
                frame_info = ctk.CTkFrame(card, fg_color="transparent")
                frame_info.pack(fill="x", padx=10, pady=5)
                
                text_frame = ctk.CTkFrame(frame_info, fg_color="transparent")
                text_frame.pack(side="left", fill="x", expand=True)
                
                btn_frame = ctk.CTkFrame(frame_info, fg_color="transparent")
                btn_frame.pack(side="right")
                
                ctk.CTkLabel(text_frame, text=f"📅 {data} | 📝 {nome}", font=("Segoe UI", 16, "bold"), text_color="#24232F").pack(anchor="w")
                ctk.CTkLabel(text_frame, text=f"{desc or 'Sem descrição'}", font=("Segoe UI", 14), text_color="#444444", wraplength=350, justify="left").pack(anchor="w")

                ctk.CTkButton(btn_frame, text="Editar", width=60, height=30, corner_radius=8,
                              command=lambda id=ativ_id, n=nome, d=data, desc=desc: self.abrir_janela_edicao(id, n, d, desc),
                              fg_color="#A9A9A9", text_color="#24232F", hover_color="#B9B9B9").pack(pady=2)
                ctk.CTkButton(btn_frame, text="Deletar", width=60, height=30, corner_radius=8,
                              command=lambda id=ativ_id: self.deletar_atividade(id),
                              fg_color="#FF6B6B", text_color="white", hover_color="#FF5252").pack(pady=2)
                    
        except sqlite3.Error as e:
            self.status.configure(text=f"Erro ao carregar atividades: {e}", text_color="red")

    def deletar_atividade(self, atividade_id):
        """Deleta uma atividade do banco."""
        dialog = JanelaConfirmacao(self, title="Confirmar Deleção", 
                               text="Tem certeza que deseja deletar esta atividade?")
        self.wait_window(dialog) 
        
        if dialog.obter_resposta():
            try:
                with conectar() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM atividades WHERE id = ?", (atividade_id,))
                
                self.status.configure(text="Atividade deletada com sucesso!", text_color="green")
                self.carregar_atividades(self.turma_selecionada.get()) # Recarrega
            except sqlite3.Error as e:
                self.status.configure(text=f"Erro ao deletar: {str(e)}", text_color="red")
        else:
            self.status.configure(text="Deleção cancelada.", text_color="#A9A9A9")

    def abrir_janela_edicao(self, ativ_id, nome, data, descricao):
        """Abre o pop-up de edição de atividade."""
        self.status.configure(text="")
        edit_window = JanelaEditarAtividade(self, ativ_id, nome, data, descricao)
        self.wait_window(edit_window)

    def abrir_calendario(self, event=None):
        """Abre o pop-up de calendário."""
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
            self.data_entrega.delete(0, "end")
            self.data_entrega.insert(0, cal.get_date())
            top.destroy() 
            
        ctk.CTkButton(top, text="Selecionar", command=pegar_data, 
                      fg_color="#24232F", hover_color="#3A3A46").pack(pady=10)
        self.wait_window(top)

    def atualizar_tela(self, event=None):
        """Recarrega turmas e atividades quando a tela fica visível."""
        print("Atualizando tela de atividades...")
        if self.status.cget("text_color") != "green":
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
            self.carregar_atividades(self.dropdown_turma.get())
        else:
            self.dropdown_turma.configure(values=["Nenhuma turma cadastrada"])
            self.dropdown_turma.set("Nenhuma turma cadastrada")
            self.carregar_atividades("Nenhuma turma cadastrada")

    def voltar(self):
        """Navega de volta para o Menu Principal."""
        self.status.configure(text="")
        self.controlador.mostrar_tela("MenuPrincipal")