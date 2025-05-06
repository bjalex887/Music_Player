import bcrypt
import sqlite3
from PyQt6.QtCore import QRegularExpression
import re


def validar_email(email):
    regex = QRegularExpression(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    print("validação de e-mail concluída.")
    return regex.match(email).hasMatch()


def validar_senha(senha: str) -> bool:
    # Verifica se a senha tem pelo menos 8 caracteres
    if len(senha) < 8:
        return False
    # Verifica se há pelo menos uma letra maiúscula
    if not re.search(r"[A-Z]", senha):
        return False
    # Verifica se há pelo menos uma letra minúscula
    if not re.search(r"[a-z]", senha):
        return False
    # Verifica se há pelo menos um número
    if not re.search(r"[0-9]", senha):
        return False
    # Verifica se há pelo menos um caractere especial
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
        return False
    print("validação de senha concluída.")
    return True


def verificar_usuario_existente(email, usuario):
    conexao = sqlite3.connect("usuarios.db")
    cur = conexao.cursor()
    cur.execute("SELECT * FROM usuarios WHERE email = ? OR usuario = ?", (email, usuario))
    usuario_existente = cur.fetchone()
    conexao.close()
    print("verificação de usuário concluida.")
    return usuario_existente is not None


def criptografar_senha(senha):
    print("senha criptografada com sucesso")
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
