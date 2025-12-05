import customtkinter as ctk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# importando pillow
from PIL import Image

# importando barra de progresso do tlinter (Substituído por CTkProgressBar)
# from tkinter.ttk import Progressbar

# importando matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# tkcalendar
from tkcalendar import Calendar, DateEntry
from datetime import date

# importando funções da view
# Estas funções (view.py) devem existir no mesmo diretório
try:
    from view import (bar_valores, pie_valores, porcentagem_valor,inserir_categoria, inserir_gastos, ver_categoria,inserir_receitas, tabela, deletar_gastos, deletar_receitas)
except ImportError:
    messagebox.showerror("Erro de Importação", "Não foi possível encontrar o arquivo 'view.py'.\nCertifique-se de que ele está no mesmo diretório e contém todas as funções necessárias.")
    exit()

def iniciar_dashboard():


    ################# Cores (Tema Dashboard Analítico) ###############
    co_janela = "#263238"  # BG da Janela (Azul-acinzentado escuro)
    co_frame = "#2e2d2b"   # BG dos Frames/Cards (Preto/Grafite)
    co_widget = "#403d3d"  # BG de botões/entradas (Cinza escuro)

    co_texto_claro = "#feffff" # Texto principal (Branco)
    co_texto_escuro = "#a9a9a9" # Texto secundário (Cinza claro)

    co_accent_purple = "#9370DB" # Roxo/Lilás (Gráfico principal)
    co_accent_blue = "#5588bb"   # Azul (Gráfico)
    co_accent_red = "#bb5555"    # Vermelho (Gráfico)
    co_accent_green = "#4fa882"  # Verde (Positivo)
    co_accent_orange = "#e06636" # Laranja (Negativo/Deletar)

    # Paleta de cores para gráficos
    chart_colors = [co_accent_green, co_accent_blue, co_accent_red, '#66bbbb', '#99bb55', '#ee9944']
    chart_colors_pie = [co_accent_purple, co_accent_blue, co_accent_red, '#66bbbb', '#99bb55', '#ee9944','#AF9164', '#B3B6B7','#F7F3E3','#F7996E','#B2EDC5','#153131','#E08DAC','#533B4D']


    # criando janela
    ctk.set_appearance_mode("dark")  # Força o modo escuro
    janela = ctk.CTk()
    janela.title("My Cash Flow - Dashboard Financeiro")
    janela.attributes('-fullscreen', False) # Começa em um tamanho bom com possibilidade de resize
    janela.configure(fg_color=co_janela)
    janela.resizable(width=TRUE, height=TRUE)

    # Configura a grade da janela principal
    janela.grid_columnconfigure(0, weight=1)
    janela.grid_rowconfigure(2, weight=1) # frameMeio (expande)
    janela.grid_rowconfigure(3, weight=0) # frameBaixo (fixo)

    # --- Estilização do TTK (para Treeview e DateEntry) ---
    style = ttk.Style(janela)
    style.theme_use("clam")

    # Estilo do Treeview (Tabela)
    style.configure("Treeview",background=co_frame,foreground=co_texto_claro,fieldbackground=co_frame,borderwidth=0,rowheight=25)  # Altura da linha
    style.configure("Treeview.Heading",background=co_widget,foreground=co_texto_claro,font=('Verdana', 10, 'bold'),relief="flat",padding=(0, 5))
    style.map("Treeview.Heading",background=[('active', co_accent_purple)])
    style.map("Treeview",background=[('selected', co_accent_purple)],foreground=[('selected', co_texto_claro)])

    # Remover bordas da área da árvore
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    # Estilo do DateEntry (Calendário)
    style.configure('TCalendar',background=co_frame,foreground=co_texto_claro,fieldbackground=co_frame,selectbackground=co_accent_purple,selectforeground=co_texto_claro,headersbackground=co_frame,headersforeground=co_texto_escuro)


    # criando frames para divisão de tela (usando CTkFrame)
    frameCima = ctk.CTkFrame(janela, height=50, fg_color=co_frame, corner_radius=0)
    frameCima.grid(row=0, column=0, sticky="new") # Mudado para "new" para não expandir verticalmente

    frameTitulo = ctk.CTkFrame(janela, height=150, fg_color=co_janela, corner_radius=0)
    frameTitulo.grid(row=1, column=0, sticky="new")

    frameMeio = ctk.CTkFrame(janela, fg_color=co_janela, corner_radius=0)
    frameMeio.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")
    frameMeio.grid_columnconfigure(0, weight=2, minsize=200) # Porcentagem
    frameMeio.grid_columnconfigure(1, weight=3, minsize=300) # Gráfico de Barras
    frameMeio.grid_columnconfigure(2, weight=3, minsize=300) # Resumo
    frameMeio.grid_columnconfigure(3, weight=4, minsize=450) # Gráfico de Pizza
    frameMeio.grid_rowconfigure(0, weight=1)

    frameBaixo = ctk.CTkFrame(janela, fg_color=co_janela, corner_radius=0)
    frameBaixo.grid(row=3, column=0, pady=10, padx=20, sticky="sew") # Fica na parte de baixo
    frameBaixo.grid_columnconfigure(0, weight=1)
    frameBaixo.grid_columnconfigure(1, weight=1)
    frameBaixo.grid_columnconfigure(2, weight=1)

    frameRodape = ctk.CTkFrame(janela, height=30, fg_color=co_janela, corner_radius=0)
    frameRodape.grid(row=4, column=0, pady=(0, 5), padx=20, sticky="sew")


    # --- trabalhando no frame Cima e Titulo ---

    # acessando a imagem com CTkImage
    try:
        app_img_pil = Image.open('logo_MCF.png')
        app_img = ctk.CTkImage(app_img_pil, size=(55, 55))
        app_logo = ctk.CTkLabel(frameCima, image=app_img, text=" Orçamento pessoal", compound=LEFT, padx=10, font=('Verdana', 20, 'bold'), text_color=co_texto_claro, fg_color="transparent")
        app_logo.pack(side=LEFT, fill=X, expand=True, padx=20)
    except FileNotFoundError:
        app_logo = ctk.CTkLabel(frameCima, text=" My Cash Flow - Orçamento pessoal", compound=LEFT, padx=10, font=('Verdana', 20, 'bold'), text_color=co_texto_claro, fg_color="transparent")
        app_logo.pack(side=LEFT, fill=X, expand=True, padx=20)


    app_titulo = ctk.CTkLabel(frameTitulo, text="My Cash Flow", font=('Verdana', 30, 'bold'), text_color=co_accent_green, fg_color="transparent")
    app_titulo.place(relx=0.5, y=30, anchor=N)

    app_descricao = ctk.CTkLabel(frameTitulo, text="O seu aplicativo de gerenciamento de dinheiro", font=('Verdana', 14, 'bold'), text_color=co_texto_escuro, fg_color="transparent")
    app_descricao.place(relx=0.5, y=80, anchor=N)


    # definindo tree como global
    global tree

    # --- Funções de Botões (Callbacks) ---

    def inserir_categoria_b():
        nome = e_categoria.get()
        if nome == '':
            messagebox.showerror('Erro', 'Preencha o nome da categoria')
            return
        
        inserir_categoria([nome])
        messagebox.showinfo('Sucesso', 'Categoria inserida com sucesso')
        e_categoria.delete(0, 'end')

        # atualizando a lista de categorias
        categorias_funcao = ver_categoria()
        categoria = [i[1] for i in categorias_funcao]
        combo_categoria_despesas.configure(values=categoria)
        combo_categoria_despesas.set('') # Limpa a seleção

    def inserir_receita_b():
        data = e_cal_receitas.get()
        quantia = e_valor_receitas.get()

        if data == '' or quantia == '':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
        
        lista_inserir = ['Receita', data, quantia]
        inserir_receitas(lista_inserir)
        messagebox.showinfo('Sucesso', 'Receita inserida com sucesso')

        e_cal_receitas.set_date(date.today())
        e_valor_receitas.delete(0, 'end')

        # atualizando dados
        atualizar_dashboard()

    def inserir_despesas_b():
        nome = combo_categoria_despesas.get()
        data = e_cal_despesas.get()
        quantia = e_valor_despesas.get()

        if nome == '' or data == '' or quantia == '':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
        
        lista_inserir = [nome, data, quantia]
        inserir_gastos(lista_inserir)
        messagebox.showinfo('Sucesso', 'Despesa inserida com sucesso')
        
        combo_categoria_despesas.set('')
        e_cal_despesas.set_date(date.today())
        e_valor_despesas.delete(0, 'end')

        # atualizando dados
        atualizar_dashboard()

    def deletar_dados():
        try:
            treev_dados = tree.focus()
            treev_dicionario = tree.item(treev_dados)
            treev_lista = treev_dicionario['values']
            valor = treev_lista[0] # ID
            nome = treev_lista[1] # Categoria

            if nome == 'Receita':
                deletar_receitas([valor])
            else:
                deletar_gastos([valor])
                
            messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso')
            
            # atualizando dados
            atualizar_dashboard()

        except IndexError:
            messagebox.showerror('Erro', 'Selecione um dos dados na tabela')

    # --- Funções de Atualização do Dashboard ---

    def atualizar_dashboard():
        """Função central para atualizar todos os elementos visuais."""
        mostrar_renda()
        porcentagem()
        grafico_bar()
        resumo()
        grafico_pie()

    # porcentagem---------------------------------------
    def porcentagem():
        # frame para agrupar os widgets de porcentagem ---
        frame_porc = ctk.CTkFrame(frameMeio, fg_color=co_frame, corner_radius=10)
        frame_porc.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        frame_porc.pack_propagate(False) # Impede que os widgets filhos redimensionem o frame

        l_nome = ctk.CTkLabel(frame_porc, text="Receita Restante", anchor="center", font=('Verdana', 14), text_color=co_texto_escuro)
        l_nome.pack(pady=(20, 5), fill=X, padx=10)
        
        valor_p = porcentagem_valor()[0]
        
        # Normaliza o valor para o range 0.0 - 1.0
        valor_normalizado = valor_p / 100.0

        bar = ctk.CTkProgressBar(frame_porc, height=25, corner_radius=10,fg_color=co_widget,progress_color="#FDE74C")
        bar.pack(pady=10, fill=X, padx=30, expand=True)
        bar.set(valor_normalizado)
        
        l_porcentagem = ctk.CTkLabel(frame_porc, text=f"{valor_p:,.2f}%", anchor="center", font=('Verdana', 24, 'bold'), text_color=co_texto_claro)
        l_porcentagem.pack(pady=(5, 20), fill=X, padx=10)


    # Frame para o gráfico de barras (criado globalmente)
    frame_gra_bar = ctk.CTkFrame(frameMeio, fg_color=co_frame, corner_radius=10)
    frame_gra_bar.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # funcao para grafico bar----------------------
    def grafico_bar():
        # Limpa gráficos antigos
        for widget in frame_gra_bar.winfo_children():
            widget.destroy()

        lista_categorias = ['Renda', 'Despesas', 'Saldo']
        lista_valores = bar_valores()

        figura = plt.Figure(figsize=(4, 3.45), dpi=60)
        ax = figura.add_subplot(111)
        figura.patch.set_facecolor(co_frame) # Fundo da figura
        ax.set_facecolor(co_frame) # Fundo do eixo

        # barras
        ax.bar(lista_categorias, lista_valores, color=chart_colors, width=0.9)

        # adiciona rótulos em cima das barras
        for i, valor in enumerate(lista_valores):
            ax.text(i, valor + 0.5, f"{valor:,.0f}", fontsize=14, fontstyle='italic',verticalalignment='bottom', color=co_texto_escuro, horizontalalignment='center')

        # define as posições e os rótulos
        ax.set_xticks(range(len(lista_categorias)))
        ax.set_xticklabels(lista_categorias, fontsize=16, color=co_texto_claro)

        # aparência do gráfico
        for lado in ['top', 'right']:
            ax.spines[lado].set_visible(False)
        for lado in ['left', 'bottom']:
            ax.spines[lado].set_color(co_widget)
            ax.spines[lado].set_linewidth(1)

        # Remove ticks e valores do eixo Y
        ax.tick_params(bottom=False, left=False, labelleft=False)
        ax.set_axisbelow(True)

        # grid
        ax.yaxis.grid(True, color=co_widget, linestyle='-', linewidth=0.7)
        ax.xaxis.grid(False)

        canva = FigureCanvasTkAgg(figura, frame_gra_bar)
        canva.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        canva.draw()


    # funcao de resumo total----------------------
    def resumo():
        valor = bar_valores()
        
        # frame para agrupar os widgets de resumo ---
        frame_res = ctk.CTkFrame(frameMeio, fg_color=co_frame, corner_radius=10)
        frame_res.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        frame_res.pack_propagate(False)

        # --- Renda ---
        l_sumario_renda = ctk.CTkLabel(frame_res, text="Total Renda Mensal".upper(), anchor="w", text_color=co_texto_escuro, font=('Verdana', 14))
        l_sumario_renda.pack(pady=(20, 0), fill=X, padx=20)
        l_valor_renda = ctk.CTkLabel(frame_res, text=f"R$ {valor[0]:,.2f}", anchor="w", text_color=co_texto_claro, font=('Ivy', 22, 'bold'))
        l_valor_renda.pack(pady=(0, 10), fill=X, padx=20)
        ctk.CTkFrame(frame_res, height=2, fg_color=co_widget).pack(fill=X, padx=20, pady=5)
        
        # --- Despesas ---
        l_sumario_desp = ctk.CTkLabel(frame_res, text="Total Despesas Mensais".upper(), anchor="w", text_color=co_texto_escuro, font=('Verdana', 14))
        l_sumario_desp.pack(pady=(10, 0), fill=X, padx=20)
        l_valor_desp = ctk.CTkLabel(frame_res, text=f"R$ {valor[1]:,.2f}", anchor="w", text_color=co_texto_claro, font=('Ivy', 22, 'bold'))
        l_valor_desp.pack(pady=(0, 10), fill=X, padx=20)
        ctk.CTkFrame(frame_res, height=2, fg_color=co_widget).pack(fill=X, padx=20, pady=5)

        # --- Saldo ---
        l_sumario_saldo = ctk.CTkLabel(frame_res, text="Total Saldo da Caixa".upper(), anchor="w", text_color=co_texto_escuro, font=('Verdana', 14))
        l_sumario_saldo.pack(pady=(10, 0), fill=X, padx=20)
        l_valor_saldo = ctk.CTkLabel(frame_res, text=f"R$ {valor[2]:,.2f}", anchor="w", text_color=co_accent_green if valor[2] >= 0 else co_accent_orange, font=('Ivy', 22, 'bold'))
        l_valor_saldo.pack(pady=(0, 20), fill=X, padx=20)


    # Frame para o gráfico de pizza (definido globalmente)
    frame_gra_pie = ctk.CTkFrame(frameMeio, fg_color=co_frame, corner_radius=10)
    frame_gra_pie.grid(row=0, column=3, sticky="nsew", padx=10, pady=10)

    def grafico_pie():
        # limpa gráficos antigos antes de desenhar
        for widget in frame_gra_pie.winfo_children():
            widget.destroy()

        figura = plt.Figure(figsize=(5, 3.5), dpi=100)
        ax = figura.add_subplot(111)
        figura.patch.set_facecolor(co_frame)
        ax.set_facecolor(co_frame)

        lista_categorias, lista_valores = pie_valores()

        if not lista_valores: # Se não houver dados, exibe mensagem
            ctk.CTkLabel(frame_gra_pie, text="Sem dados de despesa para exibir",font=('Verdana', 14), text_color=co_texto_escuro).pack(expand=True)
            return

        explode = [0.05 for _ in lista_categorias]

        wedges, texts, autotexts = ax.pie(lista_valores,explode=explode,wedgeprops=dict(width=0.40, edgecolor=co_frame),autopct='%1.1f%%',pctdistance=0.8,textprops={'color': co_texto_claro, 'fontsize': 11, 'fontweight': 'bold'},colors=chart_colors_pie,shadow=False,startangle=90)

        # título do gráfico
        ax.set_title("Distribuição de Despesas", fontsize=14, fontweight='bold', color=co_texto_claro, pad=20)

        # legenda
        leg = ax.legend(lista_categorias,title="Categorias",title_fontsize=11,fontsize=10,loc="center left",bbox_to_anchor=(1, 0.5),labelcolor=co_texto_claro,frameon=False)

        # mexendo na legenda
        leg.get_title().set_color(co_texto_claro) # <-- Use a cor que desejar aqui

        # adiciona o gráfico ao frame CustomTkinter
        canva_categoria = FigureCanvasTkAgg(figura, frame_gra_pie)
        canva_categoria.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        canva_categoria.draw()

    # --- Rodapé ---
    app_creditos = ctk.CTkLabel(frameRodape, text="Criado por: Gustavo Santos, Leonardo Pavão, Lucas Ramos, Maicon Amelio",font=('Verdana', 10, 'bold'), text_color=co_texto_escuro, fg_color="transparent")
    app_creditos.pack(side=BOTTOM, fill=X, pady=(0, 5))


    # --- Chamada inicial do Dashboard ---
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pie()


    # --- Criando frames dentro do Frame Baixo ---

    frame_operacoes = ctk.CTkFrame(frameBaixo, fg_color=co_frame, corner_radius=10)
    frame_operacoes.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    frame_renda = ctk.CTkFrame(frameBaixo, fg_color=co_frame, corner_radius=10)
    frame_renda.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    frame_configuracao = ctk.CTkFrame(frameBaixo, fg_color=co_frame, corner_radius=10)
    frame_configuracao.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")


    # --- Conteúdo do Frame Renda (Tabela) ---
    def mostrar_renda():
        # Limpa a tabela antiga antes de recriar
        for widget in frame_renda.winfo_children():
            widget.destroy()

        app_tabela = ctk.CTkLabel(frame_renda, text="Tabela Receitas e Despesas", anchor="w",font=('Verdana', 14, 'bold'), text_color=co_texto_escuro)
        app_tabela.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(10, 5), padx=10)

        tabela_head = ['#Id', 'Categoria', 'Data', 'Quantia']
        lista_itens = tabela()
        
        global tree
        tree = ttk.Treeview(frame_renda, selectmode="extended", columns=tabela_head, show="headings", style="Treeview")
        
        # Scrollbars (usando CTkScrollbar)
        vsb = ctk.CTkScrollbar(frame_renda, command=tree.yview, button_color=co_accent_purple, button_hover_color=co_accent_blue)
        hsb = ctk.CTkScrollbar(frame_renda, orientation="horizontal", command=tree.xview, button_color=co_accent_purple, button_hover_color=co_accent_blue)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(column=0, row=1, sticky='nsew', padx=(10, 0))
        vsb.grid(column=1, row=1, sticky='ns', padx=(0, 10))
        hsb.grid(column=0, row=2, sticky='ew', padx=10, pady=(0, 10))
        
        frame_renda.grid_rowconfigure(1, weight=1)
        frame_renda.grid_columnconfigure(0, weight=1)

        hd = ["center", "center", "center", "center"]
        h = [40, 130, 100, 100]
        n = 0

        for col in tabela_head:
            tree.heading(col, text=col.title(), anchor=CENTER)
            tree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in lista_itens:
            tree.insert('', 'end', values=item)

    mostrar_renda() # Chamada inicial da tabela


    # --- Conteúdo do Frame Operações (Despesas) ---
    l_info = ctk.CTkLabel(frame_operacoes, text='Insira novas despesas', height=1, anchor="w",font=('Verdana', 14, 'bold'), text_color=co_texto_claro)
    l_info.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 10))

    # Categoria
    l_categoria = ctk.CTkLabel(frame_operacoes, text='Categoria', height=1, anchor="w",font=('Ivy', 12), text_color=co_texto_escuro)
    l_categoria.grid(row=1, column=0, sticky="w", padx=10, pady=5)

    # Pegando categorias
    categoria_funcao = ver_categoria()
    categoria = [i[1] for i in categoria_funcao]

    combo_categoria_despesas = ctk.CTkComboBox(frame_operacoes, values=categoria,font=('Ivy', 10),fg_color=co_widget,border_color=co_widget,button_color=co_accent_purple,dropdown_fg_color=co_frame,state='readonly')
    combo_categoria_despesas.set('') # Inicia vazio
    combo_categoria_despesas.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

    # Despesas Data
    l_cal_despesas = ctk.CTkLabel(frame_operacoes, text='Data', height=1, anchor="w",font=('Ivy', 12), text_color=co_texto_escuro)
    l_cal_despesas.grid(row=2, column=0, sticky="w", padx=10, pady=5)
    e_cal_despesas = DateEntry(frame_operacoes, width=12, background=co_accent_purple, foreground=co_texto_claro, borderwidth=0, year=2025,date_pattern='dd/mm/yyyy')
    e_cal_despesas.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

    # Valor
    l_valor_despesas = ctk.CTkLabel(frame_operacoes, text='Quantia Total', height=1, anchor="w",font=('Ivy', 12), text_color=co_texto_escuro)
    l_valor_despesas.grid(row=3, column=0, sticky="w", padx=10, pady=5)
    e_valor_despesas = ctk.CTkEntry(frame_operacoes, width=14, justify='left',fg_color=co_widget, border_color=co_widget)
    e_valor_despesas.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

    # Botao Inserir Despesa
    try:
        img_add_pil = Image.open('add.png')
        img_add = ctk.CTkImage(img_add_pil, size=(17, 17))
    except FileNotFoundError:
        img_add = None

    # Botao Inserir Categoria


    botao_inserir_despesas = ctk.CTkButton(frame_operacoes, command=inserir_despesas_b,image=img_add, text="Adicionar".upper(),compound=LEFT, font=('Ivy', 9, 'bold'),fg_color=co_accent_green, hover_color="#3E8E6B",text_color=co_texto_claro)
    botao_inserir_despesas.grid(row=4, column=1, sticky="w", padx=10, pady=10)

    # Botao Excluir
    l_excluir = ctk.CTkLabel(frame_operacoes, text='Excluir ação', height=1, anchor="w",font=('Ivy', 12, 'bold'), text_color=co_texto_claro)
    l_excluir.grid(row=5, column=0, sticky="w", padx=10, pady=(20, 5))

    try:
        img_delete_pil = Image.open('lixo.png')
        img_delete = ctk.CTkImage(img_delete_pil, size=(17, 17))
    except FileNotFoundError:
        img_delete = None

    botao_deletar = ctk.CTkButton(frame_operacoes, command=deletar_dados,image=img_delete, text="Deletar".upper(),compound=LEFT, font=('Ivy', 9, 'bold'),fg_color=co_accent_orange, hover_color="#B35229",text_color=co_texto_claro)
    botao_deletar.grid(row=5, column=1, sticky="w", padx=10, pady=(20, 5))

    frame_operacoes.grid_columnconfigure(1, weight=1) # Coluna 1 (dos campos) expande


    # --- Conteúdo do Frame Configuração (Receitas e Categorias) ---
    l_info_conf = ctk.CTkLabel(frame_configuracao, text='Insira novas receitas', height=1, anchor="w",font=('Verdana', 14, 'bold'), text_color=co_texto_claro)
    l_info_conf.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

    # Calendario Receitas
    l_cal_receitas = ctk.CTkLabel(frame_configuracao, text='Data', height=1, anchor="w",font=('Ivy', 12), text_color=co_texto_escuro)
    l_cal_receitas.grid(row=1, column=0, sticky="w", padx=10, pady=5)
    e_cal_receitas = DateEntry(frame_configuracao, width=12, background=co_accent_purple,foreground=co_texto_claro, borderwidth=0, year=2025,date_pattern='dd/mm/yyyy')
    e_cal_receitas.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

    # Valor Receitas
    l_valor_receitas = ctk.CTkLabel(frame_configuracao, text='Quantia Total', height=1, anchor="w",font=('Ivy', 12), text_color=co_texto_escuro)
    l_valor_receitas.grid(row=2, column=0, sticky="w", padx=10, pady=5)
    e_valor_receitas = ctk.CTkEntry(frame_configuracao, width=14, justify='left',fg_color=co_widget, border_color=co_widget)
    e_valor_receitas.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

    # Botao Inserir Receita
    botao_inserir_receitas = ctk.CTkButton(frame_configuracao, command=inserir_receita_b,image=img_add, text="Adicionar".upper(),compound=LEFT, font=('Ivy', 9, 'bold'),fg_color=co_accent_green, hover_color="#3E8E6B",text_color=co_texto_claro)
    botao_inserir_receitas.grid(row=3, column=1, sticky="w", padx=10, pady=10)

    # Linha divisória
    ctk.CTkFrame(frame_configuracao, height=2, fg_color=co_widget).grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

    # Operacao Nova Categoria
    l_info_cat = ctk.CTkLabel(
    frame_configuracao, text='Nova Categoria', height=1, anchor="w",font=('Ivy', 14, 'bold'), text_color=co_texto_claro)
    l_info_cat.grid(row=5, column=0, sticky="w", padx=10, pady=(10, 5))
    e_categoria = ctk.CTkEntry(frame_configuracao, width=14, justify='left',fg_color=co_widget, border_color=co_widget)
    e_categoria.grid(row=5, column=1, sticky="ew", padx=10, pady=(10, 5))

    # Botao Inserir Categoria
    botao_inserir_categoria = ctk.CTkButton(frame_configuracao, command=inserir_categoria_b,image=img_add, text="Adicionar".upper(),compound=LEFT, font=('Ivy', 9, 'bold'),fg_color=co_accent_blue, hover_color="#41688A",text_color=co_texto_claro)
    botao_inserir_categoria.grid(row=6, column=1, sticky="w", padx=10, pady=10)

    frame_configuracao.grid_columnconfigure(1, weight=1) # Coluna 1 (dos campos) expande


    janela.mainloop()

if __name__ == "__main__":
    iniciar_dashboard