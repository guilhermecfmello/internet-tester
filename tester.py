
from socket import AF_INET, socket, SOCK_STREAM

class Tester():
    def __init__(self, port):
        self.ip = ''
        self.port = port
        self.dirResult = './result/' # Diretorio do arquivo de saida
        self.nameResult = 'result.txt' # Nome do arquivo de saida que contem os resultados do teste de velocidade
        
    # Abre uma conexao tcp e aguarda um cliente, caso nao receba uma conexao em 10 segundos
    # Lanca uma excessao de timeout
    def startTcpTest(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((self.ip, self.port)) # Abre a conexao via socket
        sock.settimeout(10) 
        sock.listen(1) # Seta o numero de conexoes a ser esperada
        client, client_address = sock.accept()
        print("%s:%s conectado." %  client_address)
        # client.send()