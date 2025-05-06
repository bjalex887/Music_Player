import sqlite3
import sys


def criar_tabela_usuarios():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        usuario TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        idade TEXT,
        genero TEXT,
        preferencias_musicais TEXT
    )
    """)
    conn.commit()
    conn.close()
    sys.stdout.write("\rTabela de usuários criada/já existente.")
    sys.stdout.flush()


def inserir_usuario(email, usuario, senha_hash, idade, genero, preferencias_musicais):
    try:
        with sqlite3.connect("usuarios.db") as conexao:
            cur = conexao.cursor()

            sys.stdout.write("\r exportando dados para banco de dados.....")
            sys.stdout.flush()

            cur.execute(
                "INSERT INTO usuarios (email, usuario, senha, idade, genero, preferencias_musicais) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (email, usuario, senha_hash, idade, genero, preferencias_musicais)
            )
            conexao.commit()
        print("Conta criada com sucesso.")

        sys.stdout.write("\r Conta criada com sucesso")
        sys.stdout.flush()

    except Exception as e:
        print("Erro ao inserir usuário:", e)

        sys.stdout.write("\r Conta criada com sucesso")
        sys.stdout.flush()
