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

    if linhas:
        if hasattr(janela, "aviso"):
            janela.aviso.destroy()

        for i, row in enumerate(linhas):
            nome = tk.Button(janela, text=str(row[1]), command=lambda id_valor=row[0], nome=row[1]: tela_aluno(janela, nome,
                                                                                                                id_valor))
            nome.grid(row=i+1, column=0, padx=3, pady=3)
        novo_aluno = tk.Button(janela, text="Inserir novo aluno", command=lambda: tela_incluir(janela))
        novo_aluno.grid(row=i + 2, column=0, padx=3, pady=3)
    else:
        janela.aviso = tk.Label(janela, text="Não há alunos")
        janela.aviso.grid(row=1, column=0, padx=3, pady=3)
        novo_aluno = tk.Button(janela, text="Inserir novo aluno", command=lambda: tela_incluir(janela))
        novo_aluno.grid(row=2, column=0, padx=3, pady=3)


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

    label_senha = tk.Label(janela, text="Senha: ")
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
            inserir(nome_valor, altura_valor, peso_valor, senha_valor)
            alunos_exibir(janela)

        # Botão voltar e incluir
    voltar = tk.Button(janela, text="VOLTAR", command=lambda: alunos_exibir(janela))
    voltar.grid(row=4, column=1, padx=10, pady=10)
    incluir = tk.Button(janela, text="INCLUIR", command=dados_de_inserir)
    incluir.grid(row=4, column=0, padx=10, pady=10)


def tela_aluno(janela, aluno_escolhido, id_valor):
    excluir_tela_anterior(janela)

    nome_escolhido = tk.Label(janela, text=aluno_escolhido)
    nome_escolhido.grid(row=0, column=0, padx=3, pady=3)

    informacoes = tk.Button(janela, text="Informações do aluno", command=lambda: informacoes_aluno(janela
                                                                                                   ,aluno_escolhido, id_valor))
    informacoes.grid(row=1, column=0, padx=3, pady=3)

    atualizar = tk.Button(janela, text="Atualizar dados", command=lambda: tela_editar(janela, aluno_escolhido, id_valor))
    atualizar.grid(row=2, column=0, padx=3, pady=3)

    excluir = tk.Button(janela, text="Excluir aluno", command=lambda: tela_excluir(janela, aluno_escolhido, id_valor))
    excluir.grid(row=3, column=0, padx=3, pady=3)
    botao_voltar = tk.Button(janela, text="VOLTAR", command=lambda: alunos_exibir(janela))
    botao_voltar.grid(row=5, column=0, padx=3, pady=3)
    botao_treino = tk.Button(janela, text="Manter treino", command=lambda: manter_treino(janela, aluno_escolhido,
                                                                                         id_valor))
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
        nome = tk.Label(janela, text="nome: " + str(linha[1]))
        nome.grid(row=0, column=0, padx=3, pady=3)

        altura = tk.Label(janela, text="altura: " + str(linha[2]))
        altura.grid(row=0, column=1, padx=3, pady=3)

        peso = tk.Label(janela, text="Peso: " + str(linha[3]))
        peso.grid(row=0, column=2, padx=3, pady=3)

        telefone = tk.Label(janela, text="Telefone: " + str(linha[4]))
        telefone.grid(row=0, column=3, padx=3, pady=3)
    else:
        vazio = tk.Label(janela, text="Nenhum aluno cadastrado")
        vazio.grid(row=0,column=0, padx=3, pady=3)

    voltar = tk.Button(janela, text="Voltar", command=lambda: tela_aluno(janela, nome_aluno, id_valor))
    voltar.grid(row=1, column=0, padx=3, pady=3)


def tela_editar(janela, aluno_escolhido, id_valor):
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
            tela_aluno(janela, aluno_escolhido, id_valor)
        else:
            # Editando os dados no banco de dados
            editar(valor_coluna, aluno_escolhido, valor_alterar)
            if valor_coluna == "nome":
                tela_aluno(janela, valor_alterar, id_valor)
            else:
                tela_aluno(janela, aluno_escolhido, id_valor)

    botao_editar = tk.Button(janela, text="Editar", command=dados_alterar)
    botao_editar.grid(row=5, column=0)
    botao_voltar = tk.Button(janela, text="Voltar", command=lambda: tela_aluno(janela, aluno_escolhido, id_valor))
    botao_voltar.grid(row=5, column=1)


def tela_excluir(janela, aluno_escolhido, id_valor):
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

    botao_voltar = tk.Button(janela, text="VOLTAR", command=lambda: tela_aluno(janela, aluno_escolhido, id_valor))
    botao_voltar.grid(row=2, column=0, padx=0, pady=5)


def manter_treino(janela, aluno_escolhido, id_valor):
    # função usada para excluir o menu principal e ir para a tela de excluir
    excluir_tela_anterior(janela)

    criar_treino = tk.Button(janela, text="Criar treino", command=lambda: tela_incluir_treino(janela, aluno_escolhido))
    criar_treino.grid(row=0, column=0, padx=3, pady=3)

    exibir_treino = tk.Button(janela, text="Ler treino", command= lambda: ler_treino(janela, aluno_escolhido, id_valor))
    exibir_treino.grid(row=1, column=0, padx=3, pady=3)

    modificar_treino = tk.Button(janela,text="Atualizar treino", command= lambda: atualizar_treino(janela, aluno_escolhido,
                                                                                                   id_valor))
    modificar_treino.grid(row=2, column=0, padx=3, pady=3)

    excluir_treino = tk.Button(janela, text="Excluir treino")
    excluir_treino.grid(row=3, column=0, padx=3, pady=3)

    botao_voltar = tk.Button(janela, text="Voltar", command=lambda: tela_aluno(janela, aluno_escolhido, id_valor))
    botao_voltar.grid(row=4, column=0, padx=3, pady=3)


""" 

ABAIXO O MANTER TREINO

"""


def tela_incluir_treino(janela, aluno_escolhido):
    excluir_tela_anterior(janela)

    linhas = ler_dados(aluno_escolhido)
    linha = linhas[0]
    id_valor = linha[0]

    label_nome_exercicio = tk.Label(janela, text="Nome exercicio: ")
    label_nome_exercicio.grid(row=0, column=0, padx=3, pady=3)
    exercicio = tk.Entry(janela)
    exercicio.grid(row=0, column=1, padx=3, pady=3)

    label_peso = tk.Label(janela, text="Peso: ")
    label_peso.grid(row=1, column=0, padx=3, pady=3)
    peso = tk.Entry(janela)
    peso.grid(row=1, column=1, padx=3, pady=3)

    label_repeticoes = tk.Label(janela, text="Repetições: ")
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

    bot_incluir = tk.Button(janela, text="Incluir", command=recuperar_valores)
    bot_incluir.grid(row=3, column=0, padx=3, pady=3)
    bot_voltar = tk.Button(janela, text="Voltar", command=lambda: manter_treino(janela, aluno_escolhido, id_valor))
    bot_voltar.grid(row=3, column=1, padx=3, pady=3)


def ler_treino(janela, aluno_escolhido, id_valor):
    excluir_tela_anterior(janela)
    linhas = ler_treino_bd(id_valor)

    for i, row in enumerate(linhas):
        linha = linhas[i]
        exercicio = tk.Label(janela, text="Exercicio: "+ str(linha[1]))
        exercicio.grid(row=i, column=0, padx=3, pady=3)
        peso = tk.Label(janela, text="Peso: "+ str(linha[2]))
        peso.grid(row=i, column=1, padx=3, pady=3)
        repeticoes = tk.Label(janela, text="Repetições: "+ str(linha[3]))
        repeticoes.grid(row=i, column=2, padx=3, pady=3)

    bot_voltar = tk.Button(janela, text="VOLTAR", command=lambda: manter_treino(janela, aluno_escolhido, id_valor))
    bot_voltar.grid(row=i+2, column=0, padx=3, pady=3)


def atualizar_treino(janela, aluno_escolhido, id_valor):
    excluir_tela_anterior(janela)

    novo_valor = tk.Label(janela, text="Novo valor: ")
    novo_valor.grid(row=0, column=0, padx=3, pady=3)
    valor = tk.Entry(janela)
    valor.grid(row=0, column=1, padx=3, pady=3)
    coluna_alterar = tk.Label(janela, text="O que deseja alterar\n(Exercicio, peso ou repetições)")
    coluna_alterar.grid(row=1, column=0, padx=3, pady=3)
    alterar = tk.Entry(janela)
    alterar.grid(row=1, column=1, padx=3, pady=3)
    def recuperar_valor():
        new_valor = valor.get().lower()
        alterar_valor = alterar.get().lower()
        if new_valor == '' or alterar_valor == '':
            print("hihi esqueceu")
        else:
            editar_treino(alterar_valor, new_valor, id_valor)
            print("alterou")

    bot_editar = tk.Button(janela, text="EDITAR", command=lambda: recuperar_valor())
    bot_editar.grid(row=2, column=0, padx=3, pady=3)
    bot_voltar = tk.Button(janela, text="VOLTAR", command=lambda: manter_treino(janela, aluno_escolhido, id_valor))
    bot_voltar.grid(row=2, column=0, padx=3, pady=3)
""" 

ABAIXO APENAS COMANDOS PARA CONEXÃO COM O BANCO DE DADOS

"""


def inserir(nome, altura, peso, senha):
    # Função para inserir no banco de dados
    cursor = connection.cursor()
    comando = "INSERT INTO tab_pessoas (nome, altura, peso, senha) VALUES (%s, %s, %s, %s)"
    values = (nome, altura, peso, senha)
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


def editar_treino(coluna, novo_valor, id_valor):
    cursor = connection.cursor()

        # SE FOR STRING
    if coluna == 'exercicio' or coluna == 'repeticoes':
        comando = f"UPDATE tab_treino SET {coluna} = {novo_valor} WHERE fk_pessoa = {id_valor}"
    else:
        #  SE FOR FLOAT
        comando = f"UPDATE tab_treino SET {coluna} = '{novo_valor}' WHERE fk_pessoa = {id_valor}"

    cursor.execute(comando)
    connection.commit()
    cursor.close()


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