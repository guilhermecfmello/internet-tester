from model.tester import Tester


PORT = 12345

# Descomentar para alterar a porta padrao
def readClient():
    # port = input("Digite a porta da conexao: ")
    port = PORT
    return port

# Cria uma Instancia de testador na porta especifica
port = readClient()
test = Tester(port)

test.startTcpTest()