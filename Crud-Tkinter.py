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


def interface():
    # Função para chamar a interface do Tkinter
    janela = tk.Tk()
    janela.geometry('400x300')
    janela.title("Crud")

    #tela_login(janela)
    tela_inicio(janela, "professor")

    janela.mainloop()


def excluir_tela_anterior(janela):
    # Função para excluir o menu atual para que os itens não fiquem sobrepostos no menu posterior
    for widget in janela.winfo_children():
        widget.grid_forget()


def tela_login(janela):
    label_login = tk.Label(janela, text="Login: ")
    label_login.grid(row=0, column=0, padx=3, pady=3)
    login = tk.Entry(janela)
    login.grid(row=0, column=1, padx=3, pady=3)

    label_senha = tk.Label(janela, text="Senha: ")
    label_senha.grid(row=0, column=2, padx=3, pady=3)
    senha = tk.Entry(janela)
    senha.grid(row=0, column=3, padx=3, pady=3)

    botao_login = tk.Button(janela, text="Login", command=lambda: verificar_login(login, senha, janela))
    botao_login.grid(row=0, column=4, padx=3, pady=3)


def verificar_login(login, senha, janela):
    if login.get() == "professor" and senha.get() == "123":
        tela_inicio(janela, "professor")
    elif login.get() == "aluno" and senha.get() == "000":
        tela_inicio(janela, "aluno")


def tela_inicio(janela, usuario):
    excluir_tela_anterior(janela)
    # Tela principal onde se encontra o "Incluir, Leitura, Editar e Excluir"
    if usuario == "professor":
        bot_manter_aluno = tk.Button(janela, text="Manter Aluno", command=lambda: alunos_exibir(janela))
        bot_manter_aluno.grid(row=0, column=0, padx=3, pady=3)

    else:
        bot_exibir_treino = tk.Button(janela, text="Exibir treino")
        bot_exibir_treino.grid(row=0, column=0, padx=3, pady=3)


def alunos_exibir(janela):
    excluir_tela_anterior(janela)

    linhas = ler_dados(None)

    nomes = tk.Label(janela, text="Alunos")
    nomes.grid(row=0, column=0, padx=3, pady=3)

    for i, row in enumerate(linhas):
        nome = tk.Button(janela, text=str(row[0]), command=lambda nome=row[0]: tela_aluno(janela, nome))
        nome.grid(row=i, column=0, padx=3, pady=3)

    novo_aluno = tk.Button(janela, text="Inserir novo aluno", command=lambda: tela_incluir(janela))
    novo_aluno.grid(row=i+2, column=0, padx=3, pady=3)


def tela_incluir(janela):
    # função usada para excluir o menu principal e ir para a tela de incluir
    excluir_tela_anterior(janela)

    # Campos para a entrada dos dados: nome, altura, peso e telefone
    label_nome = tk.Label(janela, text="Nome: ")
    label_nome.grid(row=0, column=0, padx=0, pady=10)
    nome = tk.Entry(janela)
    nome.grid(row=0, column=1, padx=0, pady=10)

    label_altura = tk.Label(janela, text="Altura")
    label_altura.grid(row=1, column=0, padx=0, pady=10)
    altura = tk.Entry(janela)
    altura.grid(row=1, column=1, padx=0, pady=10)

    label_peso = tk.Label(janela, text="Peso")
    label_peso.grid(row=2, column=0, padx=0, pady=10)
    peso = tk.Entry(janela)
    peso.grid(row=2, column=1, padx=0, pady=10)

    label_telefone = tk.Label(janela, text="Telefone")
    label_telefone.grid(row=3, column=0, padx=0, pady=10)
    telefone = tk.Entry(janela)
    telefone.grid(row=3, column=1, padx=0, pady=10)

    def dados_de_inserir():
        # Coletando os dados inseridos nos campos nome, altura, peso e telefone
        nome_valor = nome.get().lower()
        altura_valor = altura.get()
        peso_valor = peso.get()
        telefone_valor = telefone.get()

        # Verificando se os campos foram preenchidos, caso não tenham sido, o menu volta para o início
        if nome_valor == '' or altura_valor == '' or peso_valor == '' or telefone_valor == '':
            print("Campos em branco")
            alunos_exibir(janela)
        else:
            # Inserindo os dados no banco de dados
            inserir(nome_valor, altura_valor, peso_valor, telefone_valor)
            alunos_exibir(janela)

        # Botão voltar e incluir
    voltar = tk.Button(janela, text="VOLTAR", command=lambda: alunos_exibir(janela))
    voltar.grid(row=4, column=1, padx=10, pady=10)
    incluir = tk.Button(janela, text="INCLUIR", command=dados_de_inserir)
    incluir.grid(row=4, column=0, padx=10, pady=10)


def tela_aluno(janela, aluno_escolhido):
    excluir_tela_anterior(janela)

    nome_escolhido = tk.Label(janela, text=aluno_escolhido)
    nome_escolhido.grid(row=0, column=0, padx=3, pady=3)

    informacoes = tk.Button(janela, text="Informações do aluno", command=lambda: informacoes_aluno(janela,
                                                                                                   aluno_escolhido))
    informacoes.grid(row=1, column=0, padx=3, pady=3)

    atualizar = tk.Button(janela, text="Atualizar dados", command=lambda: tela_editar(janela, aluno_escolhido))
    atualizar.grid(row=2, column=0, padx=3, pady=3)

    excluir = tk.Button(janela, text="Excluir aluno", command=lambda: tela_excluir(janela, aluno_escolhido))
    excluir.grid(row=3, column=0, padx=3, pady=3)
    botao_voltar = tk.Button(janela, text="VOLTAR", command=lambda: alunos_exibir(janela))
    botao_voltar.grid(row=5, column=0, padx=3, pady=3)
    botao_treino = tk.Button(janela, text="Manter treino", command=lambda: manter_treino(janela, aluno_escolhido))
    botao_treino.grid(row=6, column=0, padx=3, pady=3)


def informacoes_aluno(janela, nome):
    # função usada para excluir o menu principal e ir para a tela de leitura de dados
    excluir_tela_anterior(janela)

    # 'linhas' recebe o retorno de "lerDados()" que retorna todas as linhas do banco de dados
    linhas = ler_dados(nome)
    nome_aluno = nome
    # Imprimindo as linhas
    if linhas:
        linha = linhas[0]
        nome = tk.Label(janela, text="nome: " + str(linha[0]))
        nome.grid(row=0, column=0, padx=3, pady=3)

        altura = tk.Label(janela, text="altura: " + str(linha[1]))
        altura.grid(row=0, column=1, padx=3, pady=3)

        peso = tk.Label(janela, text="Peso: " + str(linha[2]))
        peso.grid(row=0, column=2, padx=3, pady=3)

        telefone = tk.Label(janela, text="Telefone: " + str(linha[3]))
        telefone.grid(row=0, column=3, padx=3, pady=3)
    else:
        vazio = tk.Label(janela, text="Nenhum aluno cadastrado")
        vazio.grid(row=0,column=0, padx=3, pady=3)

    voltar = tk.Button(janela, text="Voltar", command=lambda: tela_aluno(janela, nome_aluno))
    voltar.grid(row=1, column=0, padx=3, pady=3)


def tela_editar(janela, aluno_escolhido):
    # Funcao para excluir a tela principal e ir para o editar
    excluir_tela_anterior(janela)

    label_novo_valor = tk.Label(janela, text="Novo valor: ")
    label_novo_valor.grid(row=2, column=0)
    novo_valor = tk.Entry(janela)
    novo_valor.grid(row=2, column=1)

    label_novo_coluna = tk.Label(janela, text="O que deseja alterar\n"
                                              "(Nome, altura, peso ou telefone): ")
    label_novo_coluna.grid(row=3, column=0)
    coluna_alterar = tk.Entry(janela)
    coluna_alterar.grid(row=3, column=1)

    def dados_alterar():
        valor_alterar = novo_valor.get()
        valor_coluna = coluna_alterar.get().lower()

        # Verificando se os campos foram preenchidos, caso não tenham sido, o menu volta para o início
        if aluno_escolhido == '' or valor_alterar == '' or valor_coluna == '':
            print("Campos em branco")
            tela_aluno(janela, aluno_escolhido)
        else:
            # Editando os dados no banco de dados
            editar(valor_coluna, aluno_escolhido, valor_alterar)
            if valor_coluna == "nome":
                tela_aluno(janela, valor_alterar)
            else:
                tela_aluno(janela, aluno_escolhido  )

    botao_editar = tk.Button(janela, text="Editar", command=dados_alterar)
    botao_editar.grid(row=5, column=0)
    botao_voltar = tk.Button(janela, text="Voltar", command=lambda: tela_aluno(janela, aluno_escolhido))
    botao_voltar.grid(row=5, column=1)


def tela_excluir(janela, aluno_escolhido):
    # função usada para excluir o menu principal e ir para a tela de excluir
    excluir_tela_anterior(janela)

    nome_exibir = tk.StringVar()
    nome_exibir.set(aluno_escolhido)

    label_excluir = tk.Label(janela, text="Nome a ser excluído: ")
    label_excluir.grid(row=0, column=0, padx=0, pady=0)
    nome_excluir = tk.Label(janela, textvariable=nome_exibir, relief="solid")
    nome_excluir.grid(row=0, column=1, padx=0, pady=10)

    # Função utilizada para coletar o nome da pessoa que será excluída
    def individuo_apagar():
        # Chamada da função excluir passando o nome que deve ser excluído do banco de dados.
        excluir(aluno_escolhido)
        alunos_exibir(janela)

    alerta = tk.Label(janela, text= f"Se realmente deseja excluir {aluno_escolhido},\n clique em EXCLUIR")
    alerta.grid(row=1, column=0, padx=3,pady=3)
    botao_excluir = tk.Button(janela, text="EXCLUIR", command=individuo_apagar)
    botao_excluir.grid(row=1, column=1, padx=10, pady=10)

    botao_voltar = tk.Button(janela, text="VOLTAR", command=lambda: tela_aluno(janela, aluno_escolhido))
    botao_voltar.grid(row=2, column=0, padx=0, pady=5)


def manter_treino(janela, aluno_escolhido):
    # função usada para excluir o menu principal e ir para a tela de excluir
    excluir_tela_anterior(janela)

    criar_treino = tk.Button(janela, text="Criar treino")
    criar_treino.grid(row=0, column=0, padx=3, pady=3)

    ler_treino = tk.Button(janela, text="Ler treino")
    ler_treino.grid(row=1, column=0, padx=3, pady=3)

    atualizar_treino = tk.Button(janela,text="Atualizar treino")
    atualizar_treino.grid(row=2, column=0, padx=3, pady=3)

    excluir_treino = tk.Button(janela, text="Excluir treino")
    excluir_treino.grid(row=3, column=0, padx=3, pady=3)

    botao_voltar = tk.Button(janela, text="Voltar", command=lambda: tela_aluno(janela, aluno_escolhido))
    botao_voltar.grid(row=4, column=0, padx=3, pady=3)

""" 

ABAIXO APENAS COMANDOS PARA CONEXÃO COM O BANCO DE DADOS

"""


def inserir(nome, altura, peso, telefone):
    # Função para inserir no banco de dados
    cursor = connection.cursor()
    comando = "INSERT INTO tab_pessoas (nome, altura, peso, telefone) VALUES (%s, %s, %s, %s)"
    values = (nome, altura, peso, telefone)
    cursor.execute(comando, values)
    connection.commit()
    cursor.close()
    print("Dados inseridos com sucesso")


def ler_dados(nome_escolhido):
    # Função para ler os dados do banco de dados e retornar as linhas
    cursor = connection.cursor()
    print(nome_escolhido)
    if nome_escolhido is None:
        comando = "SELECT * FROM tab_pessoas"
    else:
        comando = f"SELECT * FROM tab_pessoas WHERE nome = '{nome_escolhido}'"

    cursor.execute(comando)
    linhas = cursor.fetchall()
    print(linhas)
    return linhas


def excluir(nome_excluir):
    # Função para excluir do banco de dados as informações referentes ao nome recebido por parâmetro
    cursor = connection.cursor()
    comando = f"DELETE FROM tab_pessoas WHERE nome = '{nome_excluir}'"
    cursor.execute(comando)
    connection.commit()

    print("Dado excluído")


def editar(coluna, nome_pessoa, novo_valor):
    cursor = connection.cursor()
    # Se for STRING:
    if coluna == 'nome' or coluna == 'telefone':
        comando = f"UPDATE tab_pessoas SET {coluna} = '{novo_valor}' WHERE nome = '{nome_pessoa}'"
        print("a")
    else:
        # Se for float
        comando = f"UPDATE tab_pessoas SET {coluna} = {novo_valor} WHERE nome = '{nome_pessoa}'"

    cursor.execute(comando)
    connection.commit()
    cursor.close()
    print("Editado com sucesso!")


if __name__ == "__main__":
    # tabela
    interface()

# chamando banco de dados
"""
bot_incluir = tk.Button(janela, text="Incluir",
                                command=lambda: tela_incluir(janela))
        bot_incluir.grid(row=0, column=0, padx=10, pady=10)

        bot_ler = tk.Button(janela, text="Leitura",
                            command=lambda: tela_ler(janela))
        bot_ler.grid(row=1, column=0, padx=10, pady=10)

        bot_editar = tk.Button(janela, text="Editar", command=lambda: tela_editar(janela))
        bot_editar.grid(row=2, column=0, padx=10, pady=10)

        bot_excluir = tk.Button(janela, text="Excluir",
                                command=lambda: tela_excluir(janela))
        bot_excluir.grid(row=3, column=0, padx=10, pady=10)
"""