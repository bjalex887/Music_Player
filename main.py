import sys
from PyQt6.QtWidgets import QApplication
from music_player import App

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = App()
    janela.show()
    sys.exit(app.exec())
