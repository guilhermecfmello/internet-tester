from model.client import Client
from model.connectionConfig import Config
from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM
import struct
import sys
import time

# Trata os parametros da execucao


def parameters(param):
    ip = '127.0.0.1'
    port = 12345
    for i in range(len(param)):
        if param[i] == '-i':
            ip = param[i+1]
        elif param[i] == '-p':
            port = int(param[i+1])
    return ip, port


# ================== TESTE TCP ==================
def testTcp(cli):

    config = Config()  # Importando configuracoes globais de pacotes

    print("Iniciando teste de conexao via TCP/IP")
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((cli.ip, cli.port))

    data = b'0' * config.bufferTcp
    print("Teste Upload iniciado...")
    # Enviando pacotes necessarios para geracao das estatisticas
    for i in range(config.numberPacketsTcp):
        sock.send(data)
    print("Fim teste Upload")
    # Recebendo pacotes necessarios para geracao das estatisticas

    print("Teste Download iniciado...")
    for i in range(config.numberPacketsTcp):
        sock.recv(config.bufferTcp)
    print("Fim teste Download")

    # Pacote de calculo de latencia
    print("Teste Latencia iniciado...")
    sock.recv(config.bufferTcp)
    sock.send(data)
    print("Fim teste latencia")

    sock.close()


# ================== TESTE UDP ==================
def testUdp(cli):
    print("Iniciando teste de conexao via UDP")
    config = Config()

    # buffer - 4 para ter espaço para o número do pacote
    data = b'0' * (config.bufferUdp - 4)

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.connect((cli.ip, cli.port))

    # Teste Upload
    print("Teste Upload iniciado...")
    npackage = int(0).to_bytes(4, 'big')
    package = npackage + data
    sock.sendto(package, (cli.ip, cli.port))
    #print("Enviou pacote UDP: " + str(0) + "->" + str(package))
    i = 1
    j = 0
    while(i in range(config.numberPacketsUdp+1)):
        npackage = i.to_bytes(4, 'big')
        package = npackage + data
        sock.sendto(package, (cli.ip, cli.port))
        #print("Enviou pacote UDP: " + str(i) + "->" + str(package))
        if(i % 10 == 0):
            time.sleep(0.02)

            try:
                response = sock.recv(config.bufferUdp).decode()
                if(response.find('erro') == 0 and response.find('confirmado') < 0):
                    i = i - j - 1
                    j = -1
                    print("Erro na transmissao, tentando enviar novamente")
                elif(response.find('confirmado') == 0):
                    print("Confirmacao recebida, continuando transmissao")
                response = '/0'
            except TimeoutError:
                print("Timeout Error")
                break
            except:
                print("Erro desconhecido")
                break

        # Tratar protocolo UDP aqui

        i = i + 1
        j = j + 1
    print("Fim teste Upload")

    print("Teste Download iniciado...")
    # Teste Download
    data, addr = sock.recvfrom(config.bufferUdp)
    i = 1
    j = 0
    aux_i = 0
    while(i in range(config.numberPacketsUdp+1)):
        data = sock.recv(config.bufferUdp)
        b = data[0:4]

        npackage = struct.unpack((">I").encode(), bytearray(b))[0]

        if(npackage == i and len(data) == config.bufferUdp):
            print("Recebido pacote: "+str(npackage))
        elif(len(data != config.bufferUdp and npackage == config.numberPacketsUdp)):
            print("Recebido ultimo pacote: "+str(npackage))
        else:
            i = aux_i
            j = -1
            sock.sendto(('erro').encode(), addr)

        if(i % 10 == 0):
            j = -1
            aux_i = i
            sock.sendto(('confirmado').encode(), addr)
            print(">>> janela de 10 pacotes recebidos com sucesso!")

        # Tratar protocolo UDP aqui

        i = i + 1
        j = j + 1
    print("Fim teste Download")

    # Teste latencia
    print("Teste Latencia iniciado...")
    sock.recv(config.bufferUdp)
    sock.send(data)
    print("Fim teste latencia")
    sock.close()


param = sys.argv[1:]
ip, port = parameters(param)
cli = Client(ip, port)
print("IP: " + ip + "Port: " + str(port))


print("Iniciando testador de velocidade de conexao")
testTcp(cli)
time.sleep(1)
testUdp(cli)
print("Encerrando Internet-tester")
