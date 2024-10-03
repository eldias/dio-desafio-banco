# Precisamos de importar as bibliotecas para controle de data/hora e das classes abstratas:
from datetime import datetime
from abc import ABC, abstractclassmethod, abstractproperty


class Cliente: # Criando classe Cliente, que deriva a classe PessoaFisica, para completar novos cadastros
    def __init__(self, endereco): # Cria instância da classe Cliente.
        self.endereco = endereco # Declara o self em endereço como endereco.
        self.contas = [] # Cria um lista vazia de contas em self.contas.

    def realizar_transacao(self, conta, transacao): # Cria função realizar_transacao, que tem a conta do cliente e tipo de transação.
        transacao.registrar(conta) # Ativa classe transacao, com a função registrar.

    def adicionar_conta(self, conta): # Cria função adicionar_conta, que tem a conta do cliente.
        self.contas.append(conta) # Adiciona à lista de contas do cliente a conta criada com dados do cliente.

class PessoaFisica(Cliente): # Usando o polimorfismo, atrelar a classe Pessoa_fisica à classe Cliente.
    def __init__(self, nome, data_nascimento, cpf, endereco): # Cria instância da classe PessoaFisica.
        super().__init__(endereco) # Construtor da classe pai(Cliente).
        self.nome = nome # Declara os dados da PessoaFisica.
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta: # Criando classe Conta.
    def __init__(self, numero, cliente): # Criando instâncias privadas dos dados da conta.
        self._saldo = 0 # Definindo o saldo padrão em 0.
        self._numero = numero # Declarando o número da conta em self._numero.
        self._agencia = "0001" # Definindo o número da agência como "0001".
        self._cliente = cliente # Declarando o cliente em self._cliente
        self._historico = Historico() # Declarando em self._historico a classe Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self._saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Operação inválida, Não possui saldo suficiente!")

        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True

        else:
            print("\nOperação inválida, valor informado não é válido.")

        return False

    def depositar(self, valor):

        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!")
        else:
            print("Operação inválida, valor informado não é válido.")
            return False
        
        return True

class ContaCorrente(Conta): # Usando o polimorfismo, atrelar a classe ContaCorrente à classe Conta.
    def __init__(self, numero, cliente, limite=500, limite_saques=3): # Criando instâncias do cliente e limites, já pré-definidos nos atributos.
        super().__init__(numero, cliente) # Chamando superclass Conta com instâncias de limite e limite_saques.
        self.limite = limite
        self.limite_saques = limite_saques 

    def sacar(self, valor): # Sobreescrita do método sacar, que pede o valor de saque.
        numero_saques = len( # List comprehension que lê o histórico(tamanho/quantidade) de saques da conta em uso, filtrando saques efetuados em transação.
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite # definição de excedeu_limite se o valor for maior que o limite.
        excedeu_saques = numero_saques >= self.limite_saques # definição de excedeu_saques se o numero de saques for maior ou igual ao limite de saques(3).

        if excedeu_limite: # Erro se excedeu_limite da conta(500).
            print("Operação inválida! Valor do saque excede o limite da conta.")

        elif excedeu_saques: # Erro se excedeu o limite de saques por dia (3).
            print("Você excedeu o limite de saques do dia.")

        else:
            return super().sacar(valor) # Se tudo der certo é chamado a sacar o valor na conta.
        
        return False # Retorna falso caso ocorra erro.

    def __str__(self): # Retorna os dados da Conta.
        return f"""\
            Agência:\t\t{self.agencia}
            Conta Corrente:\t\t{self.numero}
            Titular da Conta:\t{self.cliente.nome}
        """

class Historico: # Registra o histórico de transações das contas do banco.
    def __init__(self): # Define inicialmente self.transacoes como um lista vazia.
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoestransacoes

    def adicionar_transacao(self, transacao): # Cria rotina de adicionar transação no histórico.
        self._transacoes.append( # Uso da função built-in .append() para adicionar a transação em um dicionário.
            { # Define padrão do registro com o nome(tipo saque ou depósito) da transação, valor e data/hora.
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s")
            }

        )

class Transacao(ABC): # Tornando abstrata a classe Transacao utilizando o módulo ABC.
    @property # Cria propriedade abstrata de valor
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta): # Cria método de classe abstrata da função registrar, que registra a conta
        pass

class Saque(Transacao): # Usando o polimorfismo, atrelar a classe Saque à classe Transacao.
    def __init__(self, valor): # Criando a definição de self.valor.
        self._valor = valor

    @property # Criando propriedade da função valor, que retorna privado self._valor.
    def valor(self):
        return self._valor

    def registrar(self, conta): # Cria a função registrar, que traz a conta.
        sucesso_transacao = conta.sacar(self.valor) # Cria a variável sucesso_transacao, que recebe o valor da operação sacar de conta.

        if sucesso_transacao: # Se for verdadeiro sucesso_transacao, aciona função de adicionar_transacao em conta.historico.
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao): # Usando o polimorfismo, atrelar a classe Depósito à classe Transacao
    def __init__(self, valor): # Criando a definição de self.valor.
        self._valor = valor

    @property # Criando propriedade da função valor, que retorna privado self._valor.
    def valor(self):
        return self._valor

    def registrar(self, conta): # Cria a função registrar, que traz a conta.
        sucesso_transacao = conta.depositar(self.valor) # Cria a variável sucesso_transacao, que recebe o valor da operação depositar de conta.

        if sucesso_transacao: # Se for verdadeiro sucesso_transacao, aciona função de adicionar_transacao em conta.historico.
            conta.historico.adicionar_transacao(self)

# ==================================================================================================

def menu(): # Cria função de exibição de menu, com variável string com menu multilinha e input de retorno ao usuário.
    menu = """
    +++++++++++++++++BANCO++XPTO+++++++++++++++++
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuário
    [q] Sair
    → """
    return input(menu)

def filtrar_cliente(cpf, clientes): # Cria função de filtrar clientes por CPF, caso vazio retorne None.
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente ainda não possui conta.")
        return
    
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return
    
    valor = float(input("Informe o valor a depositar: "))

    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return
    
    valor = float(input("Informe o valor a sacar: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n==================Extrato================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas transações no período."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
    
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("===========================================")

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nJá existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\nCliente criado com sucesso!")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado, encerrando criação de conta.")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso!")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(str(conta))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, selecione novamente a operação desejada.")

main()