""" simulação operações de banco em Python
operações permitidas: depósito, saque e extrato(saldo)

depósito 
depósito somente com valores positivos (deposito > 0 and type(int))

saques
limite diário de 3 saques
limite de 500,00 por saque(operação)
se não tiver saldo em conta, exibir mensagem falta de saldo

extratos
na opção de extrato consta todos os depósitos e saques feitos (lista) em R$ xxx.xx(float) """

menu = """

Banco XPTO, Bem-vindo!

Escolha sua opção:

[d] Depósito
[s] Saque
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_de_saques = 0
limite_de_saques = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor a ser depositado: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print("Operação falhou! O valor informado não é válido.")

    elif opcao == "s":
        valor = float(input("Informe e valor a sacar: "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_de_saques >= limite_de_saques

        if excedeu_saldo:
            print(f"Saldo atual: R$ {saldo:.2f}\n\nSaldo insuficiente para realizar operação de saque.")

        elif excedeu_limite:
            print(f"O valor de saque desta conta é de {limite:.2f} por operação.")

        elif excedeu_saques:
            print(f"Sua conta só permite {limite_de_saques} saques por dia.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque de {valor:.2f}\n"
            numero_de_saques += 1

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram reazlizadas movimentações" if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("=========================================")

    elif opcao == "q":
        break

    else:
        print("\nOperação inválida, por favor selecione novamente a operação desejada.")
