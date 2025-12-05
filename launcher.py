import threading
import webbrowser
import time
import sys
import requests
from flask import Flask, render_template, request, jsonify

import main as dashboard_app
import sqlite3
import os


basedir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(basedir, 'templates')


app = Flask(__name__,template_folder=template_dir)

LOGIN_SUCCESS_EVENT = threading.Event()

class Backend:
    def conecta_db(self):
        caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Cadastro_de_usuarios.db")
        self.conn = sqlite3.connect(caminho, check_same_thread=False)
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
        LOGIN_SUCCESS_EVENT.set() #coloque no cadastro se for necessário
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
    
def run_flask():
    app.run(debug=False, use_reloader=False, port=5000)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()


if __name__ == "__main__":
    print("Iniciando Servidor de Login...")

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    time.sleep(1.5)

    print("Abrindo navegador...")
    webbrowser.open("http://127.0.0.1:5000")

    print("Aguardando Login do usuário...")
    try:
        while not LOGIN_SUCCESS_EVENT.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit()

    print("Login detectado! Fechando servidor web e iniciando Dashboard...")

    time.sleep(2)

    try:
        dashboard_app.iniciar_dashboard()
    except AttributeError:
        print("ERRO: Você esqueceu de envolver seu código do main.py na função 'iniciar_dashboard()'.")
    except Exception as e:
        print(f"Erro ao iniciar dashboard: {e}")
