from socket import AF_INET, socket, SOCK_STREAM
from model.client import Client
class Tester():
    def __init__(self, port):
        self.ip = ''
        self.port = port
        self.dirResult = './result/' # Diretorio do arquivo de saida
        self.nameResult = 'result.txt' # Nome do arquivo de saida que contem os resultados do teste de velocidade
        self.userTcp = None
        self.userUdp = None



    # Abre uma conexao tcp e aguarda um cliente, caso nao receba uma conexao em 10 segundos
    def startTcpTest(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((self.ip, self.port)) # Abre a conexao via socket
        sock.settimeout(10) 
        sock.listen(1) # Seta o numero de conexoes a ser esperada
        client, client_address = sock.accept()
        self.userTcp = Client(client_address[0], client_address[1])
        # print("%s:%s conectado." %  client_address)
        # print(client_address)

        # client.send()





    # Abre uma conexao udp e aguarda um cliente, 
    def startUdpTest(self):
        print("Iniciando teste em UDP")






    def exportResults(self):
        print("Resultados")
        # Implementar impressao de resultados em arquivo,
        # preferencialmente em csv