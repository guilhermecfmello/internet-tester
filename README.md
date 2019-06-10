# internet-tester
Testador de velocidade de conexão implementado utilizando a linguagem python em sua versão 3.

Instrução de Execução:<br/>
    1. python3 server.py -p 12345<br/>
        - Para executar o servidor<br/>
        - O parametro -p indica a porta de conexao<br/>
        - Caso nao seja fornecido o -p, o padrao é setado o padrão 12345<br/>
    2. python3 user.py -i 127.0.0.1 -p 12345 <br/>
        - Para executar o lado cliente<br/>
        - Parametro -i seta o IP de conexao do servidor, seta o padrao 127.0.0.1<br/>
        - Parametro -p porta de conexao liberada do servidor, seta o padrao 12345<br/>
    

Arquivos:<br/>
    1. Arquivos na pasta Model estão os modelos de classes e o executor do teste.<br/>
    2. O Arquivo tester.py possui uma classe Tester, nela é implementada o teste em si<br/>
    3. Os metodos de tester.py devem:<br/>
        -Abrir e fechar todas as conexoes abertas<br/>
        -Instanciar um cliente e seta-lo com os resultados (Client)<br/>
        -Salvar a instancia do cliente no atributo userTcp ou userUdp<br/>
        -Esses clientes setados serao utilizados para gerar o relatorio de saida<br/>