import sys
from model.tester import Tester

def parameters(param):
    
    if len(param) > 1:
        cond = False
        for p in param:
            if p == '-p':
                cond = True
            else:
                if cond:
                    return int(p)

                else:
                    print("Erro na passagem de parametros, use: python3 server.py -p (port)")
                    sys.exit()
    else:
        return 12345

# Pega parametros
param = sys.argv[1:]
port = parameters(param)
print("port: " + str(port))


#Tratamento de parametros


# Descomentar para alterar a porta padrao
# def readClient():
    # port = input("Digite a porta da conexao: ")
    # port = PORT
    # return port

# Cria uma Instancia de testador na porta especifica
# port = readClient()
test = Tester(port)

test.startTcpTest()




