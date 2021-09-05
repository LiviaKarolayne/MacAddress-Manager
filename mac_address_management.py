#Variáveis:
#arquivoJson                 - guarda o nome do arquivo json referência
#cpf                         - guarda o valor do CPF digitado pelo usuário ou um CPF de um do dicionário CPFs
#mac                         - guarda o valor do MAC digitado pelo usuário ou um MAC de um determinado CPF do dicionário CPFs
#CPFs                        - guarda o dicionário de um arquivo .json
#menu                        - guarda as opções de execução que o usuário pode escolher
#opcao                       - guarda a opção escolhida pelo usuário
#eValida                     - guarda o resultado True/False da função validarOpcao

#Funções:
#validarOpcao                - verifica se uma string é um número inteiro entre 1 e 7
                             #Variáveis:
                             #string  - string a ser verificada
                             #eValida - guarda True/False a depender se a string é um número inteiro entre 1 e 7

#verificaExistenciaDeArquivo - verifica se um determinado arquivo existe
#criaArquivoJson             - cria um arquivo .json no diretório de execução deste programa, caso esse arquivo não exista
#leJson                      - lê o arquivo criado e retorna seu conteúdo no formato Json

#validaCPF                   - verifica se um CPF está na formatação correta
                             #Variáveis:
                             #cpf            - cpf a ser validado/retorno do cpf com máscara
                             #numerosIguais  - guarda True/False a depender se todos os números do cpf são iguais
                             #mascaraSimples - guarda True/False a depender se o cpf está com a formatação de 11 números
                             #mascaraompleta - guarda True/False a depender se o cpf está com a formatação de 11 números e com os caracteres especiais
                             #eValido        - guarda True/False a depender se o cpf está com a formatação correta

#autenticaCPF                - verifica se um CPF é válido para uso pessoal
                             #Variáveis:
                             #cpf                       - cpf a ser autenticado
                             #novoCPF                   - retorno do cpf com máscara
                             #eValido                   - guarda True/False a depender se o cpf está válido
                             #primeiroDigitoVerificador - guarda o primeiro dígito verificador do cpf
                             #segundoDigitoVerificador  - guarda o segundo dígito verificador do cpf
                             #fator                     - guarda o valor dos fatores que serão multiplicados, respectivamente, pelos 9 primeiros números do cpf
                             #indice                    - guarda o índice do cpf
                             #resultado                 - guarda os valores das operações aritiméticas necessárias

#salvaDicionarioEmArquivo    - escreve um dicionário em um arquivo .json

#cadastraCPF                 - adiciona um CPF em um dicionário e atualiza o arquivo .json
                             #Variáveis:
                             #dicionario - guarda o dicionário em que o cpf deve ser cadastrado 
                             #cpf        - guarda o cpf digitado pelo usuário
                             #arquivo    - guardda o arquivo em que as alterações devem ser feitas
                             #eValido    - guarda True/False a depender se o o cpf está autenticadp
                             #novoCPF    - guarda o cpf com a máscara completa
                             #*** AS MESMAS VARIÁVEIS SERVEM PARA AS FUNÇÕES:
                             #    removerCPF
                             #    cadastraMAC
                             #    removeMAC
                             #***

#removeCPF                   - remove um CPF de um dicionário e atualiza o arquivo .json

#cadastraMAC                 - cadastra um MAC em um dicionário e atualiza o arquivo .json
                             #Variáveis:
                             #mac - recebe o mac digitado pelo usuário

#removeMAC                   - remove o MAC de um dicionário e atualiza o arquivo .json
                             #Variáveis:
                             #mac - recebe o mac digitado pelo usuário
                             
#listaCPFs                   - lista os CPFs de um dicionário

#listaMACs                   - lista todos os MACs de um cpf informado
                             #Variáveis:
                             #cpf - recebe o cpf digitado pelo usuário

import json, re

def validarOpcao(string):
    eValida = bool(re.match(r"^[1-7]$", opcao))   
    return eValida, string

def verificaExistenciaDeArquivo(arquivo):
    try:
        with open(arquivo, 'r') as arquivo:
            return True
    except:
        return False

def criaArquivoJson(arquivo):
    if not verificaExistenciaDeArquivo(arquivo):
        arquivoJson = open(arquivo, "w")
        arquivoJson.write("{}")
        arquivoJson.close()

def leJson(arquivo):
    with open(arquivo,"r") as arquivo:
        JSON = json.load(arquivo)
        return JSON

def validaCPF(cpf):
    eValido = False
    
    mascaraSimples  = bool(re.match(r"^\d{11}$", cpf))
    mascaraCompleta = bool(re.match(r"^(\d{3}.){2}\d{3}-\d{2}$", cpf))

    if mascaraCompleta:  #Verifica se o cpf tem 11 números inteiros com os caracteres característicos
        eValido = True
            
    elif mascaraSimples: #Verifica se o cpf tem apenas 11 números inteiros e coloca a mascara completa
        cpf = cpf[0]+cpf[1]+cpf[2]+"."+cpf[3]+cpf[4]+cpf[5]+"."+cpf[6]+cpf[7]+cpf[8]+"-"+cpf[9]+cpf[10]
        eValido = True

    numerosIguais = bool(re.match(r"^(\d)\1{2}.(\d)\1{2}.(\d)\1{2}-(\d)\1{1}$", cpf))
    if numerosIguais: #verifica se todos os números do cpf são iguais
        eValido = False

    return eValido, cpf

def autenticaCPF(cpf):
    eValido, novoCPF = validaCPF(cpf)
    if eValido: #verifica se o cpf está na formatação correta
        primeiroDigitoVerificador = int(novoCPF[12])
        segundoDigitoVerificador  = int(novoCPF[13])
        fator = 10
        indice = 0
        resultado = 0

        while fator>1: #multiplica os 9 primeiros números do cpf, respectivamente, pelo número da sequência decrescente de 10 até 2 
            if novoCPF[indice] == "." or novoCPF[indice] == "-":
                indice += 1
            resultado += int(novoCPF[indice])*fator
            fator -= 1
            indice += 1
                
        resultado = (resultado * 10) % 11
        if resultado == 10: #se resultado for 10, passa a ser 0
            resultado = 0
            
        if resultado != primeiroDigitoVerificador: #se resultado é diferente do primeiroDigitoVerificador, ele não é válido para uso pessoal
            eValido = False
        else:
            fator = 11
            indice = 0
            resultado = 0
            while fator>1: #multiplica os 9 primeiros números do cpf, respectivamente, pelo número da sequência decrescente de 11 até 3; e, o primeiro dígito verificador por 2
                if novoCPF[indice] == "." or novoCPF[indice] == "-":
                    indice += 1
                resultado += int(novoCPF[indice])*fator
                fator -= 1
                indice += 1
                
            resultado = (resultado * 10) % 11
            if resultado != segundoDigitoVerificador: #se resultado é diferente do segundoDigitoVerificador, ele não é válido para uso pessoal
                eValido = False

    return eValido, novoCPF
           
def salvaDicionarioEmArquivo(dicionario, arquivo):
    with open(arquivo,"w") as arquivo:
        json.dump(dicionario, arquivo)

def cadastraCPF(dicionario, cpf, arquivo):
    eValido, novoCPF = autenticaCPF(cpf)
    if eValido: #verifica se o cpf está na formatação correta
        if novoCPF in dicionario.keys():
            print("Esse CPF já está cadastrado")
        else:
            dicionario[novoCPF] = []
            print("CPF cadastrado com sucesso")
            salvaDicionarioEmArquivo(dicionario, arquivo) #salva as alterações feitas no arquivo .json
    else:
        print("Esse CPF não é válido")

def removeCPF(dicionario, cpf, arquivo):
    eValido, novoCPF = validaCPF(cpf)
    if novoCPF in dicionario.keys(): #verifica se o cpf está no dicionário
        dicionario.pop(novoCPF)
        print("CPF removido com sucesso")
        salvaDicionarioEmArquivo(dicionario, arquivo) #salva as alterações feitas no arquivo .json
    else:
        print("Esse CPF não está cadastrado")

def cadastraMAC(dicionario, cpf, mac, arquivo):
    eValido, novoCPF = validaCPF(cpf)
    if novoCPF in dicionario.keys():   #verifica se o cpf está no dicionário
        if mac in dicionario[novoCPF]: #verifica se o mac está associado ao cpf
            print("Esse endereço MAC já existe")
        else:
            dicionario[novoCPF].append(mac)
            print("MAC cadastrado com sucesso")
            salvaDicionarioEmArquivo(dicionario, arquivo) #salva as alterações feitas no arquivo .json
    else:
        print("Esse CPF não está cadastrado")

def removeMAC(dicionario, cpf, mac, arquivo):
    eValido, novoCPF = validaCPF(cpf)
    if novoCPF in dicionario.keys():   #verifica se o cpf está no dicionário
        if mac in dicionario[novoCPF]: #verifica se o mac está associado ao cpf
            indiceDoMac = CPFs[novoCPF].index(mac)
            del dicionario[novoCPF][indiceDoMac]
            print("MAC removido com sucesso")
            salvaDicionarioEmArquivo(dicionario, arquivo) #salva as alterações feitas no arquivo .json
        else:
            print("Nenhum endereço MAC vinculado a este CPF")
    else:
        print("Esse CPF não está cadastrado")

def listaCPFs(dicionario):
    if not dicionario: #verifica se o dicionário está vazio
        print("Nenhum FPC cadastrado")
    else:
        print("---------- Lista de CPFs ----------")
        listaDeCPFs = dicionario.keys()
        for cpf in listaDeCPFs:
            print(cpf)
    
def listaMACs(dicionario, cpf):
    eValido, novoCPF = validaCPF(cpf)
    if novoCPF in dicionario.keys(): #verifica se o cpf está no dicionário
            listaDeMACs = dicionario[novoCPF] 
            if not listaDeMACs: #verifica se existe mac associado ao cpf
                print("Nenhum endereço MAC vinculado a este CPF")
            else:
                print("---------- Lista de MACs associados a %s ----------"%novoCPF)
                for mac in listaDeMACs:
                    print(mac)   
    else:
        print("Esse CPF não está cadastrado")

cpf = ""
mac = ""
arquivoJson  = "listaDeCPFs.json"
criaArquivoJson(arquivoJson)    
CPFs = leJson(arquivoJson) #inicia o dicionário com dados do aqrquivo arquivoJson 
menu = ("\n---------- ESCOLHA UMA DAS OPERAÇÕES ----------\n"
        "1 para cadastrar um CPF\n" 
        "2 para remover um CPF\n"
        "3 para adicionar um MAC vinculado a um CPF\n"
        "4 para remover um MAC vinculado a um CPF\n"
        "5 para listar os CPFs cadastrados\n"
        "6 para listar os MAC vinculados a um CPF\n"
        "7 para sair")

print(menu)
opcao = input("Opção: ")
eValida, opcao = validarOpcao(opcao)
while not eValida: #pede uma nova entrada ao usuário enuquando ela não for válida
    opcao = input("Opção inexistente, escolha uma opção válida: ")
    eValida, opcao = validarOpcao(opcao)
opcao = int(opcao)

#Análise de opcao para executar a ação do menu correspondente
while opcao != 7:
    if opcao == 1:
        cpf = input("Digite o CPF que deseja cadastrar: ")
        cadastraCPF(CPFs, cpf, arquivoJson)

    elif opcao == 2:
        cpf = input("Digite o CPF que deseja remover: ")
        removeCPF(CPFs, cpf, arquivoJson)

    elif opcao == 3:
        cpf = input("Digite o CPF que deseja vincular um endereço MAC: ")
        mac = input("Digite o endereço MAC que deseja vincular a este cpf: ")
        cadastraMAC(CPFs, cpf, mac, arquivoJson)

    elif opcao == 4:
        cpf = input("Digite o CPF que deseja remover um endereço MAC: ")
        mac = input("Digite o endereço MAC que deseja remover deste cpf: ")
        removeMAC(CPFs, cpf, mac, arquivoJson)

    elif opcao == 5:
        listaCPFs(CPFs)

    elif opcao == 6:
        cpf = input("Digite o CPF que deseja consultal os endereços MACs associado: ")
        listaMACs(CPFs, cpf)
        
    print(menu)
    opcao = input("Opção: ")
    eValida, opcao = validarOpcao(opcao)
    while not eValida:
        opcao = input("Opção inexistente, escolha uma opção válida: ")
        eValida, opcao = validarOpcao(opcao)
    opcao = int(opcao)
