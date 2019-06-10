# Classe que define alguns parametros de configuracao da conexao

BUFFER_TCP = 500 # pacotes de 500 bytes para tcp
NUM_PACKETS_TCP = 2000# Numeros de pacotes que serao enviados no protocolo tcp

BUFFERR_UDP = 1000 # pacotes de 1000 bytes para udp
NUM_PACKETS_UDP = 1000 # Numeros de pacotes que serao enviados no protocolo udp

class Config():
    def __init__(self):
        self.bufferTcp = BUFFER_TCP
        self.bufferUdp = BUFFERR_UDP
        self.numberPacketsTcp = NUM_PACKETS_TCP
        self.numberPacketsUdp = NUM_PACKETS_UDP
