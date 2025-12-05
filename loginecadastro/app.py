from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os

app = Flask(__name__)

# ================================
# MESMAS FUNÇÕES DO BACKEND
# ================================

class Backend:
    def conecta_db(self):
        caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Cadastro_de_usuarios.db")
        self.conn = sqlite3.connect(caminho)
        self.cursor = self.conn.cursor()
        print("Banco de Dados conectado")
        print(">>> Função conectar() foi chamada")

    def desconecta_db(self):
        self.conn.close()
        print("Banco de dados desconectado")

    def criar_tabela(self):
        self.conecta_db()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username  TEXT NOT NULL,
                Email TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Confirma_senha  TEXT NOT NULL
            );
        """)
        self.conn.commit()
        self.desconecta_db()

    def cadastrar_usuario(self, username, email, senha, confirma):
        # REPLICANDO A MESMA LÓGICA DO SEU CÓDIGO TKINTER
        if username == "" or email == "" or senha == "" or confirma == "":
            return "Por favor preencha todos os campos!"

        if len(username) < 4:
            return "Nome de Usuário deve ter pelo menos 4 caracteres."

        if len(senha) < 4:
            return "A senha deve ter pelo menos 4 caracteres."

        if senha != confirma:
            return "As senhas não são iguais."

        self.conecta_db()
        try:
            self.cursor.execute("""
                INSERT INTO Usuarios (Username, Email, Senha, Confirma_senha)
                VALUES (?,?,?,?)
            """, (username, email, senha, confirma))

            self.conn.commit()
            return "OK"

        except Exception as e:
            return "Erro ao cadastrar usuário!"
        
        finally:
            self.desconecta_db()

    def verifica_login(self, username, senha):
        self.conecta_db()
        print(f">>> Validar login chamado com {username} - {senha}")
        self.cursor.execute(""" 
            SELECT * FROM Usuarios WHERE (Username = ? AND Senha = ?)
        """, (username, senha))

        dados = self.cursor.fetchone()
        self.desconecta_db()

        if dados:
            return "OK"
        else:
            return "Dados incorretos!"


# ================================
# ROTAS FLASK (NOVO FRONT-END)
# ================================

backend = Backend()
backend.criar_tabela()


# Página inicial (login)
@app.route("/")
@app.route("/login", methods=["GET"])
def login_page():
    return render_template("index.html")


# Receber POST do formulário de login
@app.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username_login")
    senha = request.form.get("senha_login")

    resultado = backend.verifica_login(username, senha)

    if resultado == "OK":
        return jsonify({"status": "success", "message": "Login realizado com sucesso!"})
    else:
        return jsonify({"status": "error", "message": resultado})


# Página de cadastro
@app.route("/cadastro", methods=["GET"])
def cadastro_page():
    return render_template("cadastro.html")


# Receber POST do formulário de cadastro
@app.route("/cadastro", methods=["POST"])
def cadastro_post():
    username = request.form.get("username_cadastro")
    email = request.form.get("email_cadastro")
    senha = request.form.get("senha_cadastro")
    confirma = request.form.get("confirma_senha")

    resultado = backend.cadastrar_usuario(username, email, senha, confirma)

    if resultado == "OK":
        return jsonify({"status": "success", "message": "Cadastro feito com sucesso!"})
    else:
        return jsonify({"status": "error", "message": resultado})


if __name__ == "__main__":
    app.run(debug=True)
