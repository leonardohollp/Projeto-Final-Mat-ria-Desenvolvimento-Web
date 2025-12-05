import customtkinter as ctk 
from tkinter import *
import sqlite3
from tkinter import messagebox 
import os

class Backend():
    def conecta_db(self):
        # Caminho absoluto SEMPRE apontando para a pasta do script
        caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)),"Cadastro_de_usuarios.db")
        self.conn = sqlite3.connect(caminho)
        self.cursor = self.conn.cursor()
        print("Banco de Dados conectado")


    def desconecta_db(self):
        self.conn.close()
        print("Banco de dados desconctado")

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
        print("tabela criada com sucesso!")
        self.desconecta_db()


    def cadastrar_usuario(self):
        self.username_cadastro = self.username_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.senha_cadastro = self.senha_cadastro_entry.get()
        self.confirma_senha = self.confirma_senha_entry.get()

           
       
        if self.username_cadastro == "" or self.email_cadastro == "" or self.senha_cadastro == "" or self.confirma_senha == "":
            messagebox.showerror(title= "Sistema de Login", message="ERRO!!!\nPor favor preencha Todos os campos!! ")
            return

        if len(self.username_cadastro) < 4:
            messagebox.showwarning(title="Sistema de Login", message="Nome de Usuario deve ter pelo menos 4 caracteres.")
            return

        if len(self.senha_cadastro) < 4:
            messagebox.showwarning(title="Sistema de Login", message="A senha deve ter pelo menos 4 caracteres.")
            return

        if self.senha_cadastro != self.confirma_senha:
            messagebox.showerror(title="Sistema de Login", message="ERRO\n As senhas colocadas não são iguais.")
            return
        

        self.conecta_db()

        try:

            self.cursor.execute("""
             INSERT INTO Usuarios (Username, Email, Senha ,Confirma_senha)
                VALUES (?,?,?,?)""", 
                (self.username_cadastro, self.email_cadastro, self.senha_cadastro, self.confirma_senha))
            
            self.conn.commit()
            messagebox.showinfo(title="Sistema de Login", message=f"Parabéns {self.username_cadastro}\n Seus dados foram Cadastrados com sucesso")   
            self.desconecta_db()
            self.limpar_entry_cadastro()

         
        except Exception as e:
            messagebox.showerror(title="Sistema de Login", message="Erro no Processamento do seu Cadastro!\n Por favor tente Novamente!")
            
        finally:
            self.desconecta_db()    


    def verifica_login(self):
            self.username_login = self.username_login_entry.get()
            self.senha_login = self.senha_login_entry.get()
            
            self.conecta_db()

            self.cursor.execute(""" SELECT * FROM Usuarios WHERE (Username = ? AND Senha = ?)""", (self.username_login, self.senha_login))

            self.verifica_dados = self.cursor.fetchone() #percorrendo na tabela usuarios 
            
            try:
                if (self.username_login == "" or self.senha_login == ""):
                    messagebox.showwarning(title="Sistema de login", message="Por favor Preencha todos os campos!")

                elif (self.username_login in self.verifica_dados and self.senha_login in self.verifica_dados):
                    messagebox.showinfo(title="Sistema de Login", message=f"Parabéns {self.username_login}\n Login feito com sucesso!")
                    self.desconecta_db()
                    self.limpa_entrada_login()

            except:
                messagebox.showerror(title="Sistema de Login", message="ERRO!!! \\n Dados não encontrados no sistema \nPor favor verifique seus dados ou cadastra-se no sitema !")
                self.desconecta_db()        



class Login(ctk.CTk, Backend):
    def __init__(self):
        super().__init__()
        self.configuracao_da_janela_inicial()
        self.criar_tabela()
        self.tela_de_login()
       

    #Configurando a janela inicial
    def configuracao_da_janela_inicial(self):
        largura = 1000
        altura = 600

        self.title("Sistema de Login")
        self.resizable(False, False)

        self.update_idletasks()
        largura_tela =  self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)

        self.geometry(f"{largura}x{altura}+{x}+{y}")


    def tela_de_login(self):

        #removendo tela de cadastro
        

        #trabalhando com as imagens 
        self.img = PhotoImage(file="img/img.png")
        self.Lb_img= ctk.CTkLabel(self, text=None, image=self.img)
        self.Lb_img.place(relx=0.5, rely=0.5, anchor="center")

        #titulo da nossa plataforma
        # Título da plataforma
        self.title = ctk.CTkLabel(
        self,
        text="Faça seu login ou Cadastra-se \nna nossa Plataforma para acessar os nossos serviços!",
        font=("Century Gothic bold", 14),
        justify="center"
        )
        self.title.place(relx=0.5, y=10, anchor="n")  # relx=0.5 centraliza horizontalmente, y=10 distancia da borda superior


        #criar a frmae do formulario de login
        self.Frame_login = ctk.CTkFrame(self, width=350, height=380)
        self.Frame_login.place(x=350, y=80)  # ajustei y para não ficar em cima do título


        #colocando widgets dentro do frame- formulario de login
        self.lb_title = ctk.CTkLabel(self.Frame_login, text="Faça seu login", font=("Century Gothic bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10) 

        self.username_login_entry = ctk.CTkEntry(self.Frame_login, width=300, placeholder_text="Seu nome de Usuario...", font=("Century Gothic bold", 16), corner_radius=15)
        self.username_login_entry.grid(row=1, column=0, pady=10, padx=10)

        self.senha_login_entry = ctk.CTkEntry(self.Frame_login, width=300,placeholder_text=("Sua senha de Usuario"), font=("Century Gothic bold", 16),corner_radius=15, show="*")
        self.senha_login_entry.grid(row=2, column=0, pady=10, padx=10)
        
        self.ver_senha_login = ctk.CTkCheckBox(self.Frame_login, text="Clique para ver a senha", font=("Century Gothic bold", 14), corner_radius=20,command=self.mostrar_senha_login)
        self.ver_senha_login.grid(row=3, column=0, pady=10, padx=10)

        self.botao_login  = ctk.CTkButton(self.Frame_login, width=300, text="Fazer login".upper(), font=("Century Gothic bold", 16), corner_radius=15, command=self.verifica_login)
        self.botao_login.grid(row=4, column=0, pady=10, padx=10)

        self.span = ctk.CTkLabel(self.Frame_login, text="Se não tem conta,clique no botão abaixo para se \n cadastrar no nosso sistema", font=("Century Gothic", 10))
        self.span.grid(row=5, column=0, pady=10, padx=10)

        self.botao_cadastro  = ctk.CTkButton(self.Frame_login, width=300, fg_color="green", hover_color="#050", text="Fazer Cadastro".upper(), font=("Century Gothic bold", 16), corner_radius=15, command=self.tela_de_cadastro)
        self.botao_cadastro.grid(row=6, column=0, pady=10, padx=10)


    def tela_de_cadastro(self):
        #remover o formulario de login
        self.Frame_login.place_forget()

        #frame de formulario de cadastro
        self.Frame_cadastro = ctk.CTkFrame(self, width=350, height=380)
        self.Frame_cadastro.place(x=350, y=80)  # ajustei y para não ficar em cima do título


        #Criando o nosso titulo
        self.lb_title = ctk.CTkLabel(self.Frame_cadastro, text="Faça seu login", font=("Century Gothic bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=5) 


        #criar nossos wigets da tela de cadastro
        self.username_cadastro_entry = ctk.CTkEntry(self.Frame_cadastro, width=300, placeholder_text="Seu nome de Usuario...", font=("Century Gothic bold", 16), corner_radius=15)
        self.username_cadastro_entry.grid(row=1, column=0, pady=5, padx=10)

        self.email_cadastro_entry = ctk.CTkEntry(self.Frame_cadastro, width=300, placeholder_text="Insira seu Email", font=("Century Gothic bold", 16), corner_radius=15)
        self.email_cadastro_entry.grid(row=2, column=0, pady=5, padx=10)


        self.senha_cadastro_entry = ctk.CTkEntry(self.Frame_cadastro, width=300,placeholder_text=("Sua senha de Usuario"), font=("Century Gothic bold", 16),corner_radius=15, show="*")
        self.senha_cadastro_entry.grid(row=3, column=0, pady=5, padx=10)
        
        self.confirma_senha_entry = ctk.CTkEntry(self.Frame_cadastro, width=300, placeholder_text="Confirme sua senha de usuario", font=("Century Gothic bold", 16), corner_radius=15)
        self.confirma_senha_entry.grid(row=4, column=0, pady=5, padx=10)

        self.ver_senha_cadastro = ctk.CTkCheckBox(self.Frame_cadastro, text="Clique para ver a senha", font=("Century Gothic bold", 14), corner_radius=20,command=self.mostrar_senha_cadastro)
        self.ver_senha_cadastro.grid(row=5, column=0, pady=5)

        self.botao_cadastrar_usuario  = ctk.CTkButton(self.Frame_cadastro, width=300, fg_color="green", hover_color="#050", text="Fazer Cadastro".upper(), font=("Century Gothic bold", 14), corner_radius=15, command=self.cadastrar_usuario)
        self.botao_cadastrar_usuario.grid(row=6, column=0, pady=5, padx=10)

        self.botao_login_voltar  = ctk.CTkButton(self.Frame_cadastro, width=300, text="Voltar para tela anterior".upper(), font=("Century Gothic bold", 14), corner_radius=15, fg_color="#444", hover_color="#333", command=self.tela_de_login)
        self.botao_login_voltar.grid(row=7, column=0, pady=5, padx=10)

    def mostrar_senha_login(self):
        if self.ver_senha_login.get() == 1:
            self.senha_login_entry.configure(show="")   # Mostra senha
        else:
            self.senha_login_entry.configure(show="*")  # Esconde senha

    def mostrar_senha_cadastro(self):
        if self.ver_senha_cadastro.get() == 1:
            self.senha_cadastro_entry.configure(show="")
            self.confirma_senha_entry.configure(show="")
        else:
            self.senha_cadastro_entry.configure(show="*")
            self.confirma_senha_entry.configure(show="*")

    def limpar_entry_cadastro(self):
        self.username_cadastro_entry.delete(0, END)
        self.email_cadastro_entry.delete(0, END)
        self.senha_cadastro_entry.delete(0, END)
        self.confirma_senha_entry.delete(0, END)

    def limpa_entrada_login(self):
        self.username_login_entry.delete(0, END)
        self.senha_login_entry.delete(0, END)

if __name__=="__main__":
    app = Login()
    app.mainloop()