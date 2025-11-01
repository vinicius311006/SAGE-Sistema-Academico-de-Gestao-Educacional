import customtkinter as ctk

class Chatbot(ctk.CTkFrame):
    """
    Frame (tela) do Chatbot Acadêmico.
    Atualizado para o novo design de card.
    """
    
    GEOMETRIA = "900x750" # Tamanho Padrão

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
        
        ctk.CTkLabel(self.painel_direito, text="Assistente Acadêmico", font=("Segoe UI", 36, "bold"), text_color="#24232F").pack(pady=20)

        perguntas = [
            "Como cadastrar aluno?",
            "Como registrar aula?",
            "Como ver frequência?",
            "Como visualizar turmas?",
            "Como usar o chatbot?",
            "Estou com erro no sistema"
        ]

        frame_perguntas = ctk.CTkFrame(self.painel_direito, fg_color="transparent")
        frame_perguntas.pack(pady=10)

        for texto in perguntas:
            ctk.CTkButton(frame_perguntas, text=texto, command=lambda t=texto: self.responder(t),
                          fg_color="#24232F", hover_color="#3A3A46", 
                          text_color="white", width=300, height=35, corner_radius=10).pack(pady=5)

        self.resposta_frame = ctk.CTkFrame(self.painel_direito, fg_color="transparent")
        self.resposta_frame.pack(pady=20, padx=10, fill="both", expand=True) 

        self.resposta = ctk.CTkLabel(self.resposta_frame, text="Clique em uma pergunta para ver a resposta.", 
                                     wraplength=400, font=("Segoe UI", 14), 
                                     text_color="#444444", justify="left")
        self.resposta.pack(pady=20, padx=10)

        self.btn_voltar = ctk.CTkButton(self.painel_direito, text="Voltar", command=self.voltar, 
                                        fg_color="#A9A9A9", text_color="#24232F", 
                                        hover_color="#B9B9B9", width=150, height=35, corner_radius=10)
        self.btn_voltar.pack(pady=10, side="bottom") 
        # --- Fim do Painel Direito ---

    def responder(self, pergunta):
        # (Lógica sem alteração)
        try:
            texto = pergunta.lower()
            faq = {
                "cadastrar aluno": "Vá ao menu principal e clique em 'Cadastrar Aluno'. Preencha nome e selecione turma. Lembre-se de cadastrar uma turma primeiro!",
                "registrar aula": "Use a opção 'Registrar Aula'. Selecione a turma, a data e o tema. Os alunos carregarão automaticamente. Marque os presentes e clique em 'Salvar'.",
                "ver frequência": "Acesse 'Relatório de Aulas'. Selecione a turma para ver o histórico de aulas e presenças. Você pode editar, deletar ou exportar para CSV.",
                "visualizar turmas": "Clique em 'Visualizar Alunos'. Selecione uma turma para ver todos os alunos, seu histórico de presença, e editar ou deletar alunos.",
                "usar o chatbot": "Este é o chatbot! Você clica em uma das perguntas pré-definidas e eu mostro a resposta aqui. Simples assim.",
                "erro no sistema": "1. Verifique se o arquivo 'sistema_escolar.db' está na mesma pasta. \n2. Verifique se todas as dependências do 'requirements.txt' estão instaladas. \n3. Se um erro persistir, tente apagar o arquivo .db e reiniciar o app para criar um banco de dados limpo."
            }
            resposta_encontrada = "Desculpe, não entendi. Tente reformular."
            for chave in faq:
                if chave in texto:
                    resposta_encontrada = faq[chave]
                    break
            self.resposta.configure(text=resposta_encontrada, text_color="#24232F") 
        except Exception as e:
            self.resposta.configure(text=f"Erro inesperado: {str(e)}. Tente novamente.", text_color="red")

    def voltar(self):
        # (Lógica sem alteração)
        self.resposta.configure(text="Clique em uma pergunta para ver a resposta.", text_color="#444444")
        self.controlador.mostrar_tela("MenuPrincipal")