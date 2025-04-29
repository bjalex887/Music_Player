import sqlite3


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


def inserir_usuario(email, usuario, senha_hash, idade, genero, preferencias_musicais):
    try:
        with sqlite3.connect("usuarios.db") as conexao:
            cur = conexao.cursor()
            cur.execute(
                "INSERT INTO usuarios (email, usuario, senha, idade, genero, preferencias_musicais) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (email, usuario, senha_hash, idade, genero, preferencias_musicais)
            )
            conexao.commit()
            print("Conta criada com sucesso.")
    except Exception as e:
        print("Erro ao inserir usuário:", e)
