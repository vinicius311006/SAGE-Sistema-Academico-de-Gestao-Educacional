# SAGE - Sistema Acadêmico de Gestão Educacional

![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet)

Sistema desktop para gerenciamento acadêmico, focado em facilitar a rotina de professores.

Este projeto foi desenvolvido como o **Projeto Integrado Multidisciplinar (PIM II)** do curso de Análise e Desenvolvimento de Sistemas da **Universidade Paulista (UNIP)** - Campus Araraquara.

## 🚀 Funcionalidades

* **🔐 Autenticação:** Sistema de cadastro e login de professores, com senhas criptografadas (usando `bcrypt`).
* **📚 Gestão de Turmas:** Permite ao professor cadastrar, editar e excluir suas turmas.
* **🎓 Gestão de Alunos:** Permite cadastrar novos alunos e associá-los a uma turma específica.
* **✅ Registro de Aulas e Frequência:** A principal função do sistema. O professor pode registrar uma aula (data, tema) e marcar a presença/falta de cada aluno da turma.
* **📊 Relatórios:**
    * Visualização do histórico de aulas e presenças.
    * Edição de frequências lançadas incorretamente.
    * Exportação da frequência da turma para um arquivo `.CSV`.
* **🤖 Chatbot (IA):** Um chatbot acadêmico simples para responder dúvidas frequentes sobre o uso do software (requisito de IA do PIM).

---

## 💻 Tecnologias Utilizadas

* **Linguagem Principal:** Python 3
* **Interface Gráfica (GUI):** CustomTkinter
* **Banco de Dados:** SQLite3 (módulo nativo do Python)
* **Criptografia de Senhas:** Bcrypt

---

## ⚙️ Como Executar o Projeto (a partir do código)

1.  Clone este repositório:
    ```bash
    git clone https://github.com/vinicius311006/SAGE-Sistema-Academico-de-Gestao-Educacional.git
    ```

2.  Navegue até a pasta do projeto:
    ```bash
    cd SAGE-Sistema-Academico-de-Gestao-Educacional
    ```

3.  Instale as dependências necessárias:
    ```bash
    pip install customtkinter bcrypt
    ```

4.  Execute a aplicação principal:
    ```bash
    python main.py
    ```

---

## 🎓 Vídeo de Apresentação e Artefatos

* **Vídeo de Apresentação (Obrigatório PIM):** [Link para o Vídeo no Google Drive](https://drive.google.com/file/d/16xa-Kam4-8E5Hl_hbgdQh2VpcXyQIQ7_/view?usp=sharing)
* **Formulário de Avaliação (Ativ. Extensão):** [Link para o Google Forms](https://forms.gle/MbwtbstywSXNwdNf7)

---

## 👥 Autores do Projeto

* **Vinícius Nascimento Buzzo** ([@vinicius311006](https://github.com/vinicius311006)) - *Desenvolvimento e Documentação*
* **João Vitor de Souza pedrosa bomfim** - *Criação e Edição do Vídeo*
* **Gabriel de Oliveira**
* **Guilherme Victor da Silva Prado**
* **Biagio Morvillo Neto**
* **Felipe Rodrigues dos Santos**
