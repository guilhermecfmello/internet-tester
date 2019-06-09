from model.client import Client
from model.connectionConfig import Config
from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM
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





config = Config() # Importando configuracoes globais de pacotes

param = sys.argv[1:]
ip, port = parameters(param)
print("IP: " + ip + "Port: " + str(port))
cli = Client(ip, port)


print("Iniciando testador de conexao...")

# ================== TESTE TCP ==================
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
print("Iniciando teste de conexao via UDP")

time.sleep(1)

data = b'0' * config.bufferUdp

sock = socket(AF_INET, SOCK_DGRAM)
sock.connect((cli.ip,cli.port))


# Teste Upload
print("Teste Upload iniciado...")
sock.sendto(data, (cli.ip, cli.port))
for i in range(config.numberPacketsUdp - 1):
    sock.send(data)
    # Tratar protocolo UDP aqui
print("Fim teste Upload")

print("Teste Download iniciado...")
# Teste Download
for i in range(config.numberPacketsUdp):
    sock.recv(config.bufferUdp)
    # Tratar protocolo UDP aqui
print("Fim teste Download")

# Teste latencia
print("Teste Latencia iniciado...")
sock.recv(config.bufferUdp)
sock.send(data)
print("Fim teste latencia")



print("Encerrando Internet-tester")



sock.close()