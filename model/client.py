

class Client():


    # def __init__(self):
    #     pass

    def __init__(self, ip="", port=""):
        self.port = port
        self.ip = ip


    # Seta a velocidade de Download do cliente em Mbits/s
    def setDownRate(self, vel):
        self.velDown = round(vel, 2)
        
    # Seta a velocidade de Upload do cliente em Mbits/s
    def setUpRate(self, vel):
        self.velUp = round(vel, 2)
    
    # Seta a latencia/ping do cliente em ms
    def setLat(self, lat):
        self.lat = round(lat, 2)

    def setIp(self, ip):
        self.ip = ip

    def setPort(self, port):
        self.port = port
    