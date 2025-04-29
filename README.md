# Music Player - Reprodutor de Música com Cadastro

Este é um sistema de cadastro de usuários com interface gráfica feito em *Python + PyQt6*, que simula a criação de uma conta para um aplicativo fictício de música. O sistema armazena os dados dos usuários em um banco SQLite local e exporta as informações para um arquivo Excel.

---

## Funcionalidades

- Validação de e-mail e senha com expressões regulares.
- Cadastro de nome de usuário, data de nascimento e gênero.
- Senha criptografada com bcrypt.
- Exportação automática dos dados para um arquivo .xlsx (Excel).
- Interface gráfica simples usando PyQt6 (a interface ainda será alterada para algo mais personalizado e marcante).
- Atualmente, o projeto está em desenvolvimento na parte de cadastros — a funcionalidade de music player ainda será implementada.

---

## 📂 Estrutura do Projeto

text
📁 seu-projeto/
├── usuarios.db               # Banco de dados SQLite
├── usuarios.xlsx             # Exportação dos dados
├── README.md                 # Documentação
├── requirements.txt          # Dependências
└── main.py                   # Código principal


---

## 🛠 Requisitos
Certifique-se de ter o Python instalado (recomenda-se a versão 3.10+).

Instale as dependências com o comando:


pip install -r requirements.txt


---

## Como Executar

Clone o repositório:

git clone https://github.com/seu-usuario/seu-repositorio.git


Instale as dependências (caso ainda não tenha feito):


pip install -r requirements.txt


Execute o projeto com o comando:

python main.py


---

## Observações
Este projeto está em desenvolvimento. Futuramente, outras funcionalidades serão adicionadas.

---

## Autora
Feito com carinho por Taina de Oliveira - @bjalex887 💻
