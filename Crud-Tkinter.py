"""
Começando um CRUD: INSERIR, LER, EDITAR E EXCLUIR em Python utilizando um banco de dados e interface.
O CRUD SERÁ DE INFORMAÇÕES DE UMA PESSOA.
DEVERÁ RECEBER COMO INFORMAÇÃO: NOME, ALTURA, PESO e TELEFONE .
"""

#teste2
import tkinter as tk
import mysql.connector

# Fazendo a conexão com o banco de dados
host = 'localhost'
database = 'crudpython'
user = 'root'
password = ''

connection = mysql.connector.connect(
    host=host,
    database=database,
    user=user,
    password=password
)

if connection.is_connected():
    print("Conexao bem sucedida!")
else:
    print("Conexao nao estabelecida")

id_professor = None

def interface():
    # Função para chamar a interface do Tkinter
    janela = tk.Tk()
    janela.geometry('500x300')
    janela.title("Gestão de alunos")
    janela.iconbitmap("C:\\Users\kauas\OneDrive\Área de Trabalho\ADS\\favicon.ico")
    tela_login(janela)
    janela.mainloop()


def excluir_tela_anterior(janela):
    # Função para excluir o menu atual para que os itens não fiquem sobrepostos no menu posterior
    for widget in janela.winfo_children():
        widget.grid_forget()


def get_id(nome, senha, tipo):
    global id_professor
    cursor = connection.cursor()
    if tipo == "professor":
        comando = 'SELECT id FROM tab_professor WHERE login = %s AND senha = %s'
    else:
        comando = 'SELECT id FROM tab_pessoas WHERE nome = %s AND senha = %s'

    valores = (nome, senha)
    cursor.execute(comando, valores)
    resultado = cursor.fetchall()
    cursor.close()

    if resultado:
        id_professor = resultado[0][0]
        return resultado[0][0]
    else:
        return None


def tela_login(janela):
    janela.configure(bg='lightgrey')

    label_login = tk.Label(janela, text="Login: ", bg='lightgrey',font=('Consolas', 12, 'bold'),)
    label_login.grid(row=0, column=0, padx=3, pady=3)
    login = tk.Entry(janela)
    login.grid(row=0, column=1, padx=3, pady=3)

    label_senha = tk.Label(janela, text="Senha: ", bg='lightgrey',font=('Consolas', 12, 'bold'))
    label_senha.grid(row=0, column=2, padx=3, pady=3)
    senha = tk.Entry(janela)
    senha.grid(row=0, column=3, padx=3, pady=3)

    escolha_var = tk.StringVar()
    escolha_var.set("aluno")  # Define o valor padrão para "aluno"

    checkbox_professor = tk.Checkbutton(janela, text="Professor", variable=escolha_var, onvalue="professor",
                                        offvalue="aluno", bg='lightgrey',font=('Consolas', 12, 'bold') )
    checkbox_professor.grid(row=1, column=1, padx=0, pady=3)
    botao_login = tk.Button(janela, text="Login", bg='white',font=('Consolas', 12, 'bold'),command=lambda: verificar_login(login, senha, janela, escolha_var))
    botao_login.grid(row=0, column=4, padx=3, pady=3)


def verificar_login(login_entry, senha_entry, janela, tipo):
    login_valor = login_entry.get()
    senha_valor = senha_entry.get()
    tipo_valor = tipo.get()
    if login_valor == "" or senha_valor == "":
        print("Preencha ambos os campos.")
    else:
        id_valor = get_id(login_valor, senha_valor, tipo_valor)
        if id_valor is not None:
            tela_inicio(janela, tipo_valor, id_valor)
        else:
            print("Credenciais inválidas.")


def tela_inicio(janela, usuario, id_valor):
    #Função para separar a tela caso seja um professor ou um aluno
    excluir_tela_anterior(janela)
    if usuario == "professor":
        bot_manter_aluno = tk.Button(janela, text="Manter Aluno", bg='white', font=('consolas', 13, 'bold'),command=lambda: alunos_exibir(janela))
        bot_manter_aluno.grid(row=0, column=0, padx=3, pady=3)
    else:
        bot_exibir_treino = tk.Button(janela, text="Exibir treino", bg='white',font=('consolas', 13, 'bold'),command=lambda: exibir_treino_aluno(janela, id_valor))
        bot_exibir_treino.grid(row=0, column=0, padx=3, pady=3)


def alunos_exibir(janela):
    excluir_tela_anterior(janela)

    linhas = ler_dados(None)

    nomes = tk.Label(janela, text="Alunos", bg='lightgrey', font=('consolas', 15, 'bold'))
    nomes.grid(row=0, column=0, padx=3, pady=3)
    if linhas:
        if hasattr(janela, "aviso"):
            janela.aviso.destroy()
        for i, row in enumerate(linhas):
            nome = tk.Button(janela, text=str(row[1]), bg='white',command=lambda id_valor=row[0], nome=row[1]: tela_aluno(janela, nome, id_valor))
            nome.grid(row=i+1, column=0, padx=3, pady=3)

        novo_aluno = tk.Button(janela, text="Inserir novo aluno",bg='white', command=lambda: tela_incluir(janela))
        novo_aluno.grid(row=i + 2, column=0, padx=3, pady=3)
    else:
        janela.aviso = tk.Label(janela, text="Não há alunos", bg='lightgrey')
        janela.aviso.grid(row=1, column=0, padx=3, pady=3)
        novo_aluno = tk.Button(janela, text="Inserir novo aluno",bg='white', command=lambda: tela_incluir(janela))
        novo_aluno.grid(row=2, column=0, padx=3, pady=3)


def tela_incluir(janela):
    # função usada para excluir o menu principal e ir para a tela de incluir
    excluir_tela_anterior(janela)

    # Campos para a entrada dos dados: nome, altura, peso e senha
    label_nome = tk.Label(janela, text="Nome: ",bg='lightgrey', font=('consolas', 12, 'bold'))
    label_nome.grid(row=0, column=0, padx=0, pady=10)
    nome = tk.Entry(janela)
    nome.grid(row=0, column=1, padx=0, pady=10)

    label_altura = tk.Label(janela, text="Altura",bg='lightgrey', font=('consolas', 12, 'bold'))
    label_altura.grid(row=1, column=0, padx=0, pady=10)
    altura = tk.Entry(janela)
    altura.grid(row=1, column=1, padx=0, pady=10)

    label_peso = tk.Label(janela, text="Peso",bg='lightgrey', font=('consolas', 12, 'bold'))
    label_peso.grid(row=2, column=0, padx=0, pady=10)
    peso = tk.Entry(janela)
    peso.grid(row=2, column=1, padx=0, pady=10)

    label_senha = tk.Label(janela, text="Senha: ",bg='lightgrey', font=('consolas', 12, 'bold'))
    label_senha.grid(row=3, column=0, padx=0, pady=10)
    senha = tk.Entry(janela)
    senha.grid(row=3, column=1, padx=0, pady=10)

    def dados_de_inserir():
        # Coletando os dados inseridos nos campos nome, altura, peso e telefone
        nome_valor = nome.get().lower()
        altura_valor = altura.get()
        peso_valor = peso.get()
        senha_valor = senha.get()
        # Verificando se os campos foram preenchidos, caso não tenham sido, o menu volta para o início
        if nome_valor == '' or altura_valor == '' or peso_valor == '' or senha_valor == '':
            print("Campos em branco")
            alunos_exibir(janela)
        else:
            # Inserindo os dados no banco de dados
            inserir(nome_valor, altura_valor, peso_valor, senha_valor, id_professor)
            alunos_exibir(janela)

        # Botão voltar e incluir
    voltar = tk.Button(janela, text="VOLTAR",bg='white', font=('consolas', 12, 'bold'), command=lambda: alunos_exibir(janela))
    voltar.grid(row=4, column=1, padx=10, pady=10)
    incluir = tk.Button(janela, text="INCLUIR",bg='white', font=('consolas', 12, 'bold'), command=dados_de_inserir)
    incluir.grid(row=4, column=0, padx=10, pady=10)


def tela_aluno(janela, aluno_escolhido, id_valor):
    excluir_tela_anterior(janela)

    nome_escolhido = tk.Label(janela, text=aluno_escolhido, bg='lightgrey', font=('consolas', 14, 'bold'))
    nome_escolhido.grid(row=0, column=0, padx=3, pady=3)
    informacoes = tk.Button(janela, text="Informações do aluno",bg='white', command=lambda: informacoes_aluno(janela ,aluno_escolhido, id_valor))
    informacoes.grid(row=1, column=0, padx=3, pady=3)
    atualizar = tk.Button(janela, text="Atualizar dados", bg='white', command=lambda: tela_editar(janela, aluno_escolhido, id_valor))
    atualizar.grid(row=2, column=0, padx=3, pady=3)
    excluir = tk.Button(janela, text="Excluir aluno",bg='white', command=lambda: tela_excluir(janela, aluno_escolhido, id_valor))
    excluir.grid(row=3, column=0, padx=3, pady=3)
    botao_voltar = tk.Button(janela, text="VOLTAR", bg='white', command=lambda: alunos_exibir(janela))
    botao_voltar.grid(row=5, column=0, padx=3, pady=3)
    botao_treino = tk.Button(janela, text="Manter treino",bg='white', command=lambda: manter_treino(janela, aluno_escolhido, id_valor))
    botao_treino.grid(row=6, column=0, padx=3, pady=3)


def informacoes_aluno(janela, nome, id_valor):
    # função usada para excluir o menu principal e ir para a tela de leitura de dados
    excluir_tela_anterior(janela)

    # 'linhas' recebe o retorno de "lerDados()" que retorna todas as linhas do banco de dados
    linhas = ler_dados(nome)
    nome_aluno = nome
    # Imprimindo as linhas
    if linhas:
        linha = linhas[0]
        nome = tk.Label(janela, text="nome: " + str(linha[1]),bg='lightgrey', font=('consolas', 12, 'bold'))
        nome.grid(row=0, column=0, padx=3, pady=3)
        altura = tk.Label(janela, text="altura: " + str(linha[2]),bg='lightgrey', font=('consolas', 12, 'bold'))
        altura.grid(row=0, column=1, padx=3, pady=3)
        peso = tk.Label(janela, text="Peso: " + str(linha[3]),bg='lightgrey', font=('consolas', 12, 'bold'))
        peso.grid(row=0, column=2, padx=3, pady=3)
        telefone = tk.Label(janela, text="senha: " + str(linha[4]),bg='lightgrey', font=('consolas', 12, 'bold'))
        telefone.grid(row=0, column=3, padx=3, pady=3)
    else:
        vazio = tk.Label(janela, text="Nenhum aluno cadastrado",bg='lightgrey', font=('consolas', 12, 'bold'))
        vazio.grid(row=0,column=0, padx=3, pady=3)

    voltar = tk.Button(janela, text="Voltar",bg='white', font=('consolas', 12, 'bold'), command=lambda: tela_aluno(janela, nome_aluno, id_valor))
    voltar.grid(row=1, column=0, padx=3, pady=3)


def tela_editar(janela, aluno_escolhido, id_valor):
    # Funcao para excluir a tela principal e ir para o editar
    excluir_tela_anterior(janela)

    label_novo_valor = tk.Label(janela, text="Novo valor: ",bg='lightgrey', font=('consolas', 12, 'bold'))
    label_novo_valor.grid(row=2, column=0)
    novo_valor = tk.Entry(janela)
    novo_valor.grid(row=2, column=1)

    label_novo_coluna = tk.Label(janela, text="O que deseja alterar\n"
                                              "(Nome, senha, peso ou altura): ",bg='lightgrey', font=('consolas', 12, 'bold'))
    label_novo_coluna.grid(row=3, column=0)
    coluna_alterar = tk.Entry(janela)
    coluna_alterar.grid(row=3, column=1)

    def dados_alterar():
        valor_alterar = novo_valor.get()
        valor_coluna = coluna_alterar.get().lower()

        # Verificando se os campos foram preenchidos, caso não tenham sido, o menu volta para o início
        if aluno_escolhido == '' or valor_alterar == '' or valor_coluna == '':
            print("Campos em branco")
            tela_aluno(janela, aluno_escolhido, id_valor)
        else:
            # Editando os dados no banco de dados
            editar(valor_coluna, aluno_escolhido, valor_alterar)
            if valor_coluna == "nome":
                tela_aluno(janela, valor_alterar, id_valor)
            else:
                tela_aluno(janela, aluno_escolhido, id_valor)

    botao_editar = tk.Button(janela, text="Editar", command=dados_alterar,bg='white', font=('consolas', 12, 'bold'))
    botao_editar.grid(row=5, column=0)
    botao_voltar = tk.Button(janela, text="Voltar",bg='white', font=('consolas', 12, 'bold'),command=lambda: tela_aluno(janela, aluno_escolhido, id_valor))
    botao_voltar.grid(row=5, column=1)


def tela_excluir(janela, aluno_escolhido, id_valor):
    # função usada para excluir o menu principal e ir para a tela de excluir
    excluir_tela_anterior(janela)

    nome_exibir = tk.StringVar()
    nome_exibir.set(aluno_escolhido)

    label_excluir = tk.Label(janela, text="Nome a ser excluído: ",bg='lightgrey', font=('consolas', 12, 'bold'))
    label_excluir.grid(row=0, column=0, padx=0, pady=0)
    nome_excluir = tk.Label(janela, textvariable=nome_exibir, relief="solid",bg='white', font=('consolas', 15, 'bold'))
    nome_excluir.grid(row=0, column=1, padx=0, pady=10)

    # Função utilizada para coletar o nome da pessoa que será excluída
    def individuo_apagar():
        # Chamada da função excluir passando o nome que deve ser excluído do banco de dados.
        excluir(id_valor)
        alunos_exibir(janela)

    alerta = tk.Label(janela, text= f"Se realmente deseja excluir {aluno_escolhido},\n clique em EXCLUIR",bg='lightgrey', font=('consolas', 12, 'bold'))
    alerta.grid(row=1, column=0, padx=3,pady=3)
    botao_excluir = tk.Button(janela, text="EXCLUIR", command=individuo_apagar,bg='white', font=('consolas', 12, 'bold'))
    botao_excluir.grid(row=1, column=1, padx=10, pady=10)
    botao_voltar = tk.Button(janela, text="VOLTAR",bg='white', font=('consolas', 12, 'bold'),command=lambda: tela_aluno(janela, aluno_escolhido, id_valor))
    botao_voltar.grid(row=2, column=0, padx=0, pady=5)


def manter_treino(janela, aluno_escolhido, id_valor):
    # função usada para excluir o menu principal e ir para a tela de excluir
    excluir_tela_anterior(janela)

    criar_treino = tk.Button(janela, text="Criar treino",bg='white', font=('consolas', 12, 'bold'),command=lambda: tela_incluir_treino(janela, aluno_escolhido))
    criar_treino.grid(row=0, column=0, padx=3, pady=3)
    exibir_treino = tk.Button(janela, text="Ler treino", bg='white', font=('consolas', 12, 'bold'),command= lambda: ler_treino(janela, aluno_escolhido, id_valor))
    exibir_treino.grid(row=1, column=0, padx=3, pady=3)
    modificar_treino = tk.Button(janela,text="Atualizar treino", bg='white', font=('consolas', 12, 'bold'),command= lambda: atualizar_treino(janela, aluno_escolhido, id_valor))
    modificar_treino.grid(row=2, column=0, padx=3, pady=3)

    excluir_treino = tk.Button(janela, text="Excluir treino", bg='white', font=('consolas', 12, 'bold'),command=lambda: tela_excluir_treino(janela,aluno_escolhido, id_valor))
    excluir_treino.grid(row=3, column=0, padx=3, pady=3)
    botao_voltar = tk.Button(janela, text="Voltar", bg='white', font=('consolas', 12, 'bold'),command=lambda: tela_aluno(janela, aluno_escolhido, id_valor))
    botao_voltar.grid(row=4, column=0, padx=3, pady=3)


""" 

ABAIXO O MANTER TREINO

"""


def tela_incluir_treino(janela, aluno_escolhido):
    excluir_tela_anterior(janela)

    linhas = ler_dados(aluno_escolhido)
    linha = linhas[0]
    id_valor = linha[0]

    label_nome_exercicio = tk.Label(janela, text="Nome exercicio: ",bg='lightgrey', font=('consolas', 12, 'bold'),)
    label_nome_exercicio.grid(row=0, column=0, padx=3, pady=3)
    exercicio = tk.Entry(janela)
    exercicio.grid(row=0, column=1, padx=3, pady=3)
    label_peso = tk.Label(janela, text="Peso: ",bg='lightgrey', font=('consolas', 12, 'bold'))
    label_peso.grid(row=1, column=0, padx=3, pady=3)
    peso = tk.Entry(janela)
    peso.grid(row=1, column=1, padx=3, pady=3)
    label_repeticoes = tk.Label(janela, text="Repetições: ",bg='lightgrey', font=('consolas', 12, 'bold'))
    label_repeticoes.grid(row=2, column=0, padx=3, pady=3)
    repeticoes = tk.Entry(janela)
    repeticoes.grid(row=2, column=1, padx=3, pady=3)

    def recuperar_valores():
        valor_nome = exercicio.get().lower()
        valor_peso = peso.get()
        valor_repeticoes = repeticoes.get().lower()

        if valor_nome == "" or valor_peso == "" or valor_repeticoes == "":
            if hasattr(janela, "aviso"):
                janela.aviso.destroy()
            janela.aviso = tk.Label(janela, text="Algum campo nao foi preenchido")
            janela.aviso.grid(row=4, column=0, padx=5, pady=5)
        else:
            if hasattr(janela, 'aviso'):
                    janela.aviso.destroy()
            inserir_treino(valor_nome, valor_peso, valor_repeticoes, id_valor)
            janela.aviso = tk.Label(janela, text="Inserido com sucesso!")
            janela.aviso.grid(row=4, column=0, padx=5, pady=5)

    bot_incluir = tk.Button(janela, text="Incluir",bg='white', font=('consolas', 12, 'bold'),command=recuperar_valores)
    bot_incluir.grid(row=3, column=0, padx=3, pady=3)
    bot_voltar = tk.Button(janela, text="Voltar",bg='white', font=('consolas', 12, 'bold'),command=lambda: manter_treino(janela, aluno_escolhido, id_valor))
    bot_voltar.grid(row=3, column=1, padx=3, pady=3)


def ler_treino(janela, aluno_escolhido, id_valor):
    excluir_tela_anterior(janela)
    linhas = ler_treino_bd(id_valor)

    i = leitura_bd_treino(janela, linhas)

    bot_voltar = tk.Button(janela, text="VOLTAR",bg='white', font=('consolas', 12, 'bold'), command=lambda: manter_treino(janela, aluno_escolhido, id_valor))
    bot_voltar.grid(row=i+2, column=0, padx=3, pady=3)


def leitura_bd_treino(janela, linhas):
    i = 0
    for i, row in enumerate(linhas):
        linha = linhas[i]
        exercicio = tk.Label(janela, text="Exercicio: "+ str(linha[1]),bg='lightgrey', font=('consolas', 11, 'bold'))
        exercicio.grid(row=i, column=0, padx=0, pady=3)
        peso = tk.Label(janela, text="Peso: "+ str(linha[2]),bg='lightgrey', font=('consolas', 11, 'bold'))
        peso.grid(row=i, column=1, padx=0, pady=3)
        repeticoes = tk.Label(janela, text="Repetições: "+ str(linha[3]),bg='lightgrey', font=('consolas', 11, 'bold'))
        repeticoes.grid(row=i, column=2, padx=0, pady=3)
    return i


def atualizar_treino(janela, aluno_escolhido, id_valor):
    excluir_tela_anterior(janela)

    novo_valor = tk.Label(janela, text="Novo valor: ",bg='lightgrey', font=('consolas', 12, 'bold'))
    novo_valor.grid(row=0, column=0, padx=3, pady=3)
    valor = tk.Entry(janela)
    valor.grid(row=0, column=1, padx=3, pady=3)
    exercicio_alterar = tk.Label(janela, text="Exercicio a ser alterado: ",bg='lightgrey', font=('consolas', 12, 'bold'))
    exercicio_alterar.grid(row=1, column=0, padx=3, pady=3)
    exercicio = tk.Entry(janela)
    exercicio.grid(row=1, column=1, padx=3, pady=3)
    coluna_alterar = tk.Label(janela, text="O que deseja alterar\n(Exercicio, peso ou repetições): ",bg='lightgrey', font=('consolas', 12, 'bold'))
    coluna_alterar.grid(row=2, column=0, padx=3, pady=3)
    alterar = tk.Entry(janela)
    alterar.grid(row=2, column=1, padx=3, pady=3)

    def recuperar_valor():
        new_valor = valor.get().lower()
        exercicio_valor = exercicio.get().lower()
        coluna_valor = alterar.get().lower()
        if new_valor == '' or coluna_valor == '':
            print("hihi esqueceu")
        else:
            editar_treino(coluna_valor, new_valor, id_valor, exercicio_valor)
            manter_treino(janela, aluno_escolhido, id_valor)
            print("alterou")

    bot_editar = tk.Button(janela, text="EDITAR",bg='white', font=('consolas', 12, 'bold'), command=lambda: recuperar_valor())
    bot_editar.grid(row=3, column=0, padx=3, pady=3)
    bot_voltar = tk.Button(janela, text="VOLTAR",bg='white', font=('consolas', 12, 'bold'), command=lambda: manter_treino(janela, aluno_escolhido, id_valor))
    bot_voltar.grid(row=3, column=1, padx=3, pady=3)


def tela_excluir_treino(janela, aluno_escolhido, id_valor):
    excluir_tela_anterior(janela)
    exercicio_a_excluir = tk.Label(janela, text="Exercicio que deseja excluir: ",bg='lightgrey', font=('consolas', 12, 'bold'))
    exercicio_a_excluir.grid(row=0, column=0, padx=3, pady=3)
    exercicio = tk.Entry(janela)
    exercicio.grid(row=0, column=1, padx=3, pady=3)

    def recuperar_valor():
        excluir_valor = exercicio.get().lower()
        if excluir_valor == "":
            print("escreva algo")
        else:
            excluir_treino(excluir_valor, id_valor)
            manter_treino(janela, aluno_escolhido, id_valor)

    bot_excluir = tk.Button(janela, text="Excluir",bg='white', font=('consolas', 12, 'bold'), command=lambda: recuperar_valor())
    bot_excluir.grid(row=1, column=0, padx=3, pady=3)
    bot_voltar = tk.Button(janela, text="Voltar",bg='white', font=('consolas', 12, 'bold'), command=lambda: manter_treino(janela, aluno_escolhido, id_valor))
    bot_voltar.grid(row=1, column=1, padx=3, pady=3)

"""
 TELA ALUNO ABAIXO
"""


def exibir_treino_aluno(janela, id_valor):
    excluir_tela_anterior(janela)
    linhas = ler_treino_bd(id_valor)
    i = leitura_bd_treino(janela, linhas)

    if linhas:
        novo_peso = tk.Label(janela, text="Caso queira alterar a caraga\n entre com o novo peso: ",bg='lightgrey', font=('consolas', 12, 'bold'))
        novo_peso.grid(row=i+1, column=0, padx=3, pady=3)
        entry_peso = tk.Entry(janela)
        entry_peso.grid(row=i+1, column=1, padx=3, pady=3)
        exercicio_alterar = tk.Label(janela, text="Exercicio a ser alterado: ",bg='lightgrey', font=('consolas', 12, 'bold'))
        exercicio_alterar.grid(row=i+3, column=0, padx=3, pady=3)
        exercicio = tk.Entry(janela)
        exercicio.grid(row=i+3, column=1, padx=3, pady=3)
        def recuperar_dados():
            peso_valor = entry_peso.get()
            exercicio_valor = exercicio.get().lower()

            if peso_valor == "" or exercicio_valor == "":
                print("em branco")
            else:
                editar_treino('peso',peso_valor, id_valor, exercicio_valor)
                exibir_treino_aluno(janela, id_valor)
                print("alterado")

        bot_modificar = tk.Button(janela, text="Modificar",bg='white', font=('consolas', 12, 'bold'), command=lambda: recuperar_dados())
        bot_modificar.grid(row=i+4, column=0, padx=3, pady=3)
    else:
        aviso = tk.Label(janela, text="Não há ficha de treino",bg='lightgrey', font=('consolas', 12, 'bold'))
        aviso.grid(row=0, column=0, padx=3, pady=3)
""" 

ABAIXO APENAS COMANDOS PARA CONEXÃO COM O BANCO DE DADOS

"""


def inserir(nome, altura, peso, senha, id_prof):
    # Função para inserir no banco de dados
    cursor = connection.cursor()
    comando = "INSERT INTO tab_pessoas (nome, altura, peso, senha, id_professor) VALUES (%s, %s, %s, %s, %s)"
    values = (nome, altura, peso, senha, id_prof)
    cursor.execute(comando, values)
    connection.commit()
    cursor.close()
    print("Dados inseridos com sucesso")


def inserir_treino(exercicio, peso, repeticoes, fk_pessoa):
    cursor = connection.cursor()
    comando = "INSERT INTO tab_treino (exercicio, peso, repeticoes, fk_pessoa) VALUES (%s, %s, %s, %s)"
    values = (exercicio, peso, repeticoes, fk_pessoa)
    cursor.execute(comando, values)
    connection.commit()
    cursor.close()
    print("Treino inserido")


def ler_dados(nome_escolhido):
    # Função para ler os dados do banco de dados e retornar as linhas
    cursor = connection.cursor()
    if nome_escolhido is None:
        comando = "SELECT * FROM tab_pessoas"
    else:
        comando = f"SELECT * FROM tab_pessoas WHERE nome = '{nome_escolhido}'"

    cursor.execute(comando)
    linhas = cursor.fetchall()
    print(linhas)
    return linhas


def ler_treino_bd(id_valor):
    cursor = connection.cursor()
    comando = f"SELECT * FROM tab_treino WHERE fk_pessoa = '{id_valor}'"
    cursor.execute(comando)
    linhas = cursor.fetchall()
    return linhas


def excluir(id_valor):
    # Função para excluir do banco de dados as informações referentes ao nome recebido por parâmetro
    cursor = connection.cursor()
    verificar_treino = f"SELECT id FROM tab_treino WHERE fk_pessoa = {id_valor}"
    cursor.execute(verificar_treino)
    result = cursor.fetchall()
    if result:
        comando = f"DELETE FROM tab_treino WHERE fk_pessoa = {id_valor}"
        cursor.execute(comando)

    comando = f"DELETE FROM tab_pessoas WHERE id = {id_valor}"
    cursor.execute(comando)
    connection.commit()
    print("Dado excluído")


def excluir_treino(exercicio, id_valor):
    cursor = connection.cursor()
    comando = "DELETE from tab_treino WHERE exercicio = %s AND fk_pessoa = %s"
    valores = (exercicio, id_valor)
    cursor.execute(comando, valores)
    connection.commit()
    cursor.close()
    print("excluido")

def editar(coluna, nome_pessoa, novo_valor):
    cursor = connection.cursor()
    comando = f"UPDATE tab_pessoas SET {coluna} = %s WHERE nome = %s"
    valores = (novo_valor, nome_pessoa)
    cursor.execute(comando,valores)
    connection.commit()
    cursor.close()
    print("Editado com sucesso!")


def editar_treino(coluna, novo_valor, id_valor, exercicio):
    cursor = connection.cursor()
    comando = f"UPDATE tab_treino SET {coluna} = %s WHERE fk_pessoa = %s AND exercicio = %s"
    valores = (novo_valor, id_valor, exercicio)
    cursor.execute(comando, valores)
    connection.commit()
    cursor.close()


if __name__ == "__main__":
    # tabela
    interface()

# chamando banco de dados
