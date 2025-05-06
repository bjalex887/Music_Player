import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget
from ui.criar_conta import CriarConta
from ui.informacoes_pessoais import InformacoesPessoais
from ui.preferencias_musicais import PreferenciasMusicais
from db import criar_tabela_usuarios

def main():
    # Inicializa a tabela de usuários no banco de dados
    criar_tabela_usuarios()

    app = QApplication(sys.argv)
    stack = QStackedWidget()

    # Adiciona as telas na pilha
    stack.addWidget(CriarConta(stack))
    stack.addWidget(InformacoesPessoais(stack))
    stack.addWidget(PreferenciasMusicais(stack))

    window = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(stack)
    window.setLayout(layout)
    window.setWindowTitle("Music Player")
    window.setGeometry(100, 100, 400, 300)
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
