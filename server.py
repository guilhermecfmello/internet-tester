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
                    print(
                        "Erro na passagem de parametros, use: python3 server.py -p (port)")
                    sys.exit()
    else:
        return 12345


# Pega parametros
param = sys.argv[1:]
port = parameters(param)
print("port: " + str(port))


test = Tester(port)

# Teste de conexao via socket TCP
test.startTcpTest()

# Teste de conexao via socket UDP
test.startUdpTest()

# Exportacao dos resultados
test.exportResultsJSON()
