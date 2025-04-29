from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from PyQt6.QtCore import QRegularExpression, QDate
from PyQt6.QtGui import QRegularExpressionValidator


class InformacoesPessoais(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.email = ""
        self.usuario = ""
        self.senha_hash = ""

        layout = QVBoxLayout()

        self.label_idade = QLabel("Data de Nascimento:")
        self.input_idade = QLineEdit()
        regex = QRegularExpression(r"^\d{2}/\d{2}/\d{4}$")
        validator = QRegularExpressionValidator(regex)
        self.input_idade.setValidator(validator)
        self.input_idade.setPlaceholderText("DD/MM/AAAA")

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

        if not idade:
            QMessageBox.warning(self, "Erro", "Por favor, insira sua data de nascimento.")
            return

        try:
            dia, mes, ano = map(int, idade.split("/"))
            data = QDate(ano, mes, dia)
            if not data.isValid() or ano > QDate.currentDate().year():
                raise ValueError

        except ValueError:
            QMessageBox.warning(self, "Erro", "Data de nascimento inválida. Use o formato DD/MM/AAAA")
            return

        self.stack.widget(2).receber_dados(self.email, self.usuario, self.senha_hash, idade, genero)
        self.stack.setCurrentIndex(2)
