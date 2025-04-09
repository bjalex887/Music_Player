import sys
import sqlite3
import os
import pandas as pd
import bcrypt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QStackedWidget, QMessageBox, QHBoxLayout, QComboBox
)
from PyQt6.QtGui import (
    QRegularExpressionValidator
)
from PyQt6.QtCore import QRegularExpression

conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    usuario TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    idade TEXT,
    genero TEXT
)
""")

conn.commit()
conn.close()


class CriarConta(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        # Declarando os atributos de instância
        self.email = ""
        self.usuario = ""
        self.senha_hash = ""

        layout = QVBoxLayout()

        self.setWindowTitle("Music Player")
        self.setGeometry(100, 100, 400, 300)

        self.label_email = QLabel("E-mail:")
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Digite seu e-mail.")

        self.label_usuario = QLabel("Usuário:")
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Digite seu nome de usuário.")

        self.label_senha = QLabel("Senha:")
        senha_layout = QHBoxLayout()

        self.input_senha = QLineEdit()
        self.input_senha.setPlaceholderText("Digite uma nova senha.")
        self.input_senha.setEchoMode(QLineEdit.EchoMode.Password)

        self.botao_mostrar_senha = QPushButton("EXIBIR")
        self.botao_mostrar_senha.setCheckable(True)
        self.botao_mostrar_senha.setFixedWidth(60)
        self.botao_mostrar_senha.clicked.connect(self.toggle_senha)

        senha_layout.addWidget(self.input_senha)
        senha_layout.addWidget(self.botao_mostrar_senha)

        self.label_requisitos_senha = QLabel(
            "A senha deve conter:\n"
            "- Pelo menos 8 caracteres\n"
            "- Pelo menos 1 número\n"
            "- Pelo menos 1 letra maiúscula e 1 minúscula\n"
            "- Pelo menos 1 caractere especial (!@#$%^&*...)"
        )

        self.botao_CriarConta = QPushButton("Criar Conta!")
        self.botao_CriarConta.clicked.connect(self.criarconta)

        layout.addWidget(self.label_email)
        layout.addWidget(self.input_email)
        layout.addWidget(self.label_usuario)
        layout.addWidget(self.input_usuario)
        layout.addWidget(self.label_senha)
        layout.addLayout(senha_layout)
        layout.addWidget(self.label_requisitos_senha)
        layout.addWidget(self.botao_CriarConta)

        self.setLayout(layout)

    def toggle_senha(self):
        if self.botao_mostrar_senha.isChecked():
            self.input_senha.setEchoMode(QLineEdit.EchoMode.Normal)
            self.botao_mostrar_senha.setText("OCULTAR")
        else:
            self.input_senha.setEchoMode(QLineEdit.EchoMode.Password)
            self.botao_mostrar_senha.setText("EXIBIR")

    @staticmethod
    def validar_email(email):
        regex = QRegularExpression(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        return regex.match(email).hasMatch()

    @staticmethod
    def validar_senha(senha):
        regex = QRegularExpression(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$")
        return regex.match(senha).hasMatch()

    @staticmethod
    def verificar_usuario_existente(email, usuario):
        conexao = sqlite3.connect("usuarios.db")
        cur = conexao.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = ? OR usuario = ?", (email, usuario))
        usuario_existente = cur.fetchone()
        conexao.close()

        return usuario_existente is not None

    def criarconta(self):
        email = self.input_email.text().strip()
        usuario = self.input_usuario.text().strip()
        senha = self.input_senha.text()

        print("Tentando criar conta com:", email, usuario)

        if not self.validar_email(email):
            QMessageBox.warning(self, "ERRO", "Digite um e-mail válido.")
            return
        if not self.validar_senha(senha):
            QMessageBox.warning(self, "ERRO", "A senha não atende aos requisitos mínimos.")
            return
        if self.verificar_usuario_existente(email, usuario):
            QMessageBox.warning(self, "ERRO", "E-mail ou nome de usuário já cadastrados.")
            return

        self.email = email
        self.usuario = usuario
        self.senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
        print("Senha criptografada com sucesso.")

        # Envia os dados para a próxima tela (InformacoesPessoais)
        self.stack.widget(1).receber_dados(self.email, self.usuario, self.senha_hash)
        self.stack.setCurrentIndex(1)


class InformacoesPessoais(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        # Declarando os atributos da instância corretamente
        self.email = ""
        self.usuario = ""
        self.senha_hash = ""

        layout = QVBoxLayout()

        self.label_idade = QLabel("Data de Nascimento:")
        self.input_idade = QLineEdit()
        regex = QRegularExpression(r"^\d{2}/\d{2}/\d{4}$")
        validator = QRegularExpressionValidator(regex)
        self.input_idade.setValidator(validator)
        self.input_idade.setPlaceholderText("DD/MM/AA")

        self.label_genero = QLabel("Gênero:")
        self.input_genero = QComboBox()
        self.input_genero.addItems(["Feminino", "Masculino", "Outro", "Prefiro não informar"])

        self.botao_confirmar = QPushButton("Confirmar")
        self.botao_confirmar.clicked.connect(self.confirmar_dados)

        layout.addWidget(self.label_idade)
        layout.addWidget(self.input_idade)
        layout.addWidget(self.label_genero)
        layout.addWidget(self.input_genero)
        layout.addWidget(self.botao_confirmar)

        self.setLayout(layout)

    def receber_dados(self, email, usuario, senha_hash):
        self.email = email
        self.usuario = usuario
        self.senha_hash = senha_hash

    def confirmar_dados(self):
        idade = self.input_idade.text()
        genero = self.input_genero.currentText()

        try:
            with sqlite3.connect("usuarios.db") as conexao:
                cur = conexao.cursor()
                cur.execute("INSERT INTO usuarios (email, usuario, senha, idade, genero) VALUES (?, ?, ?, ?, ?)",
                            (self.email, self.usuario, self.senha_hash, idade, genero))
                conexao.commit()
                print("Conta criada com sucesso.")
                self.exportar_para_excel(conexao)
        except Exception as e:
            print("Erro ao criar conta:", e)
            QMessageBox.warning(self, "Erro", "Não foi possível criar a conta.")
            return

        QMessageBox.information(self, "Sucesso", "Conta criada com sucesso!")
        self.stack.setCurrentIndex(0)  # Volta para o início ou para a tela de login

    @staticmethod
    def exportar_para_excel(conexao):
        caminho_excel = os.path.join(os.getcwd(), "usuarios.xlsx")
        df = pd.read_sql_query("SELECT id, email, usuario, idade, genero FROM usuarios", conexao)
        df.to_excel(caminho_excel, index=False)
        print("Dados exportados para", caminho_excel)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Player")
        self.setGeometry(100, 100, 400, 300)

        self.stack = QStackedWidget(self)
        self.stack.addWidget(CriarConta(self.stack))
        self.stack.addWidget(InformacoesPessoais(self.stack))

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)


app = QApplication(sys.argv)
janela = App()
janela.show()
app.exec()
