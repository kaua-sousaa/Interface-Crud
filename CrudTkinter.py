"""
Começando um CRUD: INSERIR, LER, EDITAR E EXCLUIR em Python utilizando um banco de dados e interface.
O CRUD SERÁ DE INFORMAÇÕES DE UMA PESSOA.
DEVERÁ RECEBER COMO INFORMAÇÃO: NOME, ALTURA, PESO e TELEFONE.
"""
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

    tela_inicio(janela)

    janela.mainloop()


def excluir_tela_anterior(janela):
    # Função para excluir o menu atual para que os itens não fiquem sobrepostos no menu posterior
    for widget in janela.winfo_children():
        widget.grid_forget()


def excluir_e_voltar_inicio(janela):
    # Função para excluir o menu atual, tal como a função "excluir_tela_anterior" e voltar à tela de início
    for widget in janela.winfo_children():
        widget.grid_forget()
    tela_inicio(janela)


def tela_editar(janela):
    # Funcao para excluir a tela principal e ir para o editar
    excluir_tela_anterior(janela)

    label_nome_pessoa = tk.Label(janela, text="Individuo a alterar: ")
    label_nome_pessoa.grid(row=0, column=0, padx=3, pady=3)
    nome_editar = tk.Entry(janela)
    nome_editar.grid(row=0, column=1, padx=3, pady=3)

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
        valor_nome = nome_editar.get().lower()
        valor_alterar = novo_valor.get()
        valor_coluna = coluna_alterar.get().lower()

        # Verificando se os campos foram preenchidos, caso não tenham sido, o menu volta para o início
        if valor_nome == '' or valor_alterar == '' or valor_coluna == '':
            print("Campos em branco")
            excluir_e_voltar_inicio(janela)
        else:
            # Editando os dados no banco de dados
            editar(valor_coluna, valor_nome, valor_alterar)
            excluir_e_voltar_inicio(janela)

    botao_editar = tk.Button(janela, text="Editar", command=dados_alterar)
    botao_editar.grid(row=5, column=0)
    botao_voltar = tk.Button(janela, text="Voltar", command=lambda: excluir_e_voltar_inicio(janela))
    botao_voltar.grid(row=5, column=1)


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
            excluir_e_voltar_inicio(janela)
        else:
            # Inserindo os dados no banco de dados
            inserir(nome_valor, altura_valor, peso_valor, telefone_valor)
            excluir_e_voltar_inicio(janela)

        # Botão voltar e incluir
    voltar = tk.Button(janela, text="VOLTAR", command=lambda: excluir_e_voltar_inicio(janela))
    voltar.grid(row=4, column=1, padx=10, pady=10)
    incluir = tk.Button(janela, text="INCLUIR", command=dados_de_inserir)
    incluir.grid(row=4, column=0, padx=10, pady=10)


def tela_ler(janela):
    # função usada para excluir o menu principal e ir para a tela de leitura de dados
    excluir_tela_anterior(janela)

    # 'linhas' recebe o retorno de "lerDados()" que retorna todas as linhas do banco de dados
    linhas = ler_dados()

    # Imprimindo as linhas
    for i, row in enumerate(linhas):
        nome = tk.Label(janela, text="nome: " + str(row[0]))
        nome.grid(row=i, column=0, padx=3, pady=3)
        altura = tk.Label(janela, text="altura: " + str(row[1]))
        altura.grid(row=i, column=1, padx=3, pady=3)
        peso = tk.Label(janela, text="Peso: " + str(row[2]))
        peso.grid(row=i, column=2, padx=3, pady=3)
        telefone = tk.Label(janela, text="Telefone: " + str(row[3]))
        telefone.grid(row=i, column=3, padx=3, pady=3)

    botao_voltar = tk.Button(janela, text="VOLTAR", command=lambda: excluir_e_voltar_inicio(janela))
    botao_voltar.grid(padx=3, pady=3)


def tela_excluir(janela):
    # função usada para excluir o menu principal e ir para a tela de excluir
    excluir_tela_anterior(janela)

    label_excluir = tk.Label(janela, text="Nome de quem deseja excluir: ")
    label_excluir.grid(row=0, column=0, padx=0, pady=0)
    nome_excluir = tk.Entry(janela)
    nome_excluir.grid(row=0, column=1, padx=0, pady=10)

    # Função utilizada para coletar o nome da pessoa que será excluída
    def individuo_apagar():
        excluir_valor = nome_excluir.get().lower()

        # Verificando se os campos foram preenchidos, caso não tenham sido, o menu volta para o início
        if excluir_valor == '':
            print("Campo em branco")
            excluir_e_voltar_inicio(janela)
        else:
            # Chamada da função excluir passando o nome que deve ser excluído do banco de dados.
            excluir(excluir_valor)
            excluir_e_voltar_inicio(janela)

    botao_excluir = tk.Button(janela, text="EXCLUIR", command=individuo_apagar)
    botao_excluir.grid(row=0, column=2, padx=10, pady=10)

    botao_voltar = tk.Button(janela, text="VOLTAR", command=lambda: excluir_e_voltar_inicio(janela))
    botao_voltar.grid(row=1, column=0, padx=0, pady=5)


def tela_inicio(janela):
    # Tela principal onde se encontra o "Incluir, Leitura, Editar e Excluir"
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


def inserir(nome, altura, peso, telefone):
    # Função para inserir no banco de dados
    cursor = connection.cursor()
    comando = "INSERT INTO tab_pessoas (nome, altura, peso, telefone) VALUES (%s, %s, %s, %s)"
    values = (nome, altura, peso, telefone)
    cursor.execute(comando, values)
    connection.commit()
    cursor.close()
    print("Dados inseridos com sucesso")


def ler_dados():
    # Função para ler os dados do banco de dados e retornar as linhas
    cursor = connection.cursor()
    comando = "SELECT * FROM tab_pessoas"
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


if __name__ == "__main__":
    # tabela
    interface()

# chamando banco de dados
