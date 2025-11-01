import sqlite3
import bcrypt

def conectar():
    """
    Estabelece conexão com o banco de dados SQLite.
    """
    try:
        return sqlite3.connect("sistema_escolar.db")
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None

def hash_senha(senha):
    """
    Gera um hash seguro para uma senha usando bcrypt.
    """
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verificar_senha(senha, hashed):
    """
    Verifica se uma senha em texto plano corresponde a um hash.
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
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            )""")
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS turmas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )""")
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                turma_id INTEGER,
                FOREIGN KEY(turma_id) REFERENCES turmas(id)
            )""")
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS aulas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                turma_id INTEGER,
                data TEXT,
                tema TEXT,
                descricao TEXT,
                FOREIGN KEY(turma_id) REFERENCES turmas(id)
            )""")
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS presencas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aula_id INTEGER,
                aluno_id INTEGER,
                presente INTEGER,
                FOREIGN KEY(aula_id) REFERENCES aulas(id) ON DELETE CASCADE,
                FOREIGN KEY(aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
            )""")
            
            print("Tabelas verificadas/criadas com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")