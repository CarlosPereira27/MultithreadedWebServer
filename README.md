# MultithreadedWebServer

## Introdução

Implementação em Java de um servidor web multithread para a disciplina Programação Paralela e Distribuída da Universidade Federal de Lavras.

## Executando o servidor

O jar executável do projeto está no diretório dist e chama 'multithreaded-web-server.jar'.

Para executar, acesse o diretório dist pelo terminal e então execute com o comando:

```bash
java -jar multithreaded-web-server.jar -p <port> -c <queue_capacity> -s <poll_size> -l
```

Todos parâmetros no comando acima são opcionais, por padrão, a aplicação será executada na porta 8008 com um pool de threads com 3 threads e uma fila de tarefas com a capacidade máxima de 10 tarefas. Para ajustar as configurações defina os parâmetros da aplicação, segue o que cada parâmetro define:

* ```-p --port=PORT```                Porta em que o servidor está ouvindo
* ```-c --queue_capacity=CAPACITY```  Capacidade máxima da fila de tarefas
* ```-s --poll_size=SIZE```           Tamanho do pool de threads
* ```-l --log```                      Ativa o log das requisições
* ```-h --help```                     Imprime mensagem de ajuda

Exemplos:

* ```java -jar multithreaded-web-server.jar -p 9005``` ->> A aplicação é executada na porta 9005 com um pool de 3 threads e uma fila de tarefas com a capacidade máxima de 10 tarefas. 

* ```java -jar multithreaded-web-server.jar -p 9005 -s 8 - c 20``` ->>   A aplicação é executada na porta 9005 com um pool de 8 threads e uma fila de tarefas com a capacidade máxima de 20 tarefas. 


A aplicação estará disponível na porta especificada, basta acessar no seu navegador de preferência:

http://127.0.0.1:<porta>/, substituindo <porta> pela porta especificada.

## Executando o teste de carga

Foi desenvolvida uma aplicação multithread em python para realizar teste de carga. O arquivo da aplicação é o 'load_test.py' e está no diretório raiz do projeto.

Para executar o teste de carga execute:

```bash
python3 load_test.py -r <request_file> -o <host> -p <port> -n <qty_each_request> -c <num_clients>
```
onde,
* ```-r --request_file=REQUEST_FILE```           Arquivo com a lista de recursos a ser requisitado ao servidor web
* ```-o --host=HOST```                           Host do servidor web. Padrão: http://localhost
* ```-p --port=PORT```                           Porta em que o servidor web está ouvindo. Padrão: 8008
* ```-n --qty_each_request=QTY_EACH_REQUEST```   Quantidade de requisições para cada recurso. Padrão: 1
* ```-c --num_clients=NUM_CLIENTS```             Quantidade de clientes fazendo requisições. Padrão: 1
* ```-h --help```                                Imprime mensagem de ajuda

## Outras aplicações do projeto

No diretório do projeto há alguns scripts, esses scripts são:

* ```install_java_and_python.sh``` - instalação do Java e python para a execução deste projeto
* ```install_python3_pip_and_libs.sh``` - instalação do python3 e bibliotecas utilizadas nos scripts python implementados nesse projeto
* ```load_test_one_machine.sh``` - script utilizado para realizar testes com várias configurações no servidor, usando o teste de carga na mesma máquina que o servidor. O _header_ desse arquivo contém os parâmetros do script a ser executado. 
* ```load_test_ssh.sh``` - script utilizado para realizar testes com várias configurações no servidor, usando o teste de carga em uma máquina diferente do servidor. No entanto o script deve ser executado na máquina cliente que irá executar o teste de carga e a máquina cliente deve ter acesso ssh na máquina servidor para executar e matar o servidor com diferentes configurações. O _header_ desse arquivo contém os parâmetros do script a ser executado. 
* ```process_report.py``` - processa os dados de um experimento para conseguir os dados estatísticos em uma nova planilha geral do experimento e também gera os gráficos do experimento.

## Testes e relatórios gerados

O diretório _reports/gcloud_ possui relatórios de testes executados em duas máquinas na Google Cloud, onde a máquina servidor possui um processador com 24 cores e 24GB de memória RAM e a máquina cliente possui um processador com 8 cores e 8,5GB de memória RAM. Mais informações das máquinas estão nos arquivos _doc/cpu_server_machine.info_ e _doc/cpu_client_machine.info_. No relatório é possível ver informações sobre os dados brutos com todos os tempos do experimento, mas também foi criada uma planilha com os dados estatísticos, esses dados são: o tempo médio dos testes realizados em um cenário, o seu intervalo de confiança para um grau de confiança de 95%, o _speedup_, e a eficiência.