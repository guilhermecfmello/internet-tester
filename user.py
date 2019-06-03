from model.client import Client
from socket import AF_INET, socket, SOCK_STREAM
import sys

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







param = sys.argv[1:]
ip, port = parameters(param)
print("IP: " + ip + "Port: " + str(port))
cli = Client(ip, port)


print("Iniciando testador de conexao...")

sock = socket(AF_INET, SOCK_STREAM)
sock.connect((cli.ip, cli.port))
print("Conectado ao servidor de teste")


print("Iniciando teste de conexao via TCP/IP")

sock.close()
