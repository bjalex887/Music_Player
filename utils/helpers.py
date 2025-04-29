import pandas as pd
import os


def exportar_para_excel(conexao):
    caminho_excel = os.path.join(os.getcwd(), "usuarios.xlsx")
    df = pd.read_sql_query("SELECT id, email, usuario, idade, genero, preferencias_musicais FROM usuarios", conexao)
    df.to_excel(caminho_excel, index=False)
    print("Dados exportados para", caminho_excel)
