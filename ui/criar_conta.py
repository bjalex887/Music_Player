from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QMessageBox
)
from models import validar_email, validar_senha, verificar_usuario_existente, criptografar_senha


class CriarConta(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.email = ""
        self.usuario = ""
        self.senha_hash = ""

        layout = QVBoxLayout()

        self.label_email = QLabel("E-mail:")
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Digite seu e-mail")

        self.label_usuario = QLabel("Nome de usuário:")
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Digite seu nome de usuário")

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

        self.botao_criar = QPushButton("Criar Conta")
        self.botao_criar.clicked.connect(self.criarconta)

        layout.addWidget(self.label_email)
        layout.addWidget(self.input_email)
        layout.addWidget(self.label_usuario)
        layout.addWidget(self.input_usuario)
        layout.addWidget(self.label_senha)
        layout.addLayout(senha_layout)
        layout.addWidget(self.label_requisitos_senha)
        layout.addWidget(self.botao_criar)

        self.setLayout(layout)

    def toggle_senha(self):
        if self.botao_mostrar_senha.isChecked():
            self.input_senha.setEchoMode(QLineEdit.EchoMode.Normal)
            self.botao_mostrar_senha.setText("OCULTAR")
        else:
            self.input_senha.setEchoMode(QLineEdit.EchoMode.Password)
            self.botao_mostrar_senha.setText("EXIBIR")

    def criarconta(self):
        email = self.input_email.text().strip()
        usuario = self.input_usuario.text().strip()
        senha = self.input_senha.text()

        if not validar_email(email):
            QMessageBox.warning(self, "ERRO", "Digite um e-mail válido.")
            return
        if not validar_senha(senha):
            QMessageBox.warning(self, "ERRO", "A senha não atende aos requisitos mínimos.")
            return
        if verificar_usuario_existente(email, usuario):
            QMessageBox.warning(self, "ERRO", "E-mail ou nome de usuário já cadastrados.")
            return

        self.email = email
        self.usuario = usuario
        self.senha_hash = criptografar_senha(senha)
        self.stack.widget(1).receber_dados(self.email, self.usuario, self.senha_hash)
        self.stack.setCurrentIndex(1)
