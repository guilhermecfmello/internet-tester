from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM
from model.client import Client
from model.connectionConfig import Config
import struct
import time
import json


class Tester():
    def __init__(self, port):
        self.ip = ''
        self.port = port
        self.dirResult = './result/'  # Diretorio do arquivo de saida
        # Nome do arquivo de saida que contem os resultados do teste de velocidade
        self.nameResult = 'result.txt'
        self.userTcp = None
        self.userUdp = None

    # Abre uma conexao tcp e aguarda um cliente, caso nao receba uma conexao em 10 segundos

    def startTcpTest(self):
        config = Config()  # importando configuracoes globais
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((self.ip, self.port))  # Abre a conexao via socket
        sock.listen(1)  # Seta o numero de conexoes a ser esperada
        client, client_address = sock.accept()
        # Criando classe para armazenar os resultados
        self.userTcp = Client(client_address[0], client_address[1])
        print("%s:%s conectado." % client_address)

        finalData = b'1' * config.bufferTcp
        # Montagem do pacote de dados a ser enviado (Vetor de bytes 0)
        data = b'0' * config.bufferTcp

        # Teste de upload da internet do usuario
        print("Iniciando teste recebimento TCP")
        # sock.settimeout(5)
        numberPacketsTcp = 0
        startTime = time.time()
        dataRecv = client.recv(config.bufferTcp)

        while dataRecv != finalData:
            dataRecv = client.recv(config.bufferTcp)
            numberPacketsTcp = numberPacketsTcp + 1

        velUp = ((config.bufferTcp * numberPacketsTcp) /
                 8000000) / config.testTime  # Calculando velocidade de upload

        self.userTcp.setUpRate(velUp)  # Seta a velocidade de upload calculada

        # time.sleep(1) # Aguardando uma janela de tempo para o usuario receber os pacotes

        numberPacketsTcp = 0
        print("Iniciando teste de envio TCP")
        startTime = time.time()
        while time.time() - startTime < config.testTime:
            client.send(data)
            numberPacketsTcp = numberPacketsTcp + 1
        client.send(finalData)
        # Calculando velocidade de download do usuario
        velDown = ((config.bufferTcp * numberPacketsTcp) /
                   8000000)/config.testTime

        self.userTcp.setDownRate(velDown)

        time.sleep(1)
        # Pegando Latencia do cliente
        startTime = time.time()
        client.send(data)
        client.recv(config.bufferTcp)
        endTime = time.time()

        self.userTcp.setLat((endTime-startTime)*1000)
        print("Fim dos testes TCP")

        print("Velocidade de Download do cliente: " +
              str(self.userTcp.velDown) + " Mbits")
        print("Velocidade de Upload do cliente: " +
              str(self.userTcp.velUp) + " Mbits")
        print("Latencia do Cliente: " + str(self.userTcp.lat) + " ms")

        print("Fechando socketTCP")
        sock.close()

    # Abre uma conexao udp e aguarda um cliente,

    def startUdpTest(self):
        print("Iniciando teste em UDP")
        config = Config()  # Importando configuracoes globais de pacotes
        self.userUdp = Client()
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('', self.port))

        print("Iniciando teste UDP Upload...")
        finalData = b'1' * config.bufferUdp
        startTime = time.time()
        # Recebe o primeiro pacote com o metodo "recvfrom" para pegar o IP do cliente e armazenar na variavel "addr"
        data, addr = s.recvfrom(config.bufferUdp)
        # Depois de pegar o IP, recebe os pacotes com o metodo padrao "recv"
        i = 1
        j = 0
        aux_i = 0
        while True:
            data = s.recv(config.bufferUdp)
            if data == finalData:
                s.sendto(finalData, addr)
                break

            b = data[0:4]
            npackage = struct.unpack((">I").encode(), bytearray(b))[0]

            # Verifica se é o pacote que deve ser recebido
            if(npackage == i and len(data) == config.bufferUdp):
                # print("Recebido pacote: "+str(npackage))
                pass
            # Erro na transmissao do pacote
            else:
                i = aux_i
                j = -1
                config.lostPackagesUdpUp = config.lostPackagesUdpUp + 1
                s.sendto(('erro').encode(), addr)

            if(i % 10 == 0):
                j = -1
                aux_i = i
                time.sleep(0.02)
                s.sendto(("confirmado").encode(), addr)
                # print(">>> Janela de 10 pacotes recebidos com sucesso!")

            i = i + 1
            j = j + 1
        print("Fim teste UDP Upload")

        endTime = time.time()
        totalTime = endTime - startTime
        velUp = ((config.bufferUdp * i) /
                 8000000) / totalTime  # Calculo da velocidade de upload

        # Setando velocidade de upload do cliente
        self.userUdp.setUpRate(velUp)

        print("Iniciando teste UDP Download")
        # Pacote de bytes 0 para enviar com número do pacote no início
        data = b'0' * (config.bufferUdp - 4)
        startTime = time.time()

        npackage = int(0).to_bytes(4, 'big')
        package = npackage + data
        s.sendto(package, addr)
        #print("Enviou pacote UDP: " + str(0) + "->" + str(package))
        i = 1
        j = 0
        startTime = time.time()
        while time.time() - startTime < config.testTime:
            npackage = i.to_bytes(4, 'big')
            package = npackage + data
            s.sendto(package, addr)
            #print("Enviou pacote UDP: " + str(i) + "->" + str(package))
            if i % 10 == 0:
                time.sleep(0.02)

                try:

                    response = s.recv(config.bufferUdp).decode()
                    # print("Resultado response: " + response)
                    # print("Final data: " + finalData   )
                    if response == finalData:
                        print("----------------Acabou teste Download---------")
                        break
                    elif(response.find('erro') == 0 and response.find('confirmado') < 0):
                        i = i - j - 1
                        j = -1
                        print("Erro na transmissao, tentando enviar novamente")
                    elif(response.find('confirmado') == 0):
                        pass
                        # print("Confirmacao recebida, continuando transmissao")
                    response = '/0'
                except TimeoutError:
                    print("Timeout Error")
                    break
                except:
                    print("Erro desconhecido")
                    break

            i = i + 1
            j = j + 1

        s.sendto(finalData, addr)
        endTime = time.time()

        timeTotal = endTime - startTime

        velDown = ((config.bufferUdp * i) /
                   8000000) / timeTotal

        self.userUdp.setDownRate(velDown)

        time.sleep(1)

        # Pegando latencia do cliente
        print("Inicio teste UDP Latencia")
        startTime = time.time()
        s.sendto(finalData, addr)
        s.recv(config.bufferUdp)
        endTime = time.time()

        self.userUdp.setLat((endTime - startTime)*1000)
        print("Fim dos testes UDP")

        # Maciota pra imprimir o resultado do cliente no mesmo arquivo que o tcp
        self.userUdp.setIp(self.userTcp.ip)
        self.userUdp.setPort(self.userTcp.port)

        s.close()

    def exportResultsJSON(self):
        resultTcp = {
            "Protocolo": "TCP/IP",
            "IP": self.userTcp.ip,
            "Port": self.userTcp.port,
            "Download": str(self.userTcp.velDown) + " Mbits/s",
            "Upload": str(self.userTcp.velUp) + " Mbits/s",
            "Latency": str(self.userTcp.lat) + "ms",
        }

        resultUdp = {
            "Protocolo": "UDP",
            "IP": self.userUdp.ip,
            "Port": self.userUdp.port,
            "Download": str(self.userUdp.velDown) + " Mbits/s",
            "Upload": str(self.userUdp.velUp) + " Mbits/s",
            "Latency": str(self.userUdp.lat) + "ms",
        }

        file = open(self.userUdp.ip + ".json", "w")
        file.write("[")
        file.write(json.dumps(resultTcp))
        file.write(",")
        file.write(json.dumps(resultUdp))
        file.write("]")
        file.close()
