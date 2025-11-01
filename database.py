"""
Arquivo de Banco de Dados (database.py)

Este módulo centraliza todas as interações com o banco de dados SQLite.
Inclui funções para:
1. Conectar ao banco de dados.
2. Criar todas as tabelas necessárias (schema).
3. Gerenciar criptografia de senhas (hash e verificação).
"""

import sqlite3
import bcrypt

def conectar():
    """
    Estabelece conexão com o banco de dados SQLite.
    Usa um 'with' statement para garantir que a conexão
    seja fechada automaticamente (commit ou rollback).
    
    Returns:
        sqlite3.Connection: Objeto de conexão ou None se falhar.
    """
    try:
        # Tenta conectar ao arquivo do banco de dados
        return sqlite3.connect("sistema_escolar.db")
    except sqlite3.Error as e:
        # Imprime o erro se a conexão falhar
        print(f"Erro ao conectar ao banco: {e}")
        return None

def hash_senha(senha):
    """
    Gera um hash seguro para uma senha usando bcrypt.
    
    Args:
        senha (str): A senha em texto plano.
        
    Returns:
        str: A senha hasheada (em formato string).
    """
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verificar_senha(senha, hashed):
    """
    Verifica se uma senha em texto plano corresponde a um hash.
    
    Args:
        senha (str): A senha em texto plano (ex: "123456").
        hashed (str): A senha hasheada armazenada no banco.
        
    Returns:
        bool: True se a senha corresponder, False caso contrário.
    """
    try:
        return bcrypt.checkpw(senha.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

def criar_tabelas():
    """
    Cria todas as tabelas necessárias no banco de dados, se elas não existirem.
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            
            # Tabela de Usuários (para login)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            )""")
            
            # Tabela de Turmas
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS turmas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )""")
            
            # Tabela de Alunos
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                turma_id INTEGER,
                FOREIGN KEY(turma_id) REFERENCES turmas(id)
            )""")
            
            # Tabela de Aulas
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS aulas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                turma_id INTEGER,
                data TEXT,
                tema TEXT,
                descricao TEXT,
                FOREIGN KEY(turma_id) REFERENCES turmas(id)
            )""")
            
            # Tabela de Presenças
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS presencas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aula_id INTEGER,
                aluno_id INTEGER,
                presente INTEGER,
                FOREIGN KEY(aula_id) REFERENCES aulas(id) ON DELETE CASCADE,
                FOREIGN KEY(aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
            )""")
            
            # --- NOVA TABELA ADICIONADA ---
            # Tabela de Atividades (requisito do PIM)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS atividades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                turma_id INTEGER,
                nome TEXT NOT NULL,
                data_entrega TEXT,
                descricao TEXT,
                FOREIGN KEY(turma_id) REFERENCES turmas(id) ON DELETE CASCADE
            )""")
            # --- FIM DA NOVA TABELA ---
            
            print("Tabelas verificadas/criadas com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")