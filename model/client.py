

class Client():


    def __init__(self, ip, port):
        self.port = port
        self.ip = ip


    # Seta a velocidade de Download do cliente em Mbits/s
    def setDownRate(self, vel):
        self.vel = vel
        
    # Seta a velocidade de Upload do cliente em Mbits/s
    def setUpRate(self, vel):
        self.vel = vel
    
    # Seta a latencia/ping do cliente em ms
    def setLat(self, lat):
        self.lat = lat

    