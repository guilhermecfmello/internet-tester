from model.client import Client
from socket import AF_INET, socket, SOCK_STREAM


IP = '127.0.0.1'
PORT = 12345

print("Iniciando testador de conexao...")

# Descomentar leituras quando for conectar em outro servidor
def readServerInfo():
    # ip = input("Digite o IP do servidor de teste: ")
    # port = input("Digite a porta de conexao: ")
    ip = IP
    port = PORT
    return ip, port



ip, port = readServerInfo()
cli = Client(ip, port)



sock = socket(AF_INET, SOCK_STREAM)
sock.connect((cli.ip, cli.port))
print("Conectado ao servidor de teste")


print("Iniciando teste de conexao via TCP/IP")
