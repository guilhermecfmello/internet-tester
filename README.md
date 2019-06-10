# internet-tester
Testador de velocidade de conexão implementado utilizando a linguagem python em sua versão 3.

Instrução de Execução:
    1- python3 server.py -p 12345\n
        - Para executar o servidor
        - O parametro -p indica a porta de conexao
        - Caso nao seja fornecido o -p, o padrao é setado o padrão 12345
    2- python3 user.py -i 127.0.0.1 -p 12345 
        - Para executar o lado cliente
        - Parametro -i seta o IP de conexao do servidor, seta o padrao 127.0.0.1
        - Parametro -p porta de conexao liberada do servidor, seta o padrao 12345
    

Arquivos:
    Arquivos na pasta Model estão os modelos de classes e o executor do teste.
    O Arquivo tester.py possui uma classe Tester, nela é implementada o teste em si
    Os metodos de tester.py devem:
        Abrir e fechar todas as conexoes abertas
        Instanciar um cliente e seta-lo com os resultados (Client)
        Salvar a instancia do cliente no atributo userTcp ou userUdp
        Esses clientes setados serao utilizados para gerar o relatorio de saida