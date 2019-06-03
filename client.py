

class Client():


    def __init__(self, ip, port):
        self.port = port
        self.ip = ip


    # Seta a velocidade de Download do cliente em MB/s
    def setVelDown(self, vel):
        self.vel = vel