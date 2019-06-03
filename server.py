from tester import Tester


PORT = 12345

def readClient():
    # port = input("Digite a porta da conexao: ")
    port = PORT
    return port


port = readClient()
test = Tester(port)

test.startTcpTest()