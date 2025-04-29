import os
import sqlite3
import pandas as pd
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QMessageBox, QListWidgetItem
)


class PreferenciasMusicais(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.email = ""
        self.usuario = ""
        self.senha_hash = ""
        self.idade = ""
        self.genero = ""

        layout = QVBoxLayout()

        self.label_preferenciamusical = QLabel("Selecione gêneros musicais que te agradam")
        self.lista_preferenciamusical = QListWidget()
        self.lista_preferenciamusical.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

        generos = [
            "Pop", "Alternativa", "Rock", "Hard Rock", "Metal", "Grunge", "Punk",
            "Hip-Hop", "Rap", "Trap", "Lo-fi", "Eletrônica", "House", "Techno", "Trance",
            "Drum and Bass", "Dubstep", "MPB", "Sertanejo", "Sertanejo Universitário",
            "Forró", "Xote", "Baião", "Axé", "Samba", "Pagode", "Funk", "Funk Carioca",
            "Jazz", "Blues", "Soul", "R&B", "Clássica", "Opera", "Reggae", "Ska",
            "K-pop", "J-pop", "Anime", "Indie", "Indie Rock", "Indie Pop", "Gospel",
            "Religiosa", "Country", "Folk", "Latina", "Reggaeton", "Cumbia", "Tango",
            "Afrobeat", "World Music", "New Age", "Instrumental", "Experimental", "Outros"
        ]

        for genero in generos:
            item = QListWidgetItem(genero)
            self.lista_preferenciamusical.addItem(item)

        self.botao_confirmar = QPushButton("Finalizar Cadastro!")
        self.botao_confirmar.clicked.connect(self.confirmar_preferencias)

        layout.addWidget(self.label_preferenciamusical)
        layout.addWidget(self.lista_preferenciamusical)
        layout.addWidget(self.botao_confirmar)

        self.setLayout(layout)

    def receber_dados(self, email, usuario, senha_hash, idade, genero):
        self.email = email
        self.usuario = usuario
        self.senha_hash = senha_hash
        self.idade = idade
        self.genero = genero

    def confirmar_preferencias(self):
        selecionados = [item.text() for item in self.lista_preferenciamusical.selectedItems()]
        preferencias = ", ".join(selecionados)

        try:
            with sqlite3.connect("usuarios.db") as conexao:
                cur = conexao.cursor()
                cur.execute(
                    "INSERT INTO usuarios (email, usuario, senha, idade, genero, preferencias_musicais) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        self.email, self.usuario, self.senha_hash,
                        self.idade, self.genero, preferencias
                    )
                )
                conexao.commit()
                self.exportar_para_excel(conexao)

        except Exception as e:
            print("Erro ao criar conta:", e)
            QMessageBox.warning(self, "Erro", "Não foi possível criar a conta.")
            return

        QMessageBox.information(self, "Sucesso", "Conta criada com sucesso!")
        self.stack.setCurrentIndex(0)

    @staticmethod
    def exportar_para_excel(conexao):
        caminho_excel = os.path.join(os.getcwd(), "usuarios.xlsx")
        df = pd.read_sql_query(
            "SELECT id, email, usuario, idade, genero, preferencias_musicais FROM usuarios", conexao
        )
        df.to_excel(caminho_excel, index=False)
