from socket import AF_INET, socket, SOCK_STREAM
from model.client import Client
from model.connectionConfig import Config
import time



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
        config = Config() #importando configuracoes globais
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((self.ip, self.port)) # Abre a conexao via socket
        sock.settimeout(10) 
        sock.listen(1) # Seta o numero de conexoes a ser esperada
        client, client_address = sock.accept()
        self.userTcp = Client(client_address[0], client_address[1]) # Criando classe para armazenar os resultados
        print("%s:%s conectado." %  client_address)

        # Teste de upload da internet do usuario
        print("Iniciando teste recebimento FTP")
        startTime = time.time()
        for i in range(config.numberPacketsTcp):
            client.recv(config.bufferTcp)
        endTime = time.time()
        totalTime = endTime - startTime
    

        velUp = ((config.bufferTcp * config.numberPacketsTcp)/8000000)/ totalTime #Calculando velocidade de upload

        self.userTcp.setUpRate(velUp)

        # Inicio teste de Download do usuario
        print("Iniciando teste de envio FTP")

        startTime = time.time()
        data = b'0'*config.bufferTcp            
        for i in range(config.numberPacketsTcp):
            client.send(data)
        endTime = time.time()
        totalTime = endTime - startTime

        velDown = ((config.bufferTcp * config.numberPacketsTcp)/8000000)/totalTime # Calculando velocidade de download do usuario

        self.userTcp.setDownRate(velDown)


        # Pegando Latencia do cliente
        startTime = time.time()
        client.send(data)
        client.recv(config.bufferTcp)
        endTime = time.time()

        self.userTcp.setLat((endTime-startTime)*1000)
        print("Fim dos testes TCP")

        print("Velocidade de Download do cliente: " + str(self.userTcp.velDown) + " Mbits")
        print("Velocidade de Upload do cliente: " + str(self.userTcp.velUp) + " Mbits")
        print("Latencia do Cliente: " + str(self.userTcp.lat) + " ms")
        sock.close()




    # Abre uma conexao udp e aguarda um cliente, 
    def startUdpTest(self):
        print("Iniciando teste em UDP")






    def exportResults(self):
        print("Resultados")
        # Implementar impressao de resultados em arquivo,
        # preferencialmente em csv