

Dashboard dinâmico com verificação de login web 

📄 Descrição:

Nosso projeto cria uma interface visual de dashboard para o gerenciamento financeiro de gastos mensais. 
Ele ajuda pessoas que não tem grande domínio de demais ferramentas de criação de dashboards e traz uma perspectiva visual fácil de ser coompreendida pelo usuário.
Qualquer pessoa pode usufruir do nosso projeto como maneira simples de gerir seu dinheiro
O obejetivo principal do projeto é dar o poder das ferramentas de dashboard para aqueles que não tem tempo de estudar e aprender a mexer nelas

🚀 Funcionalidades:

Funcionalidades do Servidor Flask
  Autenticação de Usuário
  Login seguro usando SQLite.
  Verificação de credenciais com mensagem de erro clara.
  Bloqueio de tela até que o login seja autenticado (via threading.Event).
  
 Sistema de Cadastro
  Criação de novos usuários com:
  Validação de campos vazios
  Validação de tamanho mínimo
  Verificação de senha e confirmação
  Registro automático no SQLite.
  
 Interface Web Integrada
  Páginas HTML renderizadas com Flask (index, cadastro)
  Respostas AJAX em JSON
  Abre o navegador automaticamente
  Servidor Embutido
  Servidor Flask executado em thread paralela
  Inicialização automática do Dashboard após login bem-sucedido
  
 Gerenciamento de Banco SQLite
  Conexão persistente
  Criação automática da tabela Usuarios
  Fechamento seguro da conexão
  Controle de Eventos
  Uso de LOGIN_SUCCESS_EVENT para sincronizar o fluxo
  Loop aguardando autenticação para iniciar o Dashboard
  
Funcionalidades do Dashboard
   Gerenciamento Financeiro Completo
    Registrar categorias
    Registrar receitas
    Registrar despesas
    Excluir registros existentes

  Dashboard Analítico
    Gráficos
    Gráfico de barras: Renda / Despesas / Saldo
    Gráfico de pizza: distribuição de gastos
    Barra de progresso indicando “Receita restante”
    Resumos
    Total de renda mensal
    Total de despesas
    Saldo do caixa

 Ferramentas Visuais
  Calendário para escolher datas (tkcalendar)
  Tema dark elegante (customtkinter)
  Paleta de cores personalizada

 Interface Moderna
  Layout responsivo com grid
  Frames organizados (topo, título, meio, rodapé)
  TreeView estilizado para listagem de dados

 Integração com o Módulo View
  As funções críticas de backend são automaticamente chamadas:
  Atualizações em tempo real após inserir ou deletar
  Chamadas aos gráficos e tabelas após qualquer alteração

 Tratamento de Erros
  Verificação do arquivo view.py
  Mensagens de erro claras com messagebox


🔧Tecnologias Utilizadas:
Linguagem de Programação: Python
Frameworks / Bibliotecas:
Flask 
Pandas 
Requests 

Ferramentas de Desenvolvimento:

Git & GitHub

VS Code 

Gerenciamento de Pacotes:

pip

venv (ambiente virtual)

Banco de Dados:

SQLite / PostgreSQL / MySQL (dependendo do que seu projeto usa)

Testes:

PyTest / unittest / VS Code



▶️ Como Executar o Projeto
Pré-requisitos
Antes de iniciar, verifique se você possui instalado:
Python 3.10+
Pip (gerenciador de pacotes do Python)
Git
Ambiente virtual (venv)
As dependências que constam no requirements.txt


🛠 Passo a passo
# Clone o repositório
git clone https://github.com/seuuser/seuprojeto.git

# Acesse a pasta do projeto
cd seuprojeto

# (Opcional) Crie o ambiente virtual
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute o projeto
python launcher.py

Forma rápida (modo desenvolvedor)
Se estiver usando um editor como VS Code ou PyCharm:
Basta abrir o projeto e clicar em Run no arquivo launcher.py.


⚙️ Configurações / Variáveis de Ambiente

1. Servidor Flask – Login e Cadastro
FLASK_PORT (opcional)	Porta usada pelo servidor Flask — padrão: 5000
DATABASE_PATH	Caminho do banco Cadastro_de_usuarios.db (embutido no código, mas pode ser variabilizado)
TEMPLATES_PATH	Caminho da pasta /templates usada pelo Flask
PYTHONPATH	Deve incluir o diretório que contém main.py e o arquivo atual
DEBUG	Debug do Flask (padrão: False)

Dependências Obrigatórias
Python 3.10+
Flask
Requests
SQLite3 (nativo do Python)
Navegador web instalado
Threading (nativo)
Arquivos obrigatórios
index.html (página de login)
cadastro.html (página de cadastro)
main.py contendo a função iniciar_dashboard()

2. Dashboard Tkinter (My Cash Flow)

VIEW_PATH	Caminho para view.py contendo funções de acesso ao banco
ASSETS_PATH	Caminho para logo_MCF.png (opcional, mas recomendado)
MATPLOTLIBBACKEND	Usa TKAgg (automático)
TK_THEME_MODE	Forçado para dark no código

Dependências Obrigatórias
customtkinter
tkinter (nativo)
pillow (PIL)
matplotlib
tkcalendar
SQLite3
Arquivo view.py com funções:
bar_valores()
pie_valores()
porcentagem_valor()
inserir_categoria()
ver_categoria()
inserir_gastos()
inserir_receitas()
deletar_gastos()
deletar_receitas()
tabela()



Autores e links
  Gustavo Santos:
  https://github.com/Gustazx22
  Leonardo Pavão:
  https://github.com/leonardohollp
  Lucas Ramos:
  
  Maicon Amélio:
